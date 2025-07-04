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

## 🌐 Frontend-Backend Connection Architecture

### **How the Connection Works**

The Member Support Agent uses a **flexible environment-based connection system** that allows the React frontend to connect to different backends based on configuration.

#### **Connection Flow Overview**

```
User Browser → React Frontend → Environment Check → API Request → Railway Backend
     ↑                                                                    ↓
     ←-------------------- JSON Response ←---------------------------------
```

### **Three Deployment Configurations**

#### **1. 🎯 Current Setup: Local Frontend + Railway Backend (Hybrid)**

- **Frontend Location**: `localhost:5174` (Vite development server)
- **Backend Location**: `https://membersupportagentlangchain-production.up.railway.app`
- **Configuration File**: `frontend/.env` with `VITE_API_BASE_URL=https://railway-url`
- **Use Case**: Active development with production backend testing
- **Benefits**:
  - ✅ Hot reload for frontend changes
  - ✅ Real production data and AI responses
  - ✅ No need to run backend locally

#### **2. 🚀 Future Production: Vercel Frontend + Railway Backend**

- **Frontend Location**: `yourapp.vercel.app` (deployed)
- **Backend Location**: `https://membersupportagentlangchain-production.up.railway.app`
- **Configuration**: Vercel environment variables with same Railway URL
- **Use Case**: Full production deployment
- **Benefits**:
  - ✅ Global CDN for fast loading
  - ✅ Both components auto-scale
  - ✅ Professional hosting reliability

#### **3. 🔧 Fully Local Development**

- **Frontend Location**: `localhost:5174`
- **Backend Location**: `localhost:8000`
- **Configuration**: No `.env` file (uses default localhost)
- **Use Case**: Offline development without external dependencies
- **Benefits**:
  - ✅ Complete offline development
  - ✅ No API rate limits or costs
  - ✅ Full control over both components

### **Environment Variable System**

#### **Frontend API Configuration** (`frontend/src/api/chat.js`)

```javascript
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
```

**Configuration Matrix:**

| Environment     | File Location   | Variable            | Value                                                           |
| --------------- | --------------- | ------------------- | --------------------------------------------------------------- |
| **Local Dev**   | `frontend/.env` | `VITE_API_BASE_URL` | `https://membersupportagentlangchain-production.up.railway.app` |
| **Production**  | Vercel Settings | `VITE_API_BASE_URL` | `https://membersupportagentlangchain-production.up.railway.app` |
| **Fully Local** | None (default)  | Not set             | `http://localhost:8000`                                         |

### **API Communication Lifecycle**

#### **Step-by-Step Request Flow**

1. **User Interaction**

   - User types message in React chat interface
   - Clicks send button or presses Enter

2. **Frontend Processing**

   - React reads `VITE_API_BASE_URL` environment variable
   - Constructs full API endpoint URL
   - Packages message and session_id into JSON

3. **HTTP Request**

   - Frontend sends POST request to `/chat` endpoint
   - CORS headers included automatically
   - Request goes to Railway backend (not localhost)

4. **Backend Processing**

   - Railway FastAPI server receives request
   - LangChain Agent analyzes message and context
   - Agent searches knowledge base and executes tools
   - AI generates response using OpenAI

5. **Response Return**

   - Backend packages AI response as JSON
   - Includes session_id for conversation continuity
   - Returns with proper CORS headers

6. **Frontend Display**
   - React receives JSON response
   - Parses and displays AI message
   - Auto-scrolls to show new message

### **Cross-Origin Resource Sharing (CORS)**

The system handles cross-origin requests between the frontend and backend automatically.

#### **Backend CORS Configuration** (`backend/main.py`)

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**What This Enables:**

- ✅ Local frontend (`localhost:5174`) can call Railway backend
- ✅ Future Vercel frontend can call Railway backend
- ✅ Browser doesn't block cross-origin API requests
- ✅ Supports all HTTP methods (GET, POST, PUT, DELETE)

### **Current System Status**

| Component           | Status      | Location                                                        | Platform   |
| ------------------- | ----------- | --------------------------------------------------------------- | ---------- |
| **Backend**         | ✅ Deployed | `https://membersupportagentlangchain-production.up.railway.app` | Railway    |
| **Frontend**        | ✅ Deployed | `https://member-support-agent-langchain-mzy40fsz4.vercel.app`   | Vercel     |
| **Vector Database** | ✅ Deployed | Railway persistent storage                                      | Railway    |
| **AI Knowledge**    | ✅ Active   | ChromaDB with PDF embeddings                                    | Railway    |
| **Connection**      | ✅ Working  | Vercel Frontend → Railway Backend                               | Production |

### **Verifying the Connection**

#### **Using Browser Developer Tools**

1. **Open Network Tab** in Chrome/Firefox/Safari DevTools
2. **Send a chat message** in the frontend
3. **Look for the request** with these characteristics:

**✅ Successful Connection Indicators:**

- **Request URL**: `https://membersupportagentlangchain-production.up.railway.app/chat`
- **Method**: `POST`
- **Status**: `200 OK`
- **Response**: JSON with AI message content
- **Time**: Usually 2-5 seconds for AI processing

**❌ Connection Problems:**

- **Request URL**: Shows `localhost:8000` (backend not configured)
- **Status**: `CORS error` or `Network Error`
- **Response**: Empty or error message

#### **Example Successful Request**

```http
POST https://membersupportagentlangchain-production.up.railway.app/chat
Content-Type: application/json

Request Body:
{
  "message": "What are your hours?",
  "session_id": "abc123"
}

Response (200 OK):
{
  "response": "Hello! I'm Alexa from Horizon Bay Credit Union...",
  "session_id": "abc123"
}
```

### **Production Deployment Benefits**

#### **✅ Current Production Setup (Vercel Frontend + Railway Backend)**

**Full Production Deployment Achieved:**

- 🌍 **Global Performance**: Vercel CDN delivers frontend worldwide instantly
- 🚀 **Auto-Scaling**: Both Vercel and Railway handle traffic spikes automatically
- 🔄 **Zero Downtime**: Professional deployment with rollback capabilities
- 💪 **Production Ready**: Full professional hosting for both components
- 🔒 **Security**: CORS properly configured, environment variables secured
- 📊 **Real AI Data**: Production vector database with knowledge base
- 🧠 **Full Functionality**: Agent memory, tools, escalation system all operational

**Development Workflow Benefits:**

- ⚡ **Local Development**: Can still run `npm run dev` locally for changes
- 🧪 **Testing**: Can test against production backend during development
- 🎯 **Environment Variables**: Proper separation between local/production configs
- 📈 **Monitoring**: Both platforms provide deployment logs and analytics

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

# UI Architecture Reference (Updated)

- ChatWindow now supports Markdown-formatted Alexa responses using 'marked', with type checking for safety
- Input auto-focuses after each AI response for seamless UX
- Real-time conversation flow, error handling, and auto-scroll are implemented
- All frontend-backend chat integration is complete and matches reference UI
- Only assistant messages are parsed as Markdown; user messages remain plain text
- The frontend is implemented in JavaScript/JSX (not TypeScript)
- File names: `App.jsx`, `ChatWindow.jsx`, `chat.js` (no .ts/.tsx files)
- The UI is complete, styled, and responsive, focused on core functionality (no bubble animations or extra polish tasks)

```

```
