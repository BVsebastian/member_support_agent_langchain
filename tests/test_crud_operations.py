import sys
from pathlib import Path
import uuid

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

import pytest
from database import (
    UserCRUD, UserCreate, UserUpdate,
    ConversationCRUD, ConversationCreate, ConversationUpdate,
    MessageCRUD, MessageCreate, MessageUpdate
)

@pytest.fixture
def user_data():
    # Generate unique email for each test
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"
    return {
        "email": unique_email,
        "name": "Test User"
    }

@pytest.fixture
def test_user(user_data):
    """Create a test user and clean up after test"""
    user_create = UserCreate(**user_data)
    user = UserCRUD.create(user_create)
    yield user
    # Cleanup - no need to delete here, will be handled by individual tests

@pytest.fixture
def conversation_data(test_user):
    return {
        "user_id": test_user.id
    }

@pytest.fixture
def test_conversation(conversation_data):
    """Create a test conversation and clean up after test"""
    conversation_create = ConversationCreate(**conversation_data)
    conversation = ConversationCRUD.create(conversation_create)
    yield conversation
    # Cleanup - no need to delete here, will be handled by individual tests

@pytest.fixture
def message_data(test_conversation):
    return {
        "conversation_id": test_conversation.id,
        "content": "Test message content"
    }

# User Tests
def test_create_user(user_data):
    user_create = UserCreate(**user_data)
    user = UserCRUD.create(user_create)
    assert user.email == user_data["email"]
    assert user.name == user_data["name"]
    # Clean up
    UserCRUD.delete(user.id)

def test_get_user(user_data):
    user_create = UserCreate(**user_data)
    user = UserCRUD.create(user_create)
    fetched_user = UserCRUD.get(user.id)
    assert fetched_user.email == user.email
    assert fetched_user.name == user.name
    # Clean up
    UserCRUD.delete(user.id)

def test_update_user(user_data):
    user_create = UserCreate(**user_data)
    user = UserCRUD.create(user_create)
    updated_data = UserUpdate(name="Updated User")
    updated_user = UserCRUD.update(user.id, updated_data)
    assert updated_user.name == "Updated User"
    # Clean up
    UserCRUD.delete(user.id)

def test_delete_user(user_data):
    user_create = UserCreate(**user_data)
    user = UserCRUD.create(user_create)
    result = UserCRUD.delete(user.id)
    assert result == True
    # Verify user is deleted
    deleted_user = UserCRUD.get(user.id)
    assert deleted_user is None

# Conversation Tests
def test_create_conversation():
    # Create user first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    
    # Create conversation
    conversation_data = {"user_id": user.id}
    conversation_create = ConversationCreate(**conversation_data)
    conversation = ConversationCRUD.create(conversation_create)
    assert conversation.user_id == conversation_data["user_id"]
    assert hasattr(conversation, 'id')
    assert hasattr(conversation, 'started_at')
    
    # Clean up in correct order
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)

def test_get_conversation():
    # Create user first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    
    # Create conversation
    conversation_data = {"user_id": user.id}
    conversation = ConversationCRUD.create(ConversationCreate(**conversation_data))
    
    # Test get
    fetched_conversation = ConversationCRUD.get(conversation.id)
    assert fetched_conversation.id == conversation.id
    assert fetched_conversation.user_id == conversation.user_id
    
    # Clean up in correct order
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)

def test_update_conversation():
    # Create user first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    
    # Create another user for update
    user2_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User 2"}
    user2 = UserCRUD.create(UserCreate(**user2_data))
    
    # Create conversation
    conversation_data = {"user_id": user.id}
    conversation = ConversationCRUD.create(ConversationCreate(**conversation_data))
    
    # Update conversation
    updated_data = ConversationUpdate(user_id=user2.id)
    updated_conversation = ConversationCRUD.update(conversation.id, updated_data)
    assert updated_conversation.user_id == user2.id
    
    # Clean up in correct order
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)
    UserCRUD.delete(user2.id)

def test_delete_conversation():
    # Create user first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    
    # Create conversation
    conversation_data = {"user_id": user.id}
    conversation = ConversationCRUD.create(ConversationCreate(**conversation_data))
    
    # Delete conversation
    result = ConversationCRUD.delete(conversation.id)
    assert result == True
    
    # Verify conversation is deleted
    deleted_conversation = ConversationCRUD.get(conversation.id)
    assert deleted_conversation is None
    
    # Clean up user
    UserCRUD.delete(user.id)

def test_get_conversations_by_user():
    # Create user first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    
    # Create multiple conversations for the user
    conv1_data = {"user_id": user.id}
    conv2_data = {"user_id": user.id}
    
    conv1 = ConversationCRUD.create(ConversationCreate(**conv1_data))
    conv2 = ConversationCRUD.create(ConversationCreate(**conv2_data))
    
    conversations = ConversationCRUD.get_by_user(user.id)
    assert len(conversations) >= 2
    
    # Clean up in correct order
    ConversationCRUD.delete(conv1.id)
    ConversationCRUD.delete(conv2.id)
    UserCRUD.delete(user.id)

# Message Tests
def test_create_message():
    # Create user and conversation first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    conversation = ConversationCRUD.create(ConversationCreate(user_id=user.id))
    
    # Create message
    message_data = {"conversation_id": conversation.id, "content": "Test message content"}
    message_create = MessageCreate(**message_data)
    message = MessageCRUD.create(message_create)
    assert message.conversation_id == message_data["conversation_id"]
    assert message.content == message_data["content"]
    assert hasattr(message, 'id')
    assert hasattr(message, 'sent_at')
    
    # Clean up in correct order
    MessageCRUD.delete(message.id)
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)

def test_get_message():
    # Create user and conversation first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    conversation = ConversationCRUD.create(ConversationCreate(user_id=user.id))
    
    # Create message
    message_data = {"conversation_id": conversation.id, "content": "Test message for get"}
    message = MessageCRUD.create(MessageCreate(**message_data))
    
    # Test get
    fetched_message = MessageCRUD.get(message.id)
    assert fetched_message.id == message.id
    assert fetched_message.content == message.content
    
    # Clean up in correct order
    MessageCRUD.delete(message.id)
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)

def test_update_message():
    # Create user and conversation first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    conversation = ConversationCRUD.create(ConversationCreate(user_id=user.id))
    
    # Create message
    message_data = {"conversation_id": conversation.id, "content": "Original message"}
    message = MessageCRUD.create(MessageCreate(**message_data))
    
    # Update message
    updated_data = MessageUpdate(content="Updated message")
    updated_message = MessageCRUD.update(message.id, updated_data)
    assert updated_message.content == "Updated message"
    
    # Clean up in correct order
    MessageCRUD.delete(message.id)
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)

def test_delete_message():
    # Create user and conversation first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    conversation = ConversationCRUD.create(ConversationCreate(user_id=user.id))
    
    # Create message
    message_data = {"conversation_id": conversation.id, "content": "Message to delete"}
    message = MessageCRUD.create(MessageCreate(**message_data))
    
    # Delete message
    result = MessageCRUD.delete(message.id)
    assert result == True
    
    # Verify message is deleted
    deleted_message = MessageCRUD.get(message.id)
    assert deleted_message is None
    
    # Clean up in correct order
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id)

def test_get_messages_by_conversation():
    # Create user and conversation first
    user_data = {"email": f"testuser_{uuid.uuid4().hex[:8]}@example.com", "name": "Test User"}
    user = UserCRUD.create(UserCreate(**user_data))
    conversation = ConversationCRUD.create(ConversationCreate(user_id=user.id))
    
    # Create multiple messages for the conversation
    msg1_data = {"conversation_id": conversation.id, "content": "Message 1"}
    msg2_data = {"conversation_id": conversation.id, "content": "Message 2"}
    
    msg1 = MessageCRUD.create(MessageCreate(**msg1_data))
    msg2 = MessageCRUD.create(MessageCreate(**msg2_data))
    
    messages = MessageCRUD.get_by_conversation(conversation.id)
    assert len(messages) >= 2
    
    # Clean up in correct order
    MessageCRUD.delete(msg1.id)
    MessageCRUD.delete(msg2.id)
    ConversationCRUD.delete(conversation.id)
    UserCRUD.delete(user.id) 