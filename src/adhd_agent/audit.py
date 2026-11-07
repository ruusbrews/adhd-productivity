"""Append-only, hash-chained audit log (JSONL).

Every record stores the hash of the previous record, so any later edit/deletion breaks the chain
(`verify`). The agents write *structured reasoning traces* (beliefs, candidates, rule results,
retrieved policy records with verification status, decision, rationale) rather than free-form
chain-of-thought, so each decision can be reviewed and traced to KB sources.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

GENESIS = "0" * 64


def _canon(obj) -> str:
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


class AuditLog:
    def __init__(self, path: Path | str | None = None):
        self.path = Path(path) if path else None
        self.records: list[dict] = []
        self._prev = GENESIS
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text("", encoding="utf-8")

    def append(self, tick: int, agent: str, event: str, payload: dict) -> dict:
        rec = {"seq": len(self.records), "tick": tick, "agent": agent, "event": event,
               "payload": payload, "prev_hash": self._prev}
        rec["hash"] = hashlib.sha256((self._prev + _canon(rec)).encode()).hexdigest()
        self._prev = rec["hash"]
        self.records.append(rec)
        if self.path:
            with self.path.open("a", encoding="utf-8") as f:
                f.write(_canon(rec) + "\n")
        return rec

    def where(self, **kw) -> list[dict]:
        return [r for r in self.records if all(r.get(k) == v for k, v in kw.items())]


def verify(path: Path | str) -> tuple[bool, int, str]:
    """Re-compute the chain. Returns (ok, records_checked, message)."""
    prev, n = GENESIS, 0
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        rec = json.loads(line)
        stored = rec.pop("hash")
        if rec["prev_hash"] != prev:
            return False, n, f"broken link at seq {rec['seq']}"
        if hashlib.sha256((prev + _canon(rec)).encode()).hexdigest() != stored:
            return False, n, f"tampered record at seq {rec['seq']}"
        prev, n = stored, n + 1
    return True, n, "chain intact"
