# Implementation Plan - NovaCart Enterprise AI Assistant (Minimalist / Ponytail)

This plan specifies the implementation details for building the **NovaCart Enterprise AI Assistant** codebase for the Horrazon AI Engineering Challenge. It strictly follows the **Ponytail philosophy** (YAGNI, maximum simplicity, native library capabilities, minimal files, no over-engineering).

---

## User Review Required

> [!IMPORTANT]
> The implementation strictly limits the codebase to the requested 5 source files + 1 test file + Dockerfile + requirements.txt + README.md. Unnecessary abstractions like complex LangGraph state machines, JWT auth, or multi-agent workflows are omitted in favor of a direct multi-hop retrieval function (`pipeline.py`).

---

## Proposed Changes & File Specs

### Core Application Files

#### `[NEW]` [requirements.txt](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/requirements.txt)
- Minimal list of exact dependencies: `fastapi`, `uvicorn`, `chromadb`, `sentence-transformers`, `pytest`, `httpx`.

#### `[NEW]` [app/data.py](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/app/data.py)
- Contains 16 synthetic business documents across 4 types: `order`, `refund`, `support_ticket`, `warehouse_log`.
- Includes required edge cases:
  1. **Duplicate record**: Two identical warehouse log entries (`wh_01` & `wh_01_dup`).
  2. **Missing field**: A support ticket without the optional `resolution_time` or `warehouse_id` field (`sup_04`).
  3. **Outdated policy**: A refund record referencing `Policy v1.0 (Deprecated)` vs `Policy v2.0`.

#### `[NEW]` [app/db.py](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/app/db.py)
- Encapsulates ChromaDB in-memory/ephemeral vector store initialization.
- Uses `SentenceTransformerEmbeddingFunction` with `all-MiniLM-L6-v2`.
- Deduplicates incoming documents during indexing.
- Implements semantic search and native metadata filtering (`where={"doc_type": ...}`).

#### `[NEW]` [app/pipeline.py](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/app/pipeline.py)
- Implements direct 3-stage multi-hop retrieval:
  1. Initial query search (Refunds).
  2. Cross-reference Hop: Lookup linked Support Tickets and Warehouse Logs by entity/date matching.
  3. Synthesis: Merges evidence into an answer with citations & confidence score.

#### `[NEW]` [app/main.py](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/app/main.py)
- FastAPI app with simple `X-API-KEY` security dependency (`APIKeyHeader(name="X-API-KEY")`).
- Defines 3 endpoints:
  - `GET /health`
  - `POST /search`
  - `POST /query`
- Automatic document indexing on startup via `@asynccontextmanager` lifecycle.

#### `[NEW]` [tests/test_api.py](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/tests/test_api.py)
- Pytest integration suite using FastAPI `TestClient`:
  1. `/health` check test.
  2. `X-API-KEY` authentication failure & success test.
  3. Metadata filtered semantic search test.
  4. Multi-hop reasoning query test.

#### `[NEW]` [Dockerfile](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/Dockerfile)
- Slim Python 3.12 Dockerfile running `uvicorn app.main:app --host 0.0.0.0 --port 8000`.

#### `[NEW]` [README.md](file:///c:/Users/Yash%20Sud/.gemini/antigravity-ide/brain/5edf5134-b417-4473-97bf-da0c5b2b1fd4/New%20Assesment/README.md)
- Project quickstart, architecture explanation, and interview-ready decision rationales.

---

## Verification Plan

### Automated Verification
- Run `pytest` to execute all API, search, auth, and multi-hop tests.
- Run `docker build -t novacart-ai .` to verify Docker container compilation.

### Manual Verification
- Test `/query` with sample question: *"Why did refunds increase in March?"* and check multi-hop evidence breakdown.
