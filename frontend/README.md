# Member Support Agent - Frontend

This project is part of the Member Support Agent system for Horizon Bay Credit Union. It provides a React-based frontend for interacting with the AI-powered support agent.

## Project Overview

The Member Support Agent is designed to assist credit union members by answering FAQs, escalating issues, and routing information to the right support channels using AI.

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the frontend directory:
   ```bash
   cd member_support_agent_langchain/frontend
   ```
3. Install dependencies:
   ```bash
   npm install
   ```

## Usage

To start the development server:

```bash
npm run dev
```

## Deployment

The frontend is deployed on Vercel, and the backend is deployed on Railway. Ensure the `VITE_API_BASE_URL` is set correctly in the environment variables for production.

## Contact Information

For questions or support, please contact the project maintainer at benedict.sebastian@example.com.

# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
