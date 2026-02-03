
from langchain_qdrant import QdrantVectorStore
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from qdrant_client import QdrantClient
from qdrant_client.http import models
from src.config import EMBEDDING_MODEL_NAME, DEVICE, COLLECTION_NAME, DB_PATH

def get_embedding_model():
    model_kwargs = {"device": DEVICE}
    encode_kwargs = {"normalize_embeddings": True}
    return HuggingFaceBgeEmbeddings(
        model_name=EMBEDDING_MODEL_NAME,
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )

_client_instance = None

def get_qdrant_client():
    global _client_instance
    if _client_instance is None:
        # Persistent local storage
        _client_instance = QdrantClient(path=DB_PATH)
    return _client_instance

def initialize_vector_store(client=None):
    if client is None:
        client = get_qdrant_client()
    
    embeddings = get_embedding_model()
    
    # Ensure collection exists
    try:
        client.get_collection(COLLECTION_NAME)
    except Exception:
        # Create collection if not exists
        # BGE-M3 dimension is 1024
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=1024, distance=models.Distance.COSINE)
        )
    
    return QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )

def list_documents():
    """List unique source documents in the DB."""
    client = get_qdrant_client()
    try:
        # Scroll through points to get metadata
        # Note: This is inefficient for large datasets but fine for this scale
        scroll_result, _ = client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=None,
            limit=10000,
            with_payload=True,
            with_vectors=False
        )
        
        unique_sources = set()
        doc_info = {}
        
        for point in scroll_result:
            if point.payload and "source" in point.payload:
                source = point.payload["source"]
                user_id = point.payload.get("user_id", "unknown")
                if source not in unique_sources:
                    unique_sources.add(source)
                    doc_info[source] = {"user_id": user_id, "count": 1}
                else:
                    doc_info[source]["count"] += 1
                    
        return doc_info
    except Exception as e:
        print(f"Error listing docs: {e}")
        return {}

def delete_document(source_name: str):
    """Delete all chunks belonging to a specific source document."""
    client = get_qdrant_client()
    try:
        client.delete(
            collection_name=COLLECTION_NAME,
            points_selector=models.FilterSelector(
                filter=models.Filter(
                    must=[
                        models.FieldCondition(
                            key="metadata.source",
                            match=models.MatchValue(value=source_name)
                        )
                    ]
                )
            )
        )
        return True
    except Exception as e:
        print(f"Error deleting doc {source_name}: {e}")
        return False
