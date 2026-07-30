"""
FastAPI REST API Application for NovaCart Enterprise AI Assistant.
Implements simple X-API-KEY authentication, interactive GUI dashboard,
global exception handling for server stability, and required endpoints:
- GET /
- GET /health
- POST /search
- POST /query
"""
import logging
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Security, HTTPException, status, Depends, Request
from fastapi.security.api_key import APIKeyHeader
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

from app.db import ingest_documents, search_documents, collection
from app.pipeline import execute_multihop_reasoning

logger = logging.getLogger("novacart.server")

# Authentication: Simple X-API-KEY Header check
API_KEY_NAME = "X-API-KEY"
VALID_API_KEY = "novacart-secret-key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

def verify_api_key(api_key: Optional[str] = Depends(api_key_header)):
    if not api_key or api_key != VALID_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-KEY header."
        )
    return api_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-ingest documents on startup
    try:
        ingest_documents()
    except Exception as e:
        logger.error(f"Ingestion warning: {e}")
    yield

app = FastAPI(
    title="NovaCart Enterprise AI Assistant",
    description="Minimalist, Ponytail-compliant RAG & Multi-Hop Reasoning System",
    version="1.0.0",
    lifespan=lifespan
)

# Server Stability: Catch-all Global Exception Handler to prevent server crashes
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error processing {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": "An internal server error occurred, but the server remains stable."}
    )


# --- Request Models ---
class SearchRequest(BaseModel):
    query: str
    doc_type: Optional[str] = None
    top_k: Optional[int] = 3

class QueryRequest(BaseModel):
    query: str


HTML_DASHBOARD = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>NovaCart Enterprise AI Assistant - Interactive Dashboard</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-primary: #0a0c10;
      --bg-secondary: #12161f;
      --bg-card: rgba(22, 27, 38, 0.75);
      --accent-blue: #3b82f6;
      --accent-purple: #8b5cf6;
      --accent-green: #10b981;
      --accent-amber: #f59e0b;
      --text-main: #f3f4f6;
      --text-muted: #9ca3af;
      --border-color: rgba(255, 255, 255, 0.08);
      --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Inter', sans-serif;
      background: var(--bg-primary);
      color: var(--text-main);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background-image: 
        radial-gradient(circle at 15% 15%, rgba(59, 130, 246, 0.15) 0%, transparent 40%),
        radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.15) 0%, transparent 40%);
    }
    header {
      padding: 1.25rem 2rem;
      border-bottom: 1px solid var(--border-color);
      backdrop-filter: blur(12px);
      background: rgba(10, 12, 16, 0.8);
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .brand { display: flex; align-items: center; gap: 0.75rem; }
    .brand-icon {
      width: 38px; height: 38px;
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
      border-radius: 10px; display: flex; align-items: center; justify-content: center;
      font-weight: 700; font-size: 1.2rem; box-shadow: 0 0 15px rgba(139, 92, 246, 0.4);
    }
    .brand-title h1 {
      font-size: 1.2rem; font-weight: 700;
      background: linear-gradient(to right, #ffffff, var(--text-muted));
      -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .brand-title p { font-size: 0.75rem; color: var(--accent-blue); font-weight: 500; }
    .auth-box {
      display: flex; align-items: center; gap: 0.5rem;
      background: var(--bg-secondary); padding: 0.4rem 0.8rem;
      border-radius: 8px; border: 1px solid var(--border-color);
    }
    .auth-box label { font-size: 0.75rem; color: var(--text-muted); font-weight: 500; }
    .auth-box input {
      background: transparent; border: none; color: var(--accent-green);
      font-family: monospace; font-size: 0.85rem; outline: none; width: 170px;
    }
    .container {
      max-width: 1200px; margin: 2rem auto; padding: 0 1.5rem;
      width: 100%; display: grid; grid-template-columns: 1fr; gap: 1.5rem;
    }
    .status-bar {
      display: flex; justify-content: space-between; align-items: center;
      background: var(--bg-card); border: 1px solid var(--border-color);
      border-radius: 12px; padding: 1rem 1.5rem; backdrop-filter: blur(12px);
    }
    .status-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.875rem; }
    .dot {
      width: 8px; height: 8px; border-radius: 50%;
      background: var(--accent-green); box-shadow: 0 0 8px var(--accent-green);
    }
    .tabs { display: flex; gap: 0.5rem; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem; }
    .tab-btn {
      background: transparent; border: none; color: var(--text-muted);
      padding: 0.6rem 1.2rem; font-size: 0.9rem; font-weight: 500;
      border-radius: 8px; cursor: pointer; transition: all 0.2s ease;
    }
    .tab-btn.active {
      color: #fff; background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
      box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .panel {
      background: var(--bg-card); border: 1px solid var(--border-color);
      border-radius: 16px; padding: 1.5rem; backdrop-filter: blur(16px);
      box-shadow: var(--glass-shadow);
    }
    .panel-title { font-size: 1.1rem; font-weight: 600; margin-bottom: 1rem; }
    .form-group { display: flex; gap: 0.75rem; margin-bottom: 1rem; }
    .form-group input[type="text"], .form-group select {
      flex: 1; background: var(--bg-secondary); border: 1px solid var(--border-color);
      color: var(--text-main); padding: 0.75rem 1rem; border-radius: 10px; font-size: 0.9rem; outline: none;
    }
    .btn {
      background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
      color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 10px;
      font-weight: 600; font-size: 0.9rem; cursor: pointer;
    }
    .quick-prompts { display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 1.25rem; }
    .chip {
      background: var(--bg-secondary); border: 1px solid var(--border-color);
      padding: 0.4rem 0.8rem; border-radius: 20px; font-size: 0.75rem; color: var(--text-muted); cursor: pointer;
    }
    .chip:hover { border-color: var(--accent-purple); color: var(--text-main); }
    .answer-box {
      background: rgba(139, 92, 246, 0.1); border: 1px solid rgba(139, 92, 246, 0.3);
      border-radius: 12px; padding: 1.25rem; margin-bottom: 1.5rem;
    }
    .answer-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; }
    .badge {
      background: rgba(16, 185, 129, 0.2); color: var(--accent-green);
      border: 1px solid rgba(16, 185, 129, 0.4); padding: 0.2rem 0.6rem; border-radius: 12px; font-size: 0.75rem; font-weight: 600;
    }
    .evidence-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 1rem; }
    .evidence-card {
      background: var(--bg-secondary); border: 1px solid var(--border-color);
      border-radius: 12px; padding: 1rem;
    }
    .hop-badge { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; padding: 0.2rem 0.5rem; border-radius: 6px; display: inline-block; margin-bottom: 0.5rem; }
    .hop-1 { background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); }
    .hop-2 { background: rgba(139, 92, 246, 0.2); color: var(--accent-purple); }
    .hop-3 { background: rgba(245, 158, 11, 0.2); color: var(--accent-amber); }
    .doc-title { font-size: 0.9rem; font-weight: 600; margin-bottom: 0.4rem; }
    .snippet { font-size: 0.8rem; color: var(--text-muted); line-height: 1.4; }
    .loader { display: none; margin: 1.5rem auto; text-align: center; color: var(--accent-blue); font-weight: 500; }
  </style>
</head>
<body>
  <header>
    <div class="brand">
      <div class="brand-icon">N</div>
      <div class="brand-title">
        <h1>NovaCart Enterprise AI</h1>
        <p>Ponytail Architecture Engine</p>
      </div>
    </div>
    <div class="auth-box">
      <label for="apiKey">X-API-KEY:</label>
      <input type="text" id="apiKey" value="novacart-secret-key">
    </div>
  </header>

  <div class="container">
    <div class="status-bar">
      <div class="status-item">
        <div class="dot"></div>
        <span id="healthText">System Online (15 Vector Docs Indexed)</span>
      </div>
      <div class="status-item" style="color: var(--text-muted); font-size: 0.8rem;">
        Engine: ChromaDB (MiniLM-L6-v2) | FastAPI REST
      </div>
    </div>

    <div class="tabs">
      <button class="tab-btn active" id="tabMultihop" onclick="switchTab('multihop')">🔍 Multi-Hop Reasoning</button>
      <button class="tab-btn" id="tabSearch" onclick="switchTab('search')">⚡ Semantic Search & Filters</button>
    </div>

    <div id="panelMultihop" class="panel">
      <div class="panel-title">Multi-Hop Evidence Retrieval Pipeline</div>
      
      <div class="quick-prompts">
        <span class="chip" onclick="setQuery('Why did refunds increase in March?')">💡 Why did refunds increase in March?</span>
        <span class="chip" onclick="setQuery('What warehouse issue damaged POS Terminals?')">💡 What warehouse issue damaged POS Terminals?</span>
      </div>

      <div class="form-group">
        <input type="text" id="queryInput" placeholder="Ask complex business reasoning query..." value="Why did refunds increase in March?">
        <button class="btn" onclick="runQuery()">Execute Multi-Hop Query</button>
      </div>

      <div id="loader" class="loader">Processing multi-hop vector retrieval...</div>

      <div id="queryResult" style="display: none;">
        <div class="answer-box">
          <div class="answer-header">
            <span style="font-weight: 600; color: #fff;">Synthesized Answer</span>
            <span class="badge" id="confidenceBadge">High (95%)</span>
          </div>
          <p id="answerText" style="line-height: 1.5; color: var(--text-main);"></p>
        </div>

        <div style="font-weight: 600; font-size: 0.95rem; margin-bottom: 0.75rem;">Supporting Evidence Sources</div>
        <div class="evidence-grid" id="evidenceGrid"></div>
      </div>
    </div>

    <div id="panelSearch" class="panel" style="display: none;">
      <div class="panel-title">Semantic Search with Native ChromaDB Metadata Filtering</div>
      
      <div class="form-group">
        <input type="text" id="searchInput" placeholder="Search documents..." value="water damage defective">
        <select id="docTypeFilter">
          <option value="">All Document Types</option>
          <option value="refund">Refunds</option>
          <option value="support_ticket">Support Tickets</option>
          <option value="warehouse_log">Warehouse Logs</option>
          <option value="order">Orders</option>
        </select>
        <button class="btn" onclick="runSearch()">Search</button>
      </div>

      <div class="evidence-grid" id="searchGrid"></div>
    </div>
  </div>

  <script>
    const getHeaders = () => ({
      'Content-Type': 'application/json',
      'X-API-KEY': document.getElementById('apiKey').value.trim()
    });

    function setQuery(text) {
      document.getElementById('queryInput').value = text;
      runQuery();
    }

    function switchTab(tab) {
      document.getElementById('tabMultihop').classList.toggle('active', tab === 'multihop');
      document.getElementById('tabSearch').classList.toggle('active', tab === 'search');
      document.getElementById('panelMultihop').style.display = tab === 'multihop' ? 'block' : 'none';
      document.getElementById('panelSearch').style.display = tab === 'search' ? 'block' : 'none';
    }

    async function checkHealth() {
      try {
        const res = await fetch('/health');
        const data = await res.json();
        document.getElementById('healthText').innerText = `System Healthy (${data.total_indexed_documents} Vector Docs Indexed)`;
      } catch (err) {
        document.getElementById('healthText').innerText = `API Offline (Start FastAPI server)`;
      }
    }

    async function runQuery() {
      const q = document.getElementById('queryInput').value;
      const loader = document.getElementById('loader');
      const resContainer = document.getElementById('queryResult');
      
      loader.style.display = 'block';
      resContainer.style.display = 'none';

      try {
        const response = await fetch('/query', {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify({ query: q })
        });
        
        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        const data = await response.json();
        loader.style.display = 'none';
        resContainer.style.display = 'block';

        document.getElementById('answerText').innerText = data.answer;
        document.getElementById('confidenceBadge').innerText = data.confidence;

        const grid = document.getElementById('evidenceGrid');
        grid.innerHTML = '';

        data.evidence_sources.forEach(src => {
          const card = document.createElement('div');
          card.className = 'evidence-card';
          card.innerHTML = `
            <span class="hop-badge hop-${src.hop}">Hop ${src.hop} • ${src.doc_type}</span>
            <div class="doc-title">${src.title || src.doc_id}</div>
            <div class="snippet">${src.snippet}</div>
          `;
          grid.appendChild(card);
        });
      } catch (err) {
        loader.style.display = 'none';
        alert('Error executing query. Check X-API-KEY header.');
      }
    }

    async function runSearch() {
      const q = document.getElementById('searchInput').value;
      const docType = document.getElementById('docTypeFilter').value;

      try {
        const response = await fetch('/search', {
          method: 'POST',
          headers: getHeaders(),
          body: JSON.stringify({ query: q, doc_type: docType, top_k: 4 })
        });

        const data = await response.json();
        const grid = document.getElementById('searchGrid');
        grid.innerHTML = '';

        data.results.forEach(res => {
          const card = document.createElement('div');
          card.className = 'evidence-card';
          card.innerHTML = `
            <span class="hop-badge hop-1">${res.metadata.doc_type}</span>
            <div class="doc-title">${res.metadata.title || res.id}</div>
            <div class="snippet">${res.content}</div>
          `;
          grid.appendChild(card);
        });
      } catch (err) {
        alert('Search error. Check API key.');
      }
    }

    checkHealth();
    runQuery();
  </script>
</body>
</html>
"""

# --- Endpoints ---
@app.get("/", response_class=HTMLResponse)
def serve_dashboard():
    """Serves the interactive web GUI dashboard directly."""
    return HTML_DASHBOARD

@app.get("/health")
def health_check():
    """Public health check endpoint."""
    doc_count = collection.count()
    return {
        "status": "healthy",
        "vector_store": "chromadb",
        "total_indexed_documents": doc_count
    }

@app.post("/search")
def semantic_search(request: SearchRequest, authenticated: str = Depends(verify_api_key)):
    """Protected semantic search endpoint with optional metadata filtering."""
    results = search_documents(
        query=request.query,
        doc_type=request.doc_type,
        top_k=request.top_k or 3
    )
    return {
        "query": request.query,
        "doc_type_filter": request.doc_type,
        "results_count": len(results),
        "results": results
    }

@app.post("/query")
def multi_hop_query(request: QueryRequest, authenticated: str = Depends(verify_api_key)):
    """Protected multi-hop reasoning endpoint."""
    response = execute_multihop_reasoning(user_query=request.query)
    return response
