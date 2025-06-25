# 🚧 MVP Build Plan: Member Support Agent

## 1. Project Setup

- [x] 1.1 Init Git repo
- [x] 1.2 Create folders: `frontend/`, `backend/`, `data/`

## 2. Backend (FastAPI)

- [x] 2.1 Setup `main.py` with `/ping`
- [ ] 2.2 Add `/chat` endpoint
- [ ] 2.3 Install LangChain, Chroma, PyMuPDF (via UV)

## 3. PDF to Vector

- [ ] 3.1 Use `PyMuPDFLoader` to load docs
- [ ] 3.2 Chunk with `CharacterTextSplitter`
- [ ] 3.3 Embed with `OpenAIEmbeddings`
- [ ] 3.4 Store in ChromaDB (`/data/vector_db/`)

## 4. LangChain Chat Flow

- [ ] 4.1 Create `chat_chain.py`
- [ ] 4.2 Add `ConversationBufferMemory`
- [ ] 4.3 Return answers from `/chat`

## 5. Tools

- [ ] 5.1 Create `tools.py`
- [ ] 5.2 Add `handle_tool_call()`
- [ ] 5.3 Integrate into chain
- [ ] 5.4 Create `pushover_alerts.py`

## 6. React Frontend

- [ ] 6.1 Scaffold with CRA
- [ ] 6.2 Build `ChatWindow`
- [ ] 6.3 Create `api/chat.js`
- [ ] 6.4 Connect input to backend

## 7. Testing

- [ ] 7.1 Verify PDF ingestion
- [ ] 7.2 Verify answer flow
- [ ] 7.3 Trigger tool logic

## 8. Deployment

- [ ] 8.1 Vercel (frontend)
- [ ] 8.2 Render/Railway (backend)
- [ ] 8.3 Point React API to backend

## 9. Documentation

- [ ] 9.1 Add README.md
- [ ] 9.2 Document .env and secrets
- [x] 9.3 Setup pyproject.toml for UV
