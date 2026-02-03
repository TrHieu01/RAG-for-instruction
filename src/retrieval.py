
from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_classic.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

from src.vector_db import initialize_vector_store
from src.config import TOP_K_RETRIEVAL, TOP_K_RERANK

from qdrant_client.http import models

def get_hybrid_retriever(vector_store, all_docs=None, user_id=None):
    # Base params
    search_kwargs = {
        "k": TOP_K_RETRIEVAL,
        "fetch_k": 20, 
        "lambda_mult": 0.5
    }
    
    # Advanced Filtering: User Docs OR Global Docs
    if user_id:
        filter_condition = models.Filter(
            should=[
                models.FieldCondition(
                    key="metadata.user_id", 
                    match=models.MatchValue(value=user_id)
                ),
                models.FieldCondition(
                    key="metadata.user_id", 
                    match=models.MatchValue(value="GLOBAL")
                ),
                # Fallback for old documents without user_id (treat as global if intended, or just include to be safe)
                models.FieldCondition(
                    key="metadata.user_id", 
                    match=models.MatchValue(value="default")
                )
            ]
        )
        search_kwargs["filter"] = filter_condition
        
    return vector_store.as_retriever(
        search_type="mmr", 
        search_kwargs=search_kwargs
    )

def get_advanced_retriever_chain(all_docs=None, user_id=None):
    vector_store = initialize_vector_store()
    
    base_retriever = get_hybrid_retriever(vector_store, all_docs, user_id=user_id)
    
    # 3. Reranker
    # Using BGE-Reranker-v2-M3
    model_name = "BAAI/bge-reranker-v2-m3"
    try:
        model = HuggingFaceCrossEncoder(model_name=model_name)
        compressor = CrossEncoderReranker(model=model, top_n=TOP_K_RERANK)
        
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor,
            base_retriever=base_retriever
        )
        return compression_retriever
    except Exception as e:
        print(f"Reranker initialization failed: {e}. Returning base retriever.")
        return base_retriever
