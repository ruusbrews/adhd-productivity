# Verification log: policy provisions checked against primary text

Each entry records which provision in `docs/research/A_policy_register.md` was checked, against which official source
and paragraph, and the result. Provisions not listed here keep the `verified` flag they had in the register, and the
agents print that flag in every citation.

Sources opened:

- **[CG]** European Commission, *Guidelines on prohibited artificial intelligence practices established by Regulation
  (EU) 2024/1689*, C(2025) 884 final, English PDF from the AI Act Service Desk
  ([link](https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF)).
  Paragraph numbers below are the guidelines' own. The guidelines quote the AI Act articles verbatim in boxed text
  (Art. 5(1)(f) on p. 77; Art. 3(39) in para. 244). EUR-Lex could not be fetched automatically on 10 Nov 2026, so
  AI Act wording was checked through these official quotations.

## 10 Nov 2026

| doc_id | Provision | Result | Evidence |
|---|---|---|---|
| eu-ai-act-2024-1689 | Art. 5(1)(f) | Confirmed (was already verified) | Article text quoted in [CG] p. 77; four cumulative conditions in para. 242 |
| eu-ai-act-2024-1689 | Art. 3(39); Recital 18 | **Now verified** | Definition quoted in [CG] para. 244; Recital 18 list of emotions para. 247; pain and fatigue excluded para. 249, 261 |
| eu-ai-act-2024-1689 | Art. 5(1)(a)-(b) | **Now verified** | [CG] para. 63 (three types of technique), para. 104-108 (age, children under 18, disability) |
| ec-guidelines-prohibited-ai-practices-2025 | Art. 5(1)(f) examples | Confirmed; paraphrase made more precise | [CG] para. 255 (students' interest and attention: prohibited; gaze points only: not prohibited), para. 256-257 and 263 (medical exception) |
| ec-guidelines-prohibited-ai-practices-2025 | Intentions; biometric limitation | **Now verified**; paraphrase made more precise | [CG] para. 244-245, 250, 251 (keystrokes, eye tracking, heartbeats are behavioural biometrics), 265 (text and physical states out of scope) |

## What this means for the agent and the scenario

- **R3 and adviser rule A1 stand.** Inferring students' attention with an emotion recognition system in an education
  institution is a prohibited example in [CG] para. 255, and para. 240 lists monitoring learners' attention or
  engagement as an emotion recognition use.
- **The assistive-exception case (A5) is rightly "contested".** The exception is narrow: therapeutic use means
  CE-marked medical devices and general wellbeing monitoring is not covered ([CG] para. 256-257), yet assisting
  students with autism is given as a covered medical use (para. 263). A wellness-claim app cannot rely on it without
  device authorisation.
- **R1 has a second legal anchor.** [CG] para. 105 gives unpredictable, addictive reward schedules aimed at children
  as an example of exploitation under Art. 5(1)(b), where they cause significant harm.
- **Targeted ads from inferred emotions (A4, judges' twist).** Emotion recognition for advertising is outside
  Art. 5(1)(f) but can fall under Art. 5(1)(a)-(b) ([CG] para. 266), which is why adviser rule A3 now cites
  Art. 5(1)(a)-(b).

## Gap found during verification

- **Is task-performance telemetry biometric?** [CG] para. 251 counts keystrokes ("way of typing"), eye tracking and
  heartbeats as behavioural biometrics. It does not say whether task-performance measures such as missed items or
  reaction-time variability count. The agent's school-context attention estimate still uses reaction-time
  variability, so the boundary matters for any attention-support tool used in class.
