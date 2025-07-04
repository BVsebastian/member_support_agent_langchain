# Member Support Agent

This project is the Member Support Agent system for Horizon Bay Credit Union. It provides an AI-powered assistant to help credit union members with FAQs, issue escalation, and information routing.

## Project Overview

The Member Support Agent is designed to assist credit union members by answering FAQs, escalating issues, and routing information to the right support channels using AI.

## Architecture

The system consists of a React-based frontend and a FastAPI backend. The frontend is deployed on Vercel, and the backend is deployed on Railway.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```bash
   cd member_support_agent_langchain
   ```
3. Install backend dependencies:
   ```bash
   cd backend
   uv sync
   ```
4. Install frontend dependencies:
   ```bash
   cd ../frontend
   npm install
   ```

## Usage

To start the backend server:

```bash
uv run python backend/main.py
```

To start the frontend development server:

```bash
cd frontend
npm run dev
```

## Deployment

The frontend is deployed on Vercel, and the backend is deployed on Railway. Ensure the `VITE_API_BASE_URL` is set correctly in the environment variables for production.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## Contact Information

For questions or support, please contact the project maintainer at benedict.sebastian@example.com.
