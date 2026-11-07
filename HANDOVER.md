# Handover: AI for Good Lab Hackathon (ITU x UAE) submission

Status as of 7 Nov 2026. **Submission deadline: 10 Nov 2026.** Registration is already done.
Read `README.md` first (what the project is and how to run it), then this file (what is finished, what is not).

Key dates (event page): submission 10 Nov, first-round evaluation 11-18 Nov, shortlist announced 18 Nov,
final evaluation 8 Dec and awards 10 Dec in Dubai. Weekly mentoring: Saturdays 10:00-11:00 CEST (recordings are posted).

## What we are submitting

A local BDI agent adapts digital ADHD-support interventions for a **simulated** user. Before any intervention fires,
a policy node retrieves provisions from an open knowledge base (KB) and allows, modifies or blocks the plan with
citations. A policy adviser, a regulator and a provider agent react to an interactive error scenario in which
information arrives incomplete and unevenly distributed. Every decision is written to a tamper-evident audit log.

Ground rules for everything we write: it is a research simulation, it does not diagnose ADHD, we make no clinical
claims, and simulated effect sizes are design assumptions (not evidence).

## Quick run (from the repo root)

Python 3.11+ (developed on 3.13). Standard library only; `pip install pytest` for the tests.

```bash
export PYTHONPATH=src            # PowerShell:  $env:PYTHONPATH = "src"
python -m adhd_kb.build          # rebuild the KB from docs/research
python -m adhd_agent.scenario scenarios/error_scenario.json --out runs/scenario
python -m pytest -q              # expect: 15 passed
```

## DONE

- [x] **Agent that uses the KB and adheres to policy** (`src/adhd_agent/bdi.py`, `guardrail.py`)
- [x] **Multi-agent roles with a coordination protocol**: provider, BDI agent, policy adviser, regulator (`agents.py`)
- [x] **Interactive error scenario** with staged, incomplete, unevenly distributed information, and 10 expected outcomes
      checked against what really happened (`scenarios/error_scenario.json`, `scenario.py`)
- [x] **Audit logging and reasoning traces** with source attribution and a verifiable hash chain (`audit.py`)
- [x] **KB content**: 37 policy documents / 58 provisions, 12 typed policy gaps, 19 interventions, 22 evidence records (`data/kb/`)
- [x] **Draft Y.3172 and Readiness 2.0 mapping tables** (`docs/mapping.md`)
- [x] **Tests (15) and README**

Results of our own run: all 10 scenario outcomes pass with the guardrail on, 6 of 10 with it off (`--no-guardrail`).
Those 10 outcomes are our own expectations, so they show the pipeline behaves as designed, not that the policy
conclusions are correct. That is why the verification task below matters.

## TO DO (everything is required for submission unless marked otherwise)

### 1. Verify the unverified policy provisions against primary text (highest priority)

**Why:** judges rate "gap relevance and accuracy of global policy examples" as a critical part of the evaluation, and
KB accuracy is criterion 1. 32 of the 58 provisions are flagged `verified: false`. Deep Research produced the
paraphrases and clause numbers but could not open many of the official texts; some entries were written "from memory".
The agents print the verified/unverified flag in every citation, so wrong or unchecked clauses become visible to judges.

**What "verify" means:** open the *official* source, find the clause, and confirm that (a) the clause number is right,
(b) our paraphrase says what the clause says, (c) the reuse terms are noted. Then mark it verified. Only paraphrase;
many sources are copyrighted.

**Do these first** (the guardrail rules and adviser findings rely on them):

| Document (`doc_id`) | Check | Official source |
|---|---|---|
| `eu-ai-act-2024-1689` | Art. 5(1)(a)-(b) (manipulation / exploiting vulnerabilities); Art. 3(39) and Recital 18 (emotion recognition definition, fatigue excluded); Art. 6 and Annex III; Art. 50(3) | EUR-Lex (link in the register) |
| `ec-guidelines-prohibited-ai-practices-2025` | the example that inferring students' attention is prohibited, and the biometric-only limitation | Commission guidelines C(2025) 884 PDF |
| `eu-gdpr-2016-679` | Art. 8 (child consent age), Art. 9(1)-(2)(a), Arts. 22 and 35 | EUR-Lex |
| `eu-dsa-art28-minors-guidelines-2025` | section 6.4 (random rewards) and default-settings text (already marked verified; re-confirm clause numbers) | EUR-Lex OJ C/2025/5519 |
| `uk-ico-age-appropriate-design-code` | Standard 13 (nudge techniques) and the others cited; the register used third-party mirrors | ico.org.uk |
| `us-coppa-rule-2025-amendments` | biometric identifiers in the definition; separate consent for disclosure; compliance date 22 Apr 2026; the Federal Register page cite is reported two ways | Federal Register / eCFR |
| `mdcg-2019-11-rev1`, `fda-general-wellness-2026` | intended-purpose test; wellness policy date and what it excludes | EC MDCG page, FDA guidance page |
| `eu-ucpd-2005-29`, `ftc-dark-patterns-2022` | Art. 5(3), Arts. 8-9; the report's tactic categories | EUR-Lex, ftc.gov |
| `qatar-pdppl-13-2016`, `uae-pdpl-fdl-45-2021` | already largely verified from translations; confirm Arts. 16-17 (Qatar) and the Executive Regulations status (UAE) from an official or high-quality source | NCSA / UAE legislation portal |

**Replace these weak sources** (secondary mirrors or no URL): `eu-digital-omnibus-ai-2026-1744` (cited only through a
Cloud Security Alliance note: open the EUR-Lex text of Regulation (EU) 2026/1744 and confirm the Art. 113 dates, or
remove the entry if it cannot be confirmed), `bahrain-pdpl-30-2018`, `un-crpd-2006`, `w3c-coga-usable-2021`,
`unesco-rec-ethics-ai-2021`, `oecd-ai-principles` (page needs JavaScript), `imdrf-samd-n12-2014` (full-text link
missing), `itu-t-y3173-y3174` (cited through a standards-shop page).

**Other numbers flagged by the research, check before quoting in the report:** Saudi PDPL effective date (14 Sep vs
17 Oct 2023), EndeavorOTC sample size and clearance date, QbCheck clearance number, Monarch CE mark, the "30 vs 23
blinks per minute" figure.

**How to record the result:** the KB is generated from `docs/research/A_policy_register.md` (the JSON block). In that
JSON, change `"verified": false` to `true` for each confirmed provision, fix `url_primary` / `url_pdf_or_fulltext`, and
correct any paraphrase that was wrong. **Do not change any `doc_id`** (the guardrail and adviser rules refer to them by
name). Keep the JSON valid. Then run `python -m adhd_kb.build` and `python -m pytest -q`. If a test or scenario
outcome now fails, a rule's cited document changed meaning; fix the rule or the record, do not delete the assertion.
If a provision turns out to be wrong, correct it and note it in the report as a finding.

Also write down which provisions you verified and which remain unverified; the report should state that honestly.

### 2. Run the ITU reference ingest

**What it is:** ITU's reference code for turning policy documents into a searchable, vectorised knowledge base:
**https://github.com/CrashingGuru/ITUAIReadiness** (the code is in its `simulation/` folder). The hackathon requires
using it ("use ITU reference code to extract, structure and ingest data into a vectorized knowledge base"). From a
read of the repo: it parses PDF / txt / md files, splits them into 256-word chunks with 30 words of overlap, embeds the
chunks with Ollama `nomic-embed-text`, and stores them in a ChromaDB database with metadata (`source_file`,
`source_type`, `country`, `chunk_index`, `total_chunks`, `ingested_at`, `document_category`). Our KB records use the same
metadata keys on purpose.

**What we prepared:** `knowledge/InputDocs/Policy_Register/` contains one text file per policy document (paraphrases
and links only, no copyrighted full text). Regenerate it with `python -m adhd_kb.build` after the verification edits.

**Status: never run.** The development machine has no Ollama or ChromaDB, so our own demo uses an offline keyword
retriever (`src/adhd_kb/store.py`). Steps (needs a machine with roughly 16 GB RAM; Docker is optional):

```bash
git clone https://github.com/CrashingGuru/ITUAIReadiness
cd ITUAIReadiness/simulation
pip install -r requirements.txt
ollama pull nomic-embed-text
python -m server.knowledge.ingest --dir <path-to-this-repo>/knowledge/InputDocs
```

Then: save the console output (it prints KB statistics), run a few test queries against the resulting collection (for
example the queries in `tests/test_core.py`) and note whether the same documents come back as with our retriever.
Things to watch: the ITU script infers the *country* from the file name (ours may fall back to `global`), the category
comes from the folder name (`Policy_Register`), and the repo has a few inconsistencies (its `search_by_factor` filter
key is never written by ingest). If it fails or cannot be installed in time, document exactly why in the report; the
submission still includes the KB files in `data/kb/` and `knowledge/InputDocs/`.

The organisers' "AI for Good Lab" hosting is for selected teams only, so do not plan on hosting the KB there.

### 3. Technical report (max 5 pages, official `.docx` template)

Template: `AI-for-Good-Sandbox-Hackathon-submission-template.docx` (the page links it). It currently contains a
**smart-pen example** that must be replaced. Needed: team leader, members, contact details, GitHub link, then
sections a to h:

| Section | Content | Material in the repo |
|---|---|---|
| a. Introduction | short overview of the agentic solution | `README.md` |
| b. Use case | problem, gaps in existing solutions, how ours addresses them | `docs/research/B2_signals_parameters.md` (existing tools, harms) |
| c. Requirements | per pipeline node: data, privacy, consent, edge execution, human oversight | guardrail rules R1-R7 in `guardrail.py` |
| d. Y.3172 mapping | table: node, use-case component, Readiness dimension, policy documents | `docs/mapping.md` (draft) |
| e. Readiness 2.0 mapping | not only data/model: strategy alignment, interface, collaboration, inclusion | `docs/mapping.md` (draft) |
| f. Requirements to policies | for each requirement, the policy documents that support it | rule-to-document table below |
| g. Evaluation scenario | staged scenario, **including a controversial case** and the judges' ads escalation | `scenarios/error_scenario.json`, `runs/scenario/summary.json` |
| h. Gaps | policy / standards gaps, with global policy examples | `data/kb/policy_gaps.json` (only verified ones should be stated firmly) |

The scenario already mirrors the template's own sample (in-app purchases, then targeted ads from inferred disability
signals, then stronger guardrails and referral to national AI ethics oversight) and includes a contested case
(provider invokes an assistive exception), which the template asks for.

Rule-to-document table for section f:

| Rule | Requirement | Main documents |
|---|---|---|
| R1 | no random rewards or streaks for minors | EU DSA Art. 28 guidelines, UK Children's Code, AI Act Art. 5 |
| R2b | push prompts to minors off by default | EU DSA Art. 28 guidelines, UK Children's Code |
| R3 | no biometric attention inference in schools or workplaces | AI Act Art. 5(1)(f), Commission guidelines |
| R4 | explicit per-sensor consent | GDPR Art. 9, Qatar PDPPL Art. 16, UAE PDPL |
| R5 | wellness claims only, no therapeutic claims | MDCG 2019-11, FDA General Wellness |
| R6 | physiological-only triggers not allowed (arousal is not attention) | AI Act Art. 3(39), IEEE 7014, evidence record for HRV/EDA |
| R7 | speculative plans need opt-in | WHO ethics guidance (design rule) |

State honestly in the report: no fine-tuning was done (sandbox credits only go to selected teams), Y.3172 ML Intent
and Arabic support are not implemented, effect sizes are assumptions, the BDI loop is plain Python shaped like SPADE,
no LLM is in the loop (retrieval and rules do the reasoning), and which provisions remain unverified.

### 4. Public GitHub repository

Nothing is committed yet. Before pushing: decide what to publish (the FAQ allows publishing only the essential parts;
the plan library is also part of the lead researcher's study, so confirm with the supervisor first), commit, push, and
put the link in the report. `runs/` is **tracked** (not git-ignored) so judges can see a real audit trail, summary and
trace without running anything. Re-run the scenario commands (see Quick run and README) after any KB or rule change so
the committed `runs/scenario/` matches the final code, and re-check that its `summary.json` still shows 10/10 outcomes.

### 5. Submit the KB

The event page does not say where or how to upload the KB and the other materials. Ask at the mentoring session or
through the ITU AI for Good contact. The KB deliverable is `data/kb/` (JSON/JSONL) plus `knowledge/InputDocs/`, and the
ingest evidence from task 2.

### 6. Demo video (optional now, required if shortlisted on 18 Nov; max 7 minutes)

The FAQ asks for: (a) hardware and software setup, (b) main functions, (c) expected outcome of each scenario,
(d) real outcome. The ten checks in `scenarios/error_scenario.json` (expected) against `runs/scenario/summary.json`
(actual) map directly onto (c) and (d). Run the scenario with and without `--no-guardrail` to show the difference.

## Known limitations (also listed in README.md)

- Simulated effect sizes and plan trigger thresholds are assumptions; the baseline comparison (`python -m
  adhd_agent.compare`) is illustrative only. The hackathon says prototype accuracy is not evaluated.
- The agent's attention estimate runs low against ground truth, which inflates "unneeded prompts".
- Gulf coverage is thin: UAE and Qatar national AI strategies and the GCC AI ethics guideline are not in the KB. The
  event page says to focus on global, domain-level gaps rather than country-specific analysis.

## File map (short)

`README.md` overview | `HANDOVER.md` this file | `docs/research/` raw Deep Research outputs (KB source) | `docs/mapping.md`
Y.3172 and Readiness mapping draft | `data/kb/` the KB | `knowledge/InputDocs/` input for the ITU ingest | `src/adhd_kb/`
KB builder and retrieval | `src/adhd_agent/` simulator, BDI agent, guardrail, institutional agents, audit, scenario runner |
`scenarios/` error scenario | `tests/` 15 tests | `runs/` sample run output (audit logs, summaries; regenerate after changes).
