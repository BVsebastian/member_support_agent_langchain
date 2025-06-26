# 📐 Architecture Document: Member Support Agent (LangChain Edition)

---

## 📁 File & Folder Structure

```
member_support_agent/
├── frontend/                        # React frontend
├── backend/                         # FastAPI + LangChain
│   ├── main.py
│   ├── chat_chain.py
│   ├── document_pipeline.py
│   ├── tools.py
│   ├── pushover_alerts.py
│   ├── prompt_manager.py
│   ├── state.py
│   └── config/
├── tests/                           # Test files
│   ├── test_document_pipeline.py
│   ├── test_chat_chain.py
│   └── test_main.py
├── data/
│   ├── knowledge_base/
│   ├── logs/
│   └── vector_db/
├── .env
├── pyproject.toml                   # UV dependency management
└── README.md
```

---

## ⚙️ Module Responsibilities

| File                              | Description                                                                                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main.py`                         | FastAPI app with `/chat` endpoint that handles POST requests from React frontend                                                                      |
| `chat_chain.py`                   | Builds LangChain's `ConversationalRetrievalChain` using memory + retriever                                                                            |
| `document_pipeline.py`            | Loads all PDFs via `PyMuPDFLoader`, chunks them with `CharacterTextSplitter`, creates embeddings with `OpenAIEmbeddings`, and stores them in `Chroma` |
| `state.py`                        | Stores session metadata: `chat_history`, user flags, etc.                                                                                             |
| `prompt_manager.py`               | Loads system prompt (Alexa's tone, tool usage rules)                                                                                                  |
| `pushover_alerts.py`              | Sends alerts for unresolved or unknown queries                                                                                                        |
| `tools.py`                        | JSON-defined tool functions + central `handle_tool_call()` dispatcher                                                                                 |
| `config/constants.py`             | Configuration for chunk size, retriever behavior                                                                                                      |
| `config/secrets.env`              | Secret keys like `OPENAI_API_KEY`, `PUSHOVER_TOKEN`                                                                                                   |
| `tests/test_document_pipeline.py` | Tests document loading, chunking, and vectorstore creation                                                                                            |
| `tests/test_chat_chain.py`        | Tests LangChain conversation chain and retrieval                                                                                                      |
| `tests/test_main.py`              | Tests FastAPI endpoints and integration                                                                                                               |

## 📄 DocumentPipeline Methods

| Method                 | Purpose                                   | Input          | Output                   |
| ---------------------- | ----------------------------------------- | -------------- | ------------------------ |
| `load_documents()`     | Read PDFs from knowledge base             | Directory path | List of Document objects |
| `chunk_documents()`    | Split large documents into smaller chunks | Documents      | Smaller Document objects |
| `create_vectorstore()` | Create and populate vector database       | Documents      | ChromaDB instance        |
| `process_documents()`  | Complete pipeline: load → chunk → store   | Nothing        | ChromaDB instance        |

### ✅ DocumentPipeline Implementation Status

- **PDF Loading**: ✅ Uses `PyMuPDFLoader` to load PDFs from `data/knowledge_base/`
- **Document Chunking**: ✅ Uses `CharacterTextSplitter` with configurable chunk size/overlap
- **Vector Storage**: ✅ Uses `OpenAIEmbeddings` and stores in `data/vector_db/`
- **Testing**: ✅ Complete test suite in `tests/test_document_pipeline.py`
- **Dependencies**: ✅ All LangChain packages properly configured with compatible versions

---

## 🔌 How Services Connect

```mermaid
graph LR
  subgraph Frontend
    R1[React App] -->|POST /chat| A1[Axios Call]
  end

  subgraph Backend
    A1 --> B1[FastAPI /chat]
    B1 --> B2[LangChain Chat Chain]
    B2 --> B3[Retriever (Chroma)]
    B3 --> B4[Vector DB (ChromaDB)]
    B2 --> B5[Tool Router]
    B5 -->|Optional| B6[Pushover Alerts]
    B2 --> B7[Return Response]
  end

  subgraph Storage
    B4 --> D1[data/vector_db/]
    B5 --> D2[data/logs/]
  end
```

---

## 🧠 Where State Lives

| Component       | State                          | Persistence                  |
| --------------- | ------------------------------ | ---------------------------- |
| `state.py`      | Chat history, user flags       | In-memory (per session)      |
| `vector_db/`    | PDF embeddings                 | Persistent (ChromaDB folder) |
| `logs/`         | Unknown questions, escalations | File-based JSON              |
| React `App.jsx` | UI state, chat session         | Browser memory               |

```

```
