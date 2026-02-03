
import os
import time
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from docling.document_converter import DocumentConverter
from src.vector_db import get_embedding_model, initialize_vector_store
from src.utils import setup_logger
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

logger = setup_logger(__name__)

# Batch size for adding documents to vector store
BATCH_SIZE = 50

def load_docling_markdown(file_path: str, original_filename: str = None) -> Document:
    """Convert document to markdown using Docling"""
    start_time = time.time()
    logger.info(f"📄 Converting {file_path} using Docling...")
    
    converter = DocumentConverter()
    result = converter.convert(file_path)
    markdown_content = result.document.export_to_markdown()
    
    elapsed = time.time() - start_time
    logger.info(f"✅ Docling conversion completed in {elapsed:.1f}s ({len(markdown_content):,} characters)")
    
    source_name = original_filename if original_filename else os.path.basename(file_path)
    metadata = {"source": source_name}
    return Document(page_content=markdown_content, metadata=metadata)

def process_document(file_path: str, user_id: str = "default", original_filename: str = None) -> List[Document]:
    """Process document with optimized chunking pipeline"""
    total_start = time.time()
    
    # 1. Load with Docling
    doc = load_docling_markdown(file_path, original_filename)
    
    # 2. Structural Split using Markdown Headers
    start_time = time.time()
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"), 
        ("###", "Header 3"),
        ("####", "Header 4"),
    ]
    header_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    header_chunks = header_splitter.split_text(doc.page_content)
    logger.info(f"📑 Header split: {len(header_chunks)} sections in {time.time() - start_time:.1f}s")
    
    # 3. OPTIMIZED: Use RecursiveCharacterTextSplitter instead of SemanticChunker
    # This is 10-20x faster while still maintaining good quality
    start_time = time.time()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
        separators=["\n\n", "\n", ". ", "! ", "? ", ", ", " ", ""],
        is_separator_regex=False,
    )
    
    final_chunks = []
    source_name = original_filename if original_filename else os.path.basename(file_path)
    
    for i, h_chunk in enumerate(header_chunks):
        # Build Context from Metadata (Header Path)
        header_context_list = []
        for key in ["Header 1", "Header 2", "Header 3", "Header 4"]:
            if key in h_chunk.metadata:
                header_context_list.append(h_chunk.metadata[key])
        
        header_context = " > ".join(header_context_list) if header_context_list else "General"
        
        # Fast text splitting
        sub_chunks = text_splitter.split_text(h_chunk.page_content)
        
        for j, sub_content in enumerate(sub_chunks):
            # Skip very short chunks
            if len(sub_content.strip()) < 50:
                continue
                
            # Contextual Enrichment
            enriched_content = f"[Context: {source_name} > {header_context}]\n\n{sub_content}"
            
            new_metadata = h_chunk.metadata.copy()
            new_metadata["source"] = source_name
            new_metadata["chunk_id"] = f"{i}_{j}"
            new_metadata["user_id"] = user_id
            
            new_doc = Document(
                page_content=enriched_content,
                metadata=new_metadata
            )
            final_chunks.append(new_doc)
        
        # Progress logging every 100 sections
        if (i + 1) % 100 == 0:
            logger.info(f"   Processed {i + 1}/{len(header_chunks)} sections...")
    
    elapsed = time.time() - start_time
    logger.info(f"✂️ Text chunking: {len(final_chunks)} chunks in {elapsed:.1f}s")
    
    total_elapsed = time.time() - total_start
    logger.info(f"📊 Document processing completed in {total_elapsed:.1f}s total")
    
    return final_chunks

def ingest_file(file_path: str, user_id: str = "default", original_filename: str = None):
    """Ingest file with batch processing for better performance"""
    logger.info(f"🚀 Starting ingestion for: {file_path} (User: {user_id})")
    total_start = time.time()
    
    # Process document
    chunks = process_document(file_path, user_id, original_filename)
    
    if not chunks:
        logger.warning("⚠️ No chunks to ingest.")
        return
    
    # Initialize vector store
    start_time = time.time()
    vector_store = initialize_vector_store()
    logger.info(f"🗄️ Vector store initialized in {time.time() - start_time:.1f}s")
    
    # Batch insert for better performance
    start_time = time.time()
    total_batches = (len(chunks) + BATCH_SIZE - 1) // BATCH_SIZE
    
    for i in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        
        vector_store.add_documents(batch)
        logger.info(f"   Batch {batch_num}/{total_batches}: Added {len(batch)} chunks")
    
    elapsed = time.time() - start_time
    total_elapsed = time.time() - total_start
    
    logger.info(f"💾 Vector store insertion: {elapsed:.1f}s")
    logger.info(f"✅ INGESTION COMPLETE: {len(chunks)} chunks in {total_elapsed:.1f}s total")
    
    return len(chunks)
if __name__ == "__main__":
    # Test ingestion
    pass
