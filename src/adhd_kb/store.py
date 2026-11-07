"""Dependency-free knowledge-base store with BM25 retrieval.

Records use the same flat string-valued metadata keys as the ITU reference ingest
(source_file, source_type, country, chunk_index, total_chunks, ingested_at,
document_category), so the same files can also be ingested with ITU's own Chroma +
nomic-embed-text pipeline (see README). BM25 is the offline default so the demo runs
anywhere; a dense retriever can be swapped in behind `KnowledgeBase.search`.
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INDEX_DIR = ROOT / "data" / "kb" / "index"
COLLECTIONS = ("kb_policy", "kb_interventions", "kb_evidence", "kb_gaps")

_TOKEN = re.compile(r"[a-z0-9]+")
_STOP = frozenset(
    "a an and are as at be by for from has have in into is it its of on or that the their this to was were will with "
    "which not no than then there these those can may also per via".split()
)


def tokenize(text: str) -> list[str]:
    toks = [t for t in _TOKEN.findall(text.lower()) if t not in _STOP and len(t) > 1]
    # light stemming: plural / -ing so "notifications" matches "notification"
    return [re.sub(r"(ing|es|s)$", "", t) if len(t) > 4 else t for t in toks]


@dataclass
class Hit:
    id: str
    collection: str
    score: float
    text: str
    metadata: dict

    def cite(self) -> dict:
        m = self.metadata
        return {
            "record_id": self.id,
            "collection": self.collection,
            "doc_id": m.get("doc_id") or m.get("plan_id") or m.get("gap_id") or self.id,
            "ref": m.get("ref", ""),
            "verified": m.get("verified", "n/a"),
            "url": m.get("url_primary", ""),
            "score": round(self.score, 3),
        }


class _BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.docs, self.k1, self.b = docs, k1, b
        self.tf = [Counter(d) for d in docs]
        self.avg = (sum(len(d) for d in docs) / len(docs)) if docs else 0.0
        df = Counter(t for d in docs for t in set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def score(self, query: list[str], i: int) -> float:
        tf, dl, s = self.tf[i], len(self.docs[i]), 0.0
        for t in query:
            f = tf.get(t, 0)
            if f:
                s += self.idf.get(t, 0.0) * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * dl / self.avg))
        return s


class KnowledgeBase:
    def __init__(self, index_dir: Path = INDEX_DIR):
        self.records: dict[str, list[dict]] = {}
        self._bm25: dict[str, _BM25] = {}
        for name in COLLECTIONS:
            path = index_dir / f"{name}.jsonl"
            rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
            self.records[name] = rows
            # tags/metadata words are part of the indexed text so tag-style queries retrieve
            self._bm25[name] = _BM25([tokenize(r["text"] + " " + r["metadata"].get("tags", "").replace(",", " "))
                                      for r in rows])

    def stats(self) -> dict[str, int]:
        return {k: len(v) for k, v in self.records.items()}

    def get(self, collection: str, record_id: str) -> dict | None:
        return next((r for r in self.records[collection] if r["id"] == record_id), None)

    def search(self, query: str, collections: tuple[str, ...] = ("kb_policy",), k: int = 5,
               where: dict | None = None, min_score: float = 0.0) -> list[Hit]:
        q = tokenize(query)
        hits: list[Hit] = []
        for name in collections:
            for i, r in enumerate(self.records[name]):
                if where and any(r["metadata"].get(key) != val for key, val in where.items()):
                    continue
                s = self._bm25[name].score(q, i)
                if s > min_score:
                    hits.append(Hit(r["id"], name, s, r["text"], r["metadata"]))
        hits.sort(key=lambda h: h.score, reverse=True)
        return hits[:k]
