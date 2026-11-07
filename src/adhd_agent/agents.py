"""Institutional agents and the message bus that coordinates them.

 provider   scripted app provider (changes configuration, answers regulator requests)
 bdi        the local BDI agent (see bdi.py); sees ONLY what the provider discloses to it
 advisor    policy & legal adviser: accumulates facts as they arrive, retrieves provisions from the KB
            and reports findings with citations, verification status, missing information and policy gaps
 regulator  institutional role: maps the adviser's findings onto an enforcement ladder

Coordination protocol: FIPA-style performatives (inform / request / agree / refuse) on an audited bus.
Information is deliberately incomplete and unevenly distributed (each event names its recipients).
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Callable

from adhd_agent.audit import AuditLog
from adhd_agent.guardrail import INSTITUTIONAL, _best_per_doc
from adhd_kb.store import KnowledgeBase

SEV_ORDER = ["info", "contested", "high_risk", "non_compliant", "prohibited"]
LADDER = {
    "info": ["monitor"],
    "contested": ["defer_to_human_review_panel", "log_policy_gap"],
    "high_risk": ["request_information"],
    "non_compliant": ["order_remediation", "require_dpia"],
    "prohibited": ["suspend_feature", "require_remediation_plan"],
}
# a data-privacy/ethics breach (not just a consumer-protection issue) escalates further
ESCALATIONS = {"A4-inferred-state-advertising": [
    "prohibit_use_of_inferred_signals_for_advertising", "enforce_consent_and_purpose_limitation_children_data",
    "refer_national_ai_ethics_oversight"]}


@dataclass
class Message:
    id: int
    tick: int
    sender: str
    to: str
    performative: str
    content: dict
    in_reply_to: int | None = None


class Bus:
    def __init__(self, audit: AuditLog):
        self.audit, self.inbox, self.n = audit, defaultdict(list), 0
        self.agents: set[str] = set()

    def send(self, tick: int, sender: str, to: str, performative: str, content: dict,
             in_reply_to: int | None = None) -> Message:
        self.n += 1
        m = Message(self.n, tick, sender, to, performative, content, in_reply_to)
        self.inbox[to].append(m)
        self.audit.append(tick, sender, "message", {"id": m.id, "to": to, "performative": performative,
                                                    "in_reply_to": in_reply_to, "content": content})
        return m

    def pop(self, name: str) -> list[Message]:
        msgs, self.inbox[name] = self.inbox[name], []
        return msgs

    def pending(self) -> bool:
        return any(self.inbox[a] for a in self.agents)


# ------------------------------------------------------------------------------------ provider
class ProviderAgent:
    name = "provider"

    def __init__(self, audit: AuditLog, reply_delay: int = 30, remediation_delay: int = 10):
        self.audit, self.reply_delay, self.remediation_delay = audit, reply_delay, remediation_delay
        self.pending: list[tuple[int, str, str, dict]] = []

    def handle_message(self, msg: Message, bus: Bus) -> None:
        c, t = msg.content, msg.tick
        if c.get("type") == "information_request":
            self.pending.append((t + self.reply_delay, "inform", msg.sender, {
                "type": "provider_statement",
                "text": "We intend to restore attention monitoring in schools as an assistive tool for students with ADHD "
                        "(medical/safety exception).",
                "facts": {"claims_medical_exception": True, "deployment_context": "school"}}))
        elif c.get("type") == "enforcement_order" and "suspend_feature" in c.get("actions", []):
            d = t + self.remediation_delay
            self.pending.append((d, "request", "bdi", {"type": "config_update", "beliefs": {"deployment_context": "consumer"},
                                                       "provider_config": {"enabled_engagement_plans": []}}))
            self.pending.append((d, "inform", msg.sender, {
                "type": "compliance_report",
                "text": "Streaks, variable rewards, ad SDK and school attention mode disabled.",
                "facts": {"streaks": False, "variable_rewards": False, "iap_linked_rewards": False, "ad_sdk": False,
                          "shares_inferred_state_with_ads": False, "biometric_attention_inference_attempted": False,
                          "deployment_context": "consumer"}}))

    def tick(self, t: int, bus: Bus) -> None:
        due = [p for p in self.pending if p[0] <= t]
        self.pending = [p for p in self.pending if p[0] > t]
        for _, perf, to, content in due:
            bus.send(t, self.name, to, perf, content)


# ------------------------------------------------------------------------------------ advisor
@dataclass
class AdvisorRule:
    rule_id: str
    summary: str
    query: str
    cite: tuple[str, ...]
    severity: Callable = None            # f(facts) -> severity or None
    evidence_query: str | None = None
    missing: Callable = lambda f: []


ADVISOR_RULES: list[AdvisorRule] = [
    AdvisorRule(
        "A1-institutional-attention-inference",
        "Biometric inference of student/employee attention is prohibited in education and workplace deployments "
        "(EU AI Act Art. 5(1)(f)); a wellness-claim product cannot rely on the medical/safety exception.",
        "emotion inference attention students school workplace biometric prohibited",
        ("ec-guidelines-prohibited-ai-practices-2025", "eu-ai-act-2024-1689"),
        lambda f: "prohibited" if f.get("deployment_context") in INSTITUTIONAL
        and f.get("biometric_attention_inference_attempted") else None),
    AdvisorRule(
        "A2-persuasive-design-minors",
        "Streaks and variable/random rewards aimed at minors conflict with EU DSA Art. 28 minors guidelines, the UK "
        "Children's Code (nudge techniques) and AI Act Art. 5(1)(a)-(b) where they exploit age/disability vulnerabilities.",
        "minors persuasive design intermittent random rewards streaks excessive use default settings",
        ("eu-dsa-art28-minors-guidelines-2025", "uk-ico-age-appropriate-design-code", "eu-ai-act-2024-1689",
         "eu-ucpd-2005-29"),
        lambda f: "non_compliant" if f.get("age_group") == "minor" and (f.get("streaks") or f.get("variable_rewards")) else None,
        evidence_query="reward schedule variable partial reinforcement ADHD compulsive gaming"),
    AdvisorRule(
        "A3-in-app-purchases-vulnerable-users",
        "In-app purchases linked to engagement mechanics target users with elevated impulsive-buying risk; unfair "
        "commercial practice rules judge them from the vulnerable group's perspective.",
        "unfair commercial practices vulnerable consumers undue influence dark patterns advertising minors",
        ("eu-ucpd-2005-29", "eu-ai-act-2024-1689", "ftc-dark-patterns-2022"),
        lambda f: ("non_compliant" if f.get("iap_linked_rewards") and (f.get("age_group") == "minor" or f.get("adhd_profile_users"))
                   else "high_risk" if f.get("iap_reports") else None),
        evidence_query="impulsive buying ADHD in-app purchases overspending",
        missing=lambda f: [] if f.get("iap_linked_rewards") is not None else
        ["whether in-app purchases are linked to reward mechanics", "which engagement mechanics are enabled"]),
    AdvisorRule(
        "A4-inferred-state-advertising",
        "Using inferred attention/arousal (a proxy for a disability-related condition) or children's data for "
        "advertising breaches purpose limitation and special-category/children's data rules and manipulates "
        "vulnerable users; consent cannot cure it for children.",
        "special category health data biometric explicit consent children advertising third party sharing purpose",
        ("eu-gdpr-2016-679", "us-coppa-rule-2025-amendments", "uk-ico-age-appropriate-design-code",
         "eu-ucpd-2005-29", "unesco-rec-ethics-ai-2021"),
        lambda f: "prohibited" if f.get("shares_inferred_state_with_ads") or (f.get("ad_sdk") and f.get("age_group") == "minor") else None),
    AdvisorRule(
        "A5-assistive-exception-contested",
        "Provider invokes an assistive/medical exception for attention monitoring in schools. This is contested: the "
        "exception would require device-grade (medical) claims, which contradicts the wellness positioning the same "
        "product relies on elsewhere; the Act's text does not define the exception for non-device support tools.",
        "emotion inference attention students school medical exception assistive disability rights device",
        ("eu-ai-act-2024-1689", "ec-guidelines-prohibited-ai-practices-2025", "un-crpd-2006", "mdcg-2019-11-rev1"),
        lambda f: "contested" if f.get("claims_medical_exception") and f.get("deployment_context") in INSTITUTIONAL else None,
        missing=lambda f: ["clinical supervision arrangement", "device authorisation status"]),
    AdvisorRule(
        "A6-gulf-sensitive-data-regime",
        "Special-nature/health and children's data processing needs a regulator permit and guardian consent in Qatar; "
        "UAE PDPL implementing regulations are still unissued, so sector responsibility is unclear.",
        "special nature data permit children health consent Qatar UAE implementing regulations",
        ("qatar-pdppl-13-2016", "qatar-ncsa-privacy-notice-guideline", "uae-pdpl-fdl-45-2021"),
        lambda f: "info" if f.get("region") in ("Qatar", "UAE") else None),
]


class PolicyAdvisor:
    name = "advisor"

    def __init__(self, kb: KnowledgeBase, audit: AuditLog):
        self.kb, self.audit, self.facts, self._sig = kb, audit, {}, None
        self.gaps_seen: dict[str, dict] = {}
        self.findings: list[dict] = []

    # facts arrive in different shapes and at different times
    def _extract(self, c: dict) -> dict:
        f = dict(c.get("facts", {}))
        if c.get("type") == "guardrail_digest":
            b, p = c.get("blocks_by_rule", {}), c.get("plans_by_rule", {})
            f["deployment_context"], f["age_group"] = c.get("deployment_context"), c.get("age_group")
            r1 = set(p.get("R1-persuasive-rewards-minors", []))
            if r1:
                f["streaks"] = "streak-counter" in r1 or f.get("streaks", False)
                f["variable_rewards"] = "variable-ratio-rewards" in r1 or f.get("variable_rewards", False)
            if b.get("R3-biometric-attention-institutional"):
                f["biometric_attention_inference_attempted"] = True
        return f

    def assess(self) -> list[dict]:
        out = []
        for r in ADVISOR_RULES:
            sev = r.severity(self.facts)
            if not sev:
                continue
            hits = self.kb.search(r.query, ("kb_policy",), k=10)
            cites = _best_per_doc(hits, r.cite)
            ev = [h.cite() for h in self.kb.search(r.evidence_query, ("kb_evidence",), k=1)] if r.evidence_query else []
            gaps = [h.cite() | {"title": h.metadata["gap_id"], "type": h.metadata["gap_type"]}
                    for h in self.kb.search(r.query, ("kb_gaps",), k=2, min_score=3.0)]
            for g in gaps:
                self.gaps_seen[g["doc_id"]] = g
            missing = r.missing(self.facts)
            ver = [c for c in cites if c["verified"] == "true"]
            share = round(len(ver) / len(cites), 2) if cites else 0.0
            conf = "low" if (sev == "contested" or missing or not cites) else "medium" if share < 1 else "high"
            out.append({"rule": r.rule_id, "severity": sev, "summary": r.summary, "citations": cites,
                        "evidence": ev, "policy_gaps": gaps, "missing_information": missing,
                        "verified_share": share, "confidence": conf,
                        "unverified_provisions": [f"{c['doc_id']} {c['ref']}" for c in cites if c["verified"] != "true"]})
        return sorted(out, key=lambda x: SEV_ORDER.index(x["severity"]), reverse=True)

    def handle_message(self, msg: Message, bus: Bus) -> None:
        t, new = msg.tick, self._extract(msg.content)
        if not new and msg.content.get("type") != "assessment_request":
            return
        self.facts.update({k: v for k, v in new.items() if v is not None})
        self.findings = self.assess()
        self.audit.append(t, self.name, "assessment", {
            "trigger": {"from": msg.sender, "type": msg.content.get("type")}, "known_facts": dict(self.facts),
            "findings": self.findings,
            "reasoning": [f"{f['rule']} -> {f['severity']} (confidence {f['confidence']}; "
                          f"{len(f['citations'])} sources, {len(f['unverified_provisions'])} unverified)" for f in self.findings]})
        sig = tuple((f["rule"], f["severity"]) for f in self.findings)
        if sig != self._sig or msg.performative == "request":
            self._sig = sig
            report = {"type": "assessment", "findings": self.findings, "known_facts": dict(self.facts)}
            targets = {"regulator"} | ({msg.sender} if msg.performative == "request" and msg.sender in bus.agents else set())
            for to in sorted(targets):
                bus.send(t, self.name, to, "inform", report, in_reply_to=msg.id)


# ----------------------------------------------------------------------------------- regulator
class RegulatorRole:
    name = "regulator"

    def __init__(self, audit: AuditLog):
        self.audit, self.max_sev, self.actions, self.complaints = audit, None, [], 0
        self.requested_info = False

    def handle_message(self, msg: Message, bus: Bus) -> None:
        c, t = msg.content, msg.tick
        typ = c.get("type")
        if typ in ("complaint", "monitoring_finding", "provider_statement", "compliance_report"):
            self.complaints += typ == "complaint"
            self.audit.append(t, self.name, "intake", {"from": msg.sender, "type": typ, "text": c.get("text"),
                                                       "facts": c.get("facts", {})})
            bus.send(t, self.name, "advisor", "request", {"type": "assessment_request", "facts": c.get("facts", {})},
                     in_reply_to=msg.id)
            if typ == "complaint" and not self.requested_info:
                self.requested_info = True
                bus.send(t, self.name, "provider", "request", {
                    "type": "information_request",
                    "questions": ["Which reward and monetisation mechanics are active?", "Which sensor data leaves the device?"]})
        elif typ == "assessment":
            findings = c["findings"]
            sev = findings[0]["severity"] if findings else "info"
            actions = list(LADDER[sev])
            for f in findings:
                extra = ESCALATIONS.get(f["rule"], []) + (LADDER["contested"] if f["severity"] == "contested" else [])
                actions += [a for a in extra if a not in actions]
            if sev != self.max_sev or actions != self.actions:
                prev = self.max_sev
                self.max_sev, self.actions = sev, actions
                self.audit.append(t, self.name, "enforcement_decision", {
                    "severity": sev, "previous_severity": prev, "actions": actions,
                    "basis": [{"rule": f["rule"], "severity": f["severity"], "confidence": f["confidence"],
                               "sources": [f"{x['doc_id']} {x['ref']} ({'verified' if x['verified'] == 'true' else 'UNVERIFIED'})"
                                           for x in f["citations"]]} for f in findings[:3]],
                    "rationale": ("De-escalation: findings no longer support the previous action level."
                                  if prev and SEV_ORDER.index(sev) < SEV_ORDER.index(prev) else
                                  f"Highest finding is '{sev}': applying ladder {actions}.")})
                if sev in ("prohibited", "non_compliant"):
                    bus.send(t, self.name, "provider", "request", {"type": "enforcement_order", "actions": actions})
