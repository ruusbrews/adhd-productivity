"""Interactive error-scenario runner.

Events are released progressively; each event names its recipients, so information is incomplete and
unevenly distributed. Expected outcomes (assertions in the scenario file) are checked against what
the audit log shows actually happened (for the demo video: expected vs real outcome).

    python -m adhd_agent.scenario scenarios/error_scenario.json --out runs/scenario [--no-guardrail]
(run from the repo root with PYTHONPATH=src)
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

from adhd_agent.agents import Bus, PolicyAdvisor, ProviderAgent, RegulatorRole
from adhd_agent.audit import AuditLog, verify
from adhd_agent.bdi import BDIAgent
from adhd_agent.simulator import SimulatedUser
from adhd_kb.store import KnowledgeBase

ROOT = Path(__file__).resolve().parents[2]


def load_plans() -> list[dict]:
    return json.loads((ROOT / "data" / "kb" / "interventions.json").read_text(encoding="utf-8"))


def _blocks(audit: AuditLog, lo: int, hi: int, rule: str | None = None) -> int:
    n = 0
    for r in audit.where(agent="bdi", event="decision"):
        pr = r["payload"]["policy_review"]
        if lo <= r["tick"] <= hi and pr["decision"] == "block" and (rule is None or any(x["rule"] == rule for x in pr["rules"])):
            n += 1
    return n


def check_assertion(a: dict, audit: AuditLog, chain_ok: bool) -> tuple[bool, str]:
    k = a["kind"]
    if k == "no_blocks_between":
        n = _blocks(audit, *a["between"], rule=a.get("rule"))
        return n == 0, f"{n} blocking decisions in ticks {a['between']}"
    if k == "min_blocks":
        n = _blocks(audit, *a["between"], rule=a["rule"])
        return n >= a["min"], f"{n} blocks by {a['rule']} in ticks {a['between']}"
    if k == "advisor_finding":
        for r in audit.where(agent="advisor", event="assessment"):
            if r["tick"] > a["by_tick"]:
                break
            for f in r["payload"]["findings"]:
                if f["rule"] == a["rule"] and f["severity"] == a["severity"] and (
                        not a.get("missing_nonempty") or f["missing_information"]):
                    return True, f"seen at tick {r['tick']} (confidence {f['confidence']}, missing {f['missing_information']})"
        return False, "finding not produced in time"
    if k == "regulator_action":
        for r in audit.where(agent="regulator", event="enforcement_decision"):
            if r["tick"] <= a["by_tick"] and a["action"] in r["payload"]["actions"]:
                return True, f"ordered at tick {r['tick']}"
        return False, "action not taken in time"
    if k == "chain_intact":
        return chain_ok, "hash chain verified" if chain_ok else "chain broken"
    raise ValueError(k)


def run(scenario_path: Path, out: Path, guardrail: bool = True, seed: int | None = None) -> dict:
    sc = json.loads(Path(scenario_path).read_text(encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True)
    kb, plans = KnowledgeBase(), load_plans()
    audit = AuditLog(out / "audit.jsonl")
    bus = Bus(audit)
    u = sc["user"]
    user = SimulatedUser(u["presentation"], u["age_group"], seed=seed if seed is not None else sc["seed"])
    bdi = BDIAgent(kb, plans, audit, u["presentation"], u["age_group"], consent=u.get("consent"),
                   guardrail_enabled=guardrail)
    advisor, regulator, provider = PolicyAdvisor(kb, audit), RegulatorRole(audit), ProviderAgent(audit)
    agents = {a.name: a for a in (provider, bdi, advisor, regulator)}
    bus.agents = set(agents)
    audit.append(0, "runner", "scenario_start", {"name": sc["name"], "guardrail_enabled": guardrail, "user": u,
                                                 "kb": kb.stats()})

    def pump() -> None:
        for _ in range(12):
            if not bus.pending():
                return
            for name in ("provider", "bdi", "advisor", "regulator"):
                for m in bus.pop(name):
                    agents[name].handle_message(m, bus)

    events: dict[int, list[dict]] = {}
    for e in sc["events"]:
        events.setdefault(e["tick"], []).append(e)
    trace = []
    for _ in range(sc["ticks"]):
        t = user.t + 1
        for e in events.get(t, []):
            for to in e["to"]:
                bus.send(t, e["from"], to, e["performative"], e["content"])
        pump()
        frame = user.step()
        fired = bdi.tick(frame, user)
        provider.tick(t, bus)
        pump()
        trace.append({"tick": t, "true_attention": user.truth()["attention"],
                      "attention_estimate": round(bdi.beliefs.get("attention_estimate", float("nan")), 3),
                      "fired": fired[0]["plan"] if fired else ""})

    audit.append(user.t, "runner", "scenario_end", {"user_metrics": user.metrics()})
    ok, n, msg = verify(out / "audit.jsonl")
    results = []
    for a in sc["assertions"]:
        passed, detail = check_assertion(a, audit, ok)
        results.append({"id": a["id"], "desc": a["desc"], "passed": passed, "detail": detail})

    blocks = Counter()
    unsupported = 0
    cited = Counter()
    for r in audit.records:
        payload = r["payload"]
        reviews = [payload["policy_review"]] if r["event"] in ("decision", "standing_mode") else []
        for pr in reviews:
            for rule in pr["rules"]:
                if pr["decision"] == "block":
                    blocks[rule["rule"]] += 1
                unsupported += rule["unsupported_by_retrieval"]
                for c in rule["citations"]:
                    cited[c["verified"]] += 1
        if r["event"] == "assessment":
            for f in payload["findings"]:
                for c in f["citations"]:
                    cited[c["verified"]] += 1
    summary = {
        "scenario": sc["name"], "guardrail_enabled": guardrail, "audit_records": n, "audit_chain": msg,
        "user_metrics": user.metrics(), "blocking_decisions_by_rule": dict(blocks),
        "citations_verified_vs_unverified": {"verified": cited.get("true", 0), "unverified": cited.get("false", 0)},
        "rules_unsupported_by_retrieval": unsupported,
        "policy_gaps_surfaced": sorted(advisor.gaps_seen),
        "assertions": results, "assertions_passed": f"{sum(r['passed'] for r in results)}/{len(results)}",
        "enforcement_timeline": [{"tick": r["tick"], "severity": r["payload"]["severity"], "actions": r["payload"]["actions"]}
                                 for r in audit.where(agent="regulator", event="enforcement_decision")],
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    with (out / "trace.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(trace[0]))
        w.writeheader()
        w.writerows(trace)
    return summary


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("scenario")
    ap.add_argument("--out", default="runs/scenario")
    ap.add_argument("--no-guardrail", action="store_true")
    ap.add_argument("--seed", type=int)
    a = ap.parse_args()
    s = run(Path(a.scenario), Path(a.out), guardrail=not a.no_guardrail, seed=a.seed)
    print(json.dumps({k: v for k, v in s.items() if k != "assertions"}, indent=2))
    for r in s["assertions"]:
        print(("PASS" if r["passed"] else "FAIL"), r["id"], "-", r["desc"], "|", r["detail"])


if __name__ == "__main__":
    main()
