# ITU reference ingest: note for the report

Run on 10 Nov 2026 (13:46 to 13:50 Doha time) on Roaa's laptop. Evidence in this folder: `ingest_log.txt` (console
output), `comparison.md` / `comparison.json` (retrieval check). The ChromaDB store itself is not committed (39 MB);
`scripts/run_itu_ingest.sh` rebuilds it.

## Suggested text (report sections on the KB / Y.3172 mapping)

We ingested the knowledge base with ITU's reference pipeline (CrashingGuru/ITUAIReadiness, `simulation/`), run
unmodified: 256-word chunks with 30-word overlap, Ollama `nomic-embed-text` embeddings, ChromaDB with cosine distance.
All 37 policy documents were stored in `kb_main` (37 chunks), alongside ITU's 19 framework definitions and its own
use-case collection. On the four regression queries from our test suite, ITU's dense retrieval returned the expected
document first in 3 of 4 cases; our offline keyword retriever, which the agent uses, did so in 4 of 4.

## Findings worth one line each

- **Granularity.** Each of our document files is shorter than ITU's 256-word chunk, so every document became a single
  chunk. Dense retrieval therefore matches whole documents, while our agent cites individual provisions (58 records).
  This is why it missed Qatar PDPPL for "special nature data children health permit" and GDPR for "explicit consent
  for processing sensitive health or biometric data". Provision-level chunking would fix it.
- **Country metadata (a tooling gap).** ITU's `infer_country()` tagged 35 of 37 documents as `global`. Its file-name
  patterns have no entry for Qatar, UAE or Bahrain, and `\bEU\b`, `\bUS\b`, `\bUK\b` do not match a prefix followed by
  an underscore (`EU_…`). Only Saudi Arabia and one US file were tagged. Country-filtered search
  (`search_by_country`) would miss every Gulf and EU document. This supports the gap finding that ITU ML-pipeline
  tooling is thin on Gulf jurisdictions.
- **Agreement.** Top-1 agreement between the two retrievers was 3 of 8 queries. On the four open scenario queries
  (in-app purchases, targeted ads, consent, human oversight) the two often return different but plausible documents.
  Neither set is ground truth.

## Not done

- The agent still uses the keyword retriever; the ITU store is evidence and a deliverable, not wired into the loop.
- No fine-tuning (sandbox credits only go to selected teams).
