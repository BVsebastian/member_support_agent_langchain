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
│   ├── response_templates.py
│   ├── agent_identity.md
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
| `prompt_manager.py`               | Loads system prompt from `agent_identity.md`, creates knowledge-enhanced prompts with tool definitions and escalation guidelines                      |
| `response_templates.py`           | Provides standard response templates for welcome, escalation, and knowledge-not-found scenarios                                                       |
| `agent_identity.md`               | Markdown file defining Alexa's personality, communication style, guardrails, and response guidelines                                                  |
| `state.py`                        | Stores session metadata: `chat_history`, user flags, etc.                                                                                             |
| `pushover_alerts.py`              | Sends alerts for unresolved or unknown queries                                                                                                        |
| `tools.py`                        | JSON-defined tool functions + central `handle_tool_call()` dispatcher                                                                                 |
| `config/constants.py`             | Configuration for chunk size, retriever behavior                                                                                                      |
| `config/secrets.env`              | Secret keys like `OPENAI_API_KEY`, `PUSHOVER_TOKEN`                                                                                                   |
| `tests/test_document_pipeline.py` | Tests document loading, chunking, and vectorstore creation                                                                                            |
| `tests/test_chat_chain.py`        | Tests LangChain conversation chain and retrieval                                                                                                      |
| `tests/test_main.py`              | Tests FastAPI endpoints and integration                                                                                                               |

## 📄 DocumentPipeline Methods

| Method                 | Purpose                                     | Input          | Output                   |
| ---------------------- | ------------------------------------------- | -------------- | ------------------------ |
| `load_documents()`     | Read PDFs from knowledge base               | Directory path | List of Document objects |
| `chunk_documents()`    | Split large documents into smaller chunks   | Documents      | Smaller Document objects |
| `create_vectorstore()` | Create and populate vector database         | Documents      | ChromaDB instance        |
| `get_retriever()`      | Get LangChain retriever for document search | Nothing        | LangChain Retriever      |
| `process_documents()`  | Complete pipeline: load → chunk → store     | Nothing        | ChromaDB instance        |

### ✅ DocumentPipeline Implementation Status

- **PDF Loading**: ✅ Uses `PyMuPDFLoader` to load PDFs from `data/knowledge_base/`
- **Document Chunking**: ✅ Uses `CharacterTextSplitter` with configurable chunk size/overlap
- **Vector Storage**: ✅ Uses `OpenAIEmbeddings` and stores in `data/vector_db/`
- **Retrieval**: ✅ Uses `as_retriever()` method for semantic search
- **Testing**: ✅ Complete test suite in `tests/test_document_pipeline.py`
- **Dependencies**: ✅ All LangChain packages properly configured with compatible versions

## 🤖 Agent Identity & Prompting

### Alexa's Identity (agent_identity.md)

- **Personality**: Professional yet approachable credit union representative
- **Communication Style**: Friendly and professional, clear jargon-free explanations
- **Knowledge Domains**: Account services, online banking, loans, member benefits, security
- **Guardrails**: Knowledge base boundaries, confidentiality, financial advice limits, security protocols
- **Response Guidelines**: Always/Never rules for professional conduct
- **Escalation Triggers**: Account-specific issues, loan applications, fraud concerns, complaints

### Prompt Management (prompt_manager.py)

- **System Prompt**: Comprehensive prompt with identity, tool definitions, and escalation guidelines
- **Knowledge Integration**: Ready for document retrieval integration in Task 5
- **Tool Definitions**: send_notification, record_user_details, log_unknown_question
- **Escalation Guidelines**: Step-by-step process for handling member escalations

### Response Templates (response_templates.py)

- **Welcome Response**: Standard introduction message
- **Escalation Response**: Contact information request template
- **Knowledge Not Found**: Fallback response with contact information

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
