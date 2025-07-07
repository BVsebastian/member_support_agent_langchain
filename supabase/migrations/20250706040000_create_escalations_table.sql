-- Create escalations table
CREATE TABLE IF NOT EXISTS escalations (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    issue_type VARCHAR(50) NOT NULL CHECK (issue_type IN ('loan', 'card', 'account', 'fraud', 'refinance')),
    original_request TEXT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'notified', 'in_progress', 'resolved')),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- Create index for faster lookups
CREATE INDEX IF NOT EXISTS idx_escalations_conversation_id ON escalations(conversation_id);
CREATE INDEX IF NOT EXISTS idx_escalations_status ON escalations(status);
CREATE INDEX IF NOT EXISTS idx_escalations_issue_type ON escalations(issue_type);

-- Add comments for documentation
COMMENT ON TABLE escalations IS 'Tracks escalation requests from chat conversations';
COMMENT ON COLUMN escalations.conversation_id IS 'Reference to the conversation that triggered escalation';
COMMENT ON COLUMN escalations.issue_type IS 'Type of issue requiring escalation';
COMMENT ON COLUMN escalations.original_request IS 'Original user request that triggered escalation';
COMMENT ON COLUMN escalations.status IS 'Current status of the escalation';
COMMENT ON COLUMN escalations.created_at IS 'When the escalation was created';
COMMENT ON COLUMN escalations.resolved_at IS 'When the escalation was resolved (if applicable)'; 