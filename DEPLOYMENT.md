# 🚀 Deployment Guide

## Environment Variables Required

### Backend (.env)

```bash
# OpenAI API Configuration (Required)
OPENAI_API_KEY=your_openai_api_key_here

# Pushover Notifications (Optional)
PUSHOVER_TOKEN=your_pushover_app_token_here
PUSHOVER_USER_KEY=your_pushover_user_key_here

# FastAPI Configuration
PORT=8000
CORS_ORIGINS=https://your-frontend-domain.vercel.app

# Vector Database
VECTOR_DB_PATH=data/vector_db

# Logging
LOG_LEVEL=INFO
```

### Frontend (.env)

```bash
# API Base URL (Required)
VITE_API_BASE_URL=https://your-backend-domain.railway.app
```

## Platform Deployment

### Backend (Railway/Render)

1. Connect GitHub repository
2. Select `backend/` as root directory
3. Set environment variables in platform dashboard
4. Deploy using `backend/requirements.txt`

### Frontend (Vercel)

1. Connect GitHub repository
2. Select `frontend/` as root directory
3. Set build command: `npm run build`
4. Set environment variable: `VITE_API_BASE_URL`
5. Deploy

## Startup Commands

### Backend

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Frontend

```bash
cd frontend
npm run build
```
