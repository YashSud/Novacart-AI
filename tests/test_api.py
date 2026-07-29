"""
Comprehensive Test Suite for NovaCart Enterprise AI Assistant.
Validates:
1. Health & Dashboard endpoints
2. Authentication (Valid vs Invalid key, missing key)
3. Semantic Search & Native Metadata Filtering
4. Multi-Hop Reasoning Pipeline & Evidence Synthesis
5. Edge Cases: Duplicate records, missing fields, outdated policy, empty queries, invalid payloads
"""
import warnings
import pytest
from fastapi.testclient import TestClient

warnings.filterwarnings("ignore", category=DeprecationWarning)

from app.main import app, VALID_API_KEY
from app.db import ingest_documents, collection

client = TestClient(app)
AUTH_HEADERS = {"X-API-KEY": VALID_API_KEY}

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    ingest_documents()

def test_dashboard_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["total_indexed_documents"] >= 15

def test_authentication_enforcement():
    # Missing API Key
    res1 = client.post("/search", json={"query": "test"})
    assert res1.status_code == 401
    
    # Invalid API Key
    res2 = client.post("/search", json={"query": "test"}, headers={"X-API-KEY": "invalid-key-123"})
    assert res2.status_code == 401

def test_semantic_search_with_metadata_filter():
    payload = {
        "query": "refund policy",
        "doc_type": "refund",
        "top_k": 2
    }
    response = client.post("/search", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["results_count"] > 0
    for result in data["results"]:
        assert result["metadata"]["doc_type"] == "refund"

def test_multihop_reasoning_pipeline():
    payload = {
        "query": "Why did refunds increase in March?"
    }
    response = client.post("/query", json=payload, headers=AUTH_HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert "confidence" in data
    assert len(data["evidence_sources"]) >= 3
    
    # Verify sources across multiple hops
    doc_types = [e["doc_type"] for e in data["evidence_sources"]]
    assert "refund" in doc_types
    assert "support_ticket" in doc_types or "warehouse_log" in doc_types

def test_edge_case_deduplication():
    # Verify wh_01_dup was deduplicated during ingestion
    res = client.post("/search", json={"query": "forklift damaged humidity seal"}, headers=AUTH_HEADERS)
    assert res.status_code == 200
    ids = [item["id"] for item in res.json()["results"]]
    assert "wh_01" in ids
    assert "wh_01_dup" not in ids

def test_edge_case_missing_fields_handling():
    # Verify ticket sup_04 (resolution_time=None) was handled safely
    res = client.post("/search", json={"query": "power cable missing"}, headers=AUTH_HEADERS)
    assert res.status_code == 200
    results = res.json()["results"]
    assert len(results) > 0
    assert results[0]["id"] == "sup_04"

def test_edge_case_outdated_policy_detection():
    # Verify ref_03 returns policy_version 'v1.0 (Deprecated)'
    res = client.post("/search", json={"query": "Customer changed mind after 45 days"}, headers=AUTH_HEADERS)
    assert res.status_code == 200
    results = res.json()["results"]
    assert len(results) > 0
    assert "v1.0 (Deprecated)" in results[0]["metadata"]["policy_version"]

def test_empty_query_handling():
    res = client.post("/search", json={"query": ""}, headers=AUTH_HEADERS)
    assert res.status_code == 200
    assert "results" in res.json()

def test_invalid_payload_validation():
    # Missing required field 'query'
    res = client.post("/search", json={"top_k": 3}, headers=AUTH_HEADERS)
    assert res.status_code == 422
