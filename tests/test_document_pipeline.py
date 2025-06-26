#!/usr/bin/env python3
"""
Test script for DocumentPipeline implementation
"""

import os
import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from document_pipeline import DocumentPipeline

def test_document_pipeline():
    """Test the complete document pipeline"""
    
    print("🧪 Testing DocumentPipeline...")
    
    # Initialize pipeline
    pipeline = DocumentPipeline()
    print(f"✅ Pipeline initialized with db_name: {pipeline.db_name}")
    
    # Test loading documents
    print("\n📄 Testing document loading...")
    documents = pipeline.load_documents()
    print(f"✅ Loaded {len(documents)} documents")
    
    if documents:
        print(f"   First document: {documents[0].metadata.get('source', 'Unknown')}")
        print(f"   First document length: {len(documents[0].page_content)} characters")
    
    # Test chunking
    print("\n✂️ Testing document chunking...")
    chunks = pipeline.chunk_documents(documents)
    print(f"✅ Created {len(chunks)} chunks")
    
    if chunks:
        print(f"   First chunk length: {len(chunks[0].page_content)} characters")
        print(f"   Chunk metadata: {chunks[0].metadata}")
    
    # Test vectorstore creation
    print("\n🗄️ Testing vectorstore creation...")
    vectorstore = pipeline.create_vectorstore(chunks)
    
    if vectorstore:
        print("✅ Vectorstore created successfully")
        print(f"   Collection count: {vectorstore._collection.count()}")
    else:
        print("❌ Failed to create vectorstore")
    
    # Test complete pipeline
    print("\n🔄 Testing complete pipeline...")
    pipeline.process_documents()
    
    if pipeline.vectorstore:
        print("✅ Complete pipeline successful")
        print(f"   Final collection count: {pipeline.vectorstore._collection.count()}")
    else:
        print("❌ Complete pipeline failed")
    
    print("\n🎉 Document pipeline test completed!")

if __name__ == "__main__":
    test_document_pipeline() 