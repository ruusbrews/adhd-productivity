# Mapping to ITU-T Y.3172 and the AI Readiness Framework (Report 2.0)

Readiness dimension numbers follow the NotebookLM summary of Report 2.0 (13 dimensions); re-check against
`simulation/data/framework/dimensions.json` in the ITU repo before the report is finalised.

## Y.3172 pipeline

| Node | Our component | Status |
|---|---|---|
| SRC | `SimulatedUser.step()` frame: task telemetry, self-report, gaze, HRV/EDA, motion (simulated) | implemented |
| C | `BDIAgent.perceive`: ingests only consented channels | implemented |
| PP | rolling windows, behaviour-based attention estimate, arousal kept separate | implemented |
| M | `deliberate()`: plan library scoring + KB-backed plan metadata | implemented |
| P | `PolicyGuardrail` (R1-R7) retrieving `kb_policy`; adviser/regulator for institutional policy | implemented |
| D / SINK | `execute`: delivery mode (push / silent in-app / ambient), `SimulatedUser.receive` | implemented |
| MLFO | scenario runner + `Bus`: orchestrates agents, standing modes (notification batching), dynamic plan pool | partial |
| ML Intent | declarative user goal ("60-minute focus block") | **not implemented** |
| ML Sandbox | simulated user + scenario runner (REQ-ML-MNG-002/003: test policy changes without live users) | implemented |

## Readiness 2.0 dimensions

| # | Dimension | Where it shows up | Evidence in repo |
|---|---|---|---|
| 1 | Data/model marketplace | KB records carry licence/reuse, verification and source metadata | `data/kb/index/*.jsonl` |
| 4 | Contextualization & regional impact | Qatar PDPPL / NCSA, UAE PDPL, Bahrain AI policy records; adviser rule A6 | `kb_policy`, `A6` |
| 6 | Human interface | multimodal plans (visual/auditory/haptic), silent-delivery downgrade for minors | `interventions.json`, R2b |
| 7 | Strategy alignment | desires hierarchy; inter-agency coordination protocol | `bdi.py`, `agents.py` |
| 8 | Collaboration with AI | acceptance model, prompt budget; **one-tap pause / user override not built yet** | `simulator.receive` |
| 10 | AI & policies | sandbox for simulated policy timelines, explainability, ethics-audit trail | `scenario.py`, `audit.py` |
| 11 | AI for inclusion | local (edge-style) execution, consent-filtered data, neurodivergent focus | `bdi.perceive` |
| 13 | Digital infrastructure | CPU-only, no network, standard library (energy not measured) | `requirements` |

Hackathon perspectives (event page): open data / open-source management (KB published as open records, licence
flags), human interaction and supervision (human-review actions, contested findings), policy implementation
opportunity identification (gap register), social inclusion, digital infrastructure and energy.

## Policy gaps (candidate list, from the research register; the adviser re-derives the ones its retrieval supports)

See `data/kb/policy_gaps.json` (12 typed gaps). Gaps surfaced by the error scenario run: gap-01 (attention vs
emotion boundary), gap-02 (education ban vs assistive use), gap-05 / gap-06 (UAE / Qatar regimes), gap-07 (therapeutic
nudging vs anti-persuasive design), gap-12 (ITU ML standards silent on harms to people).
