"""
ChromaDB Vector Database Management for NovaCart Enterprise AI Assistant.
Provides document ingestion, deduplication, semantic search, and native metadata filtering.
"""
import logging
import chromadb
from chromadb.utils import embedding_functions
from app.data import SYNTHETIC_DOCS

logger = logging.getLogger(__name__)

# Initialize ephemeral in-memory ChromaDB client
client = chromadb.Client()

# Use lightweight SentenceTransformer model for embeddings
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

# Get or create collection
collection = client.get_or_create_collection(
    name="novacart_docs",
    embedding_function=embedding_func,
    metadata={"hnsw:space": "cosine"}
)


def ingest_documents():
    """
    Ingests synthetic dataset into ChromaDB.
    Handles deduplication: Ignores documents with identical content or IDs already indexed.
    Converts missing fields (None) into string placeholders for metadata compatibility.
    """
    seen_ids = set()
    seen_contents = set()
    
    documents = []
    metadatas = []
    ids = []
    
    for doc in SYNTHETIC_DOCS:
        doc_id = doc["id"]
        content = doc["content"]
        
        # Edge Case Handling: Skip Duplicate Records
        if doc_id in seen_ids or content in seen_contents:
            logger.warning(f"Deduplicating & skipping duplicate document: {doc_id}")
            continue
            
        seen_ids.add(doc_id)
        seen_contents.add(content)
        
        # Format metadata (convert None fields to string 'N/A' for ChromaDB compatibility)
        metadata = {
            "doc_type": str(doc.get("doc_type", "unknown")),
            "title": str(doc.get("title", "")),
            "date": str(doc.get("date", "N/A")),
            "policy_version": str(doc.get("policy_version", "N/A")),
            "order_id": str(doc.get("order_id", "N/A")),
            "warehouse_location": str(doc.get("warehouse_location", "N/A"))
        }
        
        documents.append(content)
        metadatas.append(metadata)
        ids.append(doc_id)
        
    if ids:
        # Index in ChromaDB
        collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        logger.info(f"Successfully ingested {len(ids)} unique documents into ChromaDB.")
    return len(ids)


def search_documents(query: str, doc_type: str = None, top_k: int = 3):
    """
    Performs semantic search with optional native metadata filtering.
    """
    where_clause = {}
    if doc_type and doc_type.strip():
        where_clause = {"doc_type": doc_type.strip().lower()}
        
    query_params = {
        "query_texts": [query],
        "n_results": top_k
    }
    if where_clause:
        query_params["where"] = where_clause
        
    results = collection.query(**query_params)
    
    formatted_results = []
    if results and results["ids"] and results["ids"][0]:
        for i in range(len(results["ids"][0])):
            formatted_results.append({
                "id": results["ids"][0][i],
                "content": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": float(results["distances"][0][i]) if "distances" in results and results["distances"] else 0.0
            })
    return formatted_results
