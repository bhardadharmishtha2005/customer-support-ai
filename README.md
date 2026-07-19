# Multi-Agent AI Customer Support Hub with RAG

An enterprise-grade, multi-agent customer support architecture designed to automatically classify incoming user requests, route them to specialized processing agents, and perform grounded Retrieval-Augmented Generation (RAG) using a private company knowledge base.

---

## 🏗️ Project Architecture & Tech Stack

This project is built using a decoupled Client-Server architecture to optimize decoupling, scalability, and error resilience:

*   **Frontend Interface:** Streamlit Engine (Designed as a high-fidelity rapid internal hub for corporate operations, integrating modern CSS layouts and session authentication).
*   **Backend REST API:** FastAPI Framework running asynchronous processing pipelines and structural object schemas with Pydantic.
*   **Orchestration Engine:** Multi-Agent Intent Routing Architecture separating duties across targeted domain experts.
*   **Vector Engine:** Semantic chunk index retrieval matching queries against loaded company document contexts.
*   **LLM Matrix Layer:** Google Gemini 3.5 Flash providing low-latency, strictly grounded text processing.

---

## 📁 Repository Directory Map

```text
customer-support-ai/
│
├── frontend/
│   └── frontend.py              # Main dashboard view, authentication layer & chat stream
│
├── backend/
│   ├── app.py                   # Main FastAPI routing microservice engine
│   ├── agents/
│   │     ├── billing.py         # Sub-agent handling invoicing and payment parameters
│   │     ├── technical.py       # Sub-agent isolating hardware, app, and system issues
│   │     ├── product.py         # Sub-agent analyzing catalog rules and specifications
│   │     ├── complaint.py       # Sub-agent assessing system complaints and escalations
│   │     ├── faq.py             # Sub-agent routing baseline general policies
│   │     └── router.py          # Central Intent Detection Matrix orchestrator
│   │
│   ├── rag/                     # Core text extraction and query enhancement algorithms
│   ├── embeddings/              # Embedding array transformers
│   ├── vectorstore/             # FAISS/Chroma dynamic context indexes
│   ├── database/                # Direct storage system schemas
│   └── models/                  # Core Pydantic structural data structures
│
├── knowledge_base/              # Grounding documentation library
│      ├── faq.pdf
│      ├── refund_policy.pdf
│      ├── shipping_policy.pdf
│      ├── warranty.pdf
│      └── user_manual.pdf
│
├── datasets/                    # Validation benchmark files
├── README.md
└── requirements.txt