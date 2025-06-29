# 📐 Architecture Document: Member Support Agent (LangChain Agent Edition)

---

## 📁 File & Folder Structure

```
member_support_agent/
├── frontend/                        # React frontend
├── backend/                         # FastAPI + LangChain Agent
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
│   ├── test_tools.py
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
| `chat_chain.py`                   | **NEW**: Builds LangChain's `AgentExecutor` with `create_tool_calling_agent` using memory + tools                                                     |
| `document_pipeline.py`            | Loads all PDFs via `PyMuPDFLoader`, chunks them with `CharacterTextSplitter`, creates embeddings with `OpenAIEmbeddings`, and stores them in `Chroma` |
| `prompt_manager.py`               | **UPDATED**: Loads system prompt with comprehensive escalation triggers and mandatory tool usage guidelines                                           |
| `response_templates.py`           | Provides standard response templates for welcome, escalation, and knowledge-not-found scenarios                                                       |
| `agent_identity.md`               | Markdown file defining Alexa's personality, communication style, guardrails, and response guidelines                                                  |
| `state.py`                        | Stores session metadata: `chat_history`, user flags, etc.                                                                                             |
| `pushover_alerts.py`              | Sends alerts for unresolved or unknown queries                                                                                                        |
| `tools.py`                        | **UPDATED**: LangChain tools with `@tool` decorators + `create_retriever_tool` + central `handle_tool_call()` dispatcher                              |
| `config/constants.py`             | Configuration for chunk size, retriever behavior                                                                                                      |
| `config/secrets.env`              | Secret keys like `OPENAI_API_KEY`, `PUSHOVER_TOKEN`                                                                                                   |
| `tests/test_document_pipeline.py` | Tests document loading, chunking, and vectorstore creation                                                                                            |
| `tests/test_tools.py`             | **UPDATED**: Tests for new tool interface and agent integration                                                                                       |
| `tests/test_main.py`              | Tests FastAPI endpoints and integration                                                                                                               |

## 🧠 Agent Architecture Overview

### **NEW: Agent-Based Architecture**

- **AgentExecutor**: Orchestrates tool calling and reasoning
- **create_tool_calling_agent**: Creates agent with structured tool calls
- **ConversationBufferMemory**: Maintains conversation history
- **Tool Integration**: Proper tool calling with structured output

### **Tool System**

- **search_knowledge_base**: LangChain retriever tool for knowledge base queries
- **record_user_details**: Records user contact information
- **send_notification**: Sends escalation notifications
- **log_unknown_question**: Logs unanswered questions

### **Memory Integration**

- **Chat History**: Properly integrated with `{chat_history}` in prompt template
- **Context Awareness**: Agent remembers previous conversation context
- **Conversation Summarization**: Can summarize previous interactions

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

### **NEW: Escalation Triggers (prompt_manager.py)**

- **Specific Issue Types**: "fraud", "loan", "card", "account", "refinance"
- **Human Assistance Requests**: "manager", "supervisor", "human representative", "speak to someone"
- **Direct Escalation Requests**: "escalate", "escalation", "transfer me", "connect me to"
- **Dissatisfaction Indicators**: "complaint", "unhappy", "not satisfied"

### **NEW: Mandatory Tool Usage**

- **Escalation Flow**: record_user_details → send_notification
- **Service Queries**: search_knowledge_base first
- **Unknown Questions**: log_unknown_question

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
    B1 --> B2[AgentExecutor]
    B2 --> B3[create_tool_calling_agent]
    B3 --> B4[Tools]
    B4 --> B5[search_knowledge_base]
    B4 --> B6[record_user_details]
    B4 --> B7[send_notification]
    B4 --> B8[log_unknown_question]
    B5 --> B9[Retriever (Chroma)]
    B9 --> B10[Vector DB (ChromaDB)]
    B7 --> B11[Pushover Alerts]
    B2 --> B12[ConversationBufferMemory]
    B2 --> B13[Return Response]
  end

  subgraph Storage
    B10 --> D1[data/vector_db/]
    B6 --> D2[data/logs/]
    B7 --> D2
    B8 --> D2
  end
```

---

## 🧠 Where State Lives

| Component         | State                                        | Persistence                                      |
| ----------------- | -------------------------------------------- | ------------------------------------------------ |
| **AgentExecutor** | **NEW**: Chat history, tool calls            | **NEW**: In-memory with ConversationBufferMemory |
| `vector_db/`      | PDF embeddings                               | Persistent (ChromaDB folder)                     |
| `logs/`           | Unknown questions, escalations, user details | File-based JSON                                  |
| React `App.jsx`   | UI state, chat session                       | Browser memory                                   |

## 🔧 Debug & Monitoring

### **NEW: Debug System**

- **Tool Call Tracking**: Debug prints for all tool calls and parameters
- **Memory State**: Track conversation history length
- **Response Structure**: Monitor agent response format
- **Error Handling**: Comprehensive error logging

### **Tool Execution Flow**

1. **Agent Analysis**: Agent analyzes user input and conversation context
2. **Tool Selection**: Agent selects appropriate tools based on escalation triggers
3. **Tool Execution**: Tools execute with proper parameters
4. **Result Integration**: Tool results integrated into final response
5. **Memory Update**: Conversation history updated with new interaction

- The ChatWindow component is now complete, matches the reference UI, and is fully styled and responsive.

# In the UI Architecture Reference section, add:

- ChatWindow: Complete, centered, styled per reference, with correct icons, colors, and font sizes.

```

```
