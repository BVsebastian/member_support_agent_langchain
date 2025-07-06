import os
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from chat_chain import ChatChain
from database import (
    UserCRUD, ConversationCRUD, MessageCRUD,
    UserCreate, UserUpdate, User,
    ConversationCreate, ConversationUpdate, Conversation,
    MessageCreate, MessageUpdate, Message,
    get_conversation_with_messages, create_user_conversation, add_message_to_conversation
)

# Load environment variables from root directory
load_dotenv(dotenv_path="../.env")

app = FastAPI(title="Member Support Agent API")

# Get CORS origins from environment or use default for development
cors_origins = os.getenv("CORS_ORIGINS", "*").split(",")

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the chat chain
chat_chain = ChatChain()

# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    status: str = "success"

@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"status": "ok", "message": "Member Support Agent API is running"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat endpoint that accepts messages and returns responses"""
    response = chat_chain.get_response(request.message)
    return ChatResponse(
        response=response
    )

# User CRUD Endpoints
@app.post("/users/", response_model=User)
async def create_user(user: UserCreate):
    """Create a new user"""
    try:
        return UserCRUD.create(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get a user by ID"""
    user = UserCRUD.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/", response_model=List[User])
async def get_all_users():
    """Get all users"""
    return UserCRUD.get_all()

@app.get("/users/email/{email}", response_model=User)
async def get_user_by_email(email: str):
    """Get a user by email"""
    user = UserCRUD.get_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user_update: UserUpdate):
    """Update a user"""
    user = UserCRUD.update(user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Delete a user"""
    success = UserCRUD.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# Conversation CRUD Endpoints
@app.post("/conversations/", response_model=Conversation)
async def create_conversation(conversation: ConversationCreate):
    """Create a new conversation"""
    try:
        return ConversationCRUD.create(conversation)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(conversation_id: int):
    """Get a conversation by ID"""
    conversation = ConversationCRUD.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.get("/conversations/", response_model=List[Conversation])
async def get_all_conversations():
    """Get all conversations"""
    return ConversationCRUD.get_all()

@app.get("/users/{user_id}/conversations", response_model=List[Conversation])
async def get_user_conversations(user_id: int):
    """Get all conversations for a user"""
    return ConversationCRUD.get_by_user(user_id)

@app.put("/conversations/{conversation_id}", response_model=Conversation)
async def update_conversation(conversation_id: int, conversation_update: ConversationUpdate):
    """Update a conversation"""
    conversation = ConversationCRUD.update(conversation_id, conversation_update)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

@app.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int):
    """Delete a conversation"""
    success = ConversationCRUD.delete(conversation_id)
    if not success:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"message": "Conversation deleted successfully"}

# Message CRUD Endpoints
@app.post("/messages/", response_model=Message)
async def create_message(message: MessageCreate):
    """Create a new message"""
    try:
        return MessageCRUD.create(message)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/messages/{message_id}", response_model=Message)
async def get_message(message_id: int):
    """Get a message by ID"""
    message = MessageCRUD.get(message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.get("/messages/", response_model=List[Message])
async def get_all_messages():
    """Get all messages"""
    return MessageCRUD.get_all()

@app.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_conversation_messages(conversation_id: int):
    """Get all messages for a conversation"""
    return MessageCRUD.get_by_conversation(conversation_id)

@app.put("/messages/{message_id}", response_model=Message)
async def update_message(message_id: int, message_update: MessageUpdate):
    """Update a message"""
    message = MessageCRUD.update(message_id, message_update)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    return message

@app.delete("/messages/{message_id}")
async def delete_message(message_id: int):
    """Delete a message"""
    success = MessageCRUD.delete(message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message not found")
    return {"message": "Message deleted successfully"}

# Convenience Endpoints
@app.get("/conversations/{conversation_id}/full")
async def get_conversation_with_all_messages(conversation_id: int):
    """Get a conversation with all its messages"""
    result = get_conversation_with_messages(conversation_id)
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return result

@app.post("/users/{user_id}/conversations", response_model=Conversation)
async def create_user_conversation_endpoint(user_id: int, title: Optional[str] = None):
    """Create a new conversation for a user"""
    try:
        return create_user_conversation(user_id, title)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/conversations/{conversation_id}/messages", response_model=Message)
async def add_message_to_conversation_endpoint(conversation_id: int, content: str, topic: Optional[str] = None, private: bool = False):
    """Add a message to a conversation"""
    try:
        return add_message_to_conversation(conversation_id, content, topic=topic, private=private)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 