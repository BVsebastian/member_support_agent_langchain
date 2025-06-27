"""
Tools for Alexa - Member Support Agent
Implements send_notification, record_user_details, log_unknown_question
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional

def send_notification(params: Dict[str, Any]) -> Dict[str, Any]:
    """Send notification about an escalation"""
    try:
        original_request = params.get("original_request", "")
        contact_info = params.get("contact_info", {})
        issue_type = params.get("issue_type", "general")
        
        # Validate issue_type
        valid_types = ["loan", "card", "account", "fraud", "refinance"]
        if issue_type not in valid_types:
            return {"status": "error", "message": f"Invalid issue_type. Must be one of: {valid_types}"}
        
        # Create notification data
        notification = {
            "timestamp": datetime.now().isoformat(),
            "original_request": original_request,
            "contact_info": contact_info,
            "issue_type": issue_type,
            "status": "pending"
        }
        
        # Save to logs directory
        logs_dir = "data/logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        filename = f"notification_{issue_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(logs_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(notification, f, indent=2)
        
        return {"status": "success", "message": f"Notification sent for {issue_type} issue"}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to send notification: {str(e)}"}

def record_user_details(params: Dict[str, Any]) -> Dict[str, Any]:
    """Record user contact information for follow-up"""
    try:
        user_details = params.get("user_details", {})
        
        # Add timestamp
        user_details["timestamp"] = datetime.now().isoformat()
        user_details["status"] = "recorded"
        
        # Save to logs directory
        logs_dir = "data/logs"
        os.makedirs(logs_dir, exist_ok=True)
        
        filename = f"user_details_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        filepath = os.path.join(logs_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(user_details, f, indent=2)
        
        return {"status": "success", "message": "User details recorded successfully"}
        
    except Exception as e:
        return {"status": "error", "message": f"Failed to record user details: {str(e)}"}

def log_unknown_question(params: Dict[str, Any]) -> Dict[str, Any]:
    """Log questions that cannot be answered"""
    try:
        question = params.get("question", "")
        context = params.get("context", {})
        
        # Create log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "question": question,
            "context": context,
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

def handle_tool_call(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Central tool dispatcher"""
    tools = {
        "send_notification": send_notification,
        "record_user_details": record_user_details,
        "log_unknown_question": log_unknown_question
    }
    
    if tool_name not in tools:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}
    
    try:
        return tools[tool_name](params)
    except Exception as e:
        return {"status": "error", "message": f"Tool execution failed: {str(e)}"} 