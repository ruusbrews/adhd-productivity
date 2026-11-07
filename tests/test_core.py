import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import pytest  # noqa: E402

from adhd_agent.audit import AuditLog, verify  # noqa: E402
from adhd_agent.bdi import BDIAgent  # noqa: E402
from adhd_agent.guardrail import PolicyGuardrail  # noqa: E402
from adhd_agent.scenario import load_plans, run  # noqa: E402
from adhd_agent.simulator import SimulatedUser  # noqa: E402
from adhd_kb.store import KnowledgeBase  # noqa: E402


@pytest.fixture(scope="module")
def kb():
    return KnowledgeBase()


@pytest.fixture(scope="module")
def plans():
    return {p["plan_id"]: p for p in load_plans()}


def beliefs(**kw):
    b = {"age_group": "adult", "deployment_context": "consumer", "profile": "combined",
         "consent": {"task_telemetry": True, "self_report": True, "gaze": True, "hrv_eda": True, "motion": True},
         "attention_estimate": 0.3, "omission_rate": 0.3}
    b.update(kw)
    return b


# ---- KB -------------------------------------------------------------------------------------
def test_kb_sizes(kb):
    assert kb.stats() == {"kb_policy": 58, "kb_interventions": 19, "kb_evidence": 22, "kb_gaps": 12}


def test_normalisation(plans):
    assert plans["variable-ratio-rewards"]["kind"] == "catalogue_only"
    assert plans["notification-batching"]["kind"] == "standing_mode"
    assert plans["permit-fidget-during-wm-tasks"]["kind"] == "belief_modifier"
    assert all(c["operator"] in ("<", ">", ">=") for p in plans.values() for c in p["context_conditions"])
    assert plans["haptic-self-monitoring-cue"]["uses_biometric"] is False   # "no biometrics" must not match
    assert plans["hrv-biofeedback-breathing"]["uses_biometric"] is True


@pytest.mark.parametrize("query,expected", [
    ("emotion inference attention students school biometric", "ec-guidelines-prohibited-ai-practices-2025"),
    ("streak variable rewards minors notification default", "eu-dsa-art28-minors-guidelines-2025"),
    ("special nature data children health permit", "qatar-pdppl-13-2016"),
    ("wellness claim medical device ADHD", "fda-general-wellness-2026"),
])
def test_retrieval_top_hit(kb, query, expected):
    assert kb.search(query, k=3)[0].metadata["doc_id"] == expected


# ---- guardrail ------------------------------------------------------------------------------
def test_streak_blocked_for_minor_not_by_r1_for_adult(kb, plans):
    g = PolicyGuardrail(kb)
    minor = g.review({**plans["streak-counter"], "matched_signals": []}, beliefs(age_group="minor"))
    adult = g.review({**plans["streak-counter"], "matched_signals": []}, beliefs())
    assert minor.decision == "block" and "R1-persuasive-rewards-minors" in [r.rule_id for r in minor.results]
    assert "R1-persuasive-rewards-minors" not in [r.rule_id for r in adult.results]


def test_biometric_blocked_in_school(kb, plans):
    v = PolicyGuardrail(kb).review({**plans["self-monitoring-prompt"], "matched_signals": ["gaze_off_task"]},
                                   beliefs(deployment_context="school"))
    assert v.decision == "block"
    r3 = next(r for r in v.results if r.rule_id.startswith("R3"))
    assert {c["doc_id"] for c in r3.citations} >= {"eu-ai-act-2024-1689"}


def test_physiological_only_trigger_needs_behavioural_corroboration(kb, plans):
    g, p = PolicyGuardrail(kb), {**plans["hrv-biofeedback-breathing"], "matched_signals": ["hrv_rmssd", "eda"]}
    fired = lambda b: "R6-physiological-only-trigger" in [r.rule_id for r in g.review(p, b).results]
    assert fired(beliefs(speculative_opt_in=True, attention_estimate=0.8, omission_rate=0.02))
    assert not fired(beliefs(speculative_opt_in=True, attention_estimate=0.3))


def test_push_to_minor_is_modified_not_blocked(kb, plans):
    v = PolicyGuardrail(kb).review({**plans["movement-break-acute-exercise"], "matched_signals": ["fatigue"]},
                                   beliefs(age_group="minor"))
    assert v.decision == "modify" and v.modifications["delivery"] == "in_app_silent"


def test_every_citation_comes_from_retrieval(kb, plans):
    v = PolicyGuardrail(kb).review({**plans["streak-counter"], "matched_signals": []}, beliefs(age_group="minor"))
    known = {r["id"] for r in kb.records["kb_policy"]}
    assert all(c["record_id"] in known for r in v.results for c in r.citations)


# ---- consent / data minimisation ------------------------------------------------------------
def test_unconsented_channel_never_enters_beliefs(kb, plans):
    audit = AuditLog()
    agent = BDIAgent(kb, list(plans.values()), audit, "combined", consent={"gaze": False})
    user = SimulatedUser("combined", seed=1)
    for _ in range(20):
        agent.tick(user.step(), user)
    assert "gaze_off_task" not in agent.beliefs and "hrv_rmssd" not in agent.beliefs


# ---- audit ----------------------------------------------------------------------------------
def test_audit_chain_detects_tampering(tmp_path):
    log = AuditLog(tmp_path / "a.jsonl")
    for i in range(5):
        log.append(i, "x", "e", {"i": i})
    assert verify(tmp_path / "a.jsonl")[0]
    lines = (tmp_path / "a.jsonl").read_text().splitlines()
    rec = json.loads(lines[2])
    rec["payload"]["i"] = 99
    lines[2] = json.dumps(rec, sort_keys=True, separators=(",", ":"))
    (tmp_path / "a.jsonl").write_text("\n".join(lines) + "\n")
    assert not verify(tmp_path / "a.jsonl")[0]


# ---- scenario -------------------------------------------------------------------------------
def test_scenario_expected_outcomes_and_determinism(tmp_path):
    sc = ROOT / "scenarios" / "error_scenario.json"
    a, b = run(sc, tmp_path / "a"), run(sc, tmp_path / "b")
    assert a["assertions_passed"] == "10/10"
    assert a["user_metrics"] == b["user_metrics"] and a["blocking_decisions_by_rule"] == b["blocking_decisions_by_rule"]


def test_guardrail_ablation_changes_outcome(tmp_path):
    sc = ROOT / "scenarios" / "error_scenario.json"
    on, off = run(sc, tmp_path / "on"), run(sc, tmp_path / "off", guardrail=False)
    assert on["user_metrics"]["bait_deliveries"] == 0 < off["user_metrics"]["bait_deliveries"]
