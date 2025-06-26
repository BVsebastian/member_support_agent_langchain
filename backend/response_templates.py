"""
Response templates for Alexa - Member Support Agent
"""

def get_welcome_response():
    """Standard welcome message"""
    return "Hello! I'm Alexa, your Member Support Agent at Horizon Bay Credit Union. How can I assist you today?"

def get_escalation_response(issue_type: str):
    """Standard escalation message"""
    return f"I understand your {issue_type} concern. I'll connect you with a specialist. Can you provide your contact information (name, email, phone) so they can reach you?"

def get_knowledge_not_found_response(topic: str):
    """Response when knowledge not available"""
    return f"I don't have specific information about {topic} in my knowledge base. I'd be happy to connect you with a member service representative who can help. You can reach them at 1-888-HBCU-HELP." 