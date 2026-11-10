# Pipeline (ITU-T Y.3172 view)

How one tick of the simulation flows through the system, and where the policy knowledge base comes in.
Node labels in brackets are the Y.3172 pipeline nodes; see [mapping.md](mapping.md) for the full mapping.

```mermaid
flowchart LR
    subgraph USER["Simulated user (ML sandbox)"]
        SRC["[SRC] SimulatedUser<br/>ADHD profile, age group, context<br/>task telemetry, self-report,<br/>gaze, HRV/EDA, motion"]
    end

    subgraph AGENT["Local BDI agent (bdi.py)"]
        C["[C] Perceive<br/>only consented channels"]
        GATE{{"R3 perception check<br/>school or workplace?<br/>drop gaze + HRV/EDA"}}
        PP["[PP] Beliefs<br/>attention from behaviour<br/>HRV/EDA = arousal only"]
        M["[M] Deliberate<br/>score 19 interventions<br/>+ provider-forced plans"]
        P{{"[P] Policy check (guardrail.py)<br/>rules R1-R7<br/>allow / modify / block"}}
        D["[D / SINK] Act<br/>push, silent in-app or ambient"]
    end

    subgraph KB["Policy knowledge base (data/kb)"]
        POL[("kb_policy<br/>58 provisions, 37 documents<br/>verified / UNVERIFIED flag")]
        EV[("kb_evidence<br/>22 records")]
        GAPS[("kb_gaps<br/>12 policy gaps")]
        BM25["BM25 retriever<br/>(store.py)"]
    end

    subgraph INST["Institutional agents (agents.py), message bus"]
        PROV["Provider<br/>changes config,<br/>hides IAP and ad SDK"]
        ADV["Policy adviser<br/>findings A1-A6 with citations,<br/>confidence, missing info"]
        REG["Regulator<br/>enforcement ladder:<br/>monitor ... suspend ... refer"]
        WORLD["Education dept,<br/>monitoring agency<br/>(scenario events)"]
    end

    AUDIT[("Audit log<br/>hash-chained JSONL<br/>every decision + citations")]

    subgraph ITU["ITU reference KB (evidence, not used by the agent)"]
        INPUT["knowledge/InputDocs<br/>37 text files"]
        CHROMA[("ChromaDB kb_main<br/>nomic-embed-text<br/>37 chunks")]
    end

    SRC --> C --> GATE --> PP --> M --> P
    P -- "allow / modify" --> D
    P -- "block: try next plan" --> M
    D -- "user response" --> SRC

    GATE -. "R3 query" .-> BM25
    P -. "rule query" .-> BM25
    BM25 --- POL
    BM25 --- EV
    BM25 --- GAPS
    ADV -. "finding query" .-> BM25

    PROV -- "config update" --> M
    ADV -- "digest request" --> P
    P -- "guardrail digest" --> ADV
    WORLD -- "complaint, finding" --> REG
    REG -- "assessment request" --> ADV
    ADV -- "findings" --> REG
    REG -- "info request, enforcement order" --> PROV
    PROV -- "statement, compliance report" --> REG

    GATE --> AUDIT
    P --> AUDIT
    ADV --> AUDIT
    REG --> AUDIT

    POL -. "build.py" .-> INPUT
    INPUT -. "ITU ingest.py (unmodified)" .-> CHROMA
```

## Reading it

- **Left to right is one tick.** The user produces signals; the agent perceives only consented channels. In a school
  or workplace, the R3 check drops gaze and HRV/EDA before they become beliefs. The agent picks an intervention, the
  policy check allows, changes or blocks it, and the user responds.
- **Dotted lines are retrieval.** The policy check, the R3 check and the adviser query the knowledge base to fetch the
  provisions they cite. Rules decide; retrieval supplies the legal basis and flags a rule whose sources are missing.
- **The bottom half is the error scenario.** The provider changes the app, outside bodies report problems to the
  regulator, the adviser assesses with the facts it has so far, and the regulator acts. The agent's guardrail digest
  is how the adviser learns what the provider tried.
- **Everything that decides something writes to the audit log**, so the run can be replayed and checked.
- **The ITU box is separate.** It is the same policy content ingested with ITU's reference pipeline, kept as evidence
  and as a deliverable. The agent does not query it.
