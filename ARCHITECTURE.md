# NovaCart Enterprise AI Assistant — Architecture Specification

This document details the system architecture, component interactions, and data flow for the **NovaCart Enterprise AI Assistant** (Horrazon AI Engineering Challenge), designed strictly under the **Ponytail minimalist philosophy**.

---

## 🏗️ High-Level System Architecture

```mermaid
graph TD
    Client["Client / User / Web Browser"] -->|"HTTP GET / (GUI Dashboard)"| FastAPI["FastAPI Application (app/main.py)"]
    Client -->|"HTTP POST /query (X-API-KEY Auth)"| FastAPI
    Client -->|"HTTP POST /search (X-API-KEY Auth)"| FastAPI
    
    subgraph Core Engine
        FastAPI --> Auth["API Key Auth Verification"]
        Auth --> Pipeline["Multi-Hop Reasoning Engine (app/pipeline.py)"]
        
        Pipeline --> Hop1["Hop 1: Refund Anomaly Search"]
        Pipeline --> Hop2["Hop 2: Support Ticket Traversal"]
        Pipeline --> Hop3["Hop 3: Warehouse Root Cause Search"]
        
        Hop1 --> DB["ChromaDB Vector Store (app/db.py)"]
        Hop2 --> DB
        Hop3 --> DB
        
        DB --> Embeddings["SentenceTransformers (all-MiniLM-L6-v2)"]
    end
    
    subgraph Data Tier
        DB --> Data["16 Synthetic Records (app/data.py)"]
        Data --> Edge1["Duplicate Deduplication (wh_01_dup)"]
        Data --> Edge2["Missing Field Safe Defaults (sup_04)"]
        Data --> Edge3["Outdated Policy Versioning (ref_03)"]
    end
```

---

## 🔄 Component Sequence & Multi-Hop Data Flow

```text
 [ Client Query ] -> "Why did refunds increase in March?"
       │
       ▼
 [ FastAPI Gateway ] ── (Verify Header: X-API-KEY: novacart-secret-key)
       │
       ▼
 [ Multi-Hop Pipeline ]
       │
       ├─► Hop 1: Retrieve Refund Records (where={"doc_type": "refund"})
       │          └─► Discovers refunds for Earbuds Pro (ref_01) and POS Terminals (ref_02).
       │
       ├─► Hop 2: Retrieve Support Tickets (where={"doc_type": "support_ticket"})
       │          └─► Discovers 45 water ingress tickets (sup_01) and transit damage (sup_02).
       │
       └─► Hop 3: Retrieve Warehouse Logs (where={"doc_type": "warehouse_log"})
                  └─► Pinpoints Forklift Humidity Seal damage (wh_01) and Conveyor Jam (wh_02).
       │
       ▼
 [ Evidence Synthesis Engine ]
       │
       ▼
 [ Structured API Response ]
       ├─► Synthesized Answer string
       ├─► Confidence Score ("High (95%)")
       └─► 6 Verified Evidence Source Cards
```

---

## 📊 Technical Stack Specs

- **Web Framework**: FastAPI `0.110+` running on Uvicorn `0.28+`
- **Embedding Model**: `sentence-transformers/all-MiniLM-L6-v2` (384-dimensional dense vectors)
- **Vector DB**: ChromaDB `0.4.24+` with native HNSW Cosine Distance indexing (`hnsw:space: cosine`)
- **Authentication**: Native FastAPI Security Dependency (`X-API-KEY`)
- **Testing**: Pytest `8.0+` with FastAPI `TestClient`
- **Container**: Slim Python 3.12 Linux base image (`python:3.12-slim`)
