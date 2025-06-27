#!/usr/bin/env python3
"""
Test pushover alerts
"""

import sys
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from pushover_alerts import push

def test_pushover():
    """Test pushover function"""
    print("🧪 Testing pushover alerts...")
    
    result = push("Test message", "Test Alert")
    print(f"✅ Result: {result}")

if __name__ == "__main__":
    test_pushover() 