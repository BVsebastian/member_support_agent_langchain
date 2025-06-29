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
- [x] 6.2 Add `handle_tool_call()`
- [x] 6.3 Integrate into chain
- [x] 6.4 Create `pushover_alerts.py`

### ✅ Task 6 Completed Files:

- `backend/tools.py` - Three tools: send_notification, record_user_details, log_unknown_question
- `backend/chat_chain.py` - Updated with LangChain Tool integration
- `backend/pushover_alerts.py` - Minimal Pushover API integration with proper error handling
- `tests/test_tools.py` - Comprehensive test suite (moved to tests folder)
- `tests/test_pushover.py` - Pushover alerts test script

## 7. **NEW: Agent Architecture Implementation**

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

## 8. React Frontend

- [ ] 8.1 Scaffold with CRA
- [ ] 8.2 Build `ChatWindow`
- [ ] 8.3 Create `api/chat.js`
- [ ] 8.4 Connect input to backend

## 9. Testing

- [x] 9.1 Verify PDF ingestion
- [x] 9.2 Verify answer flow
- [x] 9.3 Trigger tool logic
- [x] 9.4 **NEW**: Test agent memory and conversation context
- [x] 9.5 **NEW**: Test escalation triggers and tool orchestration

## 10. Deployment

- [ ] 10.1 Vercel (frontend)
- [ ] 10.2 Render/Railway (backend)
- [ ] 10.3 Point React API to backend

## 11. Documentation

- [ ] 11.1 Add README.md
- [ ] 11.2 Document .env and secrets
- [x] 11.3 Setup pyproject.toml for UV
- [x] 11.4 **NEW**: Update architecture documentation for agent-based system
