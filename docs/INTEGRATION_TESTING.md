# 🧪 Integration Testing Guide

This guide covers comprehensive testing of the Member Support Agent system, including backend, frontend, database, and escalation flow testing.

## 📋 Testing Overview

### Test Categories

1. **Backend API Testing**: FastAPI endpoints and responses
2. **Database Integration**: Supabase CRUD operations
3. **AI Agent Testing**: LangChain agent and tool execution
4. **Escalation Flow Testing**: End-to-end escalation scenarios
5. **Frontend Integration**: React app and API communication
6. **Deployment Testing**: Production environment verification

## 🔧 Backend Testing

### Running Backend Tests

```bash
cd backend

# Run all tests
uv run pytest

# Run specific test categories
uv run pytest tests/test_crud_operations.py -v
uv run pytest tests/test_tools.py -v
uv run pytest tests/test_pushover.py -v

# Run with coverage
uv run pytest --cov=. --cov-report=html
```

### Test Coverage

#### Database Operations (14 tests)

```bash
# Test CRUD operations
uv run pytest tests/test_crud_operations.py::test_create_user -v
uv run pytest tests/test_crud_operations.py::test_get_user_by_id -v
uv run pytest tests/test_crud_operations.py::test_update_user -v
uv run pytest tests/test_crud_operations.py::test_delete_user -v
```

**Expected Results:**

- ✅ All 14 database tests pass
- ✅ Foreign key constraints respected
- ✅ Data validation working
- ✅ Cleanup operations successful

#### Tool Testing

```bash
# Test notification system
uv run pytest tests/test_pushover.py -v

# Test tool execution
uv run pytest tests/test_tools.py -v
```

**Expected Results:**

- ✅ Pushover notifications sent successfully
- ✅ Tool calls execute in correct order
- ✅ Error handling works properly
- ✅ Session management functional

## 🤖 AI Agent Testing

### Agent Functionality Tests

```bash
# Test agent responses
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I open a new account?", "user_id": "test_user"}'
```

**Test Scenarios:**

1. **Basic Questions**

   ```json
   {
     "message": "What are your hours?",
     "user_id": "test_user"
   }
   ```

2. **Knowledge Base Queries**

   ```json
   {
     "message": "Tell me about loan options",
     "user_id": "test_user"
   }
   ```

3. **Escalation Triggers**
   ```json
   {
     "message": "I need to speak to someone about fraud",
     "user_id": "test_user"
   }
   ```

### Expected Agent Behavior

- ✅ **Knowledge Base Responses**: Accurate answers from PDF documentation
- ✅ **Conversation Memory**: Remembers previous context
- ✅ **Escalation Detection**: Identifies when human help needed
- ✅ **Tool Execution**: Calls appropriate tools automatically
- ✅ **Error Handling**: Graceful handling of edge cases

## 🚨 Escalation Flow Testing

### End-to-End Escalation Test

1. **Start Conversation**

   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "I think there is fraud on my account", "user_id": "fraud_test"}'
   ```

2. **Provide Contact Information**

   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "My name is John Doe, email is john@example.com, phone is 555-1234", "user_id": "fraud_test"}'
   ```

3. **Verify Database Records**

   ```sql
   -- Check user record
   SELECT * FROM users WHERE email = 'john@example.com';

   -- Check escalation record
   SELECT * FROM escalations WHERE issue_type = 'fraud';
   ```

### Escalation Test Checklist

- ✅ **Trigger Detection**: Agent identifies escalation keywords
- ✅ **Contact Capture**: User details stored correctly
- ✅ **Notification Sent**: Pushover alert delivered
- ✅ **Database Records**: Escalation record created
- ✅ **Conversation Context**: Full context preserved
- ✅ **Session Management**: Anonymous session handled properly

## 🌐 Frontend Integration Testing

### Local Development Testing

```bash
# Start backend
cd backend
uv run python main.py

# Start frontend (in new terminal)
cd frontend
npm run dev
```

### Frontend Test Scenarios

1. **Basic Chat Flow**

   - Send message via UI
   - Verify response appears
   - Check typing indicator
   - Test auto-scroll

2. **Error Handling**

   - Test network errors
   - Verify error messages
   - Check loading states

3. **Responsive Design**
   - Test on mobile viewport
   - Verify desktop layout
   - Check message bubbles

### Frontend Test Commands

```bash
cd frontend

# Run tests
npm test

# Build for production
npm run build

# Check for linting errors
npm run lint
```

## 🗄️ Database Integration Testing

### Supabase Connection Test

```bash
cd backend
uv run python -c "
from database import supabase
try:
    result = supabase.table('users').select('*').limit(1).execute()
    print('✅ Supabase connection successful')
except Exception as e:
    print(f'❌ Supabase connection failed: {e}')
"
```

### Database Schema Verification

```sql
-- Check table structure
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;

-- Verify foreign key relationships
SELECT
    tc.table_name,
    kcu.column_name,
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name
WHERE constraint_type = 'FOREIGN KEY';
```

## 🚀 Deployment Testing

### Railway Backend Testing

```bash
# Test production backend
curl -X GET https://your-railway-app.railway.app/ping

# Test chat endpoint
curl -X POST https://your-railway-app.railway.app/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "deployment_test"}'
```

### Vercel Frontend Testing

1. **Visit deployed URL**: `https://your-app.vercel.app`
2. **Test chat functionality**: Send test messages
3. **Verify API communication**: Check network tab
4. **Test error handling**: Disconnect backend temporarily

### Environment Variable Verification

```bash
# Backend environment check
curl -X GET https://your-railway-app.railway.app/ping

# Frontend environment check
# Visit your Vercel app and check browser console for errors
```

## 📊 Performance Testing

### Load Testing

```bash
# Install Apache Bench (if available)
ab -n 100 -c 10 -H "Content-Type: application/json" \
  -p test_data.json \
  http://localhost:8000/chat
```

### Response Time Monitoring

```bash
# Test response times
time curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test message", "user_id": "perf_test"}'
```

## 🐛 Debugging Common Issues

### Backend Issues

1. **Database Connection Errors**

   ```bash
   # Check environment variables
   echo $SUPABASE_URL
   echo $SUPABASE_KEY

   # Test connection
   uv run python -c "from database import supabase; print('Connected')"
   ```

2. **OpenAI API Errors**

   ```bash
   # Check API key
   echo $OPENAI_API_KEY

   # Test API call
   uv run python -c "
   import openai
   openai.api_key = '$OPENAI_API_KEY'
   try:
       response = openai.chat.completions.create(
           model='gpt-4',
           messages=[{'role': 'user', 'content': 'Hello'}],
           max_tokens=10
       )
       print('✅ OpenAI API working')
   except Exception as e:
       print(f'❌ OpenAI API error: {e}')
   "
   ```

### Frontend Issues

1. **CORS Errors**

   - Check `CORS_ORIGINS` in backend
   - Verify frontend URL is included
   - Check browser console for errors

2. **API Communication Errors**
   - Verify `VITE_API_BASE_URL` is correct
   - Check network tab in browser dev tools
   - Test API endpoint directly

## 📝 Test Documentation

### Test Results Template

```markdown
## Test Session: [Date]

### Backend Tests

- [ ] Database CRUD operations: [PASS/FAIL]
- [ ] Tool execution: [PASS/FAIL]
- [ ] Agent responses: [PASS/FAIL]
- [ ] Escalation flow: [PASS/FAIL]

### Frontend Tests

- [ ] Chat interface: [PASS/FAIL]
- [ ] API communication: [PASS/FAIL]
- [ ] Error handling: [PASS/FAIL]
- [ ] Responsive design: [PASS/FAIL]

### Deployment Tests

- [ ] Railway backend: [PASS/FAIL]
- [ ] Vercel frontend: [PASS/FAIL]
- [ ] Environment variables: [PASS/FAIL]

### Issues Found

- [List any issues discovered]

### Next Steps

- [List actions needed]
```

## 🎯 Continuous Testing

### Automated Testing Setup

```bash
# Create test script
cat > run_tests.sh << 'EOF'
#!/bin/bash
echo "🧪 Running Member Support Agent Tests..."

# Backend tests
echo "Testing backend..."
cd backend && uv run pytest -v

# Frontend tests
echo "Testing frontend..."
cd ../frontend && npm test

# Integration tests
echo "Testing integration..."
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test", "user_id": "automated_test"}'

echo "✅ All tests completed"
EOF

chmod +x run_tests.sh
```

### Pre-Deployment Checklist

- [ ] All backend tests pass
- [ ] Frontend builds successfully
- [ ] Database migrations applied
- [ ] Environment variables configured
- [ ] API endpoints responding
- [ ] Escalation flow tested
- [ ] Documentation updated

---

**Next Steps**: After completing integration testing, proceed to [Deployment Guide](DEPLOYMENT.md) for production deployment instructions.
