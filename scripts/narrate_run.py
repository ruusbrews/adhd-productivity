"""Turn a scenario audit log into a short readable story of the run.

Usage (from the repo root):
    python scripts/narrate_run.py runs/scenario/audit.jsonl

Shows the first instance of each kind of moment (allowed, changed, blocked, adviser finding,
regulator action), not every tick. Useful for explaining the project and for the demo video.
"""
import json
import sys
from pathlib import Path

rows = [json.loads(line) for line in Path(sys.argv[1]).read_text(encoding="utf-8").splitlines() if line.strip()]


def cites(rule):
    return "; ".join(f"{c['doc_id']} {c.get('ref', '')} ({'verified' if c['verified'] == 'true' else 'UNVERIFIED'})"
                     for c in rule["citations"][:3]) or "none found by retrieval"


def show_decision(r, label):
    p = r["payload"]
    pr = p["policy_review"]
    met = [f"{c['signal']}={c.get('value')}" for c in p["conditions"] if c.get("ok")]
    print(f"\n[tick {r['tick']}] {label}")
    print(f"  Agent wants: {p['intention']}  (score {p['score']}{', FORCED by provider' if p['forced_by_provider'] else ''})")
    print(f"  Because: {', '.join(met)}")
    print(f"  Beliefs: {p['beliefs']}")
    print(f"  Policy check: {pr['decision'].upper()}")
    for rule in pr["rules"]:
        print(f"    - {rule['rule']}: {rule['reason']}")
        print(f"      cites: {cites(rule)}")


seen = set()
start = rows[0]["payload"]
print("SETUP:", start["name"])
print("  user:", start["user"], "| KB:", start["kb"])

for r in rows:
    a, e, p, t = r["agent"], r["event"], r["payload"], r["tick"]
    if a == "bdi" and e == "decision":
        d = p["policy_review"]["decision"]
        rules = tuple(x["rule"] for x in p["policy_review"]["rules"])
        key = (d, rules[:1], d == "allow" and t > 80)
        if key in seen:
            continue
        seen.add(key)
        if p["intention"] == "infer-attention-from-biometrics":   # perception-step check, not an intervention
            print(f"\n[tick {t}] Perception step: biometric attention inference {d.upper()}ED")
            print(f"  {p['rationale']}")
            for rule in p["policy_review"]["rules"]:
                print(f"    - {rule['rule']}  cites: {cites(rule)}")
            continue
        show_decision(r, {"allow": "Support intervention ALLOWED", "modify": "Intervention CHANGED",
                          "block": "Intervention BLOCKED"}[d])
    elif a == "bdi" and e == "execution" and ("exec", p["delivery"]) not in seen:
        seen.add(("exec", p["delivery"]))
        print(f"  -> delivered '{p['plan']}' as {p['delivery']}; user response: {p['outcome']}")
    elif a == "bdi" and e == "belief_revision":
        print(f"\n[tick {t}] Provider changes the app: {p['changed']}  ({p['note']})")
    elif a == "regulator" and e == "intake":
        print(f"\n[tick {t}] Regulator receives {p['type']} from {p['from']}: \"{p['text']}\"")
    elif a == "advisor" and e == "assessment":
        sig = tuple((f["rule"], f["severity"]) for f in p["findings"])
        if ("adv", sig) in seen:
            continue
        seen.add(("adv", sig))
        print(f"[tick {t}] Policy adviser assessment (triggered by {p['trigger']['type']}):")
        for f in p["findings"]:
            miss = f"; MISSING: {f['missing_information']}" if f["missing_information"] else ""
            print(f"    - {f['rule']} -> {f['severity']} (confidence {f['confidence']}){miss}")
            print(f"      cites: {cites(f)}")
    elif a == "regulator" and e == "enforcement_decision":
        print(f"[tick {t}] REGULATOR ACTION: {p['actions']}")
        print(f"    rationale: {p['rationale']}")

print("\nEND OF RUN")
