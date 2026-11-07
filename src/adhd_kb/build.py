"""Build the knowledge base from the three Deep Research outputs in docs/research/.

Outputs (all under data/kb/):
  policy_register.json   cleaned JSON register (37 documents)
  policy_gaps.json       candidate gaps parsed from the register report
  interventions.json     the plan library (normalised, see NORMALISATION below)
  evidence.json          signal / parameter / tool records parsed from the B2 tables
  index/*.jsonl          retrieval records, one file per collection
and  knowledge/InputDocs/  ITU-reference-code compatible source documents.

Run:  python -m adhd_kb.build        (from the src/ directory, or with PYTHONPATH=src)
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RESEARCH = ROOT / "docs" / "research"
KB_DIR = ROOT / "data" / "kb"
INDEX_DIR = KB_DIR / "index"
INPUT_DOCS = ROOT / "knowledge" / "InputDocs"

CITE_RE = re.compile(r"\\\[\d+\\\]")  # markdown footnote markers like \[12\]


def clean(text: str) -> str:
    text = CITE_RE.sub("", text)
    text = text.replace("**", "").replace("\\_", "_")
    return re.sub(r"[ \t]+", " ", text).strip()


def extract_json_block(md: str):
    m = re.search(r"```json\s*(.*?)```", md, re.S)
    if not m:
        raise ValueError("no ```json block found")
    return json.loads(CITE_RE.sub("", m.group(1)))


# --------------------------------------------------------------------------- policy
def parse_gaps(md: str, doc_ids: list[str]) -> list[dict]:
    section = md.split("## CANDIDATE POLICY GAPS", 1)[1].split("## Recommendations", 1)[0]
    chunks = re.split(r"\n(?=\d+\. \*\*)", section.strip())
    gaps = []
    for ch in chunks:
        m = re.match(r"(\d+)\. \*\*(.+?)\*\*(.*)", ch.strip(), re.S)
        if not m:
            continue
        num, title, rest = int(m.group(1)), clean(m.group(2)), clean(m.group(3))
        gtype = re.search(r"\*Type:\*\s*([a-z ]+)", ch)
        gaps.append(
            {
                "gap_id": f"gap-{num:02d}",
                "title": title.rstrip("."),
                "type": gtype.group(1).strip() if gtype else "unspecified",
                "text": re.sub(r"\s+", " ", rest),
                "doc_ids": sorted({d for d in doc_ids if d in ch}),
            }
        )
    return gaps


def policy_records(register: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = []
    for d in register:
        provs = d.get("relevant_provisions", [])
        for i, p in enumerate(provs):
            status = "verified" if p.get("verified") else "UNVERIFIED"
            text = (
                f"{d['title']} ({d['jurisdiction']}, {d['doc_type']}, {d['year']}, {d['status']}). "
                f"Provision {p['ref']}: {p['paraphrase']} "
                f"Relevance to ADHD-support app: {p['relevance_to_adhd_app']} "
                f"Tags: {' '.join(d.get('tags', []))}. Verification: {status}."
            )
            out.append(
                {
                    "id": f"{d['doc_id']}::{i}",
                    "text": text,
                    "metadata": {
                        "doc_id": d["doc_id"],
                        "title": d["title"],
                        "ref": p["ref"],
                        "jurisdiction": d["jurisdiction"],
                        "doc_type": d["doc_type"],
                        "year": str(d["year"]),
                        "status": d["status"],
                        "verified": str(bool(p.get("verified"))).lower(),
                        "tags": ",".join(d.get("tags", [])),
                        "url_primary": d["url_primary"],
                        "license_or_reuse_terms": d["license_or_reuse_terms"],
                        # keys shared with the ITU reference ingest schema
                        "source_file": f"{d['doc_id']}.md",
                        "source_type": {"law": "policy_document", "regulation": "policy_document",
                                        "national_strategy": "national_strategy",
                                        "standard": "standards_document"}.get(
                            d["doc_type"], "international_org_report"),
                        "country": d["jurisdiction"],
                        "chunk_index": str(i),
                        "total_chunks": str(len(provs)),
                        "ingested_at": now,
                        "document_category": "Policy_Register",
                    },
                }
            )
    return out


def write_itu_input_docs(register: list[dict]) -> int:
    """One text file per policy document so the ITU ingest.py can be run unmodified.

    NB: ITU's infer_country() works from the *filename*; the jurisdiction is put first.
    Only paraphrases and links are written (many sources are (c) restricted).
    """
    folder = INPUT_DOCS / "Policy_Register"
    folder.mkdir(parents=True, exist_ok=True)
    for d in register:
        lines = [
            f"# {d['title']}",
            f"Issuer: {d['issuer']}",
            f"Jurisdiction: {d['jurisdiction']} | Type: {d['doc_type']} | Year: {d['year']} | Status: {d['status']}",
            f"Primary source: {d['url_primary']}",
            f"Reuse terms: {d['license_or_reuse_terms']}",
            f"Tags: {', '.join(d.get('tags', []))}",
            "",
            "## Provisions relevant to a digital ADHD-support app (paraphrased)",
        ]
        for p in d.get("relevant_provisions", []):
            v = "verified" if p.get("verified") else "UNVERIFIED"
            lines += ["", f"### {p['ref']} [{v}]", p["paraphrase"], f"Relevance: {p['relevance_to_adhd_app']}"]
        juris = re.sub(r"[^A-Za-z]+", "_", d["jurisdiction"]).strip("_")
        (folder / f"{juris}_{d['doc_id']}.md").write_text("\n".join(lines), encoding="utf-8")
    return len(register)


# --------------------------------------------------------------------- interventions
# NORMALISATION (our design decisions, applied on top of the research output):
# * the source gives conditions without AND/OR semantics -> condition_logic per plan below
# * "between" with a single value is malformed in the source -> normalised to ">="
# * plans with no conditions are catalogue-only (never adaptive) unless a provider injects a trigger
# * two records are not interventions but modifiers of the agent's beliefs / standing mode
CONDITION_LOGIC_ANY = {"white-pink-noise-ambient", "movement-break-acute-exercise", "timed-breaks-pomodoro"}
KIND_OVERRIDES = {
    "permit-fidget-during-wm-tasks": "belief_modifier",
    "notification-batching": "standing_mode",
}
BIOMETRIC_SIGNALS = {"hrv_rmssd", "eda", "gaze_off_task", "motion_fidget"}


def normalise_plan(p: dict) -> dict:
    p = json.loads(json.dumps(p))  # deep copy
    notes = []
    for c in p.get("context_conditions", []):
        if c["operator"] == "between":
            c["operator"] = ">="
            notes.append(f"{c['signal']}: malformed 'between' with one value normalised to '>='")
    p["condition_logic"] = "any" if p["plan_id"] in CONDITION_LOGIC_ANY else "all"
    p["kind"] = KIND_OVERRIDES.get(p["plan_id"], "intervention" if p.get("context_conditions") else "catalogue_only")
    data_used = " ".join(p.get("data_used", [])).lower()
    # the research flags biometric inputs as "(... biometric ..., flag)"; "no biometrics" must not match
    p["uses_biometric"] = bool(
        re.search(r"biometric[^)]*flag", data_used)
        or any(c["signal"] in BIOMETRIC_SIGNALS for c in p.get("context_conditions", []))
    )
    p["normalisation_notes"] = notes
    return p


def intervention_records(plans: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    out = []
    for p in plans:
        text = (
            f"Intervention {p['name']} ({p['modality']}, {p['delivery']}). {p['description']} "
            f"Expected effect: {p['expected_effect']} Evidence ({p['evidence_level']}): {p['evidence_summary']} "
            f"Contraindications: {'; '.join(p['contraindications'])}. Risks: {'; '.join(p['risks'])}. "
            f"Data used: {'; '.join(p['data_used'])}. Regulatory notes: {p['regulatory_notes']} "
            f"Reward schedule: {p['reward_schedule']}. Minors: {p['suitable_for_minors']}. Claim class: {p['claim_wording_class']}."
        )
        out.append(
            {
                "id": p["plan_id"],
                "text": text,
                "metadata": {
                    "plan_id": p["plan_id"],
                    "evidence_level": p["evidence_level"],
                    "reward_schedule": p["reward_schedule"],
                    "suitable_for_minors": p["suitable_for_minors"],
                    "claim_wording_class": p["claim_wording_class"],
                    "uses_biometric": str(p["uses_biometric"]).lower(),
                    "kind": p["kind"],
                    "source_file": "B1_interventions.md",
                    "source_type": "intervention_library",
                    "country": "global",
                    "chunk_index": "0",
                    "total_chunks": "1",
                    "ingested_at": now,
                    "document_category": "AI_Use_Cases",
                },
            }
        )
    return out


# ------------------------------------------------------------------------- evidence
def parse_table(md: str, heading_prefix: str) -> list[list[str]]:
    start = md.index(heading_prefix)
    rows = []
    for line in md[start:].splitlines()[1:]:
        if line.startswith("## ") and rows:
            break
        if not line.startswith("|"):
            if rows and line.strip() == "":
                break
            continue
        cells = [clean(c) for c in line.strip().strip("|").split("|")]
        if set("".join(cells)) <= set("-: "):
            continue
        rows.append(cells)
    return rows[1:]  # drop header


def evidence_records(md: str) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    recs = []

    def slug(s: str) -> str:
        return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:48]

    def add(kind, name, fields, text):
        recs.append({
            "id": f"{kind}::{slug(name)}", "text": text,
            "metadata": {"kind": kind, "name": name, "source_file": "B2_signals_parameters.md",
                         "source_type": "evidence_base", "country": "global", "chunk_index": "0",
                         "total_chunks": "1", "ingested_at": now, "document_category": "Evidence", **fields},
        })

    for r in parse_table(md, "## Part 1"):
        sig, a, b, c, d, e, f = r[:7]
        construct = ("arousal" if re.search(r"arousal|autonomic", e, re.I) else
                     "cognitive_control" if re.search(r"cognitive|inhibit", e, re.I) else "physical_or_fatigue")
        add("signal", sig, {"validated_realtime": "false", "construct": construct},
            f"Signal {sig}. ADHD vs neurotypical: {a} Strength/consistency: {b} Ranges: {c} "
            f"Validated for real-time adaptive intervention: {d} Construct interpretation (attention vs emotion): {e} Sources: {f}")
    for r in parse_table(md, "## Part 2"):
        name, val, bypres, cav, cit = r[:5]
        add("parameter", name, {}, f"Simulator parameter {name}: {val} By presentation: {bypres} Caveats: {cav} Source: {cit}")
    for r in parse_table(md, "## Part 5"):
        prod, cat, reg, claim, ev, sens, ver = r[:7]
        add("tool", prod, {"category": cat, "verified": ver},
            f"Existing digital ADHD tool {prod} ({cat}). Regulatory status: {reg} Claim: {claim} Evidence: {ev} "
            f"Physiological sensing: {sens} Verification: {ver}")
    return recs


def gap_records(gaps: list[dict]) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    return [{
        "id": g["gap_id"],
        "text": f"Policy gap {g['title']} (type: {g['type']}). {g['text']} Documents: {' '.join(g['doc_ids'])}.",
        "metadata": {"gap_id": g["gap_id"], "gap_type": g["type"], "doc_ids": ",".join(g["doc_ids"]),
                     "source_file": "A_policy_register.md", "source_type": "gap_analysis", "country": "global",
                     "chunk_index": "0", "total_chunks": "1", "ingested_at": now, "document_category": "Gaps"},
    } for g in gaps]


# ---------------------------------------------------------------------------- main
def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def main() -> dict:
    KB_DIR.mkdir(parents=True, exist_ok=True)
    a = (RESEARCH / "A_policy_register.md").read_text(encoding="utf-8")
    b1 = (RESEARCH / "B1_interventions.md").read_text(encoding="utf-8")
    b2 = (RESEARCH / "B2_signals_parameters.md").read_text(encoding="utf-8")

    register = extract_json_block(a)
    gaps = parse_gaps(a, [d["doc_id"] for d in register])
    plans = [normalise_plan(p) for p in extract_json_block(b1)]

    (KB_DIR / "policy_register.json").write_text(json.dumps(register, indent=2, ensure_ascii=False), encoding="utf-8")
    (KB_DIR / "policy_gaps.json").write_text(json.dumps(gaps, indent=2, ensure_ascii=False), encoding="utf-8")
    (KB_DIR / "interventions.json").write_text(json.dumps(plans, indent=2, ensure_ascii=False), encoding="utf-8")

    ev = evidence_records(b2)
    (KB_DIR / "evidence.json").write_text(json.dumps(ev, indent=2, ensure_ascii=False), encoding="utf-8")

    pol = policy_records(register)
    write_jsonl(INDEX_DIR / "kb_policy.jsonl", pol)
    write_jsonl(INDEX_DIR / "kb_interventions.jsonl", intervention_records(plans))
    write_jsonl(INDEX_DIR / "kb_evidence.jsonl", ev)
    write_jsonl(INDEX_DIR / "kb_gaps.jsonl", gap_records(gaps))
    n_docs = write_itu_input_docs(register)

    stats = {"policy_docs": len(register), "policy_records": len(pol), "gaps": len(gaps),
             "interventions": len(plans), "evidence_records": len(ev), "itu_input_docs": n_docs,
             "unverified_provisions": sum(1 for r in pol if r["metadata"]["verified"] == "false")}
    print(json.dumps(stats, indent=2))
    return stats


if __name__ == "__main__":
    main()
