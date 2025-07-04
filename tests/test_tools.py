#!/usr/bin/env python3
"""
Test script for tools.py methods
"""

import sys
from pathlib import Path
from typing import Dict, Any

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from tools import send_notification, record_user_details, log_unknown_question, search_knowledge_base

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

def handle_tool_call(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Central tool dispatcher - handles both @tool functions and tool objects"""
    from tools import send_notification, record_user_details, log_unknown_question, search_knowledge_base
    tools = {
        "send_notification": send_notification,
        "record_user_details": record_user_details,
        "log_unknown_question": log_unknown_question,
        "search_knowledge_base": search_knowledge_base
    }
    
    if tool_name not in tools:
        return {"status": "error", "message": f"Unknown tool: {tool_name}"}
    
    try:
        tool_obj = tools[tool_name]
        
        # Handle different tool types
        if tool_name == "search_knowledge_base":
            # Tool object - use .invoke() method
            result = tool_obj.invoke(params)
            return {"status": "success", "result": result}
        else:
            # @tool decorated function - call directly
            result = tool_obj(params)
            return result
            
    except Exception as e:
        return {"status": "error", "message": f"Tool execution failed: {str(e)}"}

def test_search_knowledge_base_success():
    """Test successful knowledge base search"""
    query = "How do I open a checking account?"
    
    # Test the retriever tool directly using .invoke() method
    result = search_knowledge_base.invoke({"query": query})
    
    # The retriever tool returns a string with relevant documents
    assert isinstance(result, str)
    assert len(result) > 0
    # Should contain some relevant information about checking accounts
    assert "checking" in result.lower() or "account" in result.lower()

def test_search_knowledge_base_no_results():
    """Test knowledge base search with no results"""
    query = "How do I build a rocket ship?"
    
    # Test with a query that shouldn't have results
    result = search_knowledge_base.invoke({"query": query})
    
    # Should still return a string (even if empty or minimal)
    assert isinstance(result, str)

def test_search_knowledge_base_error():
    """Test knowledge base search with error"""
    query = "test query"
    
    # Test basic functionality
    result = search_knowledge_base.invoke({"query": query})
    
    # Should return a string
    assert isinstance(result, str)

def test_search_knowledge_base_via_dispatcher():
    """Test search_knowledge_base through the tool dispatcher"""
    query = "checking account"
    
    # Test through the dispatcher
    result = handle_tool_call("search_knowledge_base", {"query": query})
    
    # Should return a dict with status and result
    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert "result" in result
    assert isinstance(result["result"], str)

if __name__ == "__main__":
    print("🚀 Starting tools tests...\n")
    
    test_send_notification()
    test_record_user_details()
    test_log_unknown_question()
    test_handle_tool_call()
    test_search_knowledge_base_success()
    test_search_knowledge_base_no_results()
    test_search_knowledge_base_error()
    test_search_knowledge_base_via_dispatcher()
    
    print("\n🎉 All tests completed!") 