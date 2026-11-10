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

### First batch: AI Act

| doc_id | Provision | Result | Evidence |
|---|---|---|---|
| eu-ai-act-2024-1689 | Art. 5(1)(f) | Confirmed (was already verified) | Article text quoted in [CG] p. 77; four cumulative conditions in para. 242 |
| eu-ai-act-2024-1689 | Art. 3(39); Recital 18 | **Now verified** | Definition quoted in [CG] para. 244; Recital 18 list of emotions para. 247; pain and fatigue excluded para. 249, 261 |
| eu-ai-act-2024-1689 | Art. 5(1)(a)-(b) | **Now verified** | [CG] para. 63 (three types of technique), para. 104-108 (age, children under 18, disability) |
| ec-guidelines-prohibited-ai-practices-2025 | Art. 5(1)(f) examples | Confirmed; paraphrase made more precise | [CG] para. 255 (students' interest and attention: prohibited; gaze points only: not prohibited), para. 256-257 and 263 (medical exception) |
| ec-guidelines-prohibited-ai-practices-2025 | Intentions; biometric limitation | **Now verified**; paraphrase made more precise | [CG] para. 244-245, 250, 251 (keystrokes, eye tracking, heartbeats are behavioural biometrics), 265 (text and physical states out of scope) |

### Second batch (10 Nov 2026)

Sources opened:

- **[GDPR]** Regulation (EU) 2016/679, text *as adopted* (identical to OJ L 119, 4.5.2016), on legislation.gov.uk:
  [Art. 8](https://www.legislation.gov.uk/eur/2016/679/article/8/adopted),
  [Art. 9](https://www.legislation.gov.uk/eur/2016/679/article/9/adopted),
  [Art. 22](https://www.legislation.gov.uk/eur/2016/679/article/22/adopted),
  [Art. 35](https://www.legislation.gov.uk/eur/2016/679/article/35/adopted).
- **[DSA-G]** Commission, *Guidelines on measures to ensure a high level of privacy, safety and security for minors
  online, pursuant to Article 28(4) of Regulation (EU) 2022/2065*, C(2025) 6826 final, 7 Oct 2025
  ([Commission page](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors),
  which links the Official Journal version OJ C/2025/5519 cited in the register).

| doc_id | Provision | Result | Evidence |
|---|---|---|---|
| eu-gdpr-2016-679 | Art. 8 | **Now verified** | [GDPR] Art. 8(1): 16, Member States may lower to not below 13; below that, consent given or authorised by the holder of parental responsibility |
| eu-gdpr-2016-679 | Art. 9(1)-(2)(a) | **Now verified**; note added | [GDPR] Art. 9(1)-(2)(a). Biometric data is special-category only when processed to uniquely identify a person; health data always |
| eu-gdpr-2016-679 | Arts. 22, 35 | **Now verified** | [GDPR] Art. 22(1); Art. 35(1), 35(3)(a)-(b) |
| eu-dsa-art28-minors-guidelines-2025 | Default settings | Confirmed; reference made exact | [DSA-G] Section 6.3.1, para. 57(b)(vi)-(viii) (push notifications off by default and in core sleep hours; streaks and autoplay off) |
| eu-dsa-art28-minors-guidelines-2025 | "Section 6.4 interface design" | **Corrected** | The register merged two sections. Engagement-driven persuasive design is Section 6.4(b); scarcity, intermittent or random rewards and random-outcome loot boxes are Section 6.6 Commercial practices, para. 69(k)-(l). Reference and paraphrase fixed |
| us-coppa-rule-2025-amendments | §312.2 'personal information' (10) | **Now verified** (checked by hand) | [eCFR] item (10): fingerprints, handprints, retina and iris patterns, genetic data, voiceprints, gait patterns, facial templates, faceprints; no physiological signals named |
| us-coppa-rule-2025-amendments | §312.5(a)(2); retention | **Now verified**; reference widened | [eCFR] §312.5(a)(2) separate consent to third-party disclosure unless integral to the service; §312.10 written retention policy; §312.2 'support for the internal operations' (2) bars behavioral advertising and profiling. Compliance date 22 Apr 2026 not shown in eCFR |
| us-coppa-rule-2025-amendments | Document citation | **Corrected** | Register reported "90 FR 16918 or 16970"; the eCFR source note gives 90 FR 16977, Apr. 22, 2025. Primary URL changed from a law-firm page to eCFR |

**[eCFR]** 16 CFR Part 312, eCFR text up to date as of 6 Nov 2026, downloaded by hand from
[ecfr.gov](https://www.ecfr.gov/current/title-16/chapter-I/subchapter-C/part-312) (eCFR blocks automated access).
COPPA defines a child as under 13 (§312.2), so for the scenario's teenage user GDPR Art. 8 (under 16) is the relevant
consent rule, not COPPA.

**Qatar.** One search found no binding Qatari rule on emotion or attention inference in schools; Qatar's AI material
is strategic and ethical guidance (MCIT National AI Strategy 2019, AI ethics principles). This supports a policy-gap
finding, worded as "no binding Qatari equivalent of AI Act Art. 5(1)(f) was found", not as a proven absence. Qatar
PDPPL Arts. 16-17 were already marked verified from translations and were not re-checked against an official
Arabic text.

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
