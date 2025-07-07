# 🤖 Member Support Agent - Horizon Bay Credit Union

[![Deploy Frontend](https://img.shields.io/badge/Frontend-Vercel-blue?style=flat-square&logo=vercel)](https://vercel.com)
[![Deploy Backend](https://img.shields.io/badge/Backend-Railway-green?style=flat-square&logo=railway)](https://railway.app)
[![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)](https://python.org)
[![React](https://img.shields.io/badge/React-18+-blue?style=flat-square&logo=react)](https://reactjs.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)

An AI-powered conversational agent for Horizon Bay Credit Union that provides instant support to members by answering FAQs, escalating issues, and routing information using LangChain and RAG (Retrieval-Augmented Generation).

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Contributing](#-contributing)

## 🎯 Overview

The Member Support Agent (Alexa) is designed to assist credit union members by:

- **Answering FAQs** from internal documentation using AI-powered RAG
- **Escalating complex issues** to human representatives when needed
- **Recording user details** for follow-up support
- **Sending real-time notifications** for urgent matters
- **Maintaining conversation context** across multiple interactions

### Key Technologies

- **Backend**: FastAPI + LangChain + OpenAI + ChromaDB + Supabase
- **Frontend**: React + Vite + TailwindCSS + Axios
- **AI/ML**: OpenAI GPT-4, OpenAI Embeddings, RAG Pipeline
- **Database**: Supabase (PostgreSQL) for user data, ChromaDB for vector storage
- **Deployment**: Railway (Backend), Vercel (Frontend)

## ✨ Features

### 🤖 AI Assistant (Alexa)

- **Conversational AI**: Multi-turn conversations with memory
- **Professional Tone**: Credit union representative personality
- **Knowledge Base**: Answers from internal PDF documentation
- **Context Awareness**: Remembers previous conversation context

### 📚 RAG-Powered Knowledge Retrieval

- **PDF Processing**: Automatic loading and chunking of documents
- **Vector Search**: Semantic search through knowledge base
- **Real-time Updates**: Dynamic retrieval of relevant information
- **High Accuracy**: Contextual answers from official documentation

### 🛠️ Smart Tool System

- **Automatic Escalation**: Detects when human assistance is needed
- **User Recording**: Captures member details for follow-up
- **Notification System**: Real-time alerts via Pushover
- **Question Logging**: Tracks unanswered questions for improvement

### 🌐 Modern Web Interface

- **Responsive Design**: Works on desktop and mobile devices
- **Real-time Chat**: Instant message exchange
- **Professional UI**: Credit union branding and styling
- **Error Handling**: Graceful error states and loading indicators

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend│    │  FastAPI Backend│    │   External APIs │
│   (Vercel)      │◄──►│   (Railway)     │◄──►│   (OpenAI, etc.)│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │   Databases     │
                       │ ┌─────────────┐ │
                       │ │   Supabase  │ │
                       │ │(PostgreSQL) │ │
                       │ └─────────────┘ │
                       │ ┌─────────────┐ │
                       │ │   ChromaDB  │ │
                       │ │(Vector DB)  │ │
                       │ └─────────────┘ │
                       └─────────────────┘
```

### Backend Components

- **`main.py`**: FastAPI application with REST endpoints
- **`chat_chain.py`**: LangChain AgentExecutor with tool integration
- **`document_pipeline.py`**: PDF processing and vector storage
- **`tools.py`**: Custom tools for escalation and logging
- **`database.py`**: Supabase CRUD operations
- **`prompt_manager.py`**: AI system prompts and identity

### Frontend Components

- **`App.jsx`**: Main application component
- **`ChatWindow.jsx`**: Chat interface with message history
- **`api/chat.js`**: API client for backend communication

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 16+
- UV package manager
- OpenAI API key
- Supabase account

### 1. Clone the Repository

```bash
git clone <repository-url>
cd member_support_agent_langchain
```

### 2. Backend Setup

```bash
# Install Python dependencies
cd backend
uv sync

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

### 3. Frontend Setup

```bash
# Install Node.js dependencies
cd frontend
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your backend URL
```

### 4. Run the Application

```bash
# Terminal 1: Start backend
cd backend
uv run python main.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

Visit `http://localhost:5174` to access the application.

## 📦 Installation

### Detailed Backend Setup

1. **Install UV Package Manager** (if not already installed):

   ```bash
   pip install uv
   ```

2. **Install Dependencies**:

   ```bash
   cd backend
   uv sync
   ```

3. **Set Up Environment Variables**:
   Create a `.env` file in the root directory:

   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here

   # Supabase Configuration
   SUPABASE_URL=your_supabase_url_here
   SUPABASE_KEY=your_supabase_anon_key_here

   # Pushover Notifications (Optional)
   PUSHOVER_TOKEN=your_pushover_token_here
   PUSHOVER_USER=your_pushover_user_here

   # CORS Configuration
   CORS_ORIGINS=http://localhost:5174,https://your-frontend-domain.vercel.app
   ```

### Detailed Frontend Setup

1. **Install Dependencies**:

   ```bash
   cd frontend
   npm install
   ```

2. **Configure API Endpoint**:
   Create a `.env` file in the frontend directory:
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   ```

## ⚙️ Configuration

### Environment Variables

| Variable         | Description                  | Required | Default |
| ---------------- | ---------------------------- | -------- | ------- |
| `OPENAI_API_KEY` | OpenAI API key for AI models | Yes      | -       |
| `SUPABASE_URL`   | Supabase project URL         | Yes      | -       |
| `SUPABASE_KEY`   | Supabase anonymous key       | Yes      | -       |
| `PUSHOVER_TOKEN` | Pushover app token           | No       | -       |
| `PUSHOVER_USER`  | Pushover user key            | No       | -       |
| `CORS_ORIGINS`   | Allowed CORS origins         | No       | `*`     |

### Knowledge Base Setup

1. **Add PDF Documents**:
   Place your credit union documentation in `data/knowledge_base/`:

   ```
   data/knowledge_base/
   ├── account_services.pdf
   ├── loan_guidelines.pdf
   ├── member_benefits.pdf
   └── security_policies.pdf
   ```

2. **Process Documents**:
   ```bash
   cd backend
   uv run python document_pipeline.py
   ```

## 📚 API Documentation

### Core Endpoints

#### `POST /chat`

Main chat endpoint for AI interactions.

**Request:**

```json
{
  "message": "How do I open a new account?",
  "user_id": "user123"
}
```

**Response:**

```json
{
  "response": "To open a new account at Horizon Bay Credit Union...",
  "status": "success"
}
```

#### `GET /ping`

Health check endpoint.

**Response:**

```json
{
  "status": "ok",
  "message": "Member Support Agent API is running"
}
```

### Database Endpoints

#### Users

- `POST /users/` - Create user
- `GET /users/{user_id}` - Get user by ID
- `GET /users/email/{email}` - Get user by email
- `PUT /users/{user_id}` - Update user
- `DELETE /users/{user_id}` - Delete user

#### Conversations

- `POST /conversations/` - Create conversation
- `GET /conversations/{conversation_id}` - Get conversation
- `GET /users/{user_id}/conversations` - Get user conversations
- `PUT /conversations/{conversation_id}` - Update conversation
- `DELETE /conversations/{conversation_id}` - Delete conversation

#### Messages

- `POST /messages/` - Create message
- `GET /conversations/{conversation_id}/messages` - Get conversation messages
- `PUT /messages/{message_id}` - Update message
- `DELETE /messages/{message_id}` - Delete message

### Interactive API Documentation

When running the backend locally, visit `http://localhost:8000/docs` for interactive API documentation powered by Swagger UI.

## 🔧 Development

### Project Structure

```
member_support_agent_langchain/
├── backend/                    # FastAPI backend
│   ├── main.py                # FastAPI application
│   ├── chat_chain.py          # LangChain agent setup
│   ├── document_pipeline.py   # PDF processing
│   ├── tools.py               # Custom tools
│   ├── database.py            # Supabase operations
│   ├── prompt_manager.py      # AI prompts
│   └── config/                # Configuration files
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── App.jsx           # Main app component
│   │   ├── components/       # React components
│   │   └── api/              # API client
│   ├── package.json          # Node.js dependencies
│   └── vite.config.js        # Vite configuration
├── data/                      # Data storage
│   ├── knowledge_base/        # PDF documents
│   ├── vector_db/            # ChromaDB storage
│   └── logs/                 # Application logs
├── tests/                     # Test files
├── docs/                      # Documentation
└── requirements.txt           # Python dependencies
```

### Running Tests

```bash
# Backend tests
cd backend
uv run pytest

# Frontend tests
cd frontend
npm test
```

### Code Style

- **Python**: Follow PEP 8 guidelines
- **JavaScript**: Use ESLint configuration
- **TypeScript**: Strict mode enabled

## 🚀 Deployment

### Backend Deployment (Railway)

1. **Connect Repository**:

   - Link your GitHub repository to Railway
   - Set the root directory to `backend/`

2. **Configure Environment Variables**:

   ```env
   OPENAI_API_KEY=your_key
   SUPABASE_URL=your_url
   SUPABASE_KEY=your_key
   PUSHOVER_TOKEN=your_token
   PUSHOVER_USER=your_user
   CORS_ORIGINS=https://your-frontend-domain.vercel.app
   ```

3. **Deploy**:
   - Railway will automatically deploy on push to main branch
   - Monitor logs for any issues

### Frontend Deployment (Vercel)

1. **Connect Repository**:

   - Link your GitHub repository to Vercel
   - Set the root directory to `frontend/`

2. **Configure Environment Variables**:

   ```env
   VITE_API_BASE_URL=https://your-railway-backend-url
   ```

3. **Deploy**:
   - Vercel will automatically deploy on push to main branch
   - Your app will be available at `https://your-app.vercel.app`

### Production Checklist

- [ ] Environment variables configured
- [ ] CORS origins set correctly
- [ ] Knowledge base documents uploaded
- [ ] Vector database initialized
- [ ] API endpoints tested
- [ ] Frontend-backend communication verified

## 🧪 Testing

### Backend Testing

```bash
cd backend

# Run all tests
uv run pytest

# Run specific test file
uv run pytest tests/test_tools.py

# Run with coverage
uv run pytest --cov=.
```

### Frontend Testing

```bash
cd frontend

# Run tests
npm test

# Run tests in watch mode
npm test -- --watch
```

### Integration Testing

```bash
# Test API endpoints
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test"}'
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow the coding protocol
4. **Add tests**: Ensure new features are tested
5. **Commit changes**: `git commit -m 'Add amazing feature'`
6. **Push to branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Guidelines

- Follow the [Coding Protocol](docs/Coding_Protocol.md)
- Write tests for new features
- Update documentation as needed
- Keep commits focused and descriptive

## 📞 Support

For questions or support:

- **Email**: benedict.sebastian@example.com
- **Issues**: Create an issue on GitHub
- **Documentation**: Check the `docs/` folder

## 📄 License

This project is proprietary software for Horizon Bay Credit Union.

---

**Built with ❤️ for Horizon Bay Credit Union**
