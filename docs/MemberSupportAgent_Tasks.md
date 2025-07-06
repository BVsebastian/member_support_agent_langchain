# 🚧 MVP Build Plan: Member Support Agent

## 1. Project Setup

- [x] 1.1 Init Git repo
- [x] 1.2 Create folders: `frontend/`, `backend/`, `data/`

## 2. Backend (FastAPI)

- [x] 2.1 Setup `main.py` with `/ping`
- [x] 2.2 Add `/chat` endpoint
- [x] 2.3 Install LangChain, Chroma, PyMuPDF (via UV)

## 3. PDF to Vector

- [x] 3.1 Use `PyMuPDFLoader` to load docs
- [x] 3.2 Chunk with `CharacterTextSplitter`
- [x] 3.3 Embed with `OpenAIEmbeddings`
- [x] 3.4 Store in ChromaDB (`/data/vector_db/`)
- [x] 3.5 Create `DocumentPipeline` class with complete pipeline
- [x] 3.6 Add comprehensive test suite
- [x] 3.7 Fix dependency conflicts and environment setup

## 4. Agent Identity & Prompting

- [x] 4.1 Define Alexa's personality and tone (professional, friendly credit union representative)
- [x] 4.2 Create system prompt with credit union context and knowledge base references
- [x] 4.3 Define response guidelines and escalation rules
- [x] 4.4 Integrate knowledge base references into prompts
- [x] 4.5 Create prompt_manager.py with Alexa's identity

### ✅ Task 4 Completed Files:

- `backend/agent_identity.md` - Alexa's complete identity and guardrails
- `backend/prompt_manager.py` - Comprehensive system prompt with tool definitions
- `backend/response_templates.py` - Standard response templates
- `backend/document_pipeline.py` - Added `get_retriever()` method

## 5. LangChain Chat Flow

- [x] 5.1 Create `chat_chain.py`
- [x] 5.2 Add `ConversationBufferMemory`
- [x] 5.3 Return answers from `/chat`

### ✅ Task 5 Completed Files:

- `backend/chat_chain.py` - ConversationalRetrievalChain with memory and retriever
- `backend/main.py` - Updated to use ChatChain for responses

## 6. Tools

- [x] 6.1 Create `tools.py`
- [x] 6.2 Add `handle_tool_call()` (moved to `test_tools.py` for testing)
- [x] 6.3 Integrate into chain
- [x] 6.4 Create `pushover_alerts.py`

### ✅ Task 6 Completed Files:

- `backend/tools.py` - Three tools: send_notification, record_user_details, log_unknown_question
- `backend/chat_chain.py` - Updated with LangChain Tool integration
- `backend/pushover_alerts.py` - Minimal Pushover API integration with proper error handling
- `tests/test_tools.py` - Comprehensive test suite (moved to tests folder)
- `tests/test_pushover.py` - Pushover alerts test script

## 7. **UPDATED: Agent Architecture Implementation**

- [x] 7.1 Replace ConversationalRetrievalChain with AgentExecutor
- [x] 7.2 Implement `create_tool_calling_agent` for structured tool calls
- [x] 7.3 Wrap retrieval as `create_retriever_tool`
- [x] 7.4 Update tools.py with `@tool` decorators
- [x] 7.5 Fix tool dispatcher to handle both `@tool` functions and tool objects
- [x] 7.6 Integrate ConversationBufferMemory with `{chat_history}` placeholder
- [x] 7.7 Add comprehensive escalation triggers and mandatory tool usage
- [x] 7.8 Implement debug system for tool calls and memory state
- [x] 7.9 Test agent memory, tool calling, and escalation flow

### ✅ Task 7 Completed Files:

- `backend/chat_chain.py` - **UPDATED**: AgentExecutor with create_tool_calling_agent
- `backend/tools.py` - **UPDATED**: LangChain tools with @tool decorators + create_retriever_tool
- `backend/prompt_manager.py` - **UPDATED**: Comprehensive escalation triggers and tool usage guidelines
- `tests/test_tools.py` - **UPDATED**: Tests for new tool interface

### ✅ Task 7 Key Features:

- **Agent-Based Architecture**: Proper LangChain agent with structured tool calling
- **Memory Integration**: Conversation history properly maintained and accessible
- **Escalation System**: Comprehensive triggers for human assistance requests
- **Tool Orchestration**: Automatic tool selection and execution based on user input
- **Debug System**: Comprehensive logging for tool calls and memory state

## 8. React Frontend ✅

- [x] 8.1 Scaffold with Vite + React (JSX)
- [x] 8.2 Build `ChatWindow` Component
- [x] 8.3 Create `api/chat.js`
- [x] 8.4 Connect input to backend
- [x] 8.5 Add TailwindCSS and Font Awesome
- [x] 8.6 ~~Implement responsive design and animations~~ **Not needed for MVP**

### ✅ Task 8.1 Completed Files:

- `frontend/` - Complete React JavaScript (JSX) application
- `frontend/src/App.jsx` - Clean, minimal app component with Horizon Bay branding
- `frontend/src/App.css` - Clean styling with credit union color scheme
- `frontend/src/components/` - Directory for chat components
- `frontend/src/api/` - Directory for API integration
- `frontend/package.json` - Dependencies including axios for API calls

### 📋 Task 8 UI Development Plan:

#### **8.2 Build ChatWindow Component**

- [x] 8.2.1 Create `ChatWindow.jsx` with header (bot icon, "Alexa", "Online" status)
- [x] 8.2.2 Add chat area with welcome message and message bubbles
- [x] 8.2.3 Implement typing indicator with animated dots
- [x] 8.2.4 Add message input footer with send button
- [x] 8.2.5 Style user messages (blue bubbles) and assistant messages (white with border)

#### **8.3 Create API Integration**

- [x] 8.3.1 Create `api/chat.js` with axios client
- [x] 8.3.2 Implement POST to `/chat` endpoint
- [x] 8.3.3 Add error handling and loading states
- [x] 8.3.4 (N/A) TypeScript interfaces not used (JSX project)

#### **8.4 Connect Frontend to Backend**

- [x] 8.4.1 Wire up send button to API calls
- [x] 8.4.2 Handle Enter key submission
- [x] 8.4.3 Implement real-time conversation flow
- [x] 8.4.4 Add auto-scroll to bottom functionality

> **Note:** All 8.3 and 8.4 subtasks are fully implemented in `frontend/src/api/chat.js` and `frontend/src/components/ChatWindow.jsx`.

#### **8.5 Add Styling and Icons**

- [x] 8.5.1 Install and configure TailwindCSS
- [x] 8.5.2 Add Heroicons (built into TailwindCSS)
- [x] 8.5.3 Implement Inter font family
- [x] 8.5.4 Style responsive design for mobile/desktop

### ✅ Task 8.5.1-8.5.3 Completed Files:

- `frontend/` - **MIGRATED**: From CRA to Vite + React + TypeScript
- `frontend/vite.config.js` - **UPDATED**: Added @tailwindcss/vite plugin
- `frontend/tailwind.config.js` - **NEW**: TailwindCSS configuration with custom colors
- `frontend/src/index.css` - **UPDATED**: Using @import "tailwindcss" (Vite plugin approach)
- `frontend/package.json` - **UPDATED**: Dependencies including @tailwindcss/vite and axios
- **Heroicons**: Built into TailwindCSS - no additional dependencies
- **Inter Font**: Already configured and imported

#### **8.6 Polish and Animations**

- [x] 8.6.1 ~~Add smooth transitions and animations~~ **Not needed for MVP**
- [x] 8.6.2 ~~Implement typing indicator animations~~ **Not needed for MVP**
- [x] 8.6.3 ~~Add message bubble animations~~ **Not needed for MVP**
- [x] 8.6.4 ~~Test responsive behavior across devices~~ **Not needed for MVP**

> **MVP Note:** Frontend is fully functional and meets MVP requirements. Advanced animations skipped for initial release.

### 📚 UI Architecture Reference:

- `docs/ui_development_plan.md` - Detailed UI component specifications
- `docs/ui_architecture_document.md` - Technical architecture and structure

## 9. Testing

- [x] 9.1 Verify PDF ingestion
- [x] 9.2 Verify answer flow
- [x] 9.3 Trigger tool logic
- [x] 9.4 **NEW**: Test agent memory and conversation context
- [x] 9.5 **NEW**: Test escalation triggers and tool orchestration

## 10. Deployment

- [x] 10.1 Vercel (frontend) - Successfully deployed
- [x] 10.2 Railway (backend) - Successfully deployed
- [x] 10.3 Point React API to backend

### Recent Changes

- **handle_tool_call**: Moved to `test_tools.py` for testing purposes and removed from the main workflow.

## 11. Documentation

- [ ] 11.1 Add README.md
- [ ] 11.2 Document .env and secrets
- [x] 11.3 Setup pyproject.toml for UV
- [x] 11.4 **NEW**: Update architecture documentation for agent-based system

### ✅ Task 8.2.1 Completed Files:

- `frontend/src/components/ChatWindow.jsx` - **NEW**: Complete chat interface with header, messages, and input
- `frontend/src/App.jsx` - **UPDATED**: Now uses ChatWindow component
- **Features**: Header with bot icon, online status, message bubbles, typing indicator, send button
- **Icons**: Using Heroicons (built into TailwindCSS) - no additional dependencies

> **Note:** ChatWindow now matches the reference UI, is centered, and uses correct colors, icons, and font sizes.

## 12. Supabase Integration with FastAPI

- [x] 12.1 Set Up Supabase

  - [x] 12.1.1 Create a Supabase account and project
  - [x] 12.1.2 Configure database tables and schema

- [x] 12.2 Configure FastAPI to Connect to Supabase

  - [x] 12.2.1 Install Supabase client library
  - [x] 12.2.2 Update FastAPI settings with Supabase URL and API key
  - [x] 12.2.3 Test Supabase connection

- [x] 12.3 Implement CRUD Operations

  - [x] 12.3.1 Create dedicated Supabase CRUD module
  - [x] 12.3.2 Use Supabase API for creating, reading, updating, and deleting records
  - [x] 12.3.3 Write unit tests for CRUD operations

### ✅ Task 12.3.3 Completed Files:

- `tests/test_crud_operations.py` - **NEW**: Comprehensive unit tests for all CRUD operations
- `backend/database.py` - **UPDATED**: Fixed deprecated `.dict()` methods to use `.model_dump()`
- **Test Coverage**: 14 tests covering Users, Conversations, and Messages CRUD operations
- **Schema Alignment**: Updated models to match actual database schema (removed non-existent fields)
- **Foreign Key Handling**: Proper cleanup order to respect database constraints
- **Test Features**: Unique test data generation, proper resource cleanup, comprehensive assertions

### 🧪 Test Results:

- **14 tests passed** - All CRUD operations working correctly
- **Schema-compliant models** - Aligned with actual database structure
- **Proper cleanup** - Foreign key constraints respected (messages → conversations → users)
- **Comprehensive coverage** - Create, Read, Update, Delete operations for all entities

## 13. Authentication and Real-Time Features

- [ ] 13.1 Implement Supabase authentication
- [ ] 13.2 Utilize real-time data synchronization

## 14. Documentation and Testing

- [ ] 14.1 Update documentation to include Supabase setup and usage
- [ ] 14.2 Conduct integration testing to ensure seamless operation with the existing system

### Recent Changes

- **handle_tool_call**: Moved to `test_tools.py` for testing purposes and removed from the main workflow.
