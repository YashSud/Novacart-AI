# NovaCart Enterprise AI Assistant

> **Horrazon AI Engineering Challenge** — Single-click runnable RAG and multi-hop reasoning system built strictly following the **Ponytail Philosophy** (YAGNI, maximum simplicity, native library capabilities, minimal files, zero over-engineering).

---

## ⚡ Quick Start (Single-Click Execution)

1. Clone or extract repository:
   ```powershell
   git clone https://github.com/DietrichGebert/ponytail.git
   cd novacart-ai
   ```

2. Run single-click execution:
   ```powershell
   python run.py
   ```

3. Open in your browser:
   - **Dashboard**: [http://localhost:8000/](http://localhost:8000/)
   - **API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

That's it. Zero manual configuration, zero cloud keys, zero environment setup required.

---

## 🎯 Key Features

- **Single-Click Setup (`run.py`)**: Automatically checks Python version, installs dependencies from `requirements.txt`, runs `pytest`, ingests data, indexes vector embeddings, and starts FastAPI.
- **16 Synthetic Documents** covering 4 business entity types and edge cases (1 duplicate record, 1 missing field, 1 outdated policy).
- **Local Neural Vector Search**: Built with ChromaDB and `all-MiniLM-L6-v2` dense embeddings.
- **Native Metadata Filtering**: Query-level filtering (`where={"doc_type": ...}`).
- **3-Hop Multi-Reasoning Pipeline**: Cross-references root cause events (*Refunds* $\rightarrow$ *Support Tickets* $\rightarrow$ *Warehouse Logs*).
- **FastAPI & X-API-KEY Auth**: Secured REST endpoints (`/health`, `/search`, `/query`).
- **Interactive Web Dashboard**: Glassmorphic HTML/CSS/JS frontend served directly at `http://localhost:8000/`.
- **Docker Support**: Built for `docker build -t novacart-ai .` and `docker run -p 8000:8000 novacart-ai`.

---

## 📁 Project Structure

```text
novacart-ai/
├── run.py                 # Single-click runnable entrypoint script
├── app/
│   ├── __init__.py        # Package initialization
│   ├── data.py            # 16 synthetic business documents + edge cases
│   ├── db.py              # ChromaDB vector store, deduplication, & search
│   ├── pipeline.py        # 3-hop multi-reasoning engine
│   └── main.py            # FastAPI REST endpoints, web GUI, & X-API-KEY auth
├── tests/
│   └── test_api.py        # Pytest test suite (10/10 test cases passed)
├── Dockerfile             # Container configuration
├── requirements.txt       # Project dependencies
└── README.md              # Documentation & interview defense guide
```

---

## 🐳 Docker Execution

```powershell
docker build -t novacart-ai .
docker run -p 8000:8000 novacart-ai
```

---

## 🔒 API Usage

Header: `X-API-KEY: novacart-secret-key`

```powershell
# Multi-Hop Reasoning Query
Invoke-RestMethod -Uri "http://localhost:8000/query" `
  -Method Post `
  -Headers @{"X-API-KEY"="novacart-secret-key"} `
  -ContentType "application/json" `
  -Body '{"query": "Why did refunds increase in March?"}'
```
"# Novacart-AI" 
