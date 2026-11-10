#!/usr/bin/env bash
# Reproduce the submitted results from the repo root (Git Bash on Windows, or any POSIX shell):
#     bash scripts/reproduce.sh             # use the committed KB in data/kb
#     bash scripts/reproduce.sh --rebuild   # regenerate data/kb from docs/research first (after editing the register)
# 1. (optional) rebuild the KB  2. run the error scenario with the policy check on and off
# 3. print a readable story of the run  4. run the tests (if pytest is installed)
set -euo pipefail
cd "$(dirname "$0")/.."
export PYTHONPATH=src PYTHONIOENCODING=utf-8
PY="${PY:-python}"

if [ "${1:-}" = "--rebuild" ]; then
  echo "== 1. Rebuild the knowledge base from docs/research =="
  "$PY" -m adhd_kb.build | tail -n 12
else
  echo "== 1. Using the committed knowledge base in data/kb (pass --rebuild after editing the register) =="
fi

echo; echo "== 2a. Error scenario, policy check ON  -> runs/scenario =="
"$PY" -m adhd_agent.scenario scenarios/error_scenario.json --out runs/scenario | grep -E "^(PASS|FAIL)"

echo; echo "== 2b. Same scenario, policy check OFF -> runs/ablation_guardrail_False =="
"$PY" -m adhd_agent.scenario scenarios/error_scenario.json --out runs/ablation_guardrail_False --no-guardrail | grep -E "^(PASS|FAIL)"

echo; echo "== 2c. Baselines over 20 seeds (also refreshes runs/ablation_guardrail_True/False) =="
"$PY" -m adhd_agent.compare --seeds 20

echo; echo "== 3. What happened in the run (policy check ON) =="
"$PY" scripts/narrate_run.py runs/scenario/audit.jsonl

echo; echo "== 4. Tests =="
if "$PY" -c "import pytest" 2>/dev/null; then "$PY" -m pytest -q; else echo "pytest not installed: skipped"; fi
