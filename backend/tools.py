"""
Tools for Alexa - Member Support Agent
Implements send_notification, record_user_details, log_unknown_question, search_knowledge_base
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from langchain_core.tools import tool
from langchain.tools.retriever import create_retriever_tool
from pushover_alerts import push
from document_pipeline import DocumentPipeline

# Initialize document pipeline for retriever tool
_document_pipeline = DocumentPipeline()

# Check if vector database needs to be populated
try:
    _retriever = _document_pipeline.get_retriever()
    # Test if the vector database has documents by checking the vectorstore directly
    vectorstore = _document_pipeline.vectorstore
    if not vectorstore:
        # Try to load existing vectorstore
        from langchain_openai import OpenAIEmbeddings
        from langchain_chroma import Chroma
        embeddings = OpenAIEmbeddings()
        vectorstore = Chroma(persist_directory=_document_pipeline.db_name, embedding_function=embeddings)
        _document_pipeline.vectorstore = vectorstore
    
    # Check if vectorstore has documents
    doc_count = vectorstore._collection.count() if vectorstore else 0
    if doc_count == 0:
        print("Vector database is empty, processing documents...")
        _document_pipeline.process_documents()
        _retriever = _document_pipeline.get_retriever()
    else:
        print(f"Vector database loaded with {doc_count} documents")
        
except Exception as e:
    print(f"Vector database not found or empty, processing documents: {e}")
    _document_pipeline.process_documents()
    _retriever = _document_pipeline.get_retriever()

# Create retriever tool using LangChain's create_retriever_tool
search_knowledge_base = create_retriever_tool(
    retriever=_retriever,
    name="search_knowledge_base",
    description="Search the credit union knowledge base for relevant information. Use this to find answers about credit union services."
)

@tool
def send_notification(original_request: str, issue_type: str, session_id: str = "", contact_name: str = "", contact_email: str = "", contact_phone: str = "") -> Dict[str, Any]:
    """Send notification for escalation with conversation context. Use when user needs escalation for loan, card, account, fraud, or refinance issues. ONLY call this AFTER record_user_details has been successfully executed."""
    print(f"DEBUG: send_notification called with issue_type='{issue_type}', session_id='{session_id}', contact_name='{contact_name}', contact_email='{contact_email}'")
    try:
        # Validate issue_type
        valid_types = ["loan", "card", "account", "fraud", "refinance"]
        if issue_type not in valid_types:
            return {"status": "error", "message": f"Invalid issue_type. Must be one of: {valid_types}"}
        
        # Check if session_id is provided
        if not session_id:
            return {"status": "error", "message": "Session ID is required for escalation notification"}
        
        # Check if contact information is provided
        if not contact_name or not contact_email:
            return {"status": "error", "message": "Contact information (name and email) is required. Please call record_user_details first to capture user details."}
        
        # Import database models
        from database import EscalationCRUD, EscalationCreate, ConversationCRUD, UserCRUD
        
        # Get conversation context if session_id provided
        conversation_context = ""
        escalation_id = None
        
        if session_id:
            # Find the user for this session
            anonymous_email = f"anonymous_{session_id}@demo.com"
            user = UserCRUD.get_by_email(anonymous_email)
            
            if not user:
                return {"status": "error", "message": "No user found for this session. Please call record_user_details first."}
            
            # Get user's conversations
            conversations = ConversationCRUD.get_by_user(user.id)
            if conversations:
                latest_conversation = conversations[-1]  # Most recent conversation
                
                # Create escalation record
                escalation = EscalationCRUD.create(EscalationCreate(
                    conversation_id=latest_conversation.id,
                    issue_type=issue_type,
                    original_request=original_request
                ))
                escalation_id = escalation.id
                
                # Get conversation messages for context
                from database import MessageCRUD
                messages = MessageCRUD.get_by_conversation(latest_conversation.id)
                if messages:
                    conversation_context = "\n".join([f"{msg.content}" for msg in messages[-5:]])  # Last 5 messages
        
        # Create contact_info dictionary from individual parameters
        contact_info = {
            "name": contact_name,
            "email": contact_email,
            "phone": contact_phone
        }
        
        # Create enhanced notification message with context
        message = f"ESCALATION: {issue_type.upper()}\nRequest: {original_request}\nContact: {contact_info}"
        if conversation_context:
            message += f"\n\nConversation Context:\n{conversation_context}"
        if escalation_id:
            message += f"\n\nEscalation ID: {escalation_id}"
            
        title = f"Member Support - {issue_type.title()} Issue"
        
        # Send Pushover notification
        push_success = push(message, title)
        
        # Update escalation record with notification status
        if escalation_id and push_success:
            EscalationCRUD.update(escalation_id, {"status": "notified"})
        
        if push_success:
            result = {"status": "success", "message": f"Notification sent for {issue_type} issue", "escalation_id": escalation_id}
            print(f"DEBUG: send_notification success - escalation {escalation_id}")
            return result
        else:
            result = {"status": "error", "message": f"Failed to send Pushover notification for {issue_type} issue"}
            print(f"DEBUG: send_notification failed")
            return result
        
    except Exception as e:
        result = {"status": "error", "message": f"Failed to send notification: {str(e)}"}
        print(f"DEBUG: send_notification error: {str(e)}")
        return result

@tool
def record_user_details(name: str = "", email: str = "", phone: str = "", notes: str = "", session_id: str = "") -> Dict[str, Any]:
    """Record user contact information for follow-up. Updates anonymous user with real details. Use when user provides any contact information."""
    print(f"DEBUG: record_user_details called with name='{name}', email='{email}', phone='{phone}', session_id='{session_id}'")
    try:
        if not session_id:
            return {"status": "error", "message": "Session ID is required to update user details"}
        
        # Import database models
        from database import UserCRUD, UserUpdate
        
        # Find the anonymous user for this session
        anonymous_email = f"anonymous_{session_id}@demo.com"
        user = UserCRUD.get_by_email(anonymous_email)
        
        if not user:
            return {"status": "error", "message": "No user found for this session"}
        
        # Update user with real details
        update_data = {}
        if name:
            update_data["name"] = name
        # Update user with real details (keep email for session lookup)
        update_data = {}
        if name:
            update_data["name"] = name
        
        # Create UserUpdate model with the data
        user_update = UserUpdate(**update_data)
        updated_user = UserCRUD.update(user.id, user_update)
        
        if not updated_user:
            return {"status": "error", "message": "Failed to update user details"}
        
        # Store contact info for escalation (email and phone will be passed to send_notification)
        print(f"DEBUG: Contact info stored - Name: {name}, Email: {email}, Phone: {phone}")
        
        result = {"status": "success", "message": f"User details updated successfully for {updated_user.name}"}
        print(f"DEBUG: record_user_details success - updated user {updated_user.id}")
        return result
        
    except Exception as e:
        result = {"status": "error", "message": f"Failed to record user details: {str(e)}"}
        print(f"DEBUG: record_user_details error: {str(e)}")
        return result

@tool
def log_unknown_question(question: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Log questions that cannot be answered from knowledge base. Use when you cannot find information to answer user's question."""
    try:
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "context": context or {},
            "status": "unanswered"
        }
        
        # Save to logs directory
        logs_dir = "data/logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        filename = f"unknown_question_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(logs_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(log_entry, f, indent=2)
        
        return {"status": "success", "message": "Unknown question logged successfully"}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to log unknown question: {str(e)}"} 