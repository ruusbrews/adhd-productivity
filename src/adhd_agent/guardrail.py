"""Policy node (Y.3172 "P"): reviews an intended intervention against the policy KB before it fires.

Each rule names the policy documents it must be grounded in. The guardrail runs a retrieval
query against `kb_policy` and only cites provisions the retriever actually surfaced. If the
retriever fails to surface a required source the rule still enforces (fail-safe) but is marked
`unsupported_by_retrieval` in the audit log, which exposes KB-quality problems instead of hiding them.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from adhd_kb.store import Hit, KnowledgeBase

CHANNEL_OF_SIGNAL = {"gaze_off_task": "gaze", "hrv_rmssd": "hrv_eda", "eda": "hrv_eda", "motion_fidget": "motion"}
PHYSIO_ONLY = {"hrv_rmssd", "eda"}
INSTITUTIONAL = {"school", "workplace"}


def required_channels(plan: dict) -> set[str]:
    ch = {CHANNEL_OF_SIGNAL[c["signal"]] for c in plan.get("context_conditions", []) if c["signal"] in CHANNEL_OF_SIGNAL}
    du = " ".join(plan.get("data_used", [])).lower()
    for word, name in (("gaze", "gaze"), ("hrv", "hrv_eda"), ("eda", "hrv_eda"), ("motion", "motion")):
        if word in du and "biometric" in du:
            ch.add(name)
    return ch


def corroborated(b: dict) -> bool:
    """A behavioural signal supports the claim that attention really dropped."""
    return b.get("attention_estimate", 1.0) < 0.55 or b.get("omission_rate", 0.0) >= 0.12


@dataclass
class Rule:
    rule_id: str
    decision: str                       # block | modify
    query: str
    cite: tuple[str, ...]
    applies: Callable[[dict, dict], bool]
    reason: str
    design_rule: bool = False           # True = our design rule, not directly a legal duty
    evidence_query: str | None = None   # optional kb_evidence lookup shown next to the policy citations


RULES: list[Rule] = [
    Rule("R1-persuasive-rewards-minors", "block",
         "minors persuasive design intermittent random rewards streaks excessive use default settings engagement",
         ("eu-dsa-art28-minors-guidelines-2025", "uk-ico-age-appropriate-design-code", "eu-ai-act-2024-1689"),
         lambda p, b: b["age_group"] == "minor" and p["reward_schedule"] in ("variable", "streak_based"),
         "Variable/streak rewards are engagement-driven persuasive design that EU DSA Art. 28 guidance says minors "
         "should not face; ADHD evidence also disfavours variable reinforcement.",
         evidence_query="reward schedule variable partial reinforcement ADHD compulsive gaming impulsive buying"),
    Rule("R2-unsuitable-for-minors", "block",
         "minors best interests of the child detrimental data use profiling off by default",
         ("uk-ico-age-appropriate-design-code", "eu-dsa-art28-minors-guidelines-2025"),
         lambda p, b: b["age_group"] == "minor" and p["suitable_for_minors"] == "no"
         and p["reward_schedule"] not in ("variable", "streak_based"),
         "Library marks this plan as not suitable for minors."),
    Rule("R2b-push-default-minors", "modify",
         "push notifications off by default minors sleep hours default settings",
         ("eu-dsa-art28-minors-guidelines-2025", "uk-ico-age-appropriate-design-code"),
         lambda p, b: b["age_group"] == "minor" and p["default_on_notification"]
         and not b.get("guardian_push_opt_in", False),
         "Push prompts to minors are off by default unless a guardian opted in: deliver silently in-app instead."),
    Rule("R3-biometric-attention-institutional", "block",
         "emotion inference attention students school workplace biometric prohibited",
         ("ec-guidelines-prohibited-ai-practices-2025", "eu-ai-act-2024-1689"),
         lambda p, b: p["uses_biometric"] and b["deployment_context"] in INSTITUTIONAL,
         "Biometric inference of attention/emotion in education or workplace deployments is prohibited under EU AI "
         "Act Art. 5(1)(f) (medical/safety exception does not apply to a wellness-claim product)."),
    Rule("R4-sensor-consent", "block",
         "explicit consent health data biometric special category children permit",
         ("eu-gdpr-2016-679", "qatar-pdppl-13-2016", "uae-pdpl-fdl-45-2021"),
         lambda p, b: any(not b["consent"].get(c, False) for c in required_channels(p)),
         "A sensor channel this plan needs has no explicit per-sensor consent."),
    Rule("R5-therapeutic-claim", "block",
         "medical device software intended purpose wellness claims treat ADHD",
         ("mdcg-2019-11-rev1", "fda-general-wellness-2026", "imdrf-samd-n12-2014"),
         lambda p, b: p["claim_wording_class"] == "therapeutic" and not b.get("device_authorised", False),
         "Therapeutic claim without medical-device authorisation; product is positioned as wellness only."),
    Rule("R6-physiological-only-trigger", "block",
         "emotion recognition infer biometric attention arousal cognitive state",
         ("eu-ai-act-2024-1689", "ieee-7014-2024"),
         lambda p, b: set(p.get("matched_signals", [])) and set(p["matched_signals"]) <= PHYSIO_ONLY
         and not corroborated(b),
         "HRV/EDA indicate arousal (construct-ambiguous: attention vs emotion); no behavioural signal corroborates "
         "an attention drop, so the inference is not allowed to trigger an intervention.",
         design_rule=True,
         evidence_query="HRV EDA arousal construct attention emotion"),
    Rule("R7-speculative-evidence", "block",
         "ethics governance AI health safety transparency evidence",
         ("who-ethics-governance-ai-health-2021",),
         lambda p, b: p["evidence_level"] == "none" and not b.get("speculative_opt_in", False),
         "No ADHD-specific evidence for this plan; speculative plans need explicit user opt-in.",
         design_rule=True),
]


@dataclass
class RuleResult:
    rule_id: str
    decision: str
    reason: str
    citations: list[dict]
    unsupported_by_retrieval: bool
    design_rule: bool
    evidence: list[dict] = field(default_factory=list)


@dataclass
class Verdict:
    decision: str                       # allow | modify | block
    results: list[RuleResult]
    retrieved: list[str]
    modifications: dict

    def as_dict(self) -> dict:
        return {
            "decision": self.decision,
            "modifications": self.modifications,
            "retrieved_record_ids": self.retrieved,
            "rules": [
                {"rule": r.rule_id, "decision": r.decision, "reason": r.reason, "citations": r.citations,
                 "unsupported_by_retrieval": r.unsupported_by_retrieval, "design_rule": r.design_rule,
                 "evidence": r.evidence}
                for r in self.results
            ],
        }


def _best_per_doc(hits: list[Hit], want: tuple[str, ...], per_doc: int = 2) -> list[dict]:
    out, count = [], {}
    for h in hits:
        d = h.metadata.get("doc_id")
        if d in want and count.get(d, 0) < per_doc:
            out.append(h.cite())
            count[d] = count.get(d, 0) + 1
    return out


class PolicyGuardrail:
    def __init__(self, kb: KnowledgeBase, enabled: bool = True):
        self.kb, self.enabled = kb, enabled

    def review(self, plan: dict, beliefs: dict) -> Verdict:
        if not self.enabled:
            return Verdict("allow", [], [], {})
        results, retrieved = [], []
        for rule in RULES:
            if not rule.applies(plan, beliefs):
                continue
            hits = self.kb.search(rule.query, ("kb_policy",), k=10)
            cites = _best_per_doc(hits, rule.cite)
            retrieved += [h.id for h in hits[:5]]
            ev = []
            if rule.evidence_query:
                ev = [h.cite() for h in self.kb.search(rule.evidence_query, ("kb_evidence",), k=2)]
            results.append(RuleResult(rule.rule_id, rule.decision, rule.reason, cites,
                                      unsupported_by_retrieval=not cites,
                                      design_rule=rule.design_rule, evidence=ev))
        if any(r.decision == "block" for r in results):
            decision, mods = "block", {}
        elif results:
            decision, mods = "modify", {"delivery": "in_app_silent"}
        else:
            decision, mods = "allow", {}
        return Verdict(decision, results, sorted(set(retrieved)), mods)
