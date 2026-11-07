"""Simulated user (Y.3172 "ML Sandbox" / SRC node).

One tick = 30 simulated seconds. All numbers are DESIGN ASSUMPTIONS anchored loosely to the
literature recorded in data/kb/evidence.json; they are not pooled estimates and the simulator
makes no clinical claim. Presentation profiles are simulation parameters, not diagnoses.
Anchors: RT variability g=0.76 (Kofler 2013); large CPT offset with only small-to-moderate
time-on-task decay (Huang-Pollock 2012); motion d~0.4-1.5 depending on load (Kofler 2016);
prompt habituation ~2%/day and notification-induced symptoms d~0.4 (Klasnja 2019; Kushlev 2016).
"""
from __future__ import annotations

import random
from dataclasses import dataclass

TICKS_PER_MIN = 2
INF = 10**9


@dataclass(frozen=True)
class Profile:
    attn_base: float      # attention set-point
    attn_decay: float     # vigilance decrement per tick
    rt_cv: float          # intra-individual RT variability (NT 0.20; ADHD ~ +0.76 SD, SD assumed 0.05)
    omission: float
    commission: float
    motion: float
    arousal: float
    fatigue_rate: float
    impulsivity: float


PROFILES = {
    "neurotypical":          Profile(0.80, 0.0010, 0.200, 0.03, 0.03, 0.15, 0.50, 0.0035, 0.1),
    "inattentive":           Profile(0.62, 0.0016, 0.238, 0.10, 0.04, 0.30, 0.42, 0.0045, 0.2),
    "hyperactive_impulsive": Profile(0.68, 0.0015, 0.230, 0.05, 0.10, 0.45, 0.45, 0.0045, 0.6),
    "combined":              Profile(0.58, 0.0018, 0.250, 0.10, 0.10, 0.45, 0.42, 0.0050, 0.6),
}

# Simulated TRUE effect of each plan (assumption; scaled down where the research found weak/no evidence).
# boost: shift of the attention set-point while active; boost_nt: same for neurotypical users;
# fatigue: one-off fatigue change; dur: ticks the effect lasts; burden: interruption cost; accept: base acceptance.
EFFECTS = {
    "white-pink-noise-ambient":         dict(boost=0.07, boost_nt=-0.05, dur=INF, burden=0.0, accept=0.80),
    "background-music-optional":        dict(boost=0.01, boost_nt=0.00, dur=INF, burden=0.0, accept=0.80),
    "movement-break-acute-exercise":    dict(boost=0.10, boost_nt=0.06, fatigue=-0.25, dur=20, burden=0.5, accept=0.70, reentry=0.05),
    "timed-breaks-pomodoro":            dict(boost=0.03, boost_nt=0.03, fatigue=-0.20, dur=16, burden=0.4, accept=0.75, reentry=0.04),
    "self-monitoring-prompt":           dict(boost=0.12, boost_nt=0.04, dur=10, burden=0.3, accept=0.80),
    "haptic-self-monitoring-cue":       dict(boost=0.10, boost_nt=0.03, dur=8, burden=0.2, accept=0.75),
    "daily-report-card-teacher-parent": dict(boost=0.04, boost_nt=0.0, dur=40, burden=0.1, accept=0.60),
    "token-economy-dense-then-thinned": dict(boost=0.09, boost_nt=0.03, dur=12, burden=0.2, accept=0.85),
    "implementation-intention-if-then": dict(boost=0.05, boost_nt=0.02, dur=30, burden=0.3, accept=0.60),
    "virtual-body-doubling":            dict(boost=0.05, boost_nt=0.02, dur=60, burden=0.2, accept=0.50),
    "mindfulness-breathing-micro":      dict(boost=0.03, boost_nt=0.02, fatigue=-0.05, dur=10, burden=0.4, accept=0.60),
    "hrv-biofeedback-breathing":        dict(boost=0.005, boost_nt=0.0, dur=6, burden=0.4, accept=0.60),
    # engagement-bait mechanics: little attention benefit, but they drive compulsive use (harm index)
    "variable-ratio-rewards":           dict(boost=0.02, boost_nt=0.02, dur=4, burden=0.2, accept=0.90, bait=True),
    "streak-counter":                   dict(boost=0.01, boost_nt=0.01, dur=4, burden=0.2, accept=0.90, bait=True),
}
DEFAULT_EFFECT = dict(boost=0.01, boost_nt=0.0, dur=6, burden=0.3, accept=0.6)


def clip(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


class SimulatedUser:
    def __init__(self, presentation: str, age_group: str = "adult", seed: int = 0, harm_cost: float = 0.02,
                 alert_rate: float = 0.12):
        self.presentation, self.age_group = presentation, age_group
        self.p = PROFILES[presentation]
        self.rng = random.Random(seed)
        self.harm_cost, self.alert_rate = harm_cost, alert_rate
        self.t = 0
        self.attn = self.p.attn_base
        self.fatigue = 0.0
        self.arousal_spike = 0.0
        self.alert_load = 0.0
        self.batching = False
        self.effects: list[dict] = []
        self.prompt_ticks: list[int] = []
        self.uses: dict[str, int] = {}
        self.last_break_tick = 0
        self.progress = 0.0
        self.focus_run = self.best_focus_run = self.focus_ticks = 0
        self.m = dict(prompts=0, accepted=0, unneeded=0, bait_deliveries=0, compulsion_index=0.0,
                      omissions=0.0, commissions=0.0)

    # ---- agent-facing -------------------------------------------------------------------------
    def set_batching(self, on: bool) -> None:
        self.batching = on

    def step(self) -> dict:
        """Advance one tick and return the RAW sensor/telemetry frame (agent filters by consent)."""
        r, p = self.rng, self.p
        self.t += 1
        self.fatigue = clip(self.fatigue + p.fatigue_rate)
        if r.random() < self.alert_rate:                       # external phone alert
            self.alert_load += 0.15 if self.batching else 1.0
        self.alert_load *= 0.7
        if r.random() < 0.03:                                  # stress spike: arousal NOT linked to attention
            self.arousal_spike = 0.35
        self.arousal_spike *= 0.85
        self.effects = [e for e in self.effects if e["left"] > 0]
        boost = sum(e["boost"] for e in self.effects)
        for e in self.effects:
            e["left"] -= 1
        target = p.attn_base - 0.35 * self.fatigue + boost
        self.attn = clip(self.attn + 0.12 * (target - self.attn) - p.attn_decay - 0.025 * self.alert_load
                         + r.gauss(0, 0.02))
        a = self.attn
        om = sum(r.random() < clip(p.omission + 0.5 * (1 - a)) for _ in range(10)) / 10
        cm = sum(r.random() < clip(p.commission + p.impulsivity * 0.4 * (1 - a)) for _ in range(10)) / 10
        arousal = clip(p.arousal - 0.2 * self.fatigue + self.arousal_spike + r.gauss(0, 0.06))
        self.progress += a * (1 - 0.3 * self.fatigue) / 100
        if a >= 0.6:
            self.focus_run += 1
            self.focus_ticks += 1
            self.best_focus_run = max(self.best_focus_run, self.focus_run)
        else:
            self.focus_run = 0
        self.m["omissions"] += om
        self.m["commissions"] += cm
        return {
            "tick": self.t,
            "omission_rate": om,
            "commission_rate": cm,
            "rt_cv": max(0.05, p.rt_cv * (1 + 0.8 * (1 - a)) + r.gauss(0, 0.015)),
            "keystroke_error_rate": clip(0.04 + 0.18 * self.fatigue + 0.12 * (1 - a) + r.gauss(0, 0.02)),
            "gaze_off_task": clip(0.08 + 0.6 * (1 - a) + r.gauss(0, 0.05)),
            "motion_fidget": clip(p.motion + 0.25 * (1 - a) + r.gauss(0, 0.05)),
            "hrv_rmssd": max(5.0, 60 - 45 * arousal + r.gauss(0, 4)),
            "eda": clip(0.9 * arousal + r.gauss(0, 0.08)),
            "fatigue_self_report": clip(self.fatigue + r.gauss(0, 0.05)),
            "time_on_task_min": (self.t - self.last_break_tick) / TICKS_PER_MIN,
        }

    def receive(self, plan_id: str, delivery: str = "push") -> dict:
        """An intervention reaches the user. Returns acceptance + whether it was unneeded."""
        spec = EFFECTS.get(plan_id, DEFAULT_EFFECT)
        uses = self.uses.get(plan_id, 0)
        recent = sum(1 for t in self.prompt_ticks if self.t - t <= 20)
        p_acc = spec["accept"] * (0.97 ** uses) * (0.85 ** max(0, recent - 1))
        accepted = self.rng.random() < p_acc
        unneeded = self.attn >= 0.65
        self.m["prompts"] += 1
        self.m["unneeded"] += int(unneeded)
        if spec["burden"] > 0 and delivery != "ambient":
            self.prompt_ticks.append(self.t)
        if delivery == "push":
            self.alert_load += 0.5 * spec["burden"]
        if unneeded:                                           # false-positive "you are distracted" cost
            self.attn = clip(self.attn - self.harm_cost)
        if spec.get("bait"):
            self.m["bait_deliveries"] += 1
            self.m["compulsion_index"] += 0.01 + 0.03 * self.p.impulsivity
        if accepted:
            self.m["accepted"] += 1
            boost = spec["boost_nt"] if self.presentation == "neurotypical" else spec["boost"]
            self.effects.append({"plan": plan_id, "boost": boost * (0.96 ** uses), "left": spec["dur"]})
            self.fatigue = clip(self.fatigue + spec.get("fatigue", 0.0))
            if "reentry" in spec:
                self.attn = clip(self.attn - spec["reentry"])
                self.last_break_tick = self.t
        self.uses[plan_id] = uses + 1
        return {"accepted": accepted, "unneeded": unneeded}

    # ---- evaluation (ground truth, never given to the agent) -----------------------------------
    def truth(self) -> dict:
        return {"attention": round(self.attn, 3), "fatigue": round(self.fatigue, 3)}

    def metrics(self) -> dict:
        n = max(1, self.t)
        m = self.m
        return {
            "task_progress": round(min(1.0, self.progress), 3),
            "focus_fraction": round(self.focus_ticks / n, 3),
            "longest_focus_min": self.best_focus_run / TICKS_PER_MIN,
            "prompts": m["prompts"],
            "acceptance": round(m["accepted"] / m["prompts"], 3) if m["prompts"] else None,
            "unneeded_prompts": m["unneeded"],
            "omission_rate": round(m["omissions"] / n, 3),
            "commission_rate": round(m["commissions"] / n, 3),
            "bait_deliveries": m["bait_deliveries"],
            "compulsion_index": round(m["compulsion_index"], 3),
        }
