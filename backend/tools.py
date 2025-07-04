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
def send_notification(original_request: str, issue_type: str, contact_name: str = "", contact_email: str = "", contact_phone: str = "") -> Dict[str, Any]:
    """Send notification for escalation. Use when user needs escalation for loan, card, account, fraud, or refinance issues."""
    print(f"DEBUG: send_notification called with issue_type='{issue_type}', contact_name='{contact_name}', contact_email='{contact_email}'")
    try:
        # Validate issue_type
        valid_types = ["loan", "card", "account", "fraud", "refinance"]
        if issue_type not in valid_types:
            return {"status": "error", "message": f"Invalid issue_type. Must be one of: {valid_types}"}
        
        # Create contact_info dictionary from individual parameters
        contact_info = {
            "name": contact_name,
            "email": contact_email,
            "phone": contact_phone
        }
        
        # Create notification message
        message = f"ESCALATION: {issue_type.upper()}\nRequest: {original_request}\nContact: {contact_info}"
        title = f"Member Support - {issue_type.title()} Issue"
        
        # Send Pushover notification
        push_success = push(message, title)
        
        # Create notification data for logging
        notification = {
            "timestamp": datetime.now().isoformat(),
            "original_request": original_request,
            "contact_info": contact_info,
            "issue_type": issue_type,
            "pushover_sent": push_success,
            "status": "pending"
        }
        
        # Save to logs directory
        logs_dir = "data/logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        filename = f"notification_{issue_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(logs_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(notification, f, indent=2)
        
        if push_success:
            result = {"status": "success", "message": f"Notification sent for {issue_type} issue"}
            print(f"DEBUG: send_notification success")
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
def record_user_details(name: str = "", email: str = "", phone: str = "", notes: str = "") -> Dict[str, Any]:
    """Record user contact information for follow-up. Use when user provides any contact information."""
    print(f"DEBUG: record_user_details called with name='{name}', email='{email}', phone='{phone}'")
    try:
        # Create user details dictionary from individual parameters
        user_details = {
            "name": name,
            "email": email,
            "phone": phone,
            "notes": notes,
            "timestamp": datetime.now().isoformat(),
            "status": "recorded"
        }
        
        # Save to logs directory
        logs_dir = "data/logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        filename = f"user_details_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(logs_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(user_details, f, indent=2)
        
        result = {"status": "success", "message": "User details recorded successfully"}
        print(f"DEBUG: record_user_details success")
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