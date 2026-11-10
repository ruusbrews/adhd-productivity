# ITU reference ingest: retrieval check

Generated 2026-11-10T10:49:15+00:00. ITU pipeline (CrashingGuru/ITUAIReadiness, `simulation/`, unmodified): 256-word chunks, 30 overlap, Ollama `nomic-embed-text`, ChromaDB cosine. Compared with our offline BM25 retriever (`src/adhd_kb/store.py`) at document level, top 3.

* KB collections: {'kb_main': 37, 'kb_framework': 19, 'kb_decisions': 0, 'kb_usecase': 1779}
* `kb_main`: 37 chunks from 37 files
* `country` metadata written by ITU's `infer_country()`: {'global': 35, 'United States': 1, 'Saudi Arabia': 1}

Labelled queries (from `tests/test_core.py`): ITU top-1 3/4, ITU top-3 3/4, BM25 top-1 4/4.
All queries: top-1 agreement 3/8.

| # | Query | Expected | ITU top-3 | BM25 top-3 |
|---|---|---|---|---|
| 1 | emotion inference attention students school biometric | ec-guidelines-prohibited-ai-practices-2025 | ec-guidelines-prohibited-ai-practices-2025<br>eu-ai-act-2024-1689<br>ieee-7014-2024 | ec-guidelines-prohibited-ai-practices-2025<br>eu-ai-act-2024-1689<br>ieee-7014-2024 |
| 2 | streak variable rewards minors notification default | eu-dsa-art28-minors-guidelines-2025 | eu-dsa-art28-minors-guidelines-2025<br>qatar-ncsa-privacy-notice-guideline<br>uk-ico-age-appropriate-design-code | eu-dsa-art28-minors-guidelines-2025<br>uk-ico-age-appropriate-design-code<br>saudi-pdpl-2021 |
| 3 | special nature data children health permit | qatar-pdppl-13-2016 | qatar-ncsa-privacy-notice-guideline<br>us-coppa-rule-2025-amendments<br>uk-ico-age-appropriate-design-code | qatar-pdppl-13-2016<br>qatar-ncsa-privacy-notice-guideline<br>eu-gdpr-2016-679 |
| 4 | wellness claim medical device ADHD | fda-general-wellness-2026 | fda-general-wellness-2026<br>imdrf-samd-n12-2014<br>imdrf-n81-2025 | fda-general-wellness-2026<br>mdcg-2019-11-rev1<br>imdrf-samd-n12-2014 |
| 5 | in-app purchases promoted to children manipulative design | - | uk-ico-age-appropriate-design-code<br>eu-dsa-art28-minors-guidelines-2025<br>ftc-dark-patterns-2022 | eu-ai-act-2024-1689<br>eu-dsa-art28-minors-guidelines-2025<br>uk-ico-age-appropriate-design-code |
| 6 | targeted advertising based on inferred disability or health signals | - | fda-general-wellness-2026<br>ftc-dark-patterns-2022<br>eu-ucpd-2005-29 | mdcg-2019-11-rev1<br>eu-ai-act-2024-1689<br>ftc-dark-patterns-2022 |
| 7 | explicit consent for processing sensitive health or biometric data | - | uae-pdpl-fdl-45-2021<br>bahrain-pdpl-30-2018<br>saudi-pdpl-2021 | eu-gdpr-2016-679<br>uae-pdpl-fdl-45-2021<br>qatar-pdppl-13-2016 |
| 8 | human oversight and review of automated decisions about a person | - | who-ethics-governance-ai-health-2021<br>unesco-rec-ethics-ai-2021<br>oecd-ai-principles | bahrain-ai-general-policy-2025<br>eu-ai-act-2024-1689<br>eu-gdpr-2016-679 |
