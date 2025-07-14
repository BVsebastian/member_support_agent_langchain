# 🗄️ Supabase Setup Guide

This guide covers the complete setup and configuration of Supabase for the Member Support Agent project.

## 📋 Overview

Supabase serves as our primary database for:

- **User Management**: Anonymous user sessions and contact information
- **Conversation Storage**: Chat history and session tracking
- **Message History**: Individual message storage with conversation context
- **Escalation Tracking**: Support ticket management and status tracking

## 🚀 Initial Setup

### 1. Create Supabase Project

1. Visit [Supabase](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - **Name**: `member-support-agent`
   - **Database Password**: Generate a strong password
   - **Region**: Choose closest to your users

### 2. Get API Credentials

1. Go to **Settings** → **API**
2. Copy the following values:

   - **Project URL**: `https://your-project-id.supabase.co`
   - **Anon/Public Key**: `eyJ...` (starts with `eyJ`)

3. Add these to your `.env` file:
   ```env
   SUPABASE_URL=https://your-project-id.supabase.co
   SUPABASE_KEY=your_anon_key_here
   ```

## 🗃️ Database Schema

### Tables Overview

The project uses four main tables:

1. **`users`** - Anonymous user sessions and contact info
2. **`conversations`** - Chat session tracking
3. **`messages`** - Individual chat messages
4. **`escalations`** - Support ticket management

### Schema Details

#### Users Table

```sql
CREATE TABLE users (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Conversations Table

```sql
CREATE TABLE conversations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Messages Table

```sql
CREATE TABLE messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Escalations Table

```sql
CREATE TABLE escalations (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    issue_type VARCHAR(50) NOT NULL,
    original_request TEXT NOT NULL,
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'notified', 'in_progress', 'resolved')),
    contact_info JSONB,
    conversation_context TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

## 🔄 Database Migrations

### Running Migrations

The project includes migration files in `supabase/migrations/`:

1. **Initial Tables** (`20250706035358_create_initial_tables.sql`)

   - Creates users, conversations, and messages tables
   - Sets up foreign key relationships
   - Adds indexes for performance

2. **Escalations Table** (`20250706040000_create_escalations_table.sql`)
   - Creates escalations table for support ticket tracking
   - Adds status tracking and conversation linking

### Applying Migrations

```bash
# Using Supabase CLI (if installed)
supabase db push

# Or manually via Supabase Dashboard:
# 1. Go to SQL Editor in your Supabase dashboard
# 2. Copy and paste each migration file
# 3. Execute the SQL commands
```

## 🔧 Integration with FastAPI

### Database Connection

The backend uses the `supabase-py` library for database operations:

```python
from supabase import create_client, Client

# Initialize client
supabase: Client = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)
```

### CRUD Operations

All database operations are handled in `backend/database.py`:

- **User Management**: Create, read, update user records
- **Conversation Tracking**: Session management and chat history
- **Message Storage**: Individual message persistence
- **Escalation Handling**: Support ticket creation and tracking

## 🧪 Testing Database Operations

### Running Tests

```bash
cd backend
uv run pytest tests/test_crud_operations.py -v
```

### Test Coverage

The test suite covers:

- ✅ User creation and retrieval
- ✅ Conversation session management
- ✅ Message storage and retrieval
- ✅ Escalation record creation
- ✅ Foreign key relationships
- ✅ Data validation and constraints

## 📊 Database Monitoring

### Supabase Dashboard

1. **Table Editor**: View and edit data directly
2. **SQL Editor**: Run custom queries
3. **Logs**: Monitor API requests and errors
4. **Analytics**: Track usage and performance

### Key Metrics to Monitor

- **Active Conversations**: Number of ongoing chat sessions
- **Escalation Rate**: Percentage of conversations requiring human support
- **Response Times**: API performance metrics
- **Error Rates**: Failed operations and their causes

## 🔒 Security Considerations

### Row Level Security (RLS)

The current implementation uses anonymous access for simplicity. For production:

1. **Enable RLS** on all tables
2. **Create policies** for anonymous access
3. **Limit permissions** to necessary operations only

### Example RLS Policy

```sql
-- Allow anonymous users to create records
CREATE POLICY "Allow anonymous insert" ON users
    FOR INSERT WITH CHECK (true);

-- Allow users to read their own data
CREATE POLICY "Allow user read own data" ON users
    FOR SELECT USING (auth.uid()::text = id::text);
```

## 🚨 Troubleshooting

### Common Issues

1. **Connection Errors**

   - Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
   - Check that your project is active
   - Ensure network connectivity

2. **Migration Failures**

   - Check SQL syntax in migration files
   - Verify table names don't conflict
   - Ensure proper foreign key relationships

3. **Data Consistency**
   - Monitor foreign key constraints
   - Check for orphaned records
   - Validate data types and constraints

### Debugging Queries

```sql
-- Check table structure
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public';

-- Monitor recent activity
SELECT * FROM conversations
ORDER BY created_at DESC
LIMIT 10;

-- Check for data integrity
SELECT c.id, COUNT(m.id) as message_count
FROM conversations c
LEFT JOIN messages m ON c.id = m.conversation_id
GROUP BY c.id;
```

## 📈 Performance Optimization

### Indexes

The schema includes indexes for common queries:

```sql
-- Conversation lookups by session_id
CREATE INDEX idx_conversations_session_id ON conversations(session_id);

-- Message lookups by conversation
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);

-- User lookups by email
CREATE INDEX idx_users_email ON users(email);
```

### Query Optimization

- Use `LIMIT` clauses for large result sets
- Implement pagination for message history
- Consider archiving old conversations
- Monitor query performance in Supabase dashboard

## 🔄 Backup and Recovery

### Automated Backups

Supabase provides automatic daily backups. For additional safety:

1. **Export Data**: Use Supabase dashboard to export tables
2. **Database Dumps**: Use `pg_dump` for complete backups
3. **Point-in-Time Recovery**: Available in Supabase Pro plans

### Recovery Procedures

1. **Data Restoration**: Import from backup files
2. **Schema Recovery**: Re-run migrations if needed
3. **Index Rebuilding**: Recreate indexes after data restoration

## 📚 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [FastAPI Database Integration](https://fastapi.tiangolo.com/tutorial/sql-databases/)
- [Row Level Security Guide](https://supabase.com/docs/guides/auth/row-level-security)

---

**Next Steps**: After setting up Supabase, proceed to [Environment Setup](ENVIRONMENT_SETUP.md) to configure your API keys and deployment settings.
