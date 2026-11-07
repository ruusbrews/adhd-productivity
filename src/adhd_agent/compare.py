"""Baseline comparison inside the sandbox: no intervention vs fixed schedule vs BDI + KB.

ILLUSTRATIVE ONLY. Simulated effect sizes are design assumptions (see simulator.py), so these numbers show
that the loop closes and behaves sensibly, not that any intervention works. The hackathon does not score
prototype accuracy; the research study evaluates these baselines properly.

    python -m adhd_agent.compare [--seeds 30] [--ticks 120]
"""
from __future__ import annotations

import argparse
import statistics as st
from pathlib import Path

from adhd_agent.audit import AuditLog
from adhd_agent.bdi import BDIAgent
from adhd_agent.scenario import ROOT, load_plans, run
from adhd_agent.simulator import PROFILES, SimulatedUser
from adhd_kb.store import KnowledgeBase

FULL_CONSENT = {"gaze": True, "hrv_eda": True, "motion": True}


def run_strategy(strategy: str, profile: str, seed: int, ticks: int, kb: KnowledgeBase, plans: list[dict]) -> dict:
    user = SimulatedUser(profile, "adult", seed=seed)
    agent = BDIAgent(kb, plans, AuditLog(), profile, "adult", consent=FULL_CONSENT) if strategy == "bdi_kb" else None
    for _ in range(ticks):
        frame = user.step()
        if agent:
            agent.tick(frame, user)
        elif strategy == "fixed_schedule" and frame["tick"] % 50 == 0:   # fixed 25-minute break, ignores state
            user.receive("timed-breaks-pomodoro", "push")
    return user.metrics()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--ticks", type=int, default=120)
    a = ap.parse_args()
    kb, plans = KnowledgeBase(), load_plans()
    cols = ("task_progress", "focus_fraction", "omission_rate", "commission_rate", "prompts", "unneeded_prompts")
    print(f"{a.seeds} seeds x {a.ticks} ticks ({a.ticks // 2} min); mean values; simulated effects are assumptions\n")
    print(f"{'profile':22}{'strategy':16}" + "".join(f"{c:>17}" for c in cols))
    for prof in PROFILES:
        for strat in ("no_intervention", "fixed_schedule", "bdi_kb"):
            rows = [run_strategy(strat, prof, s, a.ticks, kb, plans) for s in range(a.seeds)]
            print(f"{prof:22}{strat:16}" + "".join(f"{st.mean(r[c] for r in rows):17.3f}" for c in cols))
        print()
    print("Guardrail ablation on the error scenario (same seed, engagement mechanics injected by the provider):")
    for g in (True, False):
        s = run(ROOT / "scenarios" / "error_scenario.json", Path("runs") / f"ablation_guardrail_{g}", guardrail=g)
        m = s["user_metrics"]
        print(f"  guardrail={str(g):5}  bait_deliveries={m['bait_deliveries']:3}  compulsion_index={m['compulsion_index']:.2f}  "
              f"assertions={s['assertions_passed']}")


if __name__ == "__main__":
    main()
