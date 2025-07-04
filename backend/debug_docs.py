#!/usr/bin/env python3
"""
Debug script to test document processing
"""

from document_pipeline import DocumentPipeline
from config.constants import PDF_DIR, VECTOR_DB_DIR
import os

def main():
    print("=== Document Pipeline Debug ===")
    
    # Check file paths
    print(f"PDF_DIR: {PDF_DIR}")
    print(f"VECTOR_DB_DIR: {VECTOR_DB_DIR}")
    print(f"PDF_DIR exists: {os.path.exists(PDF_DIR)}")
    print(f"VECTOR_DB_DIR exists: {os.path.exists(VECTOR_DB_DIR)}")
    
    # Check PDF files
    if os.path.exists(PDF_DIR):
        pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]
        print(f"PDF files found: {pdf_files}")
    else:
        print("PDF directory not found!")
        return
    
    # Initialize pipeline
    pipeline = DocumentPipeline()
    
    # Test processing
    print("\n=== Processing Documents ===")
    try:
        vectorstore = pipeline.process_documents()
        if vectorstore:
            print(f"✅ Documents processed successfully!")
            print(f"Document count: {vectorstore._collection.count()}")
            
            # Test retrieval
            print("\n=== Testing Retrieval ===")
            retriever = pipeline.get_retriever()
            test_results = retriever.invoke("account opening requirements")
            print(f"Test search results: {len(test_results)} documents found")
            for i, doc in enumerate(test_results):
                print(f"Doc {i+1}: {doc.page_content[:100]}...")
        else:
            print("❌ Document processing failed!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 