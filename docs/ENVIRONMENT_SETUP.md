# 🔧 Environment Setup Guide

This guide covers all environment variables required for the Member Support Agent project.

## 📋 Required Environment Variables

### Backend Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# OpenAI Configuration
# Get your API key from https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_api_key_here

# Supabase Configuration
# Get these from your Supabase project settings
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_key_here

# Pushover Notifications (Optional)
# Get these from https://pushover.net/
PUSHOVER_TOKEN=your_pushover_app_token_here
PUSHOVER_USER=your_pushover_user_key_here

# CORS Configuration
# Add your frontend domain(s) for production
CORS_ORIGINS=http://localhost:5174,https://your-frontend-domain.vercel.app
```

### Frontend Configuration

Create a `.env` file in the `frontend/` directory with:

```env
# API Base URL for Frontend
# Point to your backend deployment URL
VITE_API_BASE_URL=http://localhost:8000
```

## 🔑 Getting API Keys

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key and add it to your `.env` file

### Supabase Configuration

1. Create a project at [Supabase](https://supabase.com)
2. Go to Settings → API
3. Copy the Project URL and anon/public key
4. Add them to your `.env` file

### Pushover (Optional)

1. Create an account at [Pushover](https://pushover.net/)
2. Create a new application
3. Copy the app token and user key
4. Add them to your `.env` file

## 🚀 Deployment Configuration

### Railway Backend Deployment

Set these environment variables in your Railway dashboard:

```env
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=your_supabase_anon_key
PUSHOVER_TOKEN=your_pushover_app_token
PUSHOVER_USER=your_pushover_user_key
CORS_ORIGINS=https://your-frontend-domain.vercel.app
```

### Vercel Frontend Deployment

Set this environment variable in your Vercel dashboard:

```env
VITE_API_BASE_URL=https://your-railway-backend-url
```

## 🔒 Security Best Practices

1. **Never commit `.env` files** to version control
2. **Use different API keys** for development and production
3. **Rotate keys regularly** for security
4. **Limit API key permissions** to minimum required access
5. **Monitor API usage** to prevent unexpected charges

## 🧪 Testing Environment Variables

### Backend Testing

```bash
cd backend
uv run python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = ['OPENAI_API_KEY', 'SUPABASE_URL', 'SUPABASE_KEY']
missing_vars = [var for var in required_vars if not os.getenv(var)]

if missing_vars:
    print(f'Missing required environment variables: {missing_vars}')
else:
    print('All required environment variables are set!')
"
```

### Frontend Testing

```bash
cd frontend
npm run build
# This will fail if VITE_API_BASE_URL is not set
```

## 📝 Environment Variable Reference

| Variable            | Required | Description                  | Example                   |
| ------------------- | -------- | ---------------------------- | ------------------------- |
| `OPENAI_API_KEY`    | Yes      | OpenAI API key for AI models | `sk-...`                  |
| `SUPABASE_URL`      | Yes      | Supabase project URL         | `https://xxx.supabase.co` |
| `SUPABASE_KEY`      | Yes      | Supabase anonymous key       | `eyJ...`                  |
| `PUSHOVER_TOKEN`    | No       | Pushover app token           | `azGDO...`                |
| `PUSHOVER_USER`     | No       | Pushover user key            | `uQiRz...`                |
| `CORS_ORIGINS`      | No       | Allowed CORS origins         | `http://localhost:5174`   |
| `VITE_API_BASE_URL` | Yes      | Backend API URL              | `http://localhost:8000`   |

## 🚨 Troubleshooting

### Common Issues

1. **"Missing environment variable" errors**

   - Check that `.env` files are in the correct directories
   - Verify variable names match exactly (case-sensitive)
   - Restart your development server after adding variables

2. **CORS errors in frontend**

   - Ensure `CORS_ORIGINS` includes your frontend URL
   - Check that backend is running and accessible

3. **Supabase connection errors**

   - Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
   - Check that your Supabase project is active

4. **OpenAI API errors**
   - Verify `OPENAI_API_KEY` is valid and has sufficient credits
   - Check API rate limits and usage

### Getting Help

- Check the [README.md](../README.md) for general setup instructions
- Review [DEPLOYMENT.md](../DEPLOYMENT.md) for deployment-specific guidance
- Create an issue on GitHub for persistent problems
