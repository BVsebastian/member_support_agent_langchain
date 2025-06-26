import os
from dotenv import load_dotenv
from typing import List
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from config.constants import PDF_DIR
from config.constants import CHUNK_SIZE, CHUNK_OVERLAP
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

class DocumentPipeline:
    def __init__(self):
        # Initialize the document pipeline
        self.documents = []
        self.chunks = []
        self.embeddings = []
        self.db_name = "data/vector_db"
        self.vectorstore = None

    def load_documents(self, pdf_dir: str = PDF_DIR) -> List[Document]:
        # Clear existing documents before loading new ones
        self.documents = []
        
        # Check if the directory exists
        if not os.path.exists(pdf_dir):
            print(f"Error: Directory {pdf_dir} does not exist!")
            return []
        
        # Get all PDF files from the directory
        pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]

        # Check if there are any PDF files
        if not pdf_files:
            print(f"No PDF files found in {pdf_dir}")
            return []
        else:
            print(f"Found {len(pdf_files)} PDF files in {pdf_dir}")

        for pdf_file in pdf_files:
            try:
                # Load the PDF file
                pdf_path = os.path.join(pdf_dir, pdf_file)
                loader = PyMuPDFLoader(pdf_path)
                docs = loader.load()
                self.documents.extend(docs)
                print(f"Loaded {pdf_file}")
            except Exception as e:
                print(f"Error loading {pdf_file}: {e}")
                # Skip this file and continue with the next one

        return self.documents
    
    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        if not documents:
            print("No documents to chunk")
            return []
        
        print(f"Chunking {len(documents)} documents")

        # Chunk the documents into smaller chunks
        text_splitter = CharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
        )

        self.chunks = text_splitter.split_documents(documents)

        print(f"Created {len(self.chunks)} chunks")

        return self.chunks
    
    def create_vectorstore(self, chunks: List[Document]) -> Chroma:
        if not chunks:
            print("No chunks to create vectorstore")
            return None

        embeddings = OpenAIEmbeddings()
        db_name = self.db_name

        # Delete the collection if it already exists
        if os.path.exists(db_name):
            Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

        # Create Vectorstore
        self.vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=db_name)
        print(f"Vectorstore created with {self.vectorstore._collection.count()} documents")

        return self.vectorstore
    
    def process_documents(self) -> Chroma:
        """Complete pipeline: load → chunk → create vectorstore """
        documents = self.load_documents()
        if not documents:
            return None
        
        chunks = self.chunk_documents(documents)
        if not chunks:
            return None
        
        vectorstore = self.create_vectorstore(chunks)
        if not vectorstore:
            return None
        
        return vectorstore
