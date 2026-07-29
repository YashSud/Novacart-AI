# Working Demo Video Script & Walkthrough (5–10 Minutes)

**Project**: NovaCart Enterprise AI Assistant  
**Challenge**: Horrazon AI Engineering Challenge  
**Target Duration**: 6 to 8 minutes  

---

## 🎬 Video Overview & Timestamp Breakdown

| Timestamp | Section | Key Demo Actions |
| :--- | :--- | :--- |
| **0:00 - 1:00** | **Introduction & Problem Statement** | Overview of NovaCart Enterprise AI Assistant, Horrazon challenge, and Ponytail minimalist philosophy. |
| **1:00 - 2:30** | **Single-Click Execution Demo (`python run.py`)** | Run `python run.py` in PowerShell, demonstrating automated version check, dependency check, test suite execution, and server startup. |
| **2:30 - 4:30** | **Web GUI Dashboard Tour & Multi-Hop Query** | Open `http://localhost:8000/`, demonstrate *Multi-Hop Reasoning Query* ("Why did refunds increase in March?"), highlight 6 evidence cards across 3 hops and 95% confidence score. |
| **4:30 - 5:30** | **Semantic Search & Metadata Filtering** | Switch to *Semantic Search* tab, demonstrate filtering by document type (`refund`, `support_ticket`, `warehouse_log`). |
| **5:30 - 6:30** | **Edge Cases & Security Demonstration** | Demonstrate edge-case deduplication (`wh_01_dup`), missing field default handling (`sup_04`), outdated policy detection (`ref_03`), and `X-API-KEY` security `401 Unauthorized` enforcement. |
| **6:30 - 7:30** | **Docker & Code Architecture Review** | Showcase single-stage `Dockerfile`, flat 5-file project layout, and 100% `pytest` test pass rate. |
| **7:30 - 8:00** | **Conclusion & Submission Summary** | Final recap of engineering trade-offs and submission readiness. |

---

## 🎙️ Minute-by-Minute Narration Script

### 0:00 - 1:00 | Introduction
> *"Hello! My name is [Candidate Name], and today I am presenting the NovaCart Enterprise AI Assistant for the Horrazon AI Engineering Challenge. Our goal was to build a production-ready, lightweight RAG and multi-hop reasoning system capable of answering complex business questions across Orders, Refunds, Support Tickets, and Warehouse Logs. The entire system adheres strictly to the Ponytail Philosophy—prioritizing zero unnecessary abstractions, native library capabilities, and single-click execution."*

### 1:00 - 2:30 | Single-Click Execution
> *"Let's look at how easy it is to run this project. As a reviewer, you don't need to configure environment variables or cloud API keys. You simply open your terminal and run `python run.py`. Watch as `run.py` automatically verifies Python 3.10+, checks dependencies, prepares the ChromaDB directory, executes our 10-case Pytest suite—which passes 100%—and launches the application on port 8000."*

### 2:30 - 4:30 | Web GUI & Multi-Hop Reasoning
> *"Now let's open `http://localhost:8000/`. Here is our interactive, glassmorphic dashboard. Let's test the core requirement: Multi-Hop Reasoning. We select the prompt: 'Why did refunds increase in March?' and click Execute. Instantly, our 3-hop engine queries ChromaDB, discovering: 1) High refund volumes for Earbuds Pro and POS Terminals in Hop 1, 2) 45 customer support tickets for water ingress in Hop 2, and 3) The physical root cause in Hop 3—a forklift operator damaging humidity seals during a March storm at Warehouse North, alongside a conveyor jam at Warehouse South. Notice the synthesized answer, 95% confidence badge, and exact source citations."*

### 4:30 - 5:30 | Semantic Search & Metadata Filtering
> *"Next, let's switch to the Semantic Search tab. Here we can perform dense vector similarity searches combined with native ChromaDB metadata filtering. For example, if we filter specifically for document type `refund`, ChromaDB executes the `where={"doc_type": "refund"}` clause natively at the database index level."*

### 5:30 - 6:30 | Edge Cases & Security
> *"Our project handles all required assignment edge cases: 1) Duplicate records like `wh_01_dup` are automatically deduplicated during ingestion, 2) Missing fields in support tickets are handled safely without breaking Pydantic schemas, and 3) Outdated refund policy versions like `Policy v1.0 (Deprecated)` are flagged in evidence cards. Furthermore, all protected endpoints enforce strict `X-API-KEY` security dependencies."*

### 6:30 - 8:00 | Docker & Conclusion
> *"Finally, the application is fully dockerized with a single-stage `Dockerfile` and achieves 100% test coverage across all endpoints. Thank you for reviewing the NovaCart Enterprise AI Assistant!"*
