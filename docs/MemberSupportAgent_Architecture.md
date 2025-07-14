# Architecture Document: Member Support Agent (LangChain Agent Edition)

---

## File & Folder Structure

```
member_support_agent/
├── frontend/                        # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatWindow.jsx      # Main chat interface component
│   │   ├── api/
│   │   │   └── chat.js             # API client for backend communication
│   │   ├── assets/
│   │   │   └── react.svg           # Static assets
│   │   ├── App.jsx                 # Root application component
│   │   ├── main.jsx                # Application entry point
│   │   ├── index.css               # Global styles with TailwindCSS
│   │   └── App.css                 # Component-specific styles
│   ├── public/                     # Static files
│   ├── dist/                       # Build output
│   ├── package.json                # Dependencies and scripts
│   ├── vite.config.js              # Vite configuration
│   ├── tailwind.config.js          # TailwindCSS configuration
│   ├── eslint.config.js            # ESLint configuration
│   └── vercel.json                 # Vercel deployment config
├── backend/                         # FastAPI + LangChain Agent
│   ├── main.py                      # FastAPI app with comprehensive API endpoints
│   ├── chat_chain.py                # LangChain AgentExecutor with tool integration
│   ├── document_pipeline.py         # PDF processing and vector storage
│   ├── database.py                  # Supabase CRUD operations
│   ├── tools.py                     # Agent tools for escalation and search
│   ├── pushover_alerts.py           # Notification system
│   ├── prompt_manager.py            # AI system prompts and identity
│   ├── response_templates.py        # Response templates
│   ├── agent_identity.md            # Alexa's personality and guidelines
│   ├── debug_docs.py                # Document processing debug tool
│   ├── gradio_test.py               # Gradio testing interface
│   └── config/
│       └── constants.py             # Configuration constants
├── tests/                           # Test files
│   ├── test_document_pipeline.py
│   ├── test_tools.py
│   ├── test_crud_operations.py
│   └── test_main.py
├── data/
│   ├── knowledge_base/              # PDF documents
│   ├── logs/                        # Application logs
│   └── vector_db/                   # ChromaDB storage
├── supabase/                        # Database migrations
│   └── migrations/
├── .env
├── pyproject.toml                   # UV dependency management
└── README.md
```

---

## **UPDATED: Module Responsibilities & Data Flow**

### **Frontend Modules**

| File                                     | Responsibility                                                                                       | Data Flow                                                                                 |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| `frontend/src/main.jsx`                  | **Application Entry Point**: React app initialization and root rendering                             | Renders App component with StrictMode                                                     |
| `frontend/src/App.jsx`                   | **Root Component**: Main application layout and ChatWindow integration                               | Provides layout container and renders ChatWindow component                                |
| `frontend/src/components/ChatWindow.jsx` | **Chat Interface**: Complete chat UI with message handling, typing indicators, and real-time updates | Receives user input → Calls API → Displays responses → Manages conversation state         |
| `frontend/src/api/chat.js`               | **API Client**: HTTP communication with backend, session management, error handling                  | Sends POST requests to `/chat` → Handles responses → Manages session IDs → Error handling |
| `frontend/src/index.css`                 | **Global Styles**: TailwindCSS imports and global styling                                            | Provides base styles and TailwindCSS utilities                                            |
| `frontend/src/App.css`                   | **Component Styles**: App-specific styling and layout                                                | Defines component-specific CSS classes and animations                                     |
| `frontend/src/assets/react.svg`          | **Static Assets**: React logo and static images                                                      | Provides static assets for the application                                                |
| `frontend/package.json`                  | **Dependencies**: Project dependencies, scripts, and metadata                                        | Manages npm packages, build scripts, and project configuration                            |
| `frontend/vite.config.js`                | **Build Configuration**: Vite development server and build settings                                  | Configures development server, build process, and plugins                                 |
| `frontend/tailwind.config.js`            | **Styling Configuration**: TailwindCSS theme and custom configuration                                | Defines color scheme, fonts, and custom TailwindCSS utilities                             |
| `frontend/eslint.config.js`              | **Code Quality**: ESLint rules and code formatting                                                   | Enforces code quality standards and formatting rules                                      |
| `frontend/vercel.json`                   | **Deployment Configuration**: Vercel deployment settings                                             | Configures Vercel deployment, routing, and environment variables                          |

### **Backend Modules**

| File                            | Responsibility                                                                                          | Data Flow                                                                                      |
| ------------------------------- | ------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| `backend/main.py`               | **API Gateway**: FastAPI application with 20+ endpoints for CRUD operations and chat interface          | Receives HTTP requests → Routes to appropriate handlers → Returns JSON responses               |
| `backend/chat_chain.py`         | **AI Agent Brain**: LangChain AgentExecutor with tool integration and session management                | Processes user messages → Calls tools → Generates AI responses → Manages conversation memory   |
| `backend/database.py`           | **Data Persistence**: Complete Supabase CRUD operations for users, conversations, messages, escalations | Handles database operations → Manages Pydantic models → Provides data validation               |
| `backend/tools.py`              | **Agent Tools**: LangChain tools for search, user details, notifications, and logging                   | Agent calls tools → Tools execute actions → Results integrated into responses                  |
| `backend/document_pipeline.py`  | **Knowledge Base Engine**: PDF processing, chunking, embedding, and vector storage                      | Loads PDFs → Chunks documents → Creates embeddings → Stores in ChromaDB → Provides retriever   |
| `backend/prompt_manager.py`     | **AI Personality**: System prompts, escalation triggers, and mandatory tool usage guidelines            | Defines agent behavior → Manages escalation rules → Provides tool usage instructions           |
| `backend/pushover_alerts.py`    | **Notification System**: Real-time alerts to support staff via Pushover API                             | Sends high-priority notifications → Includes conversation context → Tracks escalation status   |
| `backend/response_templates.py` | **Response Templates**: Standard response templates for common scenarios                                | Provides consistent responses → Handles welcome, escalation, and error messages                |
| `backend/agent_identity.md`     | **AI Identity**: Alexa's personality, communication style, and professional guidelines                  | Defines agent personality → Sets communication standards → Establishes professional boundaries |
| `backend/debug_docs.py`         | **Development Tool**: Debug script for testing document processing pipeline                             | Tests document loading → Validates vector storage → Provides development debugging             |
| `backend/gradio_test.py`        | **Testing Interface**: Gradio web interface for testing AI agent functionality                          | Provides web-based testing → Enables agent testing → Offers example queries                    |
| `backend/config/constants.py`   | **Configuration**: Document processing settings, file paths, and system constants                       | Defines chunk sizes → Sets file paths → Configures embedding models                            |

---

## **Complete Data Flow Architecture**

### **Frontend Data Flow**

```
User Input → ChatWindow.jsx → chat.js → Backend API → Response → UI Update
     ↓              ↓              ↓           ↓           ↓           ↓
1. User types    2. Component   3. HTTP     4. FastAPI   5. JSON     6. Display
   message         captures       request      processes    response     response
   in input        input and      to backend   request      to frontend  in chat
   field           calls API      with         and calls    with AI      interface
                   function       session_id   chat_chain   response
```

### **Backend Data Flow**

```
HTTP Request → main.py → chat_chain.py → tools.py → database.py → Response
     ↓            ↓           ↓            ↓           ↓           ↓
1. FastAPI     2. Route to   3. Agent     4. Execute   5. Store    6. Return
   receives     chat_chain    processes    tools        data in     JSON
   POST to      with          message      (search,     Supabase    response
   /chat        session_id    and calls    record,      database    to frontend
   endpoint     management    tools        notify)
```

### **Tool Execution Flow**

```
Agent Analysis → Tool Selection → Tool Execution → Result Integration → Response Generation
      ↓              ↓              ↓                ↓                    ↓
1. Agent         2. Agent        3. Tools        4. Tool results    5. AI generates
   analyzes       selects         execute with    integrated into    final response
   user input     appropriate     parameters      agent context      with context
   and context    tools based     (search,        and memory        and returns
   (escalation    on triggers     record,        updated            to frontend
   detection)     and rules       notify, log)                      via main.py
```

### **Database Integration Flow**

```
Session Management → User Creation → Conversation Tracking → Message Storage → Escalation Records
        ↓                ↓                ↓                    ↓                    ↓
1. chat_chain     2. Creates       3. Links             4. Stores all       5. Tracks
   manages         anonymous        conversations         messages with         escalation
   session IDs     users for        to users            conversation        requests with
   and creates     each session     and maintains       context and         full context
   conversations   with unique      conversation         timestamps          for human
                   email            history                                handoffs
```

---

## **UPDATED: FastAPI API Endpoints (main.py)**

### **Core Chat Endpoints**

| Endpoint | Method | Purpose             | Request Body                          | Response                                                             |
| -------- | ------ | ------------------- | ------------------------------------- | -------------------------------------------------------------------- |
| `/ping`  | GET    | Health check        | None                                  | `{"status": "ok", "message": "Member Support Agent API is running"}` |
| `/chat`  | POST   | Main chat interface | `{"message": str, "session_id": str}` | `{"response": str, "status": str}`                                   |

### **User Management Endpoints**

| Endpoint               | Method | Purpose           | Request Body       | Response                                   |
| ---------------------- | ------ | ----------------- | ------------------ | ------------------------------------------ |
| `/users/`              | POST   | Create new user   | `UserCreate` model | `User` model                               |
| `/users/{user_id}`     | GET    | Get user by ID    | None               | `User` model                               |
| `/users/`              | GET    | Get all users     | None               | `List[User]`                               |
| `/users/email/{email}` | GET    | Get user by email | None               | `User` model                               |
| `/users/{user_id}`     | PUT    | Update user       | `UserUpdate` model | `User` model                               |
| `/users/{user_id}`     | DELETE | Delete user       | None               | `{"message": "User deleted successfully"}` |

### **Conversation Management Endpoints**

| Endpoint                           | Method | Purpose                  | Request Body               | Response                                           |
| ---------------------------------- | ------ | ------------------------ | -------------------------- | -------------------------------------------------- |
| `/conversations/`                  | POST   | Create new conversation  | `ConversationCreate` model | `Conversation` model                               |
| `/conversations/{conversation_id}` | GET    | Get conversation by ID   | None                       | `Conversation` model                               |
| `/conversations/`                  | GET    | Get all conversations    | None                       | `List[Conversation]`                               |
| `/users/{user_id}/conversations`   | GET    | Get user's conversations | None                       | `List[Conversation]`                               |
| `/conversations/{conversation_id}` | PUT    | Update conversation      | `ConversationUpdate` model | `Conversation` model                               |
| `/conversations/{conversation_id}` | DELETE | Delete conversation      | None                       | `{"message": "Conversation deleted successfully"}` |

### **Message Management Endpoints**

| Endpoint                                    | Method | Purpose                   | Request Body          | Response                                      |
| ------------------------------------------- | ------ | ------------------------- | --------------------- | --------------------------------------------- |
| `/messages/`                                | POST   | Create new message        | `MessageCreate` model | `Message` model                               |
| `/messages/{message_id}`                    | GET    | Get message by ID         | None                  | `Message` model                               |
| `/messages/`                                | GET    | Get all messages          | None                  | `List[Message]`                               |
| `/conversations/{conversation_id}/messages` | GET    | Get conversation messages | None                  | `List[Message]`                               |
| `/messages/{message_id}`                    | PUT    | Update message            | `MessageUpdate` model | `Message` model                               |
| `/messages/{message_id}`                    | DELETE | Delete message            | None                  | `{"message": "Message deleted successfully"}` |

### **Convenience Endpoints**

| Endpoint                                    | Method | Purpose                            | Parameters                                          | Response                   |
| ------------------------------------------- | ------ | ---------------------------------- | --------------------------------------------------- | -------------------------- |
| `/conversations/{conversation_id}/full`     | GET    | Get conversation with all messages | None                                                | `ConversationWithMessages` |
| `/users/{user_id}/conversations`            | POST   | Create conversation for user       | `title: Optional[str]`                              | `Conversation` model       |
| `/conversations/{conversation_id}/messages` | POST   | Add message to conversation        | `content: str, topic: Optional[str], private: bool` | `Message` model            |

### **Database Models**

#### **User Model**

```python
class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime
    updated_at: datetime
```

#### **Conversation Model**

```python
class Conversation(BaseModel):
    id: int
    user_id: int
    started_at: datetime
    updated_at: datetime
```

#### **Message Model**

```python
class Message(BaseModel):
    id: int
    conversation_id: int
    content: str
    topic: Optional[str]
    private: bool
    sent_at: datetime
```

### **CORS Configuration**

```python
# Environment-based CORS configuration
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Supported Origins:**

- Development: `*` (allows all origins)
- Production: Specific domains via `CORS_ORIGINS` environment variable

---

## Agent Architecture Overview

### **UPDATED: Agent-Based Architecture**

- **AgentExecutor**: Orchestrates tool calling and reasoning, now properly utilized for all interactions
- **create_tool_calling_agent**: Creates agent with structured tool calls, ensuring `search_knowledge_base` is always used first
- **ConversationBufferMemory**: Maintains conversation history
- **Tool Integration**: Proper tool calling with structured output, no more forced search

### **Tool System**

- **search_knowledge_base**: LangChain retriever tool for knowledge base queries, always called first
- **record_user_details**: Records user contact information
- **send_notification**: Sends escalation notifications
- **log_unknown_question**: Logs unanswered questions

### **Memory Integration**

- **Chat History**: Properly integrated with `{chat_history}` in prompt template
- **Context Awareness**: Agent remembers previous conversation context
- **Conversation Summarization**: Can summarize previous interactions

---

## DocumentPipeline Methods

| Method                 | Purpose                                     | Input          | Output                   |
| ---------------------- | ------------------------------------------- | -------------- | ------------------------ |
| `load_documents()`     | Read PDFs from knowledge base               | Directory path | List of Document objects |
| `chunk_documents()`    | Split large documents into smaller chunks   | Documents      | Smaller Document objects |
| `create_vectorstore()` | Create and populate vector database         | Documents      | ChromaDB instance        |
| `get_retriever()`      | Get LangChain retriever for document search | Nothing        | LangChain Retriever      |
| `process_documents()`  | Complete pipeline: load → chunk → store     | Nothing        | ChromaDB instance        |

### DocumentPipeline Implementation Status

- **PDF Loading**: ✅ Uses `PyMuPDFLoader` to load PDFs from `data/knowledge_base/`
- **Document Chunking**: ✅ Uses `CharacterTextSplitter` with configurable chunk size/overlap
- **Vector Storage**: ✅ Uses `OpenAIEmbeddings` and stores in `data/vector_db/`
- **Retrieval**: ✅ Uses `as_retriever()` method for semantic search
- **Testing**: ✅ Complete test suite in `tests/test_document_pipeline.py`
- **Dependencies**: ✅ All LangChain packages properly configured with compatible versions

---

## Agent Identity & Prompting

### Alexa's Identity (agent_identity.md)

- **Personality**: Professional yet approachable credit union representative
- **Communication Style**: Friendly and professional, clear jargon-free explanations
- **Knowledge Domains**: Account services, online banking, loans, member benefits, security
- **Guardrails**: Knowledge base boundaries, confidentiality, financial advice limits, security protocols
- **Response Guidelines**: Always/Never rules for professional conduct

### **NEW: Comprehensive Escalation System (prompt_manager.py)**

#### **Automated Escalation Triggers**

- **Specific Issue Types**: "fraud", "loan", "card", "account", "refinance"
- **Human Assistance Requests**: "manager", "supervisor", "human representative", "speak to someone"
- **Direct Escalation Requests**: "escalate", "escalation", "transfer me", "connect me to"
- **Dissatisfaction Indicators**: "complaint", "unhappy", "not satisfied"

#### **Mandatory Tool Usage Flow**

- **Always Search First**: search_knowledge_base for every question (no exceptions)
- **Escalation Flow**: record_user_details → send_notification (strict sequential execution)
- **Service Queries**: search_knowledge_base first, then provide accurate information
- **Unknown Questions**: log_unknown_question when knowledge base lacks information
- **Tool Validation**: send_notification requires contact info and session_id validation

#### **Database Integration**

- **Escalations Table**: Tracks issue_type, original_request, status, conversation_id
- **Status Tracking**: "pending", "notified", "in_progress", "resolved"
- **Conversation Linking**: Links escalations to chat conversations for full context
- **Contact Information**: Name, email, phone captured for human follow-up
- **Session Management**: Anonymous users with preserved session emails for reliable lookup
- **Escalation Records**: Successfully created and tracked in Supabase database

#### **Notification System**

- **Pushover Integration**: Real-time alerts to support staff with high priority
- **Structured Messages**: Issue type, contact info, conversation context (last 5 messages)
- **Escalation ID**: Unique tracking for each escalation request
- **Human Handoff**: Complete conversation history for seamless transitions
- **Contact Validation**: Ensures contact information is provided before sending notifications
- **Error Handling**: Comprehensive error messages for missing data or failed operations

### Response Templates (response_templates.py)

- **Welcome Response**: Standard introduction message
- **Escalation Response**: Contact information request template
- **Knowledge Not Found**: Fallback response with contact information

---

## How Services Connect

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
    B6 --> D2[Supabase Database]
    B7 --> D2
    B8 --> D2
  end
```

---

## Frontend-Backend Connection Architecture

### **How the Connection Works**

The Member Support Agent uses a **flexible environment-based connection system** that allows the React frontend to connect to different backends based on configuration.

#### **Connection Flow Overview**

```
User Browser → React Frontend → Environment Check → API Request → Railway Backend
     ↑                                                                    ↓
     ←-------------------- JSON Response ←---------------------------------
```

### **Three Deployment Configurations**

#### **1. Current Setup: Local Frontend + Railway Backend (Hybrid)**

- **Frontend Location**: `localhost:5174` (Vite development server)
- **Backend Location**: `https://membersupportagentlangchain-production.up.railway.app`
- **Configuration File**: `frontend/.env` with `VITE_API_BASE_URL=https://railway-url`
- **Use Case**: Active development with production backend testing
- **Benefits**:
  - ✅ Hot reload for frontend changes
  - ✅ Real production data and AI responses
  - ✅ No need to run backend locally

#### **2. Future Production: Vercel Frontend + Railway Backend**

- **Frontend Location**: `yourapp.vercel.app` (deployed)
- **Backend Location**: `https://membersupportagentlangchain-production.up.railway.app`
- **Configuration**: Vercel environment variables with same Railway URL
- **Use Case**: Full production deployment
- **Benefits**:
  - ✅ Global CDN for fast loading
  - ✅ Both components auto-scale
  - ✅ Professional hosting reliability

#### **3. Fully Local Development**

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
# Get CORS origins from environment or use default for development
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
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

**Successful Connection Indicators:**

- **Request URL**: `https://membersupportagentlangchain-production.up.railway.app/chat`
- **Method**: `POST`
- **Status**: `200 OK`
- **Response**: JSON with AI message content
- **Time**: Usually 2-5 seconds for AI processing

**Connection Problems:**

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
  "status": "success"
}
```

### **Production Deployment Benefits**

#### **Current Production Setup (Vercel Frontend + Railway Backend)**

**Full Production Deployment Achieved:**

- **Global Performance**: Vercel CDN delivers frontend worldwide instantly
- **Auto-Scaling**: Both Vercel and Railway handle traffic spikes automatically
- **Zero Downtime**: Professional deployment with rollback capabilities
- **Production Ready**: Full professional hosting for both components
- **Security**: CORS properly configured, environment variables secured
- **Real AI Data**: Production vector database with knowledge base
- **Full Functionality**: Agent memory, tools, escalation system all operational

**Development Workflow Benefits:**

- **Local Development**: Can still run `npm run dev` locally for changes
- **Testing**: Can test against production backend during development
- **Environment Variables**: Proper separation between local/production configs
- **Monitoring**: Both platforms provide deployment logs and analytics

---

## Where State Lives

| Component         | State                                        | Persistence                                      |
| ----------------- | -------------------------------------------- | ------------------------------------------------ |
| **AgentExecutor** | **NEW**: Chat history, tool calls            | **NEW**: In-memory with ConversationBufferMemory |
| `vector_db/`      | PDF embeddings                               | Persistent (ChromaDB folder)                     |
| `supabase/`       | Conversations, messages, users, escalations  | Persistent (PostgreSQL database)                 |
| `logs/`           | Unknown questions, escalations, user details | File-based JSON                                  |
| React `App.jsx`   | UI state, chat session                       | Browser memory                                   |

## Debug & Monitoring

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

## Potential Future Enhancements

### Tool Call Order Management

To ensure specific tools are called in a desired order without altering the core workflow, consider the following strategies:

1. **Prompt Engineering**: Modify the prompt template to include instructions that guide the agent to call `record_user_details` before `send_notification`. This can be done by adding explicit instructions or examples in the system prompt that emphasize the desired order of operations.

2. **Tool Logic**: Adjust the logic within the tools themselves to check if prerequisites have been met. For example, `send_notification` could check if `record_user_details` has been executed and handle the situation accordingly.

3. **State Management**: Implement a simple state management system within the agent's memory to track which tools have been called. This can be used to influence the agent's decision-making process.

4. **Custom Tool Wrappers**: Create wrapper functions for the tools that enforce the desired order. These wrappers can be bound to the language model instead of the original tools.

These strategies can help maintain the current workflow while ensuring the correct sequence of tool calls. They can be explored further as the project evolves.

### Deployment Status

- **Frontend**: Successfully deployed to Vercel.
- **Backend**: Deployed on Railway.

### Recent Changes

- **handle_tool_call**: Moved to `test_tools.py` for testing purposes and removed from the main workflow.

### Database Integration

#### Supabase with FastAPI

The Member Support Agent uses Supabase to store conversation data for escalation follow-ups and conversation history. The database structure is:

**Tables:**

- **users**: `id`, `name`, `email` (for escalation contact info)
- **conversations**: `id`, `user_id`, `started_at` (chat sessions)
- **messages**: `id`, `conversation_id`, `content`, `topic`, `private`, `sent_at` (chat messages)
- **escalations**: `id`, `conversation_id`, `issue_type`, `original_request`, `status`, `created_at`, `resolved_at` (escalation tracking)

**Integration Status:**

- ✅ **Supabase Setup**: Project created and configured
- ✅ **Database Schema**: Tables created via migrations
- ✅ **CRUD Operations**: Complete operations in `database.py`
- ✅ **FastAPI Integration**: Comprehensive endpoints for all database operations
- ✅ **Testing**: Complete test suite in `test_crud_operations.py` (14+ tests)

**API Endpoints:**

- ✅ **User Management**: Create, read, update, delete users
- ✅ **Conversation Management**: Full CRUD for conversations with user relationships
- ✅ **Message Management**: Complete message handling with conversation context
- ✅ **Convenience Endpoints**: Get conversations with messages, create user conversations
- ✅ **Error Handling**: Proper HTTP status codes and error messages

**Purpose:**

- Store conversation history for context
- Track user information for escalation follow-ups
- Maintain chat sessions across browser sessions
- Enable conversation analytics and improvement
- **NEW**: Track escalation requests with full conversation context for human handoffs
- **NEW**: Monitor escalation status and resolution tracking
- **NEW**: Successfully tested escalation flow with database integration and notifications

**No Authentication Required:**

- Users are anonymous (no login required)
- Conversations tracked by session ID
- User info only collected when escalation needed

```

```
