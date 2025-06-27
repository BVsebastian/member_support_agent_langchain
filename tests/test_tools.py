#!/usr/bin/env python3
"""
Test script for tools.py methods
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from tools import send_notification, record_user_details, log_unknown_question, handle_tool_call

def test_send_notification():
    """Test send_notification method"""
    print("🧪 Testing send_notification...")
    
    # Test valid notification
    params = {
        "original_request": "I need help with my loan application",
        "contact_info": {"name": "John Doe", "email": "john@example.com", "phone": "555-1234"},
        "issue_type": "loan"
    }
    
    result = send_notification(params)
    print(f"✅ Result: {result}")
    
    # Test invalid issue_type
    params["issue_type"] = "invalid"
    result = send_notification(params)
    print(f"✅ Invalid type result: {result}")

def test_record_user_details():
    """Test record_user_details method"""
    print("\n🧪 Testing record_user_details...")
    
    params = {
        "user_details": {
            "name": "Jane Smith",
            "email": "jane@example.com", 
            "phone": "555-5678",
            "notes": "Interested in checking account"
        }
    }
    
    result = record_user_details(params)
    print(f"✅ Result: {result}")

def test_log_unknown_question():
    """Test log_unknown_question method"""
    print("\n🧪 Testing log_unknown_question...")
    
    params = {
        "question": "What are your international wire transfer fees?",
        "context": {"user_id": "12345", "session_id": "abc123"}
    }
    
    result = log_unknown_question(params)
    print(f"✅ Result: {result}")

def test_handle_tool_call():
    """Test handle_tool_call dispatcher"""
    print("\n🧪 Testing handle_tool_call...")
    
    # Test valid tool
    result = handle_tool_call("log_unknown_question", {"question": "Test question"})
    print(f"✅ Valid tool result: {result}")
    
    # Test invalid tool
    result = handle_tool_call("invalid_tool", {})
    print(f"✅ Invalid tool result: {result}")

if __name__ == "__main__":
    print("🚀 Starting tools tests...\n")
    
    test_send_notification()
    test_record_user_details()
    test_log_unknown_question()
    test_handle_tool_call()
    
    print("\n🎉 All tests completed!") 