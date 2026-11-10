# Policy-grounded BDI agent for digital ADHD support (AI for Good Lab Hackathon, ITU x UAE)

A local BDI agent adapts digital support interventions for a **simulated** user from consented behavioural and
physiological signals. Before any intervention fires, a **policy node retrieves provisions from an open knowledge
base** (EU AI Act, GDPR, DSA minors guidelines, Qatar PDPPL, FDA/MDR software rules, …) and allows, modifies or blocks
the plan with citations. Institutional agents (policy adviser, regulator, provider) react to an interactive error
scenario in which information arrives incomplete and unevenly distributed. Every decision lands in a hash-chained
audit log.

> Teammates: see [HANDOVER.md](HANDOVER.md) for what is done and what remains before submission.

> Research simulation only. It does not diagnose ADHD and makes no clinical claim. Presentation profiles are
> simulation parameters. All simulated effect sizes are design assumptions (`src/adhd_agent/simulator.py`).

## Quick start (Python 3.11+, standard library only; `pytest` for tests)

One command reproduces the submitted results (scenario with and without the policy check, baselines, a readable
story of the run, tests): `bash scripts/reproduce.sh` (add `--rebuild` after editing `docs/research/`). Step by step:

```bash
export PYTHONPATH=src
python -m adhd_kb.build                                   # research docs -> KB (data/kb) + ITU-style InputDocs
python -m adhd_agent.scenario scenarios/error_scenario.json --out runs/scenario
python -m adhd_agent.scenario scenarios/error_scenario.json --out runs/ablation_guardrail_False --no-guardrail
python scripts/narrate_run.py runs/scenario/audit.jsonl   # readable story of the run
python -m adhd_agent.compare --seeds 20                   # no-intervention vs fixed-schedule vs BDI+KB
python -m pytest -q
```

## What is in the knowledge base (`data/kb/`)

| Collection | Records | Source |
|---|---|---|
| `kb_policy` | 58 provision records from 37 documents (global + Gulf) | `docs/research/A_policy_register.md` |
| `kb_gaps` | 12 candidate policy / standards gaps (typed) | same |
| `kb_interventions` | 19 evidence-labelled interventions (the plan library) | `docs/research/B1_interventions.md` |
| `kb_evidence` | 8 signals, 7 simulator parameters, 7 existing-tool records | `docs/research/B2_signals_parameters.md` |

Records carry the ITU reference schema keys (`source_file, source_type, country, chunk_index, total_chunks,
ingested_at, document_category`) plus `verified` / `url_primary` / `license_or_reuse_terms`. **26 of 58 policy
provisions are still `UNVERIFIED`** (not confirmed against primary text); the agents surface that flag in every
citation. What was checked, against which source and paragraph, is recorded in
[docs/verification_log.md](docs/verification_log.md). Only paraphrases and links are stored (several sources are copyrighted).

## Architecture (Y.3172 mapping: see `docs/mapping.md`)

```
SimulatedUser (SRC / ML sandbox) -> BDIAgent.perceive (C+PP, consent-filtered) -> deliberate (M: plan library + scoring)
   -> PolicyGuardrail (P: kb_policy retrieval, rules R1-R7) -> execute (D/SINK) -> user outcome -> next tick
Bus (MLFO-style orchestration, FIPA-style performatives) <-> provider | bdi | advisor | regulator
AuditLog: append-only JSONL, sha256 chain, structured reasoning traces with source attribution
```

Key design choices that come from the research evidence:
* attention is inferred from **behaviour** (omissions, RT variability, consented gaze); HRV/EDA stay "arousal
  (construct-ambiguous)" and cannot trigger an intervention without a behavioural corroborator (rule R6);
* motion is never treated as inattention evidence (it can be compensatory);
* variable-ratio rewards and streaks are blocked for minors (R1), push prompts to minors are downgraded to silent
  in-app delivery (R2b), biometric attention inference is blocked in school/workplace contexts (R3). R3 acts at the
  perception step: gaze and HRV/EDA are dropped before they reach the belief base, because the restriction targets
  the inference itself, not only the interventions that would use it;
* unconsented sensor channels never enter the belief base (data minimisation).

## Error scenario (`scenarios/error_scenario.json`)

Consumer app → provider pivots to schools with streaks / variable rewards → complaint about in-app spending
(adviser: high-risk, lists *missing information*) → guardrail digest reaches the adviser (prohibited institutional
attention inference; regulator orders suspension) → provider remediates → monitoring agency finds targeted ads
derived from inferred state (escalation to ethics-oversight referral) → provider invokes an assistive exception
(flagged *contested*, human review, policy gap logged). Ten expected outcomes are checked against the audit log.

## Using the ITU reference code (required by the hackathon)

`knowledge/InputDocs/Policy_Register/` holds one text file per policy document so the ITU pipeline
(`CrashingGuru/ITUAIReadiness`, `simulation/server/knowledge/ingest.py`: Ollama `nomic-embed-text` + ChromaDB) can be
run on it unmodified:

```bash
git clone https://github.com/CrashingGuru/ITUAIReadiness && cd ITUAIReadiness/simulation
pip install -r requirements.txt && ollama pull nomic-embed-text
python -m server.knowledge.ingest --dir /path/to/adhd-productivity/knowledge/InputDocs
```

**Status: run on 10 Nov 2026** with `bash scripts/run_itu_ingest.sh` (ITU code unmodified). All 37 policy documents
are in ITU's `kb_main` collection. Evidence: `runs/itu_ingest/ingest_log.txt` and `runs/itu_ingest/comparison.md`
(ITU dense retrieval vs our BM25 on 8 queries; the expected document ranks first in 3 of 4 labelled queries for
ITU, 4 of 4 for BM25). The ChromaDB store is not committed (39 MB); the script rebuilds it. Two findings:
each document file is shorter than ITU's 256-word chunk, so dense retrieval matches whole documents rather than
provisions; and ITU's file-name-based `infer_country()` tagged 35 of 37 documents as `global` (no Gulf patterns, and
`EU_`/`UK_`/`US_` prefixes are not matched). The agent keeps using the provision-level BM25 retriever
(`src/adhd_kb/store.py`).

## Honest limitations

* Simulator effect sizes and all plan trigger thresholds are assumptions; the baseline comparison is illustrative
  (the hackathon does not score prototype accuracy; the research study evaluates this properly).
* The BDI agent's attention estimate is biased low versus ground truth, which inflates "unneeded prompts"
  (visible in `compare.py`); calibration is future work.
* The BDI loop is plain Python shaped like SPADE behaviours (SPADE needs an XMPP server); the research version uses SPADE.
* No LLM is in the loop yet: retrieval + rules do the reasoning. Adviser findings are rule-driven templates grounded
  in retrieved provisions, not generated text.
* ML Intent (Y.3172) and Arabic / multilingual support are not implemented.
* Rules decide; retrieval supplies the cited provisions and flags a rule whose sources it cannot find
  (`unsupported_by_retrieval`). The policy check is grounded in retrieved, cited provisions; it does not reason from the KB.
* The regulator takes the provider's compliance report at face value; verifying remediation is not modelled.
* The simulated minor consents to sensors without a guardian; guardian consent (GDPR Art. 8, Qatar PDPPL children's
  provisions) is not enforced by R4.
* The scenario timeline is compressed: 200 ticks of 30 simulated seconds stand for roughly six months of events.
