# Global Policy, Law and Standards Register for an AI-Driven ADHD-Support App (status as of 6 November 2026)

The key finding is that an ADHD-support app inferring attention from HRV, EDA, gaze, motion and keystrokes falls under three regimes at once. First, the EU AI Act bans emotion inference in schools and workplaces. Second, health and biometric data rules apply worldwide, including Qatar's permit regime and the UAE PDPL, whose implementing regulations are still missing. Third, the medical-device boundary turns almost entirely on your claims. The safest design is therefore an app that users get directly, makes only wellness claims, and asks for consent first. It should never be sold to schools or employers as an attention monitor, and it should never claim to diagnose or treat ADHD.

## TL;DR
- **The biggest legal risk comes from where the app is used, not the technology.** The EU AI Act Art. 5(1)(f) ban has applied since 2 February 2025.\[1\] It covers AI that infers emotions or intentions from biometric data in workplaces and education.\[2\] A WSGR summary of the Commission's guidelines (C(2025) 884) says they list "an education institution using an emotion recognition AI system to infer the interest and attention of students" as prohibited, while "detecting fatigue in pilots or drivers" is exempt. The Digital Omnibus (Regulation (EU) 2026/1744, in force 27 July 2026) delayed Annex III high-risk duties to 2 December 2027 but left the prohibitions untouched.\[3\]
- **Physiological and inferred data counts as sensitive almost everywhere, and Gulf rules are uneven.** GDPR Art. 9 applies. So does Qatar PDPPL Art. 16, which treats health, psychological condition and children's data as "special nature" data needing a permit.\[4\] The amended US COPPA Rule now covers biometric identifiers. Its Federal Register notice says regulated entities "have until April 22, 2026 to comply". The UAE PDPL has been in force since January 2022. Chambers and Partners' Data Protection and Privacy 2026 guide says its Implementing Regulations "have yet to be issued". Business-CISO also reports that on 14 June 2026 the UAE Cabinet created the Federal Authority for Artificial Intelligence and Data, which absorbs the UAE Data Office.
- **Whether the app is a medical device depends on its claims.** FDA's revised General Wellness guidance (6 January 2026) and MDCG 2019-11 rev.1 (June 2025) both turn on intended purpose.\[5\]\[6\]\[7\] Claiming to manage, treat or diagnose ADHD likely makes the software a regulated device. "Focus/wellbeing" claims with non-invasive sensors can stay outside.\[8\] The Congressional Research Service (IN12657) quotes the FDA guidance as covering products that "use non-invasive sensing (e.g., optical sensing) to estimate, infer, or output physiologic parameters", explicitly including heart rate variability.

## Key Findings
1. **EU AI Act status.** I confirmed on EUR-Lex that a consolidated AI Act dated 27 July 2026 exists. The enrichment check of the EUR-Lex text of Regulation (EU) 2026/1744 of 8 July 2026 (in force 27 July 2026) found that amended Art. 113 sets these dates. They match analyses by Cloud Security Alliance, DLA Piper and Gibson Dunn:
   - Annex III high-risk duties: 2 December 2027.\[3\]
   - AI embedded in Annex I products: 2 August 2028.\[3\]
   - Art. 50(2) watermarking for systems already on the market: 2 December 2026.\[9\]
   
   I did not open the Omnibus text myself; the Art. 113 dates come from the enrichment check.
2. **The line between emotion and attention decides the case.** The Commission's guidelines treat fatigue as a physical state, so pilot-fatigue alerts are not banned.\[1\] Yet they list inferring students' attention as prohibited.\[10\] Germany's Bundesnetzagentur list likewise names "An AI system that monitors the attention of students and/or teachers" as prohibited. An ADHD app's "attention state" sits right on that line.
3. **Rules on persuasive design target the app's own intervention tools.** The DSA Art. 28 minors guidelines (C/2025/5519, 14 July 2025) say "push notifications are turned off by default and are always off during core sleep hours". The Commission's press page lists streaks among features to disable by default for minors. The guidelines also warn against intermittent or random rewards. The ICO Children's Code bans nudges that weaken privacy.\[11\] Rewards and notifications for a neurodivergent minor therefore need to be user-controlled and justified as therapeutic.
4. **Gulf position:**
   - Qatar needs NCSA permission before processing special-nature data, plus guardian consent for children.\[4\]\[12\]
   - Bahrain's 2025 AI Policy binds only government entities.\[13\]\[14\]
   - For the UAE, Chambers and Partners (Data Protection and Privacy 2026) says the PDPL Implementing Regulations "have yet to be issued".
5. **ITU-T Y.317x are network-ML architecture standards, not ethics or health standards.** They are useful as a pattern for the agent's design (ML pipeline, orchestrator, sandbox) but say nothing about user rights.\[15\]

## Document register (JSON)

```json
[
{"doc_id":"eu-ai-act-2024-1689","title":"Regulation (EU) 2024/1689 (Artificial Intelligence Act), incl. consolidated version 02024R1689-20260727","issuer":"European Parliament and Council of the EU","jurisdiction":"EU","doc_type":"regulation","year":2024,"status":"in force","url_primary":"https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng","url_pdf_or_fulltext":"https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng","language":"24 EU languages","license_or_reuse_terms":"EUR-Lex reuse with attribution (Commission Decision 2011/833/EU); only OJ text authentic. Not re-checked.",
"relevant_provisions":[
{"ref":"Art. 5(1)(f)","paraphrase":"Bans placing on the market, putting into service or using AI to infer emotions of people in workplace and education institutions, except for medical or safety reasons.","relevance_to_adhd_app":"School/employer deployment inferring attention or frustration from biometrics is likely prohibited unless medical; consumer self-use is outside.","verified":true},
{"ref":"Art. 5(1)(a)-(b)","paraphrase":"Bans manipulative/deceptive techniques and exploitation of vulnerabilities due to age, disability or socio-economic situation that materially distort behaviour and cause significant harm.","relevance_to_adhd_app":"Reward loops or nudges exploiting impulsivity (e.g., to drive purchases) risk this ban. Commission guidelines C(2025) 884 para. 105 give as a prohibited example a game that gives children personalised, unpredictable rewards through addictive reinforcement schedules, where it causes significant harm.","verified":true},
{"ref":"Art. 3(39); Recital 18","paraphrase":"Emotion recognition means inferring emotions or intentions from biometric data; physical states such as pain or fatigue are excluded.","relevance_to_adhd_app":"Whether 'attention' is an emotion or a cognitive/physical state decides applicability. Commission guidelines para. 240 and 255 treat inferring learners' attention or interest as emotion recognition; fatigue stays excluded (para. 249, 261).","verified":true},
{"ref":"Art. 6, Annex III (1(c), 3); Arts. 13-14","paraphrase":"Certain emotion recognition and education AI is high-risk, requiring transparency and effective human oversight including override.","relevance_to_adhd_app":"Education or emotion-recognition variants become high-risk from 2 Dec 2027 (post-Omnibus).","verified":false},
{"ref":"Art. 50(3)","paraphrase":"Deployers of emotion recognition systems must inform exposed persons.","relevance_to_adhd_app":"Tell users when physiological signals are used to infer affective states.","verified":false}],
"tags":["emotion_inference","biometric","human_oversight","audit_transparency","dark_patterns","children_data"]},

{"doc_id":"eu-digital-omnibus-ai-2026-1744","title":"Digital Omnibus on AI — Regulation (EU) 2026/1744 amending the AI Act","issuer":"European Parliament and Council of the EU","jurisdiction":"EU","doc_type":"regulation","year":2026,"status":"in force","url_primary":"https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/","url_pdf_or_fulltext":"https://eur-lex.europa.eu/eli/reg/2024/1689/2026-07-27/eng","language":"English (secondary analysis)","license_or_reuse_terms":"Official text not opened; CSA note is third-party — cite, do not copy.",
"relevant_provisions":[
{"ref":"Amended application dates (as reported)","paraphrase":"Published in OJ 24 July 2026, in force 27 July 2026; Annex III high-risk deferred to 2 Dec 2027, Annex I to 2 Aug 2028, Art. 50(2) watermarking for existing systems to 2 Dec 2026.","relevance_to_adhd_app":"Extra runway for any high-risk variant; prohibitions and Art. 50 disclosure still apply now.","verified":false}],
"tags":["audit_transparency","human_oversight"]},

{"doc_id":"ec-guidelines-prohibited-ai-practices-2025","title":"Commission Guidelines on prohibited AI practices under Regulation (EU) 2024/1689 (C(2025) 884 final)","issuer":"European Commission","jurisdiction":"EU","doc_type":"guidance","year":2025,"status":"non-binding","url_primary":"https://ai-act-service-desk.ec.europa.eu/en/faq?page=2","url_pdf_or_fulltext":"https://ai-act-service-desk.ec.europa.eu/sites/default/files/2025-08/guidelines_on_prohibited_artificial_intelligence_practices_established_by_regulation_eu_20241689_ai_act_english_ied3r5nwo50xggpcfmwckm3nuc_112367-1.PDF","language":"English","license_or_reuse_terms":"Commission reuse policy (attribution); not re-checked.",
"relevant_provisions":[
{"ref":"Art. 5(1)(f) examples","paraphrase":"An education institution using emotion recognition to infer students' interest and attention is a prohibited example (para. 255); gaze tracking that only records fixation points without inferring emotions is not prohibited (para. 255); fatigue detection for pilots/drivers is not emotion recognition (para. 249, 261). The medical exception is narrow: therapeutic use means CE-marked medical devices, general wellbeing monitoring is not covered (para. 256-257), while assisting students with autism can qualify (para. 263).","relevance_to_adhd_app":"Directly maps onto attention-state monitoring; avoid institutional deployment. A wellness-claim app cannot rely on the medical exception.","verified":true},
{"ref":"Intentions; biometric limitation","paraphrase":"Covers inference of emotions and intentions, but only on the basis of biometric data (para. 244-245, 250). Biometric data includes behavioural biometrics such as keystrokes (way of typing), eye tracking and heartbeats (para. 251); inferring emotions from written text is outside (para. 251, 265).","relevance_to_adhd_app":"Gaze, HRV/EDA and keystroke dynamics are biometric; typed content sentiment is not. The guidelines do not say whether task-performance data (missed items, reaction-time variability) counts as behavioural biometrics.","verified":true}],
"tags":["emotion_inference","biometric","children_data"]},

{"doc_id":"eu-gdpr-2016-679","title":"Regulation (EU) 2016/679 — General Data Protection Regulation","issuer":"European Parliament and Council of the EU","jurisdiction":"EU","doc_type":"regulation","year":2016,"status":"in force","url_primary":"https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng","url_pdf_or_fulltext":"https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng","language":"24 EU languages","license_or_reuse_terms":"EUR-Lex reuse (attribution). Page opened; article text not rendered in fetch.",
"relevant_provisions":[
{"ref":"Art. 9(1)-(2)(a)","paraphrase":"Prohibits processing health data and identifying biometric data unless an exception such as explicit consent applies.","relevance_to_adhd_app":"HRV/EDA-derived attention or stress states in an ADHD context are very likely health data; explicit granular consent needed. Note Art. 9(1) covers biometric data only when processed for uniquely identifying a person.","verified":true},
{"ref":"Art. 8","paraphrase":"Child consent for online services valid from 16 (Member States may lower to 13); below that parental authorisation is required.","relevance_to_adhd_app":"Younger students need verifiable parental consent.","verified":true},
{"ref":"Arts. 22, 35","paraphrase":"Limits solely automated decisions with significant effects; DPIA required for high-risk processing such as large-scale special-category data.","relevance_to_adhd_app":"DPIA effectively mandatory.","verified":true}],
"tags":["sensitive_health","biometric","children_data","consent"]},

{"doc_id":"uk-ico-age-appropriate-design-code","title":"Age appropriate design: a code of practice for online services (Children's Code)","issuer":"Information Commissioner's Office (UK)","jurisdiction":"UK","doc_type":"guidance","year":2020,"status":"in force","url_primary":"https://gdprlocal.com/age-appropriate-design/","url_pdf_or_fulltext":"https://cdn.comparitech.com/wp-content/uploads/2025/06/age-appropriate-design-a-code-of-practice-for-online-services.pdf","language":"English","license_or_reuse_terms":"ICO usually Open Government Licence v3.0 (unverified); PDF is a third-party mirror — ico.org.uk original NOT opened.",
"relevant_provisions":[
{"ref":"Standard 13 (Nudge techniques)","paraphrase":"No nudges leading children to give unnecessary data or weaken privacy protections.","relevance_to_adhd_app":"Rewards must never unlock extra sensor permissions or sharing.","verified":true},
{"ref":"Standards 1, 2, 5, 7, 12","paraphrase":"Best interests of the child, DPIA, no detrimental data use, high-privacy defaults, profiling off by default.","relevance_to_adhd_app":"Attention profiling of under-18s off by default.","verified":true},
{"ref":"Data (Use and Access) Act 2025 (reported)","paraphrase":"A secondary source says children's protection was embedded in UK GDPR Art. 25(1) from 19 June 2025.","relevance_to_adhd_app":"Would make child-centred design statutory; NOT verified on legislation.gov.uk.","verified":false}],
"tags":["children_data","dark_patterns","consent"]},

{"doc_id":"us-coppa-rule-2025-amendments","title":"Children's Online Privacy Protection Rule, 16 CFR Part 312 — 2025 amendments (Federal Register, 22 April 2025; page cite reported as both 90 FR 16918 and 90 FR 16970 — unverified)","issuer":"US Federal Trade Commission","jurisdiction":"US","doc_type":"regulation","year":2025,"status":"in force","url_primary":"https://www.privacylawnetwork.com/news/coppa-rule-2025-amendments.html","url_pdf_or_fulltext":"https://www.finnegan.com/en/insights/articles/coppas-amended-rule-is-now-in-full-effect-what-operators-need-to-know.html","language":"English","license_or_reuse_terms":"US federal text public domain; Federal Register original NOT opened (secondary sources).",
"relevant_provisions":[
{"ref":"§312.2 'personal information' (10)","paraphrase":"Adds biometric identifiers usable for automated recognition, e.g. fingerprints, iris/retina, voiceprints, gait patterns, facial templates, genetic data.","relevance_to_adhd_app":"Gait/motion and face templates from under-13s covered; HRV/EDA not named.","verified":false},
{"ref":"§312.5(a)(2); retention policy","paraphrase":"Separate parental consent before disclosing children's data to third parties; written retention policy; compliance due 22 April 2026.","relevance_to_adhd_app":"No ad/analytics SDK sharing without separate consent; define deletion schedules.","verified":false}],
"tags":["children_data","biometric","advertising","consent"]},

{"doc_id":"uae-pdpl-fdl-45-2021","title":"Federal Decree-Law No. (45) of 2021 Concerning the Protection of Personal Data","issuer":"United Arab Emirates (UAE Data Office as regulator)","jurisdiction":"UAE","doc_type":"law","year":2021,"status":"in force","url_primary":"https://u.ae/en/about-the-uae/digital-uae/data/data-protection-laws","url_pdf_or_fulltext":"https://uaelegislation.gov.ae/en/legislations/1972/download","language":"Arabic (official); English translation","license_or_reuse_terms":"No open licence found — link rather than copy.",
"relevant_provisions":[
{"ref":"Art. 2 (exclusions)","paraphrase":"Excludes health personal data governed by its own legislation and free zones with their own data laws.","relevance_to_adhd_app":"If treated as health data, UAE health-data law may apply instead; DIFC/ADGM hosting changes regime.","verified":true},
{"ref":"Art. 28","paraphrase":"Cabinet to issue Executive Regulations within six months.","relevance_to_adhd_app":"2026 secondary sources (Chambers 2026, uaeexperthub) say still unissued, so breach timelines, DPO thresholds and fines remain unclear.","verified":true},
{"ref":"Sensitive data and consent provisions","paraphrase":"Sensitive data includes health, biometric and genetic data; processing generally needs consent subject to exceptions.","relevance_to_adhd_app":"Treat physiological/attention data as sensitive.","verified":false}],
"tags":["sensitive_health","biometric","consent"]},

{"doc_id":"qatar-pdppl-13-2016","title":"Law No. (13) of 2016 on Protecting Personal Data Privacy (PDPPL)","issuer":"State of Qatar (NCSA / National Cyber Governance and Assurance Affairs)","jurisdiction":"Qatar","doc_type":"law","year":2016,"status":"in force","url_primary":"https://www.dataguidance.com/sites/default/files/law_no._13_of_2016_on_protecting_personal_data_privacy_-_english.pdf","url_pdf_or_fulltext":"https://www.worldlii.org/int/other/NDPrivLegis/2016/8.pdf","language":"Arabic (official); English translation","license_or_reuse_terms":"Official Arabic on Al Meezan not opened; translations hosted by third parties — cite only.",
"relevant_provisions":[
{"ref":"Art. 16","paraphrase":"Data on ethnic origin, children, health, physical or psychological condition, religion, marital relations and criminal offences is 'special nature' data, processable only with permission from the competent department.","relevance_to_adhd_app":"Attention/stress/ADHD data and any child data need an NCSA permit in addition to consent.","verified":true},
{"ref":"Art. 17","paraphrase":"Child-directed website operators must give notice, obtain explicit guardian consent and not condition participation on unnecessary data.","relevance_to_adhd_app":"Student versions need guardian consent and minimisation.","verified":true}],
"tags":["children_data","sensitive_health","consent"]},

{"doc_id":"qatar-ncsa-privacy-notice-guideline","title":"Privacy Notice — Guidelines for Regulated Entities (PDPPL-02050213E v2.0)","issuer":"National Cyber Security Agency, Qatar","jurisdiction":"Qatar","doc_type":"guidance","year":2022,"status":"non-binding","url_primary":"https://assurance.ncsa.gov.qa/sites/default/files/library/2022-12/Privacy%20Notice%20-%20Guideline%20for%20Regulated%20Entities.pdf","url_pdf_or_fulltext":"https://assurance.ncsa.gov.qa/sites/default/files/library/2022-12/Privacy%20Notice%20-%20Guideline%20for%20Regulated%20Entities.pdf","language":"English","license_or_reuse_terms":"No licence stated — link only.",
"relevant_provisions":[
{"ref":"Children section","paraphrase":"Confirms children's data is special-nature and expects child-directed notices that highlight special-nature processing.","relevance_to_adhd_app":"Notices must flag physiological data in child-readable form.","verified":true}],
"tags":["children_data","audit_transparency"]},

{"doc_id":"saudi-pdpl-2021","title":"Personal Data Protection Law (Royal Decree M/19, as amended) and Implementing Regulation","issuer":"Saudi Data and AI Authority (SDAIA)","jurisdiction":"Saudi Arabia","doc_type":"law","year":2021,"status":"in force","url_primary":"https://dgp.sdaia.gov.sa/","url_pdf_or_fulltext":"https://dgp.sdaia.gov.sa/wps/wcm/connect/85a664fd-6e4e-4edb-bab4-1cbdb02ba6d5/Guide+to+the+saudi+PDP+law+HANDBOOK__%D9%90EN.pdf?MOD=AJPERES","language":"Arabic (official); English guide","license_or_reuse_terms":"Not stated; seen by research subagent only.",
"relevant_provisions":[
{"ref":"Sensitive data; Impl. Reg. Arts. 24, 32","paraphrase":"Health and biometric data are sensitive; 72-hour breach notification to SDAIA; DPO where core activities involve sensitive data.","relevance_to_adhd_app":"GCC rollout needs DPO and 72-hour breach process; effective date reported inconsistently (14 Sep vs 17 Oct 2023).","verified":false}],
"tags":["sensitive_health","biometric"]},

{"doc_id":"bahrain-pdpl-30-2018","title":"Law No. (30) of 2018 with respect to Personal Data Protection","issuer":"Kingdom of Bahrain; Personal Data Protection Authority","jurisdiction":"Bahrain","doc_type":"law","year":2018,"status":"in force","url_primary":"UNVERIFIED — no official URL opened","url_pdf_or_fulltext":"UNVERIFIED","language":"Arabic","license_or_reuse_terms":"Unknown",
"relevant_provisions":[
{"ref":"Whole law","paraphrase":"Bahrain's general data protection law (reported in force 1 Aug 2019), named as a compliance baseline in Bahrain's 2025 AI policy.","relevance_to_adhd_app":"Applies to Bahraini users; sensitive-data clauses NOT verified.","verified":false}],
"tags":["sensitive_health","consent"]},

{"doc_id":"mdcg-2019-11-rev1","title":"MDCG 2019-11 rev.1 — Qualification and classification of software (MDR 2017/745, IVDR 2017/746)","issuer":"Medical Device Coordination Group / European Commission","jurisdiction":"EU","doc_type":"guidance","year":2025,"status":"non-binding","url_primary":"https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en","url_pdf_or_fulltext":"https://health.ec.europa.eu/medical-devices-sector/new-regulations/guidance-mdcg-endorsed-documents-and-other-guidance_en","language":"English","license_or_reuse_terms":"Commission reuse policy; MDR text not opened.",
"relevant_provisions":[
{"ref":"Qualification","paraphrase":"Software is medical device software based on intended purpose (e.g., diagnosis, monitoring, treatment or alleviation of disease or disability), regardless of platform.","relevance_to_adhd_app":"'Helps manage ADHD' claims can make the app MDSW; 'study habits' claims less likely.","verified":false},
{"ref":"MDR Annex VIII Rule 11 (as explained)","paraphrase":"Software informing diagnostic/therapeutic decisions is at least Class IIa, other MDSW generally Class I; rev.1 (June 2025) clarified intended purpose and modules.","relevance_to_adhd_app":"Modular design can keep wellness modules outside MDR.","verified":false},
{"ref":"MDCG 2025-6 (listed on page)","paraphrase":"June 2025 FAQ on interplay between MDR/IVDR and the AI Act.","relevance_to_adhd_app":"Notified-body MDSW makes its AI high-risk via AI Act Art. 6(1), now from 2 Aug 2028.","verified":true}],
"tags":["medical_device"]},

{"doc_id":"fda-general-wellness-2026","title":"General Wellness: Policy for Low Risk Devices (January 2026)","issuer":"US FDA, CDRH","jurisdiction":"US","doc_type":"guidance","year":2026,"status":"non-binding","url_primary":"https://fda.gov/regulatory-information/search-fda-guidance-documents/general-wellness-policy-low-risk-devices","url_pdf_or_fulltext":"https://www.fda.gov/media/90652/download","language":"English","license_or_reuse_terms":"US government work, generally public domain.",
"relevant_provisions":[
{"ref":"General wellness product definition","paraphrase":"Low-risk (non-invasive, non-implanted) products intended only for general wellness fall under enforcement discretion; issued 6 Jan 2026, superseding 2019.","relevance_to_adhd_app":"Non-invasive HRV/EDA/motion wearables with focus/stress wellness claims can stay outside device oversight.","verified":true},
{"ref":"Disease-related claims","paraphrase":"Claims to diagnose or treat a specific disease fall outside the policy.","relevance_to_adhd_app":"'ADHD management' claims probably exceed it; not verified clause-by-clause.","verified":false}],
"tags":["medical_device","biometric"]},

{"doc_id":"imdrf-samd-n12-2014","title":"Software as a Medical Device: Possible Framework for Risk Categorization (IMDRF/SaMD WG/N12FINAL:2014)","issuer":"International Medical Device Regulators Forum","jurisdiction":"global","doc_type":"framework","year":2014,"status":"non-binding","url_primary":"https://www.imdrf.org/documents/software-medical-device-possible-framework-risk-categorization-and-corresponding-considerations","url_pdf_or_fulltext":"UNVERIFIED — IMDRF blocks automated fetch","language":"English","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Risk matrix","paraphrase":"Categories I–IV by significance of information (treat/diagnose, drive or inform clinical management) against healthcare situation (critical, serious, non-serious).","relevance_to_adhd_app":"A medical ADHD tool that informs management of a non-serious condition would be lowest category. NOT opened.","verified":false}],
"tags":["medical_device"]},

{"doc_id":"imdrf-n81-2025","title":"Characterization Considerations for Medical Device Software and Software-Specific Risk (IMDRF/SaMD WG/N81 FINAL:2025)","issuer":"International Medical Device Regulators Forum","jurisdiction":"global","doc_type":"guidance","year":2025,"status":"non-binding","url_primary":"https://www.imdrf.org/documents/characterization-considerations-medical-device-software-and-software-specific-risk","url_pdf_or_fulltext":"https://www.imdrf.org/sites/default/files/2025-01/IMDRF_SaMD%20WG_Software-Specific%20Risk_N81%20Final_0.pdf","language":"English","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Whole document (secondary summary)","paraphrase":"Published 29 Jan 2025; complements N12, stresses clear intended purpose and direct and indirect harms.","relevance_to_adhd_app":"Indirect harms such as anxiety from false 'distracted' alerts belong in the risk file.","verified":false}],
"tags":["medical_device"]},

{"doc_id":"eu-dsa-art28-minors-guidelines-2025","title":"Guidelines on measures to ensure a high level of privacy, safety and security for minors online, Art. 28(4) Regulation (EU) 2022/2065 (C/2025/5519)","issuer":"European Commission","jurisdiction":"EU","doc_type":"guidance","year":2025,"status":"non-binding","url_primary":"https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors","url_pdf_or_fulltext":"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:C_202505519","language":"24 EU languages","license_or_reuse_terms":"EUR-Lex/Commission reuse (attribution).",
"relevant_provisions":[
{"ref":"Section 6.4(b); Section 6.6 para. 69(k)-(l)","paraphrase":"Minors should not be exposed to persuasive design features aimed predominantly at engagement that may lead to overuse (Section 6.4, Online interface design), nor to manipulative design techniques such as scarcity, intermittent or random rewards, or to paid loot boxes with random outcomes, that can lead to excessive or unwanted spending or addictive behaviour (Section 6.6, Commercial practices, para. 69(k)-(l)).","relevance_to_adhd_app":"Variable-ratio rewards collide with this; use predictable user-set rewards.","verified":true},
{"ref":"Section 6.3.1 Default settings, para. 57(b)","paraphrase":"Push notifications should be off by default for minors and always off during core sleep hours (para. 57(b)(vii)); streaks, autoplay and similar excessive-use features disabled by default (para. 57(b)(vi), (viii)).","relevance_to_adhd_app":"Break prompts for minors should be opt-in, if the app is an 'online platform' (uncertain).","verified":true}],
"tags":["dark_patterns","children_data","advertising"]},

{"doc_id":"eu-ucpd-2005-29","title":"Directive 2005/29/EC — Unfair Commercial Practices Directive","issuer":"European Parliament and Council of the EU","jurisdiction":"EU","doc_type":"law","year":2005,"status":"in force","url_primary":"https://eur-lex.europa.eu/eli/dir/2005/29/oj","url_pdf_or_fulltext":"https://eur-lex.europa.eu/eli/dir/2005/29/oj","language":"24 EU languages","license_or_reuse_terms":"EUR-Lex reuse. Opened by subagent; consolidated version not opened.",
"relevant_provisions":[
{"ref":"Art. 5(3); Arts. 8-9","paraphrase":"Practices affecting groups vulnerable through mental or physical infirmity, age or credulity are judged from that group's view; aggressive practices incl. undue influence are unfair.","relevance_to_adhd_app":"Upsells timed to low-attention or stress states risk being unfair.","verified":false}],
"tags":["dark_patterns","advertising"]},

{"doc_id":"ftc-dark-patterns-2022","title":"Bringing Dark Patterns to Light (FTC Staff Report, Sept 2022)","issuer":"US FTC Bureau of Consumer Protection","jurisdiction":"US","doc_type":"guidance","year":2022,"status":"non-binding","url_primary":"https://www.ftc.gov/reports/bringing-dark-patterns-light","url_pdf_or_fulltext":"https://www.ftc.gov/system/files/ftc_gov/pdf/P214800%20Dark%20Patterns%20Report%209.14.2022%20-%20FINAL.pdf","language":"English","license_or_reuse_terms":"US government work, generally public domain.",
"relevant_provisions":[
{"ref":"Tactic categories","paraphrase":"Flags disguised ads, hard cancellation, buried terms/fees and tricking users into sharing data.","relevance_to_adhd_app":"Simple cancellation and honest data prompts for impulsive users. Seen via subagent only.","verified":false}],
"tags":["dark_patterns","advertising","consent"]},

{"doc_id":"un-crpd-2006","title":"Convention on the Rights of Persons with Disabilities (A/RES/61/106)","issuer":"United Nations General Assembly","jurisdiction":"global","doc_type":"law","year":2006,"status":"in force","url_primary":"UNVERIFIED — not opened","url_pdf_or_fulltext":"UNVERIFIED","language":"Six UN languages","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Arts. 9, 22, 25 (from memory)","paraphrase":"ICT accessibility; privacy of health and rehabilitation information; health care on free and informed consent.","relevance_to_adhd_app":"Frames neurodivergent users as rights-holders. NOT verified.","verified":false}],
"tags":["accessibility","sensitive_health","consent"]},

{"doc_id":"w3c-wcag-2-2","title":"Web Content Accessibility Guidelines (WCAG) 2.2","issuer":"W3C","jurisdiction":"global","doc_type":"standard","year":2023,"status":"in force","url_primary":"https://www.w3.org/TR/WCAG22/","url_pdf_or_fulltext":"https://www.w3.org/TR/WCAG22/","language":"English","license_or_reuse_terms":"W3C Document License (not re-checked).",
"relevant_provisions":[
{"ref":"SC 2.2.1, 3.2.6, 3.3.7, 3.3.8","paraphrase":"Adjustable timing, consistent help, no redundant entry, authentication without cognitive tests.","relevance_to_adhd_app":"Timed tasks and prompts adjustable; no memory-based login. Seen via subagent.","verified":false}],
"tags":["accessibility"]},

{"doc_id":"w3c-coga-usable-2021","title":"Making Content Usable for People with Cognitive and Learning Disabilities (W3C Note)","issuer":"W3C COGA Task Force","jurisdiction":"global","doc_type":"guidance","year":2021,"status":"non-binding","url_primary":"UNVERIFIED — not opened","url_pdf_or_fulltext":"UNVERIFIED","language":"English","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Design objectives (from memory)","paraphrase":"Objectives include helping users focus and avoid mistakes.","relevance_to_adhd_app":"Closest neurodiversity-specific design guidance; NOT verified.","verified":false}],
"tags":["accessibility"]},

{"doc_id":"unesco-rec-ethics-ai-2021","title":"Recommendation on the Ethics of Artificial Intelligence","issuer":"UNESCO General Conference","jurisdiction":"global","doc_type":"guidance","year":2021,"status":"non-binding","url_primary":"UNVERIFIED — not opened","url_pdf_or_fulltext":"UNVERIFIED","language":"Six UN languages","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Values/principles (from memory)","paraphrase":"Human oversight, transparency, privacy, fairness and wellbeing.","relevance_to_adhd_app":"Ethics baseline; NOT verified.","verified":false}],
"tags":["human_oversight","audit_transparency"]},

{"doc_id":"unesco-ram-2023","title":"Readiness assessment methodology: a tool of the Recommendation on the Ethics of AI","issuer":"UNESCO","jurisdiction":"global","doc_type":"framework","year":2023,"status":"non-binding","url_primary":"https://www.unesco.org/ethics-ai/en/ram","url_pdf_or_fulltext":"No official PDF located","language":"English","license_or_reuse_terms":"© UNESCO 2023; terms not verified.",
"relevant_provisions":[
{"ref":"Five dimensions","paraphrase":"Country diagnostic across legal, social/cultural, economic, scientific/educational and technological dimensions.","relevance_to_adhd_app":"Assesses countries, not products. Seen via subagent.","verified":false}],
"tags":["audit_transparency"]},

{"doc_id":"oecd-ai-principles","title":"Recommendation of the Council on Artificial Intelligence (OECD/LEGAL/0449), 2019, amended 2024","issuer":"OECD Council","jurisdiction":"global","doc_type":"guidance","year":2019,"status":"non-binding","url_primary":"https://legalinstruments.oecd.org/en/instruments/OECD-LEGAL-0449","url_pdf_or_fulltext":"UNVERIFIED — page needs JavaScript; content not retrieved","language":"English, French","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Principles 1.1-1.5 (from memory)","paraphrase":"Human rights and privacy, transparency, robustness/safety incl. override mechanisms, accountability.","relevance_to_adhd_app":"Supports user override; NOT verified.","verified":false}],
"tags":["human_oversight","audit_transparency"]},

{"doc_id":"oecd-classification-ai-systems-2022","title":"OECD Framework for the Classification of AI Systems (Digital Economy Papers No. 323)","issuer":"OECD","jurisdiction":"global","doc_type":"framework","year":2022,"status":"non-binding","url_primary":"https://oecd.org/en/publications/oecd-framework-for-the-classification-of-ai-systems_cb6d9eca-en.html","url_pdf_or_fulltext":"https://www.oecd.org/content/dam/oecd/en/publications/reports/2022/02/oecd-framework-for-the-classification-of-ai-systems_336a8b57/cb6d9eca-en.pdf","language":"English","license_or_reuse_terms":"OECD terms not checked; DOI 10.1787/cb6d9eca-en.",
"relevant_provisions":[
{"ref":"Five dimensions","paraphrase":"Characterises AI systems by People & Planet, Economic Context, Data & Input, AI Model, Task & Output.","relevance_to_adhd_app":"Ready-made tagging schema for the KB.","verified":true}],
"tags":["audit_transparency"]},

{"doc_id":"who-ethics-governance-ai-health-2021","title":"Ethics and governance of artificial intelligence for health: WHO guidance","issuer":"World Health Organization","jurisdiction":"global","doc_type":"guidance","year":2021,"status":"non-binding","url_primary":"https://www.who.int/publications/i/item/9789240029200","url_pdf_or_fulltext":"https://www.who.int/publications/i/item/9789240029200","language":"English and others","license_or_reuse_terms":"WHO typically CC BY-NC-SA 3.0 IGO; not verified.",
"relevant_provisions":[
{"ref":"Six consensus principles","paraphrase":"Identifies ethical risks of AI for health and six principles so AI serves the public benefit.","relevance_to_adhd_app":"Principle names (autonomy, safety, transparency, accountability, inclusiveness, sustainability) from memory.","verified":true}],
"tags":["sensitive_health","human_oversight","audit_transparency"]},

{"doc_id":"iso-iec-42001-2023","title":"ISO/IEC 42001:2023 AI — Management system","issuer":"ISO/IEC JTC 1/SC 42","jurisdiction":"global","doc_type":"standard","year":2023,"status":"in force","url_primary":"https://www.iso.org/standard/42001","url_pdf_or_fulltext":"Paid — no free full text","language":"English, French","license_or_reuse_terms":"ISO copyright; metadata/paraphrase only.",
"relevant_provisions":[
{"ref":"Clauses 4-10, Annex A","paraphrase":"Certifiable AI management system with controls on impact assessment, data and third parties.","relevance_to_adhd_app":"Auditable governance wrapper. Seen via subagent.","verified":false}],
"tags":["audit_transparency","human_oversight"]},

{"doc_id":"iso-iec-23894-2023","title":"ISO/IEC 23894:2023 AI — Guidance on risk management","issuer":"ISO/IEC JTC 1/SC 42","jurisdiction":"global","doc_type":"standard","year":2023,"status":"in force","url_primary":"https://www.iso.org/standard/77304.html","url_pdf_or_fulltext":"Paid — no free full text","language":"English","license_or_reuse_terms":"ISO copyright.",
"relevant_provisions":[
{"ref":"Whole standard","paraphrase":"Lifecycle AI risk guidance built on ISO 31000; not certifiable.","relevance_to_adhd_app":"Structure for risks like over-alerting and psychological harm.","verified":false}],
"tags":["audit_transparency"]},

{"doc_id":"ieee-7014-2024","title":"IEEE 7014-2024 Standard for Ethical Considerations in Emulated Empathy in Autonomous and Intelligent Systems","issuer":"IEEE Standards Association","jurisdiction":"global","doc_type":"standard","year":2024,"status":"in force","url_primary":"https://ieeexplore.ieee.org/document/10576666","url_pdf_or_fulltext":"https://ieeexplore.ieee.org/browse/standards/get-program/page/series?id=93","language":"English","license_or_reuse_terms":"Free via IEEE GET Program for personal use; IEEE copyright — no redistribution.",
"relevant_provisions":[
{"ref":"Scope","paraphrase":"Ethics model for systems that identify, quantify, respond to or simulate affective states, including emotions and cognitive states; published 28 June 2024.","relevance_to_adhd_app":"Explicitly covers cognitive states like attention — best-fit design standard.","verified":true},
{"ref":"IEEE 7014.1-2026","paraphrase":"Recommended practice on emulated empathy in partner-based general-purpose AI.","relevance_to_adhd_app":"Relevant if adding an LLM coach.","verified":true}],
"tags":["emotion_inference","human_oversight","dark_patterns"]},

{"doc_id":"itu-t-y3172","title":"ITU-T Y.3172 (2019) Architectural framework for machine learning in future networks including IMT-2020","issuer":"ITU-T Study Group 13","jurisdiction":"global","doc_type":"standard","year":2019,"status":"in force","url_primary":"https://www.itu.int/epublications/publication/itu-t-y-3144-2024-09-future-networks-including-imt-2020-requirements-and-functional-architecture-of-distributed-core-network","url_pdf_or_fulltext":"https://www.itu.int/rec/dologin_pub.asp?lang=s&id=T-REC-Y.Sup96-202511-I%21%21PDF-E&type=items","language":"English","license_or_reuse_terms":"Free download, ITU copyright. Own page itu.int/rec/T-REC-Y.3172 NOT opened; verified via ITU documents citing it.",
"relevant_provisions":[
{"ref":"Definitions/architecture","paraphrase":"Defines ML pipeline, ML overlay, ML Function Orchestrator and ML sandbox; Supplement 96 (11/2025) lists it in force.","relevance_to_adhd_app":"Pattern for separating sensing, model and intervention nodes and sandbox-testing the agent.","verified":true}],
"tags":["audit_transparency"]},

{"doc_id":"itu-t-y3173-y3174","title":"ITU-T Y.3173 (intelligence levels of future networks) and Y.3174 (2020, data handling to enable ML)","issuer":"ITU-T Study Group 13","jurisdiction":"global","doc_type":"standard","year":2020,"status":"in force","url_primary":"https://standards.globalspec.com/std/13407401/Y.3172","url_pdf_or_fulltext":"https://www.itu.int/rec/dologin_pub.asp?lang=s&id=T-REC-Y.Sup96-202511-I%21%21PDF-E&type=items","language":"English","license_or_reuse_terms":"ITU copyright; own pages NOT opened.",
"relevant_provisions":[
{"ref":"Y.3173 / Y.3174 scope","paraphrase":"Grading network intelligence levels; data collection, processing and output handling for ML.","relevance_to_adhd_app":"Analogy for grading agent autonomy and a data-flow template; no health-privacy safeguards.","verified":false}],
"tags":["audit_transparency"]},

{"doc_id":"itu-ai-ready-report-2-0","title":"AI Ready – Analysis Towards a Standardized Readiness Framework (Report 2.0)","issuer":"International Telecommunication Union","jurisdiction":"global","doc_type":"framework","year":2026,"status":"non-binding","url_primary":"https://www.itu.int/epublications/ru/publication/ai-ready-analysis-towards-a-standardized-readiness-framework/en","url_pdf_or_fulltext":"https://www.itu.int/dms_pub/itu-t/opb/ai4g/T-AI4G-AI4GOOD-2025-6-PDF-E.pdf","language":"English","license_or_reuse_terms":"ITU copyright; not checked.",
"relevant_provisions":[
{"ref":"Basic framework","paraphrase":"Bottom-up framework with six factors (data, research, deployment support, standards, open source, sandboxes) and a pilot toolkit; e-publication dated 19 Jan 2026.","relevance_to_adhd_app":"KB can map to 'standards' and 'sandbox' factors.","verified":true}],
"tags":["audit_transparency"]},

{"doc_id":"bahrain-ai-general-policy-2025","title":"General Policy for the Use of Artificial Intelligence, Version 1.0 (20 May 2025)","issuer":"Information & eGovernment Authority (iGA), Bahrain; approved by MCICT","jurisdiction":"Bahrain","doc_type":"national_strategy","year":2025,"status":"in force","url_primary":"https://www.iga.gov.bh/Media/Publications/National%20Digital%20Policies/General%20Policy%20for%20the%20Use%20of%20AI.pdf","url_pdf_or_fulltext":"https://www.iga.gov.bh/Media/Publications/National%20Digital%20Policies/General%20Policy%20for%20the%20Use%20of%20AI%20-%20%20Final%2030%20Jul%202025.pdf","language":"English, Arabic","license_or_reuse_terms":"'©iGA ... All rights reserved' — link and paraphrase only.",
"relevant_provisions":[
{"ref":"Section 3 Scope","paraphrase":"Applies to all government entities in Bahrain.","relevance_to_adhd_app":"Binds only public-sector deployments (e.g., public schools).","verified":true},
{"ref":"Section 4, First and Second Principles","paraphrase":"Final decisions on important matters stay under human control; AI must prevent physical or psychological harm.","relevance_to_adhd_app":"Human-in-the-loop for escalations; psychological-harm testing.","verified":true},
{"ref":"Glossary 'Sensitive Data'; Section 2","paraphrase":"Sensitive data includes health information; entities must comply with the PDPL and GCC AI Ethics guideline.","relevance_to_adhd_app":"Physiological data in government use is sensitive.","verified":true}],
"tags":["human_oversight","sensitive_health","audit_transparency"]},

{"doc_id":"bahrain-ntp6-2023","title":"Sixth National Telecommunications Plan (NTP6), Edict (102) of 2023","issuer":"Ministry of Transportation and Telecommunications, Bahrain","jurisdiction":"Bahrain","doc_type":"national_strategy","year":2023,"status":"in force","url_primary":"https://www.mtt.gov.bh/index.php/projects/sixth-national-telecommunications-plan","url_pdf_or_fulltext":"https://www.mtt.gov.bh/telecom-laws-and-regulations","language":"English, Arabic","license_or_reuse_terms":"Not stated.",
"relevant_provisions":[
{"ref":"Edict Art. I; plan period","paraphrase":"Adopted November 2023 for three years (2023–2026) under Telecommunications Law Art. 15, with six pillars starting with infrastructure and connectivity; 2024 WSIS Prize.","relevance_to_adhd_app":"Context only; term ends around Nov 2026 and no NTP7 found — check for successor.","verified":true}],
"tags":[]},

{"doc_id":"nt-ai-assurance-framework","title":"Northern Territory Government AI Assurance Framework (via NT AI Policy for public sector officers)","issuer":"Northern Territory Government, Australia","jurisdiction":"Australia (NT)","doc_type":"framework","year":2024,"status":"in force","url_primary":"https://dcdd.nt.gov.au/publications/artificial-intelligence-policy","url_pdf_or_fulltext":"UNVERIFIED — framework PDF not opened","language":"English","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"AI Policy — acceptable use","paraphrase":"AI with tangible impact on services, operations or the public must be assessed against the Framework; no personal or sensitive (incl. health) information in public AI tools.","relevance_to_adhd_app":"Model for risk-tiered self-assessment and banning sensitive data in third-party LLM calls.","verified":true},
{"ref":"Release date","paraphrase":"Secondary sources conflict: 26 June 2024 vs November 2025 version.","relevance_to_adhd_app":"Unresolved; cite the policy page.","verified":false}],
"tags":["sensitive_health","audit_transparency","human_oversight"]},

{"doc_id":"ilia-2025","title":"Latin American Artificial Intelligence Index (ILIA) 2025, third edition","issuer":"CENIA (Chile) and UN ECLAC","jurisdiction":"Latin America and Caribbean","doc_type":"framework","year":2025,"status":"non-binding","url_primary":"https://www.cepal.org/en/events/launch-third-edition-latin-american-artificial-intelligence-index-ilia-2025","url_pdf_or_fulltext":"https://indicelatam.cl/wp-content/uploads/2026/03/ILIA-2025.-Key-Findings-Applied-Artificial-Intelligence-and-Human-Talent-compressed.pdf","language":"Spanish, English","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Structure","paraphrase":"Measures AI readiness, adoption and governance in 19 countries via 100+ sub-indicators in three dimensions; launched 3 Oct 2025.","relevance_to_adhd_app":"Regional governance benchmark; a fourth edition (20 countries) is advertised.","verified":true}],
"tags":["audit_transparency"]},

{"doc_id":"un-pact-future-gdc-a-res-79-1","title":"The Pact for the Future (A/RES/79/1), Annex I: Global Digital Compact","issuer":"United Nations General Assembly","jurisdiction":"global","doc_type":"framework","year":2024,"status":"non-binding","url_primary":"https://www.un.org/en/summit-of-the-future/pact-for-the-future","url_pdf_or_fulltext":"https://documents.un.org/doc/undoc/gen/n24/272/22/pdf/n2427222.pdf","language":"Six UN languages","license_or_reuse_terms":"Not verified.",
"relevant_provisions":[
{"ref":"Annex I (GDC)","paraphrase":"Adopted 22 Sept 2024; objectives and commitments for an open, safe, secure digital future incl. AI and data governance.","relevance_to_adhd_app":"Political anchor for inclusive, rights-respecting AI; no enforceable duties.","verified":true}],
"tags":["accessibility","audit_transparency"]}
]
```

## CANDIDATE POLICY GAPS

1. **"Attention" is neither clearly an emotion nor clearly a physical state.**
   - *Conflict:* eu-ai-act-2024-1689 (Art. 3(39), Recital 18) and ec-guidelines-prohibited-ai-practices-2025 exclude fatigue but prohibit inferring students' attention.\[1\]\[10\] ieee-7014-2024 explicitly covers cognitive states.\[16\]
   - *Example:* https://www.insideprivacy.com/artificial-intelligence/european-commission-guidelines-on-prohibited-ai-practices-under-the-eu-artificial-intelligence-act/
   - *Type:* missing standard.

2. **The education ban may block assistive use by neurodivergent students.** The medical exception in eu-ai-act-2024-1689 Art. 5(1)(f) is undefined for non-device support tools.\[17\] A student's voluntary ADHD aid inside a university platform may be prohibited, while the same tool used at home is not. un-crpd-2006 accommodation duties (unverified) point the other way.
   - *Example:* https://epale.ec.europa.eu/en/content/commission-guidelines-prohibited-ai-practices-education
   - *Type:* conflicting objectives.

3. **Wellness vs. medical claims diverge across jurisdictions.**
   - *Conflict:* fda-general-wellness-2026 allows non-invasive sensing with wellness claims. mdcg-2019-11-rev1 treats "alleviation of disability" as a medical purpose.\[6\]\[8\]
   - *Silent:* I found no published Gulf wellness carve-out.
   - *Example:* https://www.cov.com/en/news-and-insights/insights/2026/01/fda-issues-revised-guidance-on-general-wellness-products
   - *Type:* coordination problem.

4. **Non-identifying physiological signals fall through definitional cracks.**
   - us-coppa-rule-2025-amendments §312.2(10) lists gait, face and voice but not HRV or EDA.\[18\]
   - eu-gdpr-2016-679 Art. 9 covers them only if they count as health data.
   - *Example:* https://www.privacylawnetwork.com/news/coppa-rule-2025-amendments.html
   - *Type:* legislative gap.

5. **The UAE has no operative detail for sensitive data.** The Art. 28 Executive Regulations of uae-pdpl-fdl-45-2021 are still unissued, and Art. 2 carves health data out to sectoral law.\[19\]\[20\] It is unclear which regime governs inferred attention data.
   - *Example:* https://www.uaeexperthub.com/uae-data-protection-law-pdpl/
   - *Type:* unclear responsibility.

6. **Qatar's permit model does not scale to consumer apps.** qatar-pdppl-13-2016 Art. 16 requires a permit for any health, psychological-condition or child data.\[4\] I found no published fast-track or sandbox for low-risk support tools.
   - *Example:* https://assurance.ncsa.gov.qa/sites/default/files/library/2022-12/Privacy%20Notice%20-%20Guideline%20for%20Regulated%20Entities.pdf
   - *Type:* missing standard.

7. **Therapeutic nudging collides with anti-persuasive-design rules.** None of these rules has an exception for reminders or rewards the user chose for their own support:
   - eu-dsa-art28-minors-guidelines-2025 §6.4;\[21\]
   - uk-ico-age-appropriate-design-code Standard 13;\[22\]
   - eu-ai-act-2024-1689 Art. 5(1)(b).
   - *Example:* https://digital-strategy.ec.europa.eu/en/library/commission-publishes-guidelines-protection-minors
   - *Type:* conflicting objectives.

8. **No standard for validating the accuracy of inferred states.** iso-iec-23894-2023, imdrf-n81-2025 and ieee-7014-2024 set no accuracy, bias or false-alert thresholds for wearable attention inference in neurodivergent populations.
   - *Example:* no verified precedent found.
   - *Type:* missing standard.

9. **Binding duties for private apps are delayed.** eu-digital-omnibus-ai-2026-1744 pushes Annex III oversight and conformity duties to 2 December 2027.\[23\] bahrain-ai-general-policy-2025 binds only government entities.\[13\]
   - *Example:* https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/
   - *Type:* legislative gap.

10. **Public-sector assurance stops at procurement.** nt-ai-assurance-framework and bahrain-ai-general-policy-2025 bind agencies, not vendors.\[13\]\[24\] A school-procured ADHD app's duties therefore depend on its contract.
    - *Example:* https://dcdd.nt.gov.au/publications/artificial-intelligence-policy
    - *Type:* unclear responsibility.

11. **No binding neurodiversity-specific accessibility standard exists.**
    - w3c-wcag-2-2 covers only some cognitive criteria.
    - w3c-coga-usable-2021 is a non-normative Note.
    - un-pact-future-gdc-a-res-79-1 and unesco-rec-ethics-ai-2021 mention inclusion generally.
    - *Example:* none verified.
    - *Type:* missing standard.

12. **The ITU ML standards are silent on harms to people.** itu-t-y3172 and itu-t-y3173-y3174 have no hooks for consent, special-category data or user override.\[25\] itu-ai-ready-report-2-0 lists "standards" as a readiness factor without mapping health or child protections.\[26\]
    - *Example:* https://www.itu.int/rec/dologin_pub.asp?lang=s&id=T-REC-Y.Sup96-202511-I%21%21PDF-E&type=items
    - *Type:* coordination problem.

## Recommendations
- **Deployment:** offer the app directly to consumers only. Do not build dashboards that show schools or employers their students' or staff's inferred attention.
- **Claims:** use only wellness wording such as "build focus routines". Avoid "manage" or "treat ADHD" unless you pursue MDR or FDA authorisation.
- **Data:** treat all physiological and inferred-state data as special-category.
  - Ask for explicit consent per sensor.
  - Run inference on the device where possible.
  - Use no ad or analytics SDKs.
  - Keep a written retention schedule.
- **Interventions:** make every intervention user-configured and predictable.
  - No random rewards.
  - Notifications opt-in for minors.
  - One-tap pause or override.
  - A plain-language reason for each prompt.
- **Governance:** align with ISO/IEC 42001 and IEEE 7014 now, so any later AI Act high-risk compliance is incremental.

## Caveats
- **Unverified items:** entries marked "verified": false were not confirmed against primary text. The CRPD, UNESCO Recommendation, OECD AI Principles, W3C COGA and Bahrain PDPL had no URL opened and must be checked before publication.
- **Digital Omnibus:** the enrichment check reports that the EUR-Lex text of Regulation (EU) 2026/1744 sets the Art. 113 dates above. In this session I only opened the 27 July 2026 consolidated AI Act on EUR-Lex directly. The Omnibus register entry therefore stays "verified": false.
- **UAE status:** this relies on secondary sources. Claims that the Executive Regulations were issued in 2026 lack a decision number and were treated as unreliable.\[27\] The June 2026 creation of the Federal Authority for Artificial Intelligence and Data is reported by Business-CISO only and has not been confirmed in an official gazette.
- **Not covered:** the UK CMA, other national AI laws (Korea, China, Brazil) and the GCC AI Ethics guideline, because the research budget ran out. Whether a single-user app is a DSA "online platform" is also uncertain.

## Sources

1. [European Commission Guidelines on Prohibited AI Practices under the EU Artificial Intelligence Act](https://www.insideprivacy.com/artificial-intelligence/european-commission-guidelines-on-prohibited-ai-practices-under-the-eu-artificial-intelligence-act/)
2. [EU AI Act unpacked #25: European Commission releases critical AI Act implementation guidelines (Part 3) - Prohibited AI Practices](https://www.freshfields.com/en/our-thinking/blogs/technology-quotient/eu-ai-act-unpacked-25-european-commission-releases-critical-ai-act-implementati-102kfql)
3. [EU AI Act’s High-Risk Deadline: Deferred, Not Cancelled](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-high-risk-deadline-omnibus-20260/)
4. [Law No. 13 of 2016 on the Protection of…](https://qatarlaw.ai/laws/qa-personal-data-privacy-law-13-2016)
5. [FDA Issues Revised Guidance on General Wellness Products](https://www.cov.com/en/news-and-insights/insights/2026/01/fda-issues-revised-guidance-on-general-wellness-products)
6. [EU MDCG Guidance on Medical Device Software](https://www.pureglobal.com/news/mdcg-guidance-documents-clarify-rules-on-medical-device-software-in-the-eu)
7. [MTL-323: MDCG 2019-11 Software Qualification and Classification](https://medtechlearning.com/learning/mdcg-2019-11-software-qualification-and-classification.html)
8. [FDA Updates Its "General Wellness" Device Framework—What Companies Need To Know - Healthcare - United States](https://www.mondaq.com/unitedstates/healthcare/1732360/fda-updates-its-general-wellness-device-frameworkwhat-companies-need-to-know)
9. [AI Act rules on high-risk AI delayed as AI Digital Omnibus agreed - Winston Taylor](https://www.winstontaylor.com/insights/ai-act-rules-on-high-risk-ai-delayed-as-ai-digital-omnibus-agreed)
10. [EU Commission Issues Guidelines on Prohibited AI Practices Under EU AI Act](https://www.wsgrdataadvisor.com/2025/02/eu-commission-issues-guidelines-on-prohibited-ai-practices-under-eu-ai-act/)
11. [What do you need to know about the ICO's Age Appropriate Design Code?](https://brodies.com/insights/ip-technology-and-data/what-do-you-need-to-know-about-the-icos-age-appropriate-design-code/)
12. [Law No.13 of 2016 - Personal Data Privacy Protection](https://www.dataguidance.com/sites/default/files/law_no._13_of_2016_on_protecting_personal_data_privacy_-_english.pdf)
13. [General Policy for the Use of Artificial Intelligence](https://www.iga.gov.bh/Media/Publications/National%20Digital%20Policies/General%20Policy%20for%20the%20Use%20of%20AI%20-%20%20Final%2030%20Jul%202025.pdf)
14. [Bahrain Makes National AI Policy Binding on Government](https://www.theleveragedyears.com/ai-regulation-news/bahrain-iga-general-ai-policy-gov-2025)
15. [ITUPublications International Telecommunication Union Recommendations](https://www.itu.int/rec/dologin_pub.asp?lang=f&amp=&id=T-REC-Y.3142-202404-I%21%21PDF-E&amp=&type=items)
16. [Loading \[MathJax\]/extensions/MathMenu.js](https://ieeexplore.ieee.org/document/10576666)
17. [Commission Guidelines on Prohibited AI Practices in Education - EPA...](https://epale.ec.europa.eu/en/content/commission-guidelines-prohibited-ai-practices-education)
18. [COPPA Rule Amendments and Compliance Dates](https://www.privacylawnetwork.com/news/coppa-rule-2025-amendments.html)
19. [Federal Decree-Law No. 45 of 2021 on the Protection of ...](http://protection-data.ae/wp-content/uploads/2023/10/federal-decret-law-45-uae.pdf)
20. [UAE Data Protection Law (PDPL) 2026: Rules for Businesses](https://www.uaeexperthub.com/uae-data-protection-law-pdpl/)
21. [Guidelines on measures to ensure a high level of privacy ...](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:C_202505519)
22. [The ICO’s Age Appropriate Design Code: is your organisation in scope?](https://www.dacbeachcroft.com/en/What-we-think/The-ICOs-Age-Appropriate-Design-Code-is-your-organisation-in-scope)
23. [EU AI Act High-Risk Deadline Pushed to December 2027](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-omnibus-vii-deadline-delay-20260/)
24. [Artificial Intelligence Policy](https://dcdd.nt.gov.au/publications/artificial-intelligence-policy)
25. [ITU-T Y.3172 - Architectural framework for machine learning in future networks including IMT-2020](https://standards.globalspec.com/std/13407401/Y.3172)
26. [ITU releases second edition of AI readiness assessment framework - CADE](https://cadeproject.org/updates/itu-releases-second-edition-of-ai-readiness-assessment-framework/)
27. [UAE PDPL in 2026: The Law Is In Force, the Executive Regulations Still Are Not](https://www.businessdubai.ae/blogs/uae-pdpl-data-protection)
