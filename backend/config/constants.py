# Document processing settings
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# File paths
import os
# Check if running from backend directory and adjust paths accordingly
if os.path.exists("../data/knowledge_base"):
    PDF_DIR = "../data/knowledge_base"
    VECTOR_DB_DIR = "../data/vector_db" 
    LOGS_DIR = "../data/logs"
else:
    PDF_DIR = "data/knowledge_base"
    VECTOR_DB_DIR = "data/vector_db"
    LOGS_DIR = "data/logs"

# Embedding settings
EMBEDDING_MODEL = "text-embedding-3-small"

# Vector store settings
COLLECTION_NAME = "member_support_docs" 