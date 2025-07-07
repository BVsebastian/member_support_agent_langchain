"""
Supabase Database CRUD Operations Module

This module provides a centralized interface for all database operations
using Supabase as the backend database service.
"""

import os
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables from root directory
load_dotenv(dotenv_path="../.env")

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Pydantic Models
class UserBase(BaseModel):
    email: str
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None

class User(UserBase):
    id: int

class ConversationBase(BaseModel):
    user_id: int

class ConversationCreate(ConversationBase):
    pass

class ConversationUpdate(BaseModel):
    user_id: Optional[int] = None

class Conversation(ConversationBase):
    id: int
    started_at: datetime

class MessageBase(BaseModel):
    conversation_id: int
    content: str

class MessageCreate(MessageBase):
    pass

class MessageUpdate(BaseModel):
    content: Optional[str] = None

class Message(MessageBase):
    id: int
    sent_at: datetime

class EscalationBase(BaseModel):
    conversation_id: int
    issue_type: str
    original_request: str
    status: str = "pending"

class EscalationCreate(EscalationBase):
    pass

class EscalationUpdate(BaseModel):
    status: Optional[str] = None
    resolved_at: Optional[datetime] = None

class Escalation(EscalationBase):
    id: int
    created_at: datetime
    resolved_at: Optional[datetime] = None

# CRUD Operations for Users
class UserCRUD:
    @staticmethod
    def create(user: UserCreate) -> User:
        """Create a new user"""
        response = supabase.table("users").insert(user.model_dump()).execute()
        if response.data:
            return User(**response.data[0])
        raise Exception("Failed to create user")

    @staticmethod
    def get(user_id: int) -> Optional[User]:
        """Get user by ID"""
        response = supabase.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            return User(**response.data[0])
        return None

    @staticmethod
    def get_by_email(email: str) -> Optional[User]:
        """Get user by email"""
        response = supabase.table("users").select("*").eq("email", email).execute()
        if response.data:
            return User(**response.data[0])
        return None

    @staticmethod
    def get_all() -> List[User]:
        """Get all users"""
        response = supabase.table("users").select("*").execute()
        return [User(**user) for user in response.data] if response.data else []

    @staticmethod
    def update(user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user"""
        update_data = {k: v for k, v in user_update.model_dump().items() if v is not None}
        if not update_data:
            return UserCRUD.get(user_id)
        
        response = supabase.table("users").update(update_data).eq("id", user_id).execute()
        if response.data:
            return User(**response.data[0])
        return None

    @staticmethod
    def delete(user_id: int) -> bool:
        """Delete user"""
        response = supabase.table("users").delete().eq("id", user_id).execute()
        return len(response.data) > 0 if response.data else False

# CRUD Operations for Conversations
class ConversationCRUD:
    @staticmethod
    def create(conversation: ConversationCreate) -> Conversation:
        """Create a new conversation"""
        response = supabase.table("conversations").insert(conversation.model_dump()).execute()
        if response.data:
            return Conversation(**response.data[0])
        raise Exception("Failed to create conversation")

    @staticmethod
    def get(conversation_id: int) -> Optional[Conversation]:
        """Get conversation by ID"""
        response = supabase.table("conversations").select("*").eq("id", conversation_id).execute()
        if response.data:
            return Conversation(**response.data[0])
        return None

    @staticmethod
    def get_by_user(user_id: int) -> List[Conversation]:
        """Get all conversations for a user"""
        response = supabase.table("conversations").select("*").eq("user_id", user_id).execute()
        return [Conversation(**conv) for conv in response.data] if response.data else []

    @staticmethod
    def get_all() -> List[Conversation]:
        """Get all conversations"""
        response = supabase.table("conversations").select("*").execute()
        return [Conversation(**conv) for conv in response.data] if response.data else []

    @staticmethod
    def update(conversation_id: int, conversation_update: ConversationUpdate) -> Optional[Conversation]:
        """Update conversation"""
        update_data = {k: v for k, v in conversation_update.model_dump().items() if v is not None}
        if not update_data:
            return ConversationCRUD.get(conversation_id)
        
        response = supabase.table("conversations").update(update_data).eq("id", conversation_id).execute()
        if response.data:
            return Conversation(**response.data[0])
        return None

    @staticmethod
    def delete(conversation_id: int) -> bool:
        """Delete conversation"""
        response = supabase.table("conversations").delete().eq("id", conversation_id).execute()
        return len(response.data) > 0 if response.data else False

# CRUD Operations for Messages
class MessageCRUD:
    @staticmethod
    def create(message: MessageCreate) -> Message:
        """Create a new message"""
        response = supabase.table("messages").insert(message.model_dump()).execute()
        if response.data:
            return Message(**response.data[0])
        raise Exception("Failed to create message")

    @staticmethod
    def get(message_id: int) -> Optional[Message]:
        """Get message by ID"""
        response = supabase.table("messages").select("*").eq("id", message_id).execute()
        if response.data:
            return Message(**response.data[0])
        return None

    @staticmethod
    def get_by_conversation(conversation_id: int) -> List[Message]:
        """Get all messages for a conversation"""
        response = supabase.table("messages").select("*").eq("conversation_id", conversation_id).order("sent_at").execute()
        return [Message(**msg) for msg in response.data] if response.data else []

    @staticmethod
    def get_all() -> List[Message]:
        """Get all messages"""
        response = supabase.table("messages").select("*").execute()
        return [Message(**msg) for msg in response.data] if response.data else []

    @staticmethod
    def update(message_id: int, message_update: MessageUpdate) -> Optional[Message]:
        """Update message"""
        update_data = {k: v for k, v in message_update.model_dump().items() if v is not None}
        if not update_data:
            return MessageCRUD.get(message_id)
        
        response = supabase.table("messages").update(update_data).eq("id", message_id).execute()
        if response.data:
            return Message(**response.data[0])
        return None

    @staticmethod
    def delete(message_id: int) -> bool:
        """Delete message"""
        response = supabase.table("messages").delete().eq("id", message_id).execute()
        return len(response.data) > 0 if response.data else False

# Convenience functions for common operations
def get_conversation_with_messages(conversation_id: int) -> Optional[Dict[str, Any]]:
    """Get conversation with all its messages"""
    conversation = ConversationCRUD.get(conversation_id)
    if not conversation:
        return None
    
    messages = MessageCRUD.get_by_conversation(conversation_id)
    return {
        "conversation": conversation,
        "messages": messages
    }

def create_user_conversation(user_id: int, title: str = None) -> Conversation:
    """Create a new conversation for a user"""
    conversation_data = ConversationCreate(
        user_id=user_id,
        title=title or f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
    )
    return ConversationCRUD.create(conversation_data)

def add_message_to_conversation(conversation_id: int, content: str, **kwargs) -> Message:
    """Add a message to a conversation"""
    message_data = MessageCreate(
        conversation_id=conversation_id,
        content=content,
        **kwargs
    )
    return MessageCRUD.create(message_data)

# CRUD Operations for Escalations
class EscalationCRUD:
    @staticmethod
    def create(escalation: EscalationCreate) -> Escalation:
        """Create a new escalation"""
        response = supabase.table("escalations").insert(escalation.model_dump()).execute()
        if response.data:
            return Escalation(**response.data[0])
        raise Exception("Failed to create escalation")

    @staticmethod
    def get(escalation_id: int) -> Optional[Escalation]:
        """Get escalation by ID"""
        response = supabase.table("escalations").select("*").eq("id", escalation_id).execute()
        if response.data:
            return Escalation(**response.data[0])
        return None

    @staticmethod
    def get_by_conversation(conversation_id: int) -> List[Escalation]:
        """Get all escalations for a conversation"""
        response = supabase.table("escalations").select("*").eq("conversation_id", conversation_id).execute()
        return [Escalation(**esc) for esc in response.data] if response.data else []

    @staticmethod
    def get_all() -> List[Escalation]:
        """Get all escalations"""
        response = supabase.table("escalations").select("*").execute()
        return [Escalation(**esc) for esc in response.data] if response.data else []

    @staticmethod
    def update(escalation_id: int, escalation_update: EscalationUpdate) -> Optional[Escalation]:
        """Update escalation"""
        update_data = {k: v for k, v in escalation_update.model_dump().items() if v is not None}
        if not update_data:
            return EscalationCRUD.get(escalation_id)
        
        response = supabase.table("escalations").update(update_data).eq("id", escalation_id).execute()
        if response.data:
            return Escalation(**response.data[0])
        return None

    @staticmethod
    def delete(escalation_id: int) -> bool:
        """Delete escalation"""
        response = supabase.table("escalations").delete().eq("id", escalation_id).execute()
        return len(response.data) > 0 if response.data else False 