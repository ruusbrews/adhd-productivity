#!/usr/bin/env bash
# Hackathon task 2: run the ITU reference ingest on knowledge/InputDocs, then compare retrieval with BM25.
# Run from Git Bash (Windows) at the repo root:
#     bash scripts/run_itu_ingest.sh
# Needs: Ollama running with nomic-embed-text pulled; ITUAIReadiness cloned next to this repo.
# BASE_PY must be Python 3.11-3.13 (chromadb had no 3.14 wheels when this was run).
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
ITU_SIM="${ITU_SIM:-$REPO/../ITUAIReadiness/simulation}"
OUT="$REPO/runs/itu_ingest"
BASE_PY="${BASE_PY:-python}"
VPY="$ITU_SIM/.venv/Scripts/python.exe"

# 1. ITU environment (separate venv inside the ITU clone).
if [ ! -x "$VPY" ]; then
  "$BASE_PY" -m venv "$ITU_SIM/.venv"
  "$VPY" -m pip install -q --upgrade pip
  "$VPY" -m pip install -q -r "$ITU_SIM/requirements.txt"
fi
"$VPY" -c "import chromadb, ollama, fitz; print('chromadb', chromadb.__version__)"

# 2. Regenerate InputDocs from the register so the ingest sees the latest verification edits.
( cd "$REPO" && PYTHONPATH=src python -m adhd_kb.build > /dev/null )

# 3. ITU ingest, unmodified, into a fresh ChromaDB under runs/itu_ingest.
rm -rf "$OUT/chromadb"; mkdir -p "$OUT"
export AIREADY_CHROMADB_DIR="$OUT/chromadb" PYTHONIOENCODING=utf-8
( cd "$ITU_SIM" && "$VPY" -m server.knowledge.ingest --dir "$REPO/knowledge/InputDocs" ) 2>&1 | tee "$OUT/ingest_log.txt"

# 4. Retrieval comparison -> runs/itu_ingest/comparison.{json,md}
"$VPY" "$REPO/scripts/compare_itu_retrieval.py" --itu-sim "$ITU_SIM" --chroma "$OUT/chromadb" --out "$OUT"
echo "done: $OUT"
