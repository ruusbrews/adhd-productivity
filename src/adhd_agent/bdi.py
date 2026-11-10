"""Local BDI agent: Perception -> Deliberation -> Execution over a belief base and the plan library.

Structure mirrors the SPADE design in the research (PeriodicBehaviour = perception, CyclicBehaviour =
deliberation and execution) but runs as a deterministic, single-process loop so the demo is
reproducible without an XMPP server.

 Beliefs    python dict (sensor-derived, consent-filtered, plus deployment/provider context)
 Desires    D1 stay compliant (hard filter via policy node) > D2 sustain focus > D3 minimise interruptions
 Intentions the highest-scoring candidate plan that survives the policy node; if the top plan is blocked,
            the agent re-deliberates with the next candidate (means-end reasoning with alternatives)
"""
from __future__ import annotations

from collections import Counter, defaultdict, deque

from adhd_agent.audit import AuditLog
from adhd_agent.guardrail import PolicyGuardrail
from adhd_kb.store import KnowledgeBase

EVIDENCE_WEIGHT = {"meta-analysis": 1.0, "RCT": 0.8, "observational": 0.5, "theory/expert opinion": 0.3, "none": 0.1}
CHANNELS = {  # consent channel -> belief keys it feeds
    "task_telemetry": ("omission_rate", "commission_rate", "rt_cv", "keystroke_error_rate", "time_on_task_min"),
    "self_report": ("fatigue_self_report",),
    "gaze": ("gaze_off_task",),
    "hrv_eda": ("hrv_rmssd", "eda"),
    "motion": ("motion_fidget",),
}
SIGNAL_BELIEF = {"attention_level": "attention_estimate", "fatigue": "fatigue"}
FORCED_COOLDOWN, PLAN_COOLDOWN, PROMPT_WINDOW = 10, 20, 20


def _cmp(op: str, v: float, thr: float) -> bool:
    return v < thr if op == "<" else v > thr if op == ">" else v >= thr


class BDIAgent:
    name = "bdi"

    def __init__(self, kb: KnowledgeBase, plans: list[dict], audit: AuditLog, presentation: str,
                 age_group: str = "adult", deployment_context: str = "consumer", consent: dict | None = None,
                 guardrail_enabled: bool = True, min_gap_ticks: int = 8, threshold: float = 0.25):
        self.plans = {p["plan_id"]: p for p in plans}
        self.audit, self.guardrail = audit, PolicyGuardrail(kb, guardrail_enabled)
        self.min_gap, self.threshold = min_gap_ticks, threshold
        self.windows: dict[str, deque] = defaultdict(lambda: deque(maxlen=10))
        self.last_fire: dict[str, int] = {}
        self.uses: Counter = Counter()
        self.prompt_ticks: list[int] = []
        self.active_ambient: set[str] = set()
        self.standing: set[str] = set()
        self.beliefs: dict = {
            "profile": presentation, "age_group": age_group, "deployment_context": deployment_context,
            "consent": {"task_telemetry": True, "self_report": True, "gaze": False, "hrv_eda": False,
                        "motion": False, **(consent or {})},
            "device_authorised": False, "speculative_opt_in": False, "guardian_push_opt_in": False,
            "provider_config": {"enabled_engagement_plans": []},
        }
        self.desires = ["D1 stay compliant (hard filter)", "D2 sustain focus", "D3 minimise interruptions"]
        self.log = lambda t, ev, payload: self.audit.append(t, self.name, ev, payload)

    # ------------------------------------------------------------------ perception (periodic)
    def _biometric_gate(self, t: int) -> set[str]:
        """Channels the policy node bars from attention inference in this context (R3). Re-checked and logged
        only when the deployment context or consent changes, so the audit shows one decision per change."""
        key = (self.beliefs["deployment_context"], tuple(sorted(c for c, ok in self.beliefs["consent"].items() if ok)))
        if key != getattr(self, "_gate_key", None):
            self._gate_key = key
            verdict = self.guardrail.review_inference(self.beliefs)
            self._gate = set(verdict.modifications.get("suppressed_channels", []))
            if verdict.decision == "block":
                self.log(t, "decision", {
                    "intention": "infer-attention-from-biometrics", "score": None, "forced_by_provider": False,
                    "conditions": [], "evidence_level": "n/a",
                    "beliefs": {k: self.beliefs[k] for k in ("age_group", "deployment_context", "profile")},
                    "policy_review": verdict.as_dict(),
                    "rationale": f"Perception step: {', '.join(sorted(self._gate))} data may not be used to infer "
                                 f"attention in a {self.beliefs['deployment_context']} deployment (R3). These channels "
                                 "are dropped before they reach the belief base; attention is estimated from "
                                 "behaviour only."})
        return self._gate

    def perceive(self, frame: dict) -> None:
        b, consent = self.beliefs, self.beliefs["consent"]
        barred = self._biometric_gate(frame["tick"])
        active = [c for c, ok in consent.items() if ok and c not in barred]
        for ch in active:
            for key in CHANNELS[ch]:
                if key in frame:
                    self.windows[key].append(frame[key])
        for ch, keys in CHANNELS.items():           # data minimisation: drop beliefs of withdrawn or barred channels
            if not consent.get(ch) or ch in barred:
                for k in keys:
                    self.windows.pop(k, None)
                    b.pop(k, None)
        mean = lambda k: sum(self.windows[k]) / len(self.windows[k]) if self.windows.get(k) else None
        for k in ("omission_rate", "commission_rate", "rt_cv", "keystroke_error_rate", "gaze_off_task",
                  "hrv_rmssd", "eda", "motion_fidget"):
            v = mean(k)
            if v is not None:
                b[k] = v
        if "time_on_task_min" in frame and consent["task_telemetry"]:
            b["time_on_task_min"] = frame["time_on_task_min"]
        if (v := mean("fatigue_self_report")) is not None:
            b["fatigue"] = v
        # attention is inferred from BEHAVIOUR (+ gaze if consented). HRV/EDA are kept as 'arousal' only and
        # motion never counts as inattention (permit-fidget-during-wm-tasks): both are construct-ambiguous.
        if "omission_rate" in b:
            est = 1 - (1.2 * b["omission_rate"] + 0.6 * b.get("gaze_off_task", 0.0)
                       + 1.0 * max(0.0, b.get("rt_cv", 0.2) - 0.2))
            b["attention_estimate"] = max(0.0, min(1.0, est))
        b["tick"] = frame["tick"]

    # ----------------------------------------------------------------------- deliberation
    def _evaluate(self, plan: dict) -> tuple[bool, list[dict], float]:
        b, details, margins = self.beliefs, [], []
        for c in plan["context_conditions"]:
            key = SIGNAL_BELIEF.get(c["signal"], c["signal"])
            v = b.get(key)
            if v is None:
                details.append({"signal": c["signal"], "ok": False, "why": "signal_unavailable"})
                continue
            ok = _cmp(c["operator"], v, c["value"])
            details.append({"signal": c["signal"], "op": c["operator"], "thr": c["value"], "value": round(v, 3), "ok": ok})
            if ok:
                margins.append(min(1.0, abs(v - c["value"]) / max(abs(c["value"]), 1e-6)))
        oks = [d["ok"] for d in details]
        matched = (any(oks) if plan["condition_logic"] == "any" else all(oks)) if oks else False
        return matched, details, (sum(margins) / len(margins) if margins else 0.0)

    def _pool(self) -> list[dict]:
        pool = [p for p in self.plans.values() if p["kind"] == "intervention"]
        for pid in self.beliefs["provider_config"].get("enabled_engagement_plans", []):
            if pid in self.plans:   # provider-injected engagement rule: fires whenever the user is mid-task
                pool.append({**self.plans[pid], "kind": "intervention", "forced": True, "condition_logic": "all",
                             "context_conditions": [{"signal": "time_on_task_min", "operator": ">=", "value": 2.0,
                                                     "rationale": "provider engagement campaign"}]})
        return pool

    def deliberate(self, t: int) -> list[dict]:
        b, cands = self.beliefs, []
        recent = sum(1 for x in self.prompt_ticks if t - x <= PROMPT_WINDOW)
        since_prompt = t - (self.prompt_ticks[-1] if self.prompt_ticks else -10**6)
        for plan in self._pool():
            pid = plan["plan_id"]
            if plan["delivery"] == "ambient" and pid in self.active_ambient:
                continue
            cd = FORCED_COOLDOWN if plan.get("forced") else PLAN_COOLDOWN
            if t - self.last_fire.get(pid, -10**6) < cd:
                continue
            if plan["delivery"] != "ambient" and since_prompt < self.min_gap and not plan.get("forced"):
                continue
            matched, details, strength = self._evaluate(plan)
            if not matched:
                continue
            fit = plan["target_presentations"].get(b["profile"], 0.0)
            score = (1.0 if plan.get("forced") else
                     fit * EVIDENCE_WEIGHT[plan["evidence_level"]] * (0.5 + 0.5 * strength)
                     * (0.97 ** self.uses[pid]) - 0.15 * recent)
            matched_signals = [d["signal"] for d in details if d["ok"]]
            cands.append({"plan": {**plan, "matched_signals": matched_signals}, "plan_id": pid, "score": round(score, 3),
                          "forced": bool(plan.get("forced")), "conditions": details})
        cands = [c for c in cands if c["score"] >= self.threshold]
        return sorted(cands, key=lambda c: c["score"], reverse=True)

    # ------------------------------------------------------------------------- execution
    def tick(self, frame: dict, user) -> list[dict]:
        t = frame["tick"]
        self.perceive(frame)
        if t == 1:
            self._activate_standing(t, user)
        if t % 20 == 0:
            self.log(t, "perception", {k: round(v, 3) for k, v in self.beliefs.items() if isinstance(v, float)}
                     | {"sensors_active": [c for c, ok in self.beliefs["consent"].items() if ok]})
        fired = []
        for cand in self.deliberate(t)[:3]:      # try alternatives if the top intention is blocked
            plan = cand["plan"]
            verdict = self.guardrail.review(plan, self.beliefs)
            self.log(t, "decision", {
                "intention": cand["plan_id"], "score": cand["score"], "forced_by_provider": cand["forced"],
                "conditions": cand["conditions"], "evidence_level": plan["evidence_level"],
                "beliefs": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in self.beliefs.items()
                            if k in ("attention_estimate", "fatigue", "omission_rate", "age_group",
                                     "deployment_context", "profile")},
                "policy_review": verdict.as_dict(),
                "rationale": self._rationale(cand, verdict),
            })
            self.last_fire[cand["plan_id"]] = t      # blocked plans also back off (no log spam)
            if verdict.decision == "block":
                continue
            delivery = verdict.modifications.get("delivery") or ("ambient" if plan["delivery"] == "ambient" else "push")
            outcome = user.receive(cand["plan_id"], delivery)
            self.uses[cand["plan_id"]] += 1
            if delivery != "ambient":
                self.prompt_ticks.append(t)
            else:
                self.active_ambient.add(cand["plan_id"])
            self.log(t, "execution", {"plan": cand["plan_id"], "delivery": delivery, "modified": verdict.decision == "modify",
                                      "outcome": outcome})
            fired.append({"plan": cand["plan_id"], **outcome})
            break
        return fired

    def _activate_standing(self, t: int, user) -> None:
        for p in self.plans.values():
            if p["kind"] == "standing_mode" and p["plan_id"] == "notification-batching":
                v = self.guardrail.review(p, self.beliefs)
                if v.decision != "block":
                    user.set_batching(True)
                    self.standing.add(p["plan_id"])
                self.log(t, "standing_mode", {"plan": p["plan_id"], "policy_review": v.as_dict(),
                                              "rationale": "Hold non-urgent notifications during focus sessions "
                                                           "(Kushlev 2016; aligned with DSA default-off guidance)."})

    @staticmethod
    def _rationale(cand: dict, verdict) -> str:
        hit = [c["signal"] for c in cand["conditions"] if c["ok"]]
        base = (f"Plan '{cand['plan_id']}' scored {cand['score']} (conditions met: {', '.join(hit)})"
                + ("; forced by provider engagement rule" if cand["forced"] else "") + ". ")
        if verdict.decision == "allow":
            return base + "Policy node found no applicable restriction: executing."
        rules = ", ".join(r.rule_id for r in verdict.results)
        return base + f"Policy node decision: {verdict.decision.upper()} under {rules}."

    # --------------------------------------------------------------------------- messaging
    def handle_message(self, msg, bus) -> None:
        t, c = msg.tick, msg.content
        if msg.performative == "request" and c.get("type") == "config_update":
            old = {k: self.beliefs.get(k) for k in c.get("beliefs", {})}
            for k, v in c.get("beliefs", {}).items():
                self.beliefs[k] = v
            if "provider_config" in c:
                self.beliefs["provider_config"].update(c["provider_config"])
            self.log(t, "belief_revision", {"from": msg.sender, "changed": c.get("beliefs", {}) | {
                "provider_config": c.get("provider_config", {})}, "previous": old,
                "note": "Only the fields the provider disclosed are visible to this agent."})
        elif msg.performative == "request" and c.get("type") == "digest":
            blocks = Counter()
            plans = defaultdict(set)
            for r in self.audit.where(agent=self.name, event="decision"):
                pr = r["payload"]["policy_review"]
                if pr["decision"] == "block" and r["tick"] >= c.get("since_tick", 0):
                    for rule in pr["rules"]:
                        blocks[rule["rule"]] += 1
                        plans[rule["rule"]].add(r["payload"]["intention"])
            content = {"type": "guardrail_digest", "blocks_by_rule": dict(blocks),
                       "plans_by_rule": {k: sorted(v) for k, v in plans.items()},
                       "deployment_context": self.beliefs["deployment_context"],
                       "age_group": self.beliefs["age_group"]}
            bus.send(t, self.name, msg.sender, "inform", content, in_reply_to=msg.id)
