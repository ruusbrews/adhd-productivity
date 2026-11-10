"""Compare ITU reference retrieval (ChromaDB + nomic-embed-text) with our offline BM25 retriever.

Run with the ITU venv Python, after the ITU ingest has written its ChromaDB:
    python scripts/compare_itu_retrieval.py --itu-sim <ITUAIReadiness/simulation> --chroma runs/itu_ingest/chromadb

Writes runs/itu_ingest/comparison.json and runs/itu_ingest/comparison.md.
The ITU side uses ITU's own KnowledgeBase.search and embed_texts, unmodified.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Queries 1-4 are the regression queries in tests/test_core.py (expected top document known).
# Queries 5-8 come from the error scenario; no single right answer, so we only report agreement.
QUERIES = [
    ("emotion inference attention students school biometric", "ec-guidelines-prohibited-ai-practices-2025"),
    ("streak variable rewards minors notification default", "eu-dsa-art28-minors-guidelines-2025"),
    ("special nature data children health permit", "qatar-pdppl-13-2016"),
    ("wellness claim medical device ADHD", "fda-general-wellness-2026"),
    ("in-app purchases promoted to children manipulative design", None),
    ("targeted advertising based on inferred disability or health signals", None),
    ("explicit consent for processing sensitive health or biometric data", None),
    ("human oversight and review of automated decisions about a person", None),
]
K = 3


def doc_id_from_file(source_file: str, doc_ids: list[str]) -> str:
    """InputDocs files are named <Jurisdiction>_<doc_id>.md; jurisdictions can contain underscores."""
    stem = Path(source_file).stem
    for d in sorted(doc_ids, key=len, reverse=True):
        if stem.endswith("_" + d) or stem == d:
            return d
    return stem


def top_docs_itu(kb, embed_texts, query: str, doc_ids: list[str], k: int) -> list[dict]:
    emb = embed_texts([query])[0]
    res = kb.search(emb, n_results=30)  # chunks; several can come from one document
    seen, out = set(), []
    for meta, dist in zip(res["metadatas"][0], res["distances"][0]):
        d = doc_id_from_file(meta["source_file"], doc_ids)
        if d in seen:
            continue
        seen.add(d)
        out.append({"doc_id": d, "cosine_distance": round(dist, 4), "chunk": f'{meta["chunk_index"]}/{meta["total_chunks"]}',
                    "country": meta.get("country"), "document_category": meta.get("document_category")})
        if len(out) == k:
            break
    return out


def top_docs_bm25(bm25, query: str, k: int) -> list[dict]:
    seen, out = set(), []
    for h in bm25.search(query, k=50):
        d = h.metadata["doc_id"]
        if d in seen:
            continue
        seen.add(d)
        out.append({"doc_id": d, "bm25": round(h.score, 3)})
        if len(out) == k:
            break
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--itu-sim", type=Path, required=True, help="path to ITUAIReadiness/simulation")
    ap.add_argument("--chroma", type=Path, default=ROOT / "runs" / "itu_ingest" / "chromadb")
    ap.add_argument("--out", type=Path, default=ROOT / "runs" / "itu_ingest")
    args = ap.parse_args()

    os.environ["AIREADY_CHROMADB_DIR"] = str(args.chroma.resolve())
    sys.path.insert(0, str(args.itu_sim.resolve()))
    sys.path.insert(0, str(ROOT / "src"))
    from server.knowledge.ingest import embed_texts  # ITU reference code
    from server.knowledge.kb import KnowledgeBase as ITUKB
    from adhd_kb.store import KnowledgeBase as BM25KB

    itu, bm25 = ITUKB(), BM25KB()
    doc_ids = sorted({r["metadata"]["doc_id"] for r in bm25.records["kb_policy"]})

    # What metadata did ITU's ingest actually write? (country is inferred from file names)
    allmeta = itu.get_all()["metadatas"]
    files = Counter(m["source_file"] for m in allmeta)
    countries = Counter(m.get("country") for m in allmeta)

    rows = []
    for q, expected in QUERIES:
        a = top_docs_itu(itu, embed_texts, q, doc_ids, K)
        b = top_docs_bm25(bm25, q, K)
        ia, ib = [x["doc_id"] for x in a], [x["doc_id"] for x in b]
        rows.append({
            "query": q, "expected_top1": expected, "itu_topk": a, "bm25_topk": b,
            "top1_agree": ia[:1] == ib[:1],
            "overlap_at_k": len(set(ia) & set(ib)),
            "itu_hit_at_1": (ia[:1] == [expected]) if expected else None,
            "itu_hit_at_k": (expected in ia) if expected else None,
            "bm25_hit_at_1": (ib[:1] == [expected]) if expected else None,
        })

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "kb_stats": itu.stats(),
        "files_in_kb_main": len(files),
        "chunks_in_kb_main": sum(files.values()),
        "country_metadata": dict(countries),
        "k": K,
        "queries": rows,
    }
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "comparison.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    labelled = [r for r in rows if r["expected_top1"]]
    md = [
        "# ITU reference ingest: retrieval check",
        "",
        f"Generated {summary['generated_at']}. ITU pipeline (CrashingGuru/ITUAIReadiness, `simulation/`, unmodified): "
        "256-word chunks, 30 overlap, Ollama `nomic-embed-text`, ChromaDB cosine. Compared with our offline BM25 retriever "
        f"(`src/adhd_kb/store.py`) at document level, top {K}.",
        "",
        f"* KB collections: {summary['kb_stats']}",
        f"* `kb_main`: {summary['chunks_in_kb_main']} chunks from {summary['files_in_kb_main']} files",
        f"* `country` metadata written by ITU's `infer_country()`: {summary['country_metadata']}",
        "",
        f"Labelled queries (from `tests/test_core.py`): ITU top-1 {sum(r['itu_hit_at_1'] for r in labelled)}/{len(labelled)}, "
        f"ITU top-{K} {sum(r['itu_hit_at_k'] for r in labelled)}/{len(labelled)}, "
        f"BM25 top-1 {sum(r['bm25_hit_at_1'] for r in labelled)}/{len(labelled)}.",
        f"All queries: top-1 agreement {sum(r['top1_agree'] for r in rows)}/{len(rows)}.",
        "",
        "| # | Query | Expected | ITU top-3 | BM25 top-3 |",
        "|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        md.append(f"| {i} | {r['query']} | {r['expected_top1'] or '-'} | "
                  f"{'<br>'.join(x['doc_id'] for x in r['itu_topk'])} | {'<br>'.join(x['doc_id'] for x in r['bm25_topk'])} |")
    (args.out / "comparison.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
