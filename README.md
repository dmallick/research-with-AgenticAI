# Multi-Agent Gold Price Prediction Engine 🪙🤖

**Business Overview:** In the current environment of war, political disturbances, unstable economy, policy changes that's impacting the commodity market. The objective of this MVP is to build a prototye for predicting the Gold Price. 

**Tech Overview:** An asynchronous, state-driven multi-agent prototype built with Python and LangChain/LangGraph principles. This system decouples complex commodity forecasting into specialized, domain-expert agents that analyze macroeconomic data, market sentiment, and technical trend indicators in parallel, synthesizing them into a single, cohesive market intelligence report.


## Architecture & Workflow

A single LLM context window often struggles to balance diverse analytical vectors simultaneously without hallucinating or over-simplifying. This architecture solves that by utilizing a **Fan-Out/Fan-In state graph model**.

1. **Supervisor Node (Orchestrator):** Accepts an input URL, scrapes raw text payloads, initializes the global `GoldPredictionState`, and dispatches jobs.

2. **Parallel Specialist Agents (Fan-Out):**
   - **Macroeconomic Agent:** Evaluates interest rate cycles, currency indices ($DXY$), and central bank policies.
   - **Geopolitical Sentiment Agent:** Analyzes regional conflicts, market volatility, and safe-haven demand spikes.
   - **Technical Analyst Agent:** Scans for structural momentum, pricing trends, and support/resistance mentions.

3. **Synthesizer Node (Fan-In):** Acts as the "Chief Investment Officer," merging data frames, resolving context contradictions, weighing agent outputs, and generating the final execution forecast.


## Tech Stack & Tooling

**Python 3.10+**: Base Platform. Default language for high-performance data & AI orchestration workflows
**LangChain**: LLM Interface. Standardizes unified API calls, prompting layers, and structured message schemas.
**Pydantic / Advanced Typing** | Data Validation | Enforces strict compile-time and runtime validation contracts to eliminate downstream agent compilation errors.
**BeautifulSoup4 & Requests**: Text Scraping. Provides lightweight, clean extraction of visible DOM elements from financial portals

---

##  Codebase Structure

```text
gold_predictor_agents/
│
├── agents/
│   ├── __init__.py
│   ├── supervisor.py        # Brain Node: Manages orchestration, state, and final synthesis
│   ├── macro_agent.py       # Specialist: Processes macroeconomic data indicators
│   ├── sentiment_agent.py   # Specialist: Evaluates geopolitical risk and safe-haven sentiment
│   └── technical_agent.py   # Specialist: Audits price action and support/resistance lines
│
├── state/
│   ├── __init__.py
│   └── graph_state.py       # Strict typing: TypedDict and Pydantic schemas for multi-agent state
│
├── tools/
│   ├── __init__.py
│   └── web_scrapers.py      # Content Extraction Utility: Scrapes visible DOM text safely
│
├── app.py                   # Main Application Hub: Root orchestration runtime execution
└── requirements.txt         # Package Dependencies Matrix


**Codebase Structure**




                    [ User Input / URL ]
                             │
                             ▼
                    ┌─────────────────┐
                    │ Supervisor Agent│◀─────────────────────────┐
                    └─────────────────┘                          │
                             │                                   │
         ┌───────────────────┼───────────────────┐               │
         ▼                   ▼                   ▼               │ Evaluates &
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐      │ Synthesizes
│  Macroeconomic  │ │   Geopolitical  │ │Technical Analyst│      │
│     Agent       │ │ Sentiment Agent │ │      Agent      │      │
└─────────────────┘ └─────────────────┘ └─────────────────┘      │
         │                   │                   │               │
         └───────────────────┼───────────────────┘               │
                             ▼                                   │
                    ┌─────────────────┐                          │
                    │   Synthesizer   │──────────────────────────┘
                    │  (Output Node)  │
                    └─────────────────┘
                             │
                             ▼
                 [Final Gold Price Report]
