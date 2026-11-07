# Evidence-Labelled Digital ADHD-Support Intervention Library (Simulation Use Only)

Only a handful of digitally deliverable supports have meta-analytic backing that holds up in ADHD: self-monitoring prompts, teacher/parent daily report cards, consequence-based token systems with dense or immediate reinforcement, white/pink noise (small lab effect, harmful for non-ADHD users), and physical-activity breaks. Most popular "ADHD hacks" (Pomodoro, body doubling, visual timers, streaks, HRV prompts) have no ADHD-specific controlled evidence, and brain-training/neurofeedback approaches lose their effect under blinded assessment.

**TL;DR**
- Best-supported records: self-monitoring prompts (combined self-regulation effect sizes >1.0 for on-task behaviour in Reid et al. 2005), daily report cards (Hedges' g = 0.36 on teacher-rated symptoms), exercise/movement breaks, and white/pink noise (Nigg et al. 2024: small benefit in ADHD, g = 0.249, 95% CI 0.135–0.363, across 13 studies and 335 participants; a negative effect in non-ADHD comparison groups, g = −0.212, k = 11).
- Null or contested: computerized cognitive/working-memory training and neurofeedback show no significant effect on probably-blinded ADHD symptom ratings; AKL-T01 improved the TOVA API objective attention score (mean change 0.93 vs 0.03 for control, n = 180 vs 168, adjusted p = 0.006; Kollins et al., Lancet Digital Health 2020) but ADHD-RS was not different from control; variable/partial reinforcement is theoretically disfavoured in ADHD and directly conflicts with the EU DSA Article 28 minors guidelines, which also target streaks and push notifications.
- Simulation defaults: notifications off by default for minors, no variable-ratio or streak rewards for minors, do not suppress fidgeting during working-memory tasks, and treat all context-condition thresholds as design assumptions rather than evidence-derived values.

**Caveats (read before use)**
- "verified": true means the exact URL's landing page or abstract text was retrieved during this research session (via direct fetch or search-engine page extraction) and matched the claim; several PubMed/PMC pages returned a captcha on direct fetch, so their verification rests on search-extracted abstract text. "verified": false means the claim came from a secondary/citing source or a blocked page.
- Almost no study stratifies results by DSM presentation; the target_presentations weights are informed design priors, not measured effect moderators.
- All context_conditions thresholds are simulation design assumptions (marked "design assumption" in rationale), not empirically validated cut-offs.
- Most evidence is from children in school/lab settings; transfer to adult self-delivered apps is an extrapolation.

```json
[
  {
    "plan_id": "white-pink-noise-ambient",
    "name": "White/pink noise during focused tasks",
    "description": "Optional ambient white or pink noise played during attention-demanding tasks, user-adjustable volume, off by default for users without elevated ADHD traits.",
    "modality": "auditory",
    "delivery": "ambient",
    "target_presentations": {"inattentive": 0.7, "hyperactive_impulsive": 0.5, "combined": 0.6, "neurotypical": 0.1},
    "context_conditions": [
      {"signal": "attention_level", "operator": "<", "value": 0.4, "rationale": "Design assumption: arousal-based (moderate brain arousal) account predicts benefit when under-aroused/low attention."},
      {"signal": "omission_rate", "operator": ">", "value": 0.15, "rationale": "Design assumption: lab studies report gains on attention task errors; trigger when omissions elevated."}
    ],
    "expected_effect": "Small improvement in laboratory attention/executive task performance in ADHD or high-symptom youth (g = 0.249, 95% CI 0.135–0.363); small impairment in non-ADHD individuals (g = −0.212, 95% CI −0.355 to −0.069, k = 11) (Nigg et al. 2024).",
    "evidence_level": "meta-analysis",
    "evidence_summary": "A preregistered systematic review and meta-analysis (13 studies, 335 participants) found white/pink noise gave a small benefit on laboratory attention tasks in youth with ADHD or elevated attention problems. The same noise impaired performance in non-ADHD comparison participants.\[1\] No brown-noise studies existed and evidence is lab-based, not real-world.",\[2\]
    "citations": [
      {"ref": "Nigg JT, Bruton A, Kozlowski MB, et al. (2024). Systematic Review and Meta-Analysis: Do White Noise or Pink Noise Help With Task Performance in Youth With ADHD or With Elevated Attention Problems? J Am Acad Child Adolesc Psychiatry.", "doi_or_url": "https://pubmed.ncbi.nlm.nih.gov/38428577/", "verified": true}
    ],
    "contraindications": ["users without ADHD traits (evidence of impairment)", "auditory sensory sensitivity", "tasks requiring speech/audio comprehension"],
    "risks": ["performance decrement in neurotypical users", "hearing exposure if volume uncapped"],
    "data_used": ["attention_level (inferred from behaviour)", "omission_rate (task telemetry)"],
    "habituation_note": "Unknown; studies are mostly single-session. Simulation should model possible novelty decay.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Wellness framing only ('may help some people focus'); claims of treating ADHD would move toward medical-device territory. Volume caps advisable for minors."
  },
  {
    "plan_id": "background-music-optional",
    "name": "Background music during tasks",
    "description": "User-selected background music (calm, low-salience) available as an optional focus aid.",
    "modality": "auditory",
    "delivery": "ambient",
    "target_presentations": {"inattentive": 0.3, "hyperactive_impulsive": 0.3, "combined": 0.3, "neurotypical": 0.2},
    "context_conditions": [
      {"signal": "time_on_task_min", "operator": ">", "value": 10, "rationale": "Design assumption: offer only after the user has settled into a task, never as an interruption."}
    ],
    "expected_effect": "Task performance; minimal effect overall.",
    "evidence_level": "meta-analysis",
    "evidence_summary": "A small meta-analysis (5 studies) concluded music interventions were minimally effective for increasing task performance in children and adolescents with ADHD.\[3\] The authors called for better-designed research.\[4\] Treat as weak/near-null evidence.",
    "citations": [
      {"ref": "Maloy M, Peterson R. (2014). A meta-analysis of the effectiveness of music interventions for children and adolescents with ADHD. Psychomusicology: Music, Mind, and Brain, 24(4), 328–339.", "doi_or_url": "https://doi.org/10.1037/pmu0000083", "verified": true}
    ],
    "contraindications": ["lyrics during reading/verbal tasks", "auditory sensory sensitivity"],
    "risks": ["distraction", "evidence base very small (k=5)"],
    "data_used": ["time_on_task_min"],
    "habituation_note": "Not studied.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "yes",
    "claim_wording_class": "wellness",
    "regulatory_notes": ""
  },
  {
    "plan_id": "movement-break-acute-exercise",
    "name": "Short moderate-intensity movement break",
    "description": "Prompted 5–15 min bout of moderate physical activity (walk, active game) between task blocks.",
    "modality": "text",
    "delivery": "notification",
    "target_presentations": {"inattentive": 0.6, "hyperactive_impulsive": 0.7, "combined": 0.7, "neurotypical": 0.4},
    "context_conditions": [
      {"signal": "time_on_task_min", "operator": ">", "value": 30, "rationale": "Design assumption: offer at natural block boundaries, not mid-task."},
      {"signal": "fatigue", "operator": ">", "value": 0.6, "rationale": "Design assumption: fatigue as a trigger for a restorative break."}
    ],
    "expected_effect": "Executive function (inhibitory control, working memory, cognitive flexibility) improvement; chronic programmes show moderate effects (e.g., inhibitory control SMD −0.69 in one 2026 meta-analysis); acute single-session effects positive but smaller.",\[5\]
    "evidence_level": "meta-analysis",
    "evidence_summary": "Multiple meta-analyses of RCTs report that physical activity improves executive functions in children with ADHD, with largest effects on inhibitory control and substantial heterogeneity.\[6\]\[7\]\[8\] A three-level meta-analysis specifically examined single exercise sessions, supporting the acute 'break' form.\[9\] Evidence is mainly from children and chronic programmes; acute break effects are less certain.",
    "citations": [
      {"ref": "Chen C, Fan M, Yu C, Wan S. (2026). Effects of different physical activity modalities on executive function in children with ADHD: a systematic review and meta-analysis. Frontiers in Psychiatry.", "doi_or_url": "https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1824121/full", "verified": true},
      {"ref": "Intervention effect of a single exercise session on executive function in children and adolescents with ADHD: a three-level meta-analysis (PMC12220223).", "doi_or_url": "https://pmc.ncbi.nlm.nih.gov/articles/PMC12220223/", "verified": false}
    ],
    "contraindications": ["do not interrupt hyperfocus/productive flow", "physical limitations or unsafe environment (e.g., classroom without supervision)"],
    "risks": ["task re-entry cost after break", "heterogeneous effect sizes"],
    "data_used": ["time_on_task_min", "fatigue (self-report or inferred)"],
    "habituation_note": "Chronic programmes show sustained effects; prompt compliance may decay—model declining acceptance.",
    "reward_schedule": "none",
    "default_on_notification": true,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "For minors, push prompts should respect DSA Art. 28 guideline expectations on notifications (e.g., none during sleep hours)."\[10\]
  },
  {
    "plan_id": "permit-fidget-during-wm-tasks",
    "name": "Do-not-suppress movement policy during working-memory tasks",
    "description": "System rule: when motion/fidget is detected during working-memory-heavy tasks, do NOT prompt the user to sit still; optionally suggest a fidget tool or standing position.",
    "modality": "environmental",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.4, "hyperactive_impulsive": 0.8, "combined": 0.8, "neurotypical": 0.0},
    "context_conditions": [
      {"signal": "motion_fidget", "operator": ">", "value": 0.5, "rationale": "Design assumption: high movement in ADHD may be compensatory during phonological WM tasks; suppress 'sit still' interventions."}
    ],
    "expected_effect": "Preserve working-memory performance; in ADHD, higher within-child gross motor activity predicted better WM performance (not normalised); in typically developing children it predicted somewhat lower performance.",\[11\]
    "evidence_level": "observational",
    "evidence_summary": "In 29 boys with ADHD and 23 typically developing boys (8–12 y), more gross motor activity predicted significantly better phonological working-memory performance in ADHD but not in controls, and did not change attention. Authors recommend not over-correcting movement during WM-dependent academic tasks.\[11\] Small, all-male, correlational within-subject design.",
    "citations": [
      {"ref": "Sarver DE, Rapport MD, Kofler MJ, Raiker JS, Friedman LM. (2015). Hyperactivity in ADHD: Impairing Deficit or Compensatory Behavior? J Abnorm Child Psychol, 43(7), 1219–1232.", "doi_or_url": "https://doi.org/10.1007/s10802-015-0011-1", "verified": true}
    ],
    "contraindications": ["neurotypical users (movement associated with lower WM performance)", "unsafe movement contexts"],
    "risks": ["misclassifying non-compensatory restlessness", "small all-male sample limits generalisation"],
    "data_used": ["motion_fidget (accelerometer/camera — biometric/inferred, flag)"],
    "habituation_note": "Not applicable (suppression rule, not a prompt).",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Motion sensing of minors is personal data; under the UK Children's Code, keep profiling/monitoring off by default and inform the child when monitoring is active."\[12\]\[13\]
  },
  {
    "plan_id": "timed-breaks-pomodoro",
    "name": "Fixed-interval timed breaks (Pomodoro variant)",
    "description": "Work/break cycles (e.g., 25/5 or 12/3) with an in-app visual timer; adaptive variant lets the user self-regulate break timing.",
    "modality": "visual",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.5, "hyperactive_impulsive": 0.4, "combined": 0.5, "neurotypical": 0.5},
    "context_conditions": [
      {"signal": "time_on_task_min", "operator": ">", "value": 25, "rationale": "Design assumption: classic Pomodoro interval; no ADHD-specific evidence for any interval."},
      {"signal": "fatigue", "operator": ">", "value": 0.6, "rationale": "Design assumption: switch to break if fatigue high."}
    ],
    "expected_effect": "Fatigue, concentration, motivation; no reliable learning-performance difference vs self-regulated breaks in general students; direction of subjective effects is mixed across studies.",
    "evidence_level": "theory/expert opinion",
    "evidence_summary": "No controlled trial compares fixed versus self-regulated breaks in people with ADHD.\[14\]\[15\] In general university students, a 2023 RCT reported less fatigue and better concentration with systematic breaks, while a 2026 study (N=176) found self-regulated breaks produced better mood with no difference in reading comprehension.\[16\]\[17\] The only ADHD-specific Pomodoro study found was a small robot-guided conference paper in 8-year-olds without a self-regulated comparison.",\[18\]
    "citations": [
      {"ref": "(2026). When to Take a Break: Comparing Effects of Systematic Short (Pomodoro) and Self-Regulated Breaks on Subjective Experience and Actual Learning. Behavioral Sciences, 16(7), 1158 (includes de Bruin ABH).", "doi_or_url": "https://doi.org/10.3390/bs16071158", "verified": true},
      {"ref": "Biwer F, de Bruin A, et al. (2023). Understanding effort regulation: Comparing 'Pomodoro' breaks and self-regulated breaks. British Journal of Educational Psychology.", "doi_or_url": "https://doi.org/10.1111/bjep.12593", "verified": false},
      {"ref": "Calle-Urgilés MG, Ordoñez-Ordoñez JO, et al. (2025). Integration of the Pomodoro Technique in a Social Robot to Work on Concentration in 8-Year-Old ADHD Children. ICICT 2025, Springer.", "doi_or_url": "https://doi.org/10.1007/978-981-96-6432-0_14", "verified": true}
    ],
    "contraindications": ["do not interrupt hyperfocus", "time pressure anxiety from visible countdowns"],
    "risks": ["fixed interruptions may break productive flow", "no ADHD-specific evidence"],
    "data_used": ["time_on_task_min", "fatigue (self-report)"],
    "habituation_note": "Unknown in ADHD; general-student studies are single-session or single-day.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "yes",
    "claim_wording_class": "wellness",
    "regulatory_notes": ""
  },
  {
    "plan_id": "self-monitoring-prompt",
    "name": "Periodic self-monitoring prompt ('Was I on task?')",
    "description": "At intervals, the app asks the user to self-record whether they were on task; optional self-graphing and self-reinforcement.",
    "modality": "text",
    "delivery": "notification",
    "target_presentations": {"inattentive": 0.8, "hyperactive_impulsive": 0.6, "combined": 0.8, "neurotypical": 0.3},
    "context_conditions": [
      {"signal": "gaze_off_task", "operator": ">", "value": 0.3, "rationale": "Design assumption: prompt when off-task proportion rises; classroom studies used fixed intervals (e.g., ~3 min)."},
      {"signal": "time_on_task_min", "operator": "between", "value": 3, "rationale": "Design assumption: fixed-interval floor; avoid prompting more often than every few minutes."}
    ],
    "expected_effect": "Increased on-task behaviour and academic productivity/accuracy; combined effect sizes >1.0 (single-case/classroom studies).",
    "evidence_level": "meta-analysis",
    "evidence_summary": "A meta-analysis of self-regulation interventions (self-monitoring, self-monitoring plus reinforcement, self-management, self-reinforcement) for children with ADHD reported combined effect sizes above 1.0 for on-task behaviour, inappropriate behaviour, and academic accuracy and productivity.\[19\]\[20\] A later meta-analytic review of classroom interventions found self-regulation and consequence-based strategies among the most effective for off-task behaviour.\[21\]\[22\] Effects come largely from single-case designs with teacher-supported implementation.",
    "citations": [
      {"ref": "Reid R, Trout AL, Schartz M. (2005). Self-Regulation Interventions for Children With Attention Deficit/Hyperactivity Disorder. Exceptional Children.", "doi_or_url": "https://eric.ed.gov/?id=EJ697216", "verified": true},
      {"ref": "Gaastra GF, Groen Y, Tucha L, Tucha O. (2016). The Effects of Classroom Interventions on Off-Task and Disruptive Classroom Behavior in Children with Symptoms of ADHD: A Meta-Analytic Review. PLoS ONE 11(2): e0148841.", "doi_or_url": "https://doi.org/10.1371/journal.pone.0148841", "verified": true}
    ],
    "contraindications": ["do not interrupt hyperfocus", "users who find frequent prompts aversive"],
    "risks": ["prompt fatigue", "self-report inaccuracy", "single-case evidence may overstate effects"],
    "data_used": ["self-report on-task ratings", "gaze_off_task (camera/eye-tracking — biometric, flag) if adaptive"],
    "habituation_note": "Classroom studies often thin prompt intervals over time; model gradual interval lengthening.",
    "reward_schedule": "fixed",
    "default_on_notification": true,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Frequent push prompts to minors should be guardian-configurable and quiet during sleep hours per EU DSA Art. 28 minors guidelines; gaze tracking of minors is high-risk data under the UK Children's Code."\[23\]
  },
  {
    "plan_id": "haptic-self-monitoring-cue",
    "name": "Wearable vibration cue for self-monitoring",
    "description": "A wrist/waist wearable vibrates at fixed or variable intervals as a private cue to check and record on-task status.",
    "modality": "haptic",
    "delivery": "wearable",
    "target_presentations": {"inattentive": 0.8, "hyperactive_impulsive": 0.5, "combined": 0.7, "neurotypical": 0.3},
    "context_conditions": [
      {"signal": "time_on_task_min", "operator": "between", "value": 3, "rationale": "Design assumption based on a classroom study using ~3-min vibration intervals; lengthen as on-task improves."}
    ],
    "expected_effect": "Increased on-task behaviour (single-case: mean ~55% baseline to 70–100% during intervention in one study); student-operated cue outperformed teacher-operated in one thesis.",\[24\]\[25\]
    "evidence_level": "observational",
    "evidence_summary": "Single-case classroom studies pairing self-monitoring with a vibrating MotivAider cue report increased on-task behaviour.\[25\]\[26\] A doctoral study found student use of the device produced more time on task than teacher use.\[24\] Evidence is small-n single-case and partly unpublished; no RCTs located.",
    "citations": [
      {"ref": "Summey C. Self-Monitoring to Increase On-Task Behavior Using the MotivAider®. East Tennessee State University dissertation.", "doi_or_url": "https://dc.etsu.edu/etd/3450/", "verified": true},
      {"ref": "Amato-Zech NA, Hoff KE, Doepke KJ. (2006). Increasing on-task behavior in the classroom: Extension of self-monitoring strategies. Psychology in the Schools (figures quoted via citing source).", "doi_or_url": "https://www.researchgate.net/publication/227873495_Increasing_on-task_behavior_in_the_classroom_Extension_of_self-monitoring_strategies", "verified": false}
    ],
    "contraindications": ["tactile sensory sensitivity", "do not interrupt hyperfocus"],
    "risks": ["habituation to vibration", "stigma if device visible"],
    "data_used": ["timer only (no biometrics) in basic form; optional self-report"],
    "habituation_note": "Device supports variable intervals; studies lengthened intervals while on-task was maintained.",
    "reward_schedule": "none",
    "default_on_notification": true,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": ""
  },
  {
    "plan_id": "daily-report-card-teacher-parent",
    "name": "Digital daily report card (teacher/parent-assisted)",
    "description": "Teacher rates 2–5 target behaviours daily in-app; parent receives summary and delivers home-based rewards for goals met.",
    "modality": "text",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.6, "hyperactive_impulsive": 0.8, "combined": 0.8, "neurotypical": 0.1},
    "context_conditions": [
      {"signal": "commission_rate", "operator": ">", "value": 0.2, "rationale": "Design assumption: daily-cycle intervention; trigger on persistent disruptive/impulsive indicators rather than moment-to-moment signals."}
    ],
    "expected_effect": "Reduced teacher-rated ADHD symptoms (Hedges' g = 0.36, 95% CI 0.12–0.60, I² = 0); larger effects on direct observation (g = 1.05, very high heterogeneity).",\[27\]
    "evidence_level": "meta-analysis",
    "evidence_summary": "A meta-analysis of 7 group-design studies (272 children, mean age 7.9) found daily behaviour report cards reduced teacher-rated ADHD symptoms with a small-to-moderate effect and low heterogeneity.\[27\] A separate meta-analysis of 14 single-case papers (40 cases) also supported the DRC, moderated by study quality and class type.\[28\] Raters were often not blind.",
    "citations": [
      {"ref": "Iznardo M, Rogers MA, Volpe RJ, Labelle PR, Robaey P. (2020). The Effectiveness of Daily Behavior Report Cards for Children With ADHD: A Meta-Analysis. Journal of Attention Disorders.", "doi_or_url": "https://doi.org/10.1177/1087054717734646", "verified": true},
      {"ref": "Pyle K, Fabiano GA. (2017). Daily Report Card Intervention and ADHD: A Meta-Analysis of Single-Case Studies. Exceptional Children, 83(4), 378–395.", "doi_or_url": "https://eric.ed.gov/?id=EJ1151257", "verified": true}
    ],
    "contraindications": ["absent or unwilling teacher/parent", "punitive use"],
    "risks": ["teacher burden", "privacy of school behaviour data shared across settings"],
    "data_used": ["teacher ratings", "parent-delivered reward logs"],
    "habituation_note": "Goals typically raised as child succeeds; reward value may decline—rotate rewards.",
    "reward_schedule": "fixed",
    "default_on_notification": false,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Processes children's behavioural data across school and home; requires a data-protection basis and transparency to the child (UK Children's Code parental-controls and transparency standards)."\[29\]
  },
  {
    "plan_id": "token-economy-dense-then-thinned",
    "name": "Token economy: continuous/immediate reinforcement, gradually thinned",
    "description": "Immediate in-app tokens for each completed micro-task, exchangeable for chosen rewards; reinforcement ratio stretched gradually ('stretching the ratio') once behaviour is established.",
    "modality": "gamified",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.6, "hyperactive_impulsive": 0.8, "combined": 0.8, "neurotypical": 0.3},
    "context_conditions": [
      {"signal": "keystroke_error_rate", "operator": "<", "value": 0.2, "rationale": "Design assumption: reward accurate completion, not speed alone."}
    ],
    "expected_effect": "Task completion and on-task behaviour; consequence-based classroom strategies are among the most effective; stretching ratios gave faster acquisition than partial reinforcement with equal persistence.",\[22\]\[30\]
    "evidence_level": "meta-analysis",
    "evidence_summary": "Classroom meta-analytic evidence ranks consequence-based strategies (rewards, response cost) among the most effective for off-task behaviour in ADHD.\[21\]\[22\] Experimental work shows children with ADHD learn more slowly under both continuous and partial reinforcement and persist less after partial (20%) reinforcement, while a stretching-ratio schedule produced faster learning than partial reinforcement with equal persistence.\[30\]\[31\] A review notes children with ADHD prefer immediate reward and respond to high reinforcement intensity.",\[32\]
    "citations": [
      {"ref": "Gaastra GF, Groen Y, Tucha L, Tucha O. (2016). PLoS ONE 11(2): e0148841.", "doi_or_url": "https://doi.org/10.1371/journal.pone.0148841", "verified": true},
      {"ref": "Hulsbosch A-K, et al. (2023). Instrumental learning and behavioral persistence in children with ADHD: does reinforcement frequency matter? J Child Psychol Psychiatry.", "doi_or_url": "https://doi.org/10.1111/jcpp.13805", "verified": true},
      {"ref": "Hulsbosch A-K, et al. (2019/2020). Reinforcement Contingency Learning in Children with ADHD: Back to the Basics of Behavior Therapy. J Abnorm Child Psychol.", "doi_or_url": "https://doi.org/10.1007/s10802-019-00572-z", "verified": true},
      {"ref": "Luman M, Oosterlaan J, Sergeant JA. (2005). The impact of reinforcement contingencies on AD/HD: A review and theoretical appraisal. Clinical Psychology Review.", "doi_or_url": "https://www.sciencedirect.com/science/article/abs/pii/S0272735804001527", "verified": true}
    ],
    "contraindications": ["rewarding speed over accuracy", "overjustification risk for intrinsically motivated tasks"],
    "risks": ["reward dependence; extinction when tokens stop", "engagement-maximising drift"],
    "data_used": ["task completion events", "keystroke_error_rate"],
    "habituation_note": "Thin the schedule gradually; abrupt withdrawal after partial reinforcement leads to faster extinction in ADHD.",
    "reward_schedule": "fixed",
    "default_on_notification": false,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Fixed, task-contingent rewards are compatible with EU DSA Art. 28 guidelines if not designed to prolong use; avoid any intermittent/random element for minors."
  },
  {
    "plan_id": "variable-ratio-rewards",
    "name": "Variable-ratio / random rewards (loot-style surprise rewards)",
    "description": "Rewards delivered unpredictably after a variable number of completed tasks.",
    "modality": "gamified",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.2, "hyperactive_impulsive": 0.2, "combined": 0.2, "neurotypical": 0.4},
    "context_conditions": [],
    "expected_effect": "Behavioural persistence; in ADHD, persistence after partial reinforcement is reduced (attenuated partial-reinforcement extinction effect), so expected benefit is low or negative.",\[31\]
    "evidence_level": "RCT",
    "evidence_summary": "Randomised laboratory experiments show children with ADHD learn more slowly under partial reinforcement and show reduced persistence after it, consistent with dopamine-transfer-deficit theory, although one study found no acquisition deficit at a denser 33% rate.\[31\]\[33\] Findings are mixed and come from short lab tasks, not apps. Not recommended as a default mechanism.",
    "citations": [
      {"ref": "Hulsbosch A-K, et al. (2023). J Child Psychol Psychiatry.", "doi_or_url": "https://doi.org/10.1111/jcpp.13805", "verified": true},
      {"ref": "Hulsbosch A-K, Beckers T, Furukawa E, Danckaerts M, Van Liefferinge D, Tripp G, Van der Oord S. (2026). Behavioral and Emotional Responding During Instrumental Learning in Children With ADHD: Reinforcement Schedule Effects. Journal of Attention Disorders.", "doi_or_url": "https://doi.org/10.1177/10870547261430072", "verified": true}
    ],
    "contraindications": ["minors", "users with gambling-related or compulsive-use vulnerability"],
    "risks": ["compulsive engagement", "frustration on non-reward", "faster extinction in ADHD"],
    "data_used": ["task completion events"],
    "habituation_note": "Designed to resist habituation—this is precisely the persuasive-design risk.",
    "reward_schedule": "variable",
    "default_on_notification": false,
    "suitable_for_minors": "no",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Direct conflict: EU Commission Article 28(4) DSA guidelines (C/2025/5519) state minors should not be exposed to manipulative design techniques such as intermittent or random rewards.\[34\] Exclude for minors in simulation."
  },
  {
    "plan_id": "streak-counter",
    "name": "Daily streak counter",
    "description": "Counts consecutive days of app use/task completion with visual streak badge.",
    "modality": "gamified",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.2, "hyperactive_impulsive": 0.2, "combined": 0.2, "neurotypical": 0.3},
    "context_conditions": [],
    "expected_effect": "Engagement/adherence; no ADHD-specific outcome evidence found.",
    "evidence_level": "none",
    "evidence_summary": "No peer-reviewed ADHD study of streak mechanics was identified in this review. Streaks are included only so the simulation can model their regulatory exclusion. Loss of a streak may be particularly aversive for users with ADHD-related emotional dysregulation (theoretical).",
    "citations": [
      {"ref": "European Commission. Guidelines on measures to ensure a high level of privacy, safety and security for minors online, pursuant to Article 28(4) of Regulation (EU) 2022/2065 (C/2025/5519).", "doi_or_url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:C_202505519", "verified": true}
    ],
    "contraindications": ["minors", "users prone to shame/frustration on missed days"],
    "risks": ["excessive use", "anxiety on streak loss"],
    "data_used": ["daily usage logs"],
    "habituation_note": "N/A.",
    "reward_schedule": "streak_based",
    "default_on_notification": false,
    "suitable_for_minors": "no",
    "claim_wording_class": "wellness",
    "regulatory_notes": "EU DSA Art. 28 minors guidelines (14 July 2025) call for features contributing to excessive use, such as streaks, to be disabled by default for minors and for removal of persuasive features aimed predominantly at engagement."\[35\]
  },
  {
    "plan_id": "implementation-intention-if-then",
    "name": "If-then plan builder (implementation intentions) with task chunking",
    "description": "Before a task, the user writes or selects 'If [cue], then I will [action]' plans and breaks the task into concrete steps; the app surfaces the plan when the cue context occurs.",
    "modality": "text",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.6, "hyperactive_impulsive": 0.8, "combined": 0.8, "neurotypical": 0.4},
    "context_conditions": [
      {"signal": "commission_rate", "operator": ">", "value": 0.15, "rationale": "Design assumption: lab evidence targets response inhibition (Go/No-Go commission errors)."}
    ],
    "expected_effect": "Reduced commission errors/improved response inhibition; children with ADHD reached the inhibition level of controls in one study.",\[36\]
    "evidence_level": "RCT",
    "evidence_summary": "In experimental studies, children with ADHD who added an if-then plan to a suppression goal improved Go/No-Go inhibition to the level of non-ADHD children, and combining plans with stimulant medication gave the best inhibition.\[37\] Evidence is laboratory-based with small samples; task chunking itself was not separately tested.",
    "citations": [
      {"ref": "Gawrilow C, Gollwitzer PM. (2008). Implementation intentions facilitate response inhibition in children with ADHD. Cognitive Therapy and Research.", "doi_or_url": "https://www.socmot.uni-konstanz.de/publications/implementation-intentions-facilitate-response-inhibition-adhd-children", "verified": true},
      {"ref": "The effectiveness of implementation intentions in children: A systematic review and meta-analysis (2025/2026; details from ResearchGate preview only).", "doi_or_url": "https://www.researchgate.net/publication/401583895_The_effectiveness_of_implementation_intentions_in_children_A_systematic_review_and_meta-analysis", "verified": false}
    ],
    "contraindications": ["overly complex plan-building flows for young children"],
    "risks": ["plan-setting burden", "lab-to-life transfer unproven"],
    "data_used": ["user-entered plans", "commission_rate (task telemetry)"],
    "habituation_note": "Plans need refreshing per task; effect durability not established.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "yes",
    "claim_wording_class": "wellness",
    "regulatory_notes": ""
  },
  {
    "plan_id": "notification-batching",
    "name": "Notification batching / silence during focus",
    "description": "Hold non-urgent notifications during focus sessions and deliver them in batches at breaks.",
    "modality": "environmental",
    "delivery": "notification",
    "target_presentations": {"inattentive": 0.8, "hyperactive_impulsive": 0.7, "combined": 0.8, "neurotypical": 0.7},
    "context_conditions": [
      {"signal": "time_on_task_min", "operator": ">", "value": 0, "rationale": "Design assumption: active whenever a focus session is running."}
    ],
    "expected_effect": "Lower self-reported inattention and hyperactivity symptoms when alerts are off; inattention in turn predicted lower productivity and well-being.",\[38\]
    "evidence_level": "RCT",
    "evidence_summary": "A two-week within-subjects field experiment with 221 general-population participants found higher self-reported inattention and hyperactivity when phone alerts were on than when off.\[38\]\[39\] The authors explicitly state the findings do not show that notifications cause ADHD or that silencing them treats ADHD.\[40\] ADHD-diagnosed samples were not tested.",
    "citations": [
      {"ref": "Kushlev K, Proulx J, Dunn EW. (2016). 'Silence Your Phones': Smartphone Notifications Increase Inattention and Hyperactivity Symptoms. Proceedings of CHI 2016, 1011–1020.", "doi_or_url": "https://doi.org/10.1145/2858036.2858359", "verified": true}
    ],
    "contraindications": ["safety-critical or caregiver alerts must bypass batching"],
    "risks": ["missed urgent messages", "anxiety about missing notifications"],
    "data_used": ["focus-session state", "notification metadata"],
    "habituation_note": "Low habituation risk (removes stimuli rather than adding them).",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "yes",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Aligned with EU DSA Art. 28 minors guidelines, which favour disabling push notifications that contribute to excessive use by default."\[41\]
  },
  {
    "plan_id": "virtual-body-doubling",
    "name": "Virtual body doubling (human or AI co-worker presence)",
    "description": "Live or AI-simulated co-working presence during a task session.",
    "modality": "visual",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.6, "hyperactive_impulsive": 0.4, "combined": 0.5, "neurotypical": 0.3},
    "context_conditions": [
      {"signal": "time_on_task_min", "operator": "<", "value": 5, "rationale": "Design assumption: aimed at task initiation."}
    ],
    "expected_effect": "Faster task completion and higher perceived accuracy/sustained attention vs working alone (pilot).",\[42\]
    "evidence_level": "observational",
    "evidence_summary": "A small HCI study (12 adults with ADHD) in a VR bricklaying task found faster completion and greater perceived attention with a human or AI body double than alone, with divergent preferences between human and AI.\[43\] The authors note prior work found no conclusive effectiveness and some discomfort with social presence.\[42\] Vendor self-report surveys exist but are not peer-reviewed and were excluded.",\[44\]
    "citations": [
      {"ref": "Ara Z, Rahim IB, Zhou P, Yu L, Esmaeili B, Yu L-F, Hong SR. (2025). You Are Not Alone: Designing Body Doubling for ADHD in Virtual Reality. arXiv:2509.12153 (preprint).", "doi_or_url": "https://arxiv.org/abs/2509.12153", "verified": true}
    ],
    "contraindications": ["social anxiety or discomfort with being observed", "live stranger matching for minors"],
    "risks": ["privacy of video presence", "stranger contact"],
    "data_used": ["session presence; video if live (personal data, flag)"],
    "habituation_note": "Unknown; single-session pilot.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Live contact with unknown adults conflicts with child-safety expectations (EU DSA Art. 28 guidelines on contact by strangers; UK Children's Code high-privacy defaults); AI companions require disclosure that the user is interacting with AI under the DSA guidelines."\[45\]
  },
  {
    "plan_id": "mindfulness-breathing-micro",
    "name": "Brief mindfulness/breathing micro-practice",
    "description": "1–3 minute guided breathing or mindful attention exercise offered at breaks or after errors spike.",
    "modality": "auditory",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.5, "hyperactive_impulsive": 0.5, "combined": 0.5, "neurotypical": 0.4},
    "context_conditions": [
      {"signal": "keystroke_error_rate", "operator": ">", "value": 0.25, "rationale": "Design assumption: offer at break points when errors/frustration rise."}
    ],
    "expected_effect": "ADHD symptom reduction for multi-week MBI programmes (children/adolescents SMD −1.30 but I² = 91%); effect of brief in-app micro-practices unknown.",\[46\]
    "evidence_level": "meta-analysis",
    "evidence_summary": "Meta-analyses of mindfulness-based interventions report reductions in ADHD symptoms, including a 2026 meta-analysis of 14 RCTs in children/adolescents with a large but highly heterogeneous effect.\[46\] These are multi-week, often clinician- or group-delivered programmes; brief app-delivered breathing prompts are an untested extrapolation. Earlier meta-analytic work (Cairncross & Miller) covered only 10 studies.",\[47\]
    "citations": [
      {"ref": "Shen F, Zhou H, Zhang T. (2026). Efficacy of mindfulness-based interventions for children and adolescents with ADHD: a systematic review and meta-analysis. Frontiers in Psychiatry.", "doi_or_url": "https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1894822/full", "verified": true},
      {"ref": "Cairncross M, Miller CJ. (2016/2020). The Effectiveness of Mindfulness-Based Therapies for ADHD: A Meta-Analytic Review. Journal of Attention Disorders.", "doi_or_url": "https://doi.org/10.1177/1087054715625301", "verified": false}
    ],
    "contraindications": ["do not interrupt hyperfocus", "trauma-related distress with interoceptive focus"],
    "risks": ["low engagement", "overclaiming from programme-level evidence"],
    "data_used": ["keystroke_error_rate", "self-report"],
    "habituation_note": "Likely engagement decay with repeated identical prompts; vary content.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "yes",
    "claim_wording_class": "wellness",
    "regulatory_notes": ""
  },
  {
    "plan_id": "hrv-biofeedback-breathing",
    "name": "HRV-triggered paced-breathing prompt",
    "description": "Wearable detects low HRV/high arousal and prompts slow paced breathing (~6 breaths/min) with real-time HRV feedback.",
    "modality": "haptic",
    "delivery": "wearable",
    "target_presentations": {"inattentive": 0.2, "hyperactive_impulsive": 0.3, "combined": 0.3, "neurotypical": 0.3},
    "context_conditions": [
      {"signal": "hrv_rmssd", "operator": "<", "value": 20, "rationale": "Design assumption: low RMSSD as stress proxy; no ADHD-validated threshold exists."},
      {"signal": "eda", "operator": ">", "value": 0.7, "rationale": "Design assumption: elevated normalised EDA as arousal proxy."}
    ],
    "expected_effect": "Emotional well-being/stress in non-ADHD samples; no ADHD-specific attention outcome evidence found.",
    "evidence_level": "none",
    "evidence_summary": "No ADHD-specific controlled trial of HRV biofeedback was located in this review. RCTs in other populations (e.g., a 5-week HRV-ER trial in younger and older adults) test emotion-regulation effects, not attention in ADHD.\[48\] Include only as a clearly labelled speculative record.",
    "citations": [
      {"ref": "Multimodal neuroimaging data from a 5-week heart rate variability biofeedback randomized clinical trial (HRV-ER, NCT03458910). Scientific Data (2023).", "doi_or_url": "https://www.nature.com/articles/s41597-023-02396-5", "verified": true}
    ],
    "contraindications": ["cardiac conditions", "anxiety triggered by body monitoring"],
    "risks": ["false triggers from physical activity", "biometric data sensitivity"],
    "data_used": ["hrv_rmssd (biometric, flag)", "eda (biometric, flag)"],
    "habituation_note": "Unknown.",
    "reward_schedule": "none",
    "default_on_notification": false,
    "suitable_for_minors": "unclear",
    "claim_wording_class": "wellness",
    "regulatory_notes": "Processing physiological data is special-category (health) data under GDPR/UK GDPR; claims about treating ADHD would risk medical-device classification."
  },
  {
    "plan_id": "eeg-neurofeedback",
    "name": "EEG neurofeedback attention training",
    "description": "Consumer or clinical EEG headset provides game-based feedback on brain-activity targets.",
    "modality": "gamified",
    "delivery": "wearable",
    "target_presentations": {"inattentive": 0.2, "hyperactive_impulsive": 0.1, "combined": 0.2, "neurotypical": 0.0},
    "context_conditions": [],
    "expected_effect": "ADHD symptoms: significant only on unblinded ratings (SMD 0.35); no significant improvement on probably-blinded ratings (SMD 0.04, 95% CI −0.10 to 0.18, k=20, n=1214).",\[49\]\[50\]
    "evidence_level": "meta-analysis",
    "evidence_summary": "A 2016 meta-analysis found neurofeedback effects only on ratings by unblinded proximal raters, not on probably-blinded ratings or in sham-controlled trials.\[51\] An updated meta-analysis by Westwood, Aggensteiner, Cortese, Sonuga-Barke and colleagues for the European ADHD Guidelines Group (JAMA Psychiatry 2025;82(2):118–129; 38 RCTs, 2,472 participants aged 5–40) likewise found no significant improvement in probably-blinded ADHD total symptoms (k = 20; n = 1214; SMD 0.04, 95% CI −0.10 to 0.18). Null evidence for core symptoms.",
    "citations": [
      {"ref": "Cortese S, Ferrin M, Brandeis D, et al. (2016). Neurofeedback for ADHD: Meta-Analysis of Clinical and Neuropsychological Outcomes From RCTs. J Am Acad Child Adolesc Psychiatry, 55(6), 444–455.", "doi_or_url": "https://doi.org/10.1016/j.jaac.2016.03.007", "verified": true},
      {"ref": "Westwood SJ, Aggensteiner P-M, … Cortese S, Sonuga-Barke EJS; European ADHD Guidelines Group. (2025). Neurofeedback for Attention-Deficit/Hyperactivity Disorder: A Systematic Review and Meta-Analysis. JAMA Psychiatry, 82(2), 118–129. doi:10.1001/jamapsychiatry.2024.3702", "doi_or_url": "https://jamanetwork.com/journals/jamapsychiatry/fullarticle/2827733", "verified": true}
    ],
    "contraindications": ["any use framed as ADHD treatment"],
    "risks": ["cost and time burden without blinded benefit", "brain-data sensitivity"],
    "data_used": ["EEG (biometric/neural, flag)"],
    "habituation_note": "N/A (null evidence).",
    "reward_schedule": "fixed",
    "default_on_notification": false,
    "suitable_for_minors": "no",
    "claim_wording_class": "therapeutic",
    "regulatory_notes": "Therapeutic claims would require medical-device conformity; neural data is highly sensitive health data."
  },
  {
    "plan_id": "game-based-attention-training",
    "name": "Adaptive game-based attention training (AKL-T01 class)",
    "description": "Adaptive multitasking video game targeting attentional control, ~25 min/day for 4 weeks.",
    "modality": "gamified",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.5, "hyperactive_impulsive": 0.2, "combined": 0.5, "neurotypical": 0.0},
    "context_conditions": [],
    "expected_effect": "Improved objective attention (TOVA API mean change 0.93 vs 0.03 for control, adjusted p = 0.006) vs digital control; no difference on ADHD-RS symptoms.",
    "evidence_level": "RCT",
    "evidence_summary": "The STARS-ADHD RCT (348 children aged 8–12, 20 US sites) found AKL-T01 improved an objective attention measure versus a word-game control, but not clinician-rated ADHD-RS symptoms.\[52\]\[53\]\[54\] A broader computerized cognitive training meta-analysis (Westwood et al., Mol Psychiatry 2023; 36 RCTs, 17 of them working-memory training) found, in the 14 trials with probably-blinded data, no effect on ADHD total symptoms (SMD 0.12, 95% CI −0.01 to 0.25) and only a small improvement in inattention (SMD 0.17, 95% CI 0.02–0.31). Trials were industry-sponsored.",
    "citations": [
      {"ref": "Kollins SH, et al. (2020). A novel digital intervention for actively reducing severity of paediatric ADHD (STARS-ADHD): a randomised controlled trial. Lancet Digital Health 2(4): e168–e178.", "doi_or_url": "https://doi.org/10.1016/S2589-7500(20)30017-0", "verified": true},
      {"ref": "Westwood SJ, Parlatini V, Rubia K, Cortese S, Sonuga-Barke EJS. (2023). Computerized cognitive training in ADHD: a meta-analysis of RCTs with blinded and objective outcomes. Molecular Psychiatry.", "doi_or_url": "https://doi.org/10.1038/s41380-023-02000-7", "verified": true}
    ],
    "contraindications": ["screen-time limits", "framing as ADHD treatment outside a regulated product"],
    "risks": ["mild treatment-related adverse events in STARS-ADHD: frustration (5/180, 3%) and headache (3/180, 2%); no serious adverse events or discontinuations (Kollins et al. 2020)", "screen time"],
    "data_used": ["gameplay performance telemetry"],
    "habituation_note": "Adaptive difficulty mitigates; durability of objective gains uncertain.",
    "reward_schedule": "fixed",
    "default_on_notification": false,
    "suitable_for_minors": "with_guardian_control",
    "claim_wording_class": "therapeutic",
    "regulatory_notes": "AKL-T01 (EndeavorRx) is an FDA-cleared prescription digital therapeutic for children 8–12;\[55\]\[56\] replicating its therapeutic claims in a simulation-derived product would imply medical-device status."
  },
  {
    "plan_id": "working-memory-training",
    "name": "Computerized working-memory training",
    "description": "Adaptive span tasks practised daily over several weeks.",
    "modality": "gamified",
    "delivery": "in-app",
    "target_presentations": {"inattentive": 0.2, "hyperactive_impulsive": 0.1, "combined": 0.2, "neurotypical": 0.1},
    "context_conditions": [],
    "expected_effect": "Improves trained working-memory performance; limited/no effect on blinded ADHD symptoms (probably-blinded ADHD total SMD 0.20, 95% CI 0.01–0.40; no effect of WM training specifically on symptoms).",\[57\]
    "evidence_level": "meta-analysis",
    "evidence_summary": "A 2015 meta-analysis found cognitive training improved working-memory performance but had limited effects on ADHD symptoms under blinded assessment, with no symptom effect of working-memory training specifically.\[57\]\[58\] A 2023 update of 36 RCTs found no effect on probably-blinded ADHD total symptoms.\[59\] External working-memory aids (lists, reminders) were not evaluated in the sources found.",
    "citations": [
      {"ref": "Cortese S, Ferrin M, Brandeis D, et al. (2015). Cognitive Training for ADHD: Meta-Analysis of Clinical and Neuropsychological Outcomes From RCTs. J Am Acad Child Adolesc Psychiatry, 54(3), 164–174.", "doi_or_url": "https://doi.org/10.1016/j.jaac.2014.12.010", "verified": true},
      {"ref": "Westwood SJ, et al. (2023). Molecular Psychiatry.", "doi_or_url": "https://doi.org/10.1038/s41380-023-02000-7", "verified": true}
    ],
    "contraindications": ["framing as symptom treatment"],
    "risks": ["time cost without functional transfer"],
    "data_used": ["task performance telemetry"],
    "habituation_note": "Gains are task-specific; little transfer.",
    "reward_schedule": "fixed",
    "default_on_notification": false,
    "suitable_for_minors": "yes",
    "claim_wording_class": "wellness",
    "regulatory_notes": ""
  }
]
```

## Sources

1. [Systematic Review and Meta-Analysis: Do White Noise or Pink Noise Help With Task Performance in Youth With Attention-Deficit/Hyperactivity Disorder or With Elevated Attention Problems? - PubMed](https://pubmed.ncbi.nlm.nih.gov/38428577/)
2. [ADHD and Background Noise: Who It Helps, Who It Hurts](https://www.scienceworkshealth.com/post/adhd-background-noise-brown-noise-focus)
3. [A Meta-Analysis of the Effectiveness of Music Interventions for Children and Adolescents With Attention-Deficit/Hyperactivity Disorder](https://www.ovid.com/journals/pmmb/abstract/10.1037/pmu0000083~a-meta-analysis-of-the-effectiveness-of-music-interventions?redirectionsource=fulltextview)
4. [A meta-analysis of the effectiveness of music interventions for children and adolescents with attention-deficit/hyperactivity disorder.](https://psycnet.apa.org/record/2015-21453-004)
5. [Frontiers](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1824121/full)
6. [Meta-analysis Finds Physical Activity Improves Executive Functions in Persons with ADHD](https://www.adhdevidence.org/blog/exercise-found-to-improve-certain-adhd-symptoms)
7. [Frontiers](https://www.frontiersin.org/journals/public-health/articles/10.3389/fpubh.2023.1133727/full)
8. [Effect of physical activity interventions on executive functions in school-age children with ADHD: A meta-analysis of randomized controlled trials - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0165032725001855)
9. [Intervention effect of a single exercise session on executive function in children and adolescents with attention deficit hyperactivity disorder: a three-level meta-analysis - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC12220223/)
10. [The long-awaited EU Guidelines on Article 28(1) DSA: What online platforms must know - Lexology](https://www.lexology.com/library/detail.aspx?g=93b2f843-a50a-4d0a-bc90-966bbdb90ff2)
11. <https://link.springer.com/article/10.1007/s10802-015-0011-1>
12. [The ICO’s Age-Appropriate Design Code (Children’s Code)](https://evalian.co.uk/childrens-code/)
13. [final-age-appropriate-design-code-of-practice.pdf](https://www.privacylaws.com/media/3093/final-age-appropriate-design-code-of-practice.pdf)
14. [Pomodoro for ADHD Students: Settings That Work](https://focusflowstudy.com/blog/pomodoro-for-adhd-students)
15. [Pomodoro Technique for ADHD: What Works, What Fails](https://focusbox.io/blog/pomodoro-technique-for-adhd/)
16. [Pomodoro Study Technique Complete Guide for 2026 - Brainflow](https://brainflow.co/understanding-the-pomodoro-technique/)
17. [When to Take a Break: Comparing Effects of Systematic Short (Pomodoro) and Self-Regulated Breaks on Subjective Experience and Actual Learning - PubMed](https://pubmed.ncbi.nlm.nih.gov/42510279/)
18. [Integration of the Pomodoro Technique in a Social Robot to Work on Concentration in 8-Year-Old ADHD Children](https://link.springer.com/chapter/10.1007/978-981-96-6432-0_14)
19. [Self-Regulation Interventions for Children With - ProQuest](https://www.proquest.com/docview/201228664?fromopenview=true&pq-origsite=gscholar&sourcetype=Scholarly+Journals)
20. [ERIC - EJ697216 - Self-Regulation Interventions for Children with Attention Deficit/Hyperactivity Disorder, Exceptional Children, 2005](https://eric.ed.gov/?id=EJ697216)
21. [The Effects of Classroom Interventions on Off-Task and Disruptive Classroom Behavior in Children with Symptoms of Attention-Deficit/Hyperactivity Disorder: A Meta-Analytic Review - PMC](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4757442/)
22. [Full article: Exploring neuropsychological effects of a self-monitoring intervention for ADHD-symptoms in school](https://www.tandfonline.com/doi/full/10.1080/21622965.2019.1575218)
23. [UK's Age Appropriate Design Code (Children’s Code): Full Compliance Guide](https://ondato.com/blog/uk-age-appropriate-design-code/)
24. ["Self-Monitoring to Increase On-Task Behavior Using the MotivAider®" by Connie Summey](https://dc.etsu.edu/etd/3450/)
25. [Increasing on‐task behavior in the classroom: Extension of self‐monitoring strategies](https://www.researchgate.net/publication/227873495_Increasing_on-task_behavior_in_the_classroom_Extension_of_self-monitoring_strategies)
26. [(PDF) Increasing On-Task Behavior in Students in a Regular Classroom: Effectiveness of a Self-Management Procedure Using a Tactile Prompt](https://www.researchgate.net/publication/258845723_Increasing_On-Task_Behavior_in_Students_in_a_Regular_Classroom_Effectiveness_of_a_Self-Management_Procedure_Using_a_Tactile_Prompt)
27. [The Effectiveness of Daily Behavior Report Cards for Children With ADHD: A Meta-Analysis - Michelle Iznardo, Maria A. Rogers, Robert J. Volpe, Patrick R. Labelle, Philippe Robaey, 2020](https://doi.org/10.1177/1087054717734646)
28. [ERIC - ED583708 - Daily Report Card Intervention and Attention Deficit Hyperactivity Disorder: A Meta-Analysis of Single-Case Studies, Grantee Submission, 2017](https://eric.ed.gov/?id=ED583708)
29. [1 UK Age-Appropriate Design Code Impact Assessment (cover page) UK](https://www.childrenandscreens.org/wp-content/uploads/2024/03/Children-and-Screens-UK-AADC-Impact-Assessment.pdf)
30. [Reinforcement Contingency Learning in Children with ADHD:](https://d-nb.info/1206063270/34)
31. [Instrumental learning and behavioral persistence in children with attention‐deficit/hyperactivity‐disorder: does reinforcement frequency matter? - Hulsbosch - 2023 - Journal of Child Psychology and Psychiatry - Wiley Online Library](https://acamh.onlinelibrary.wiley.com/doi/10.1111/jcpp.13805)
32. [The impact of reinforcement contingencies on AD/HD: A review and theoretical appraisal - ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0272735804001527)
33. [Behavioral and Emotional Responding During Instrumental Learning in Children With ADHD: Reinforcement Schedule Effects - An-Katrien Hulsbosch, Tom Beckers, Emi Furukawa, Marina Danckaerts, Dagmar Van Liefferinge, Gail Tripp, Saskia Van der Oord, 2026](https://journals.sagepub.com/doi/full/10.1177/10870547261430072)
34. [Guidelines on measures to ensure a high level of privacy ...](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:C_202505519)
35. [European Commission publishes guidelines on the protection ...](https://merlin.obs.coe.int/article/10383)
36. [Implementation intentions facilitate response inhibition in ADHD children](https://www.socmot.uni-konstanz.de/publications/implementation-intentions-facilitate-response-inhibition-adhd-children)
37. [Implementation Intentions Facilitate Response... : Cognitive Therapy & Research](https://www.ovid.com/journals/cotr/abstract/00001076-200832020-00008~implementation-intentions-facilitate-response-inhibition-in)
38. [\[PDF\] "Silence Your Phones": Smartphone Notifications Increase Inattention and Hyperactivity Symptoms](https://www.semanticscholar.org/paper/%22Silence-Your-Phones%22:-Smartphone-Notifications-and-Kushlev-Proulx/848e60fdd6f61004482e6a00a738630782280cf6)
39. [“Silence Your Phones”: Smartphone Notifications Increase](https://www.kushlev.com/s/Kushlev-et-al-Silence-Your-Phones.pdf)
40. [Study: Smartphone Alerts Increase Inattention](https://news.virginia.edu/content/study-smartphone-alerts-increase-inattention-and-hyperactivity)
41. [EU Digital Services Act Guidelines Raise the Bar for Safer Design for Minors - DEV Community](https://dev.to/alifar/eu-digital-services-act-guidelines-raise-the-bar-for-safer-design-for-minors-5egg)
42. [You Are Not Alone: Designing Body Doubling for ADHD in Virtual Reality](https://arxiv.org/pdf/2509.12153)
43. [Virtual Body Doubling: What It Is and How to Do It Online](https://getmotivated.ai/blog/virtual-body-doubling-online)
44. [Virtual Body Doubling for ADHD: What 117 Adults Reported After 12 Weeks](https://flown.com/blog/adhd/body-doubling-adhd-study)
45. [Deep Dive on new Child Online Safety Guidelines - WILLIAM FRY](https://www.williamfry.com/knowledge/deep-dive-on-new-child-online-safety-guidelines/)
46. [Frontiers](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2026.1894822/full)
47. [Behavioral and Cognitive Impacts of Mindfulness-Based Interventions on Adults with Attention-Deficit Hyperactivity Disorder: A Systematic Review - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6476147)
48. [Multimodal neuroimaging data from a 5-week heart rate variability biofeedback randomized clinical trial](https://www.nature.com/articles/s41597-023-02396-5)
49. [Neurofeedback for Attention-Deficit/Hyperactivity Disorder: Meta-Analysis of Clinical and Neuropsychological Outcomes From Randomized Controlled Trials - PubMed](https://pubmed.ncbi.nlm.nih.gov/27238063/?dopt=Abstract)
50. [Neurofeedback for Attention-Deficit/Hyperactivity Disorder: A Systematic Review and Meta-Analysis](https://jamanetwork.com/journals/jamapsychiatry/fullarticle/2827733)
51. [Neurofeedback for Attention-Deficit/Hyperactivity Disorder: Meta-Analysis of Clinical and Neuropsychological Outcomes From Randomized Controlled Trials - Aalborg University's Research Portal](https://vbn.aau.dk/en/publications/neurofeedback-for-attention-deficithyperactivity-disorder-meta-an/)
52. [A novel digital intervention for actively reducing severity of paediatric ADHD (STARS-ADHD): a randomised controlled trial - The Lancet Digital Health](<https://www.thelancet.com/journals/landig/article/PIIS2589-7500(20)30017-0/fulltext>)
53. [Akili Announces Publication of AKL-T01 ADHD Pivotal Study Results in the Lancet Digital Health — Akili Interactive](https://www.akiliinteractive.com/news-collection/akili-announces-publication-of-akl-t01-adhd-pivotal-study-results-in-the-lancet-digital-health)
54. [Effectiveness of a digital therapeutic as adjunct to treatment with medication in pediatric ADHD](https://www.nature.com/articles/s41746-021-00429-0)
55. [Two single arm trials of AKL-T01, a digital therapeutic for adolescents and adults with ADHD - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11187123)
56. [The Video Game Will See You Now](https://www.psychiatrictimes.com/view/video-game-will-see-you-now)
57. [Cognitive Training for Attention-Deficit/Hyperactivity Disorder: Meta-Analysis of Clinical and Neuropsychological Outcomes From Randomized Controlled Trials - King's College London](https://kclpure.kcl.ac.uk/portal/en/publications/cognitive-training-for-attention-deficithyperactivity-disorder-me/)
58. [Cognitive training for attention-deficit/hyperactivity disorder: meta-analysis of clinical and neuropsychological outcomes from randomized controlled trials - Aalborg University's Research Portal](https://vbn.aau.dk/en/publications/cognitive-training-for-attention-deficithyperactivity-disorder-me/)
59. [Computerized cognitive training in attention-deficit/hyperactivity disorder (ADHD): a meta-analysis of randomized controlled trials with blinded and objective outcomes](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC10208955/)
