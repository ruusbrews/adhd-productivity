# Hackathon submission milestones

As of 10 Nov 2026. Read with [HANDOVER.md](HANDOVER.md).

## Goal and rules

We submit the report and the knowledge base by **22:00 today**, with every legal claim the scenario relies on either
verified or openly labelled as unverified. Everything is frozen by **20:00**, leaving two hours of buffer.

- **Closed milestones.** Each has one owner, a target time and a done check. It is done only when the check passes.
- **Plan from the actual state.** The code works (10 of 10 scenario checks pass). We fix, verify and package; we do not rebuild.
- **One Ollama job at a time.** The ITU ingest runs on Roaa's laptop only when no other model job is running.
- **Freeze before submitting.** After M5 no code or KB changes, only report wording.
- **Times are targets** (assuming a 10:00 start). If a milestone slips by more than an hour, use the fallbacks below.

## Timeline

| Milestone | Owner | Target | Depends on | Status |
|---|---|---|---|---|
| M0 Agree the split | Roaa | done | – | **done**: Roaa does all core work, Farha writes the report |
| M2 Code fixes | Roaa + Claude | 14:00–15:00 | – | to do |
| M1 Verify legal claims | Roaa + Claude | 15:00–18:00 | – | to do |
| M3 ITU ingest | Roaa | 13:00–16:00 (runs beside M1) | Ollama free | **done 13:50** (send note to Farha) |
| M4 Report | Farha (writing only) | 14:00–20:00, full draft by 18:30 | inputs from Roaa | to do |
| M5 Freeze and publish | Roaa | 20:00–21:00 | M1, M2, M4 | to do |
| M6 Submit report and KB | Roaa | 21:00–21:30 | M5 | to do |
| **Deadline** | | **22:00** | | |

Roaa does all core work (code, verification, packaging, submission); Farha only writes the report from what Roaa
hands over. Code fixes (M2) go first because they are quick and independent; verification (M1) follows and may
re-word R3/A1, then one final re-run.

**Farha receives:** `runs/itu_ingest/REPORT_NOTE.md` + `comparison.md` (now), the verified/unverified provision list
(after M1), the final `runs/scenario/summary.json` (after M2), and notes on the Qatar framing and the wording
"rules grounded in retrieved, cited provisions".

## Milestones in detail

### M0. Agree the split (Roaa)

- [ ] Send Farha the review findings: the Qatar-vs-EU framing, the R3 gaze issue, the wording of "policy-grounded",
      the wrong Art. 5(1)(f) citation in the in-app purchase finding, and the regulator trusting the provider's compliance report
- [ ] Agree who owns verification, the public repo and the KB upload
- [ ] Ask the supervisor whether the plan library can be published

**Done when:** every milestone has a named owner and Farha has confirmed the findings.

### M1. Verify the critical legal claims (Roaa + Claude)

- [ ] EU AI Act Art. 5(1)(f): does inferring *attention* from biometrics in schools fall under it, or only emotions?
- [ ] Commission guidelines C(2025) 884: the example about students' attention, and the biometric-only limitation
- [ ] EU DSA minors guidelines §6.4 (random rewards) and the default-settings text
- [ ] GDPR Arts. 8, 9, 22 and 35, and COPPA §312.5: these carry the judges' targeted-ads twist and are all unverified today
- [ ] Qatar PDPPL Arts. 16–17
- [ ] Whether Qatar has any binding rule on attention or emotion inference in schools
- [ ] Update `docs/research/A_policy_register.md`: set `verified`, fix URLs and paraphrases, never change a `doc_id`

**Done when:** the KB rebuilds, 15 tests pass, the scenario still passes 10 of 10, and a list of verified and
still-unverified provisions goes to Farha.

### M2. Code fixes (Roaa + Claude)

- [ ] `perceive()` in `bdi.py`: drop biometric channels in school and workplace settings (R3 issue)
- [ ] Adviser rule A3 in `agents.py`: query so retrieval cites AI Act Art. 5(1)(a)-(b), not 5(1)(f)
- [ ] `scenario.py` summary: count R2b as "modified", not "blocked"
- [ ] Re-run the scenario with and without the policy check; regenerate `runs/`
- [ ] README: ITU ingest status and results; new limitations (regulator trusts the provider's compliance report,
      minor consents without a guardian, compressed timeline); HANDOVER task 2 done
- Kept as limitations, no code: guardian consent for minors (would break X1), regulator verification of provider reports

**Done when:** 10 of 10 with the policy check on, the ablation still shows a difference, tests pass and `runs/` matches the code.

### M3. ITU reference ingest (Roaa)

- [x] Download `nomic-embed-text`; write `scripts/run_itu_ingest.sh` and `scripts/compare_itu_retrieval.py`
- [x] Run `bash scripts/run_itu_ingest.sh` (10 Nov, 13:46–13:50): 37 documents in `kb_main`, exit 0
- [x] Read `runs/itu_ingest/comparison.md`: 37 chunks (1 per document); ITU top-1 3/4 vs BM25 4/4; 35 of 37 tagged `global`
- [x] Draft the report text: `runs/itu_ingest/REPORT_NOTE.md`
- [ ] Send Farha `REPORT_NOTE.md` and `comparison.md` (Roaa)

**Done when:** `runs/itu_ingest/ingest_log.txt` and `comparison.md` exist and Farha has the summary.

### M4. Report (Farha)

- [ ] Header: team leader, members, contacts, GitHub link
- [ ] Sections 1–6 of the template, max 5 pages, using the M1–M3 results
- [ ] State the limitations: no LLM in the loop, assumed effect sizes, compressed timeline, no ML Intent or Arabic,
      which provisions remain unverified, regulator does not verify provider reports

**Done when:** a full draft by 18:00 and the final version by 20:00, both read by Roaa.

### M5. Freeze and publish (team)

- [ ] Final KB build, tests and scenario run
- [ ] Commit, tag `v1-submission`, push to the public repo
- [ ] Check that the link in the report opens the repo

**Done when:** the public repo at the tag reproduces `runs/scenario/summary.json` with 10 of 10.

### M6. Submit (team)

- [ ] Upload the report
- [ ] Submit the KB: `data/kb/`, `knowledge/InputDocs/` and the ingest evidence from M3
- [ ] Save the confirmation

**Done when:** a confirmation for both is saved, before 22:00.

## Risks and fallbacks

If time runs short, cut from the bottom of this table first. The report and an honest KB matter more than any single fix.

| Risk | What it breaks | Fallback |
|---|---|---|
| AI Act Art. 5(1)(f) does not cover attention inference | R3, checks X3 and X5, the suspension at stage 4 | Re-word R3 and A1 as "emotion or attention inference" with the gap stated, or move it to a policy-gap finding; re-run |
| Verification runs out of time | KB accuracy, the main judging criterion | Verify the six critical claims only; list the rest as unverified in the report |
| A code fix breaks a scenario check | The 10 of 10 result | Revert that fix and describe it as a known limitation |
| The ITU install or ingest fails | M3 evidence | Submit without it and state exactly what blocked it, as the handover allows |
| Supervisor has not approved publishing the plan library | M5 public repo | Publish without `docs/research/B1_interventions.md` and the plan library; say so in the README |
| KB upload route still unknown | M6 | Put `data/kb/` and `knowledge/InputDocs/` in the public repo and point to them from the report |

## Open questions

- [ ] Who owns M1 beyond the six critical claims, the public repo and the KB upload?
- [ ] Does Farha agree to the M2 code fixes on the day of submission?
- [ ] Has the supervisor approved publishing the plan library?
- [ ] Where and how is the KB uploaded? The event page does not say.
- [ ] Who is listed as team leader, and which contact email goes in the report?
- [ ] Is 22:00 Doha time, or the organisers' time zone (CET)?
