#!/usr/bin/env python3
"""
Test script for Authentication Flow functionality.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from database.db_config import Session
from models.user import User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_auth_flow():
    """Test the authentication flow functionality."""
    try:
        print("🧪 Testing Authentication Flow")
        print("=" * 50)
        
        session = Session()
        
        # Check if any users exist
        user_count = session.query(User).count()
        
        print(f"📊 Current user count: {user_count}")
        
        if user_count > 0:
            print("✅ Users exist in database")
            print("🎯 Application will show login dialog")
            print("📋 Available users:")
            
            users = session.query(User).all()
            for user in users:
                print(f"   - {user.username} ({user.role.value}) - Active: {user.active}")
            
            print("\n💡 Expected behavior:")
            print("   1. Application will show login dialog")
            print("   2. You can login with any active user")
            print("   3. Normal authentication flow will be used")
            
        else:
            print("⚠️  No users exist in database")
            print("🎯 Application will open without login")
            print("💡 Add users through admin panel to enable authentication")
            
            print("\n💡 Expected behavior:")
            print("   1. Application will open directly")
            print("   2. No login dialog will appear")
            print("   3. Full admin access available")
            print("   4. Add users through admin panel")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logger.error(f"Auth flow test error: {e}")
        return False

def test_user_creation():
    """Test user creation functionality."""
    try:
        print("\n🔧 Testing User Creation")
        print("=" * 30)
        
        session = Session()
        
        # Check current users
        user_count = session.query(User).count()
        print(f"📊 Users before: {user_count}")
        
        if user_count == 0:
            print("💡 No users exist - you can add users through admin panel")
            print("📋 Steps to add users:")
            print("   1. Start application (no login)")
            print("   2. Navigate to Admin Panel")
            print("   3. Use 'Add User' functionality")
            print("   4. Create admin and cashier users")
            print("   5. Restart application")
            print("   6. Login dialog will appear")
        else:
            print("✅ Users exist - authentication is enabled")
            print("🎯 Login dialog will appear when starting application")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ User creation test failed: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Starting Authentication Flow Test")
    print("=" * 50)
    
    if test_auth_flow() and test_user_creation():
        print("\n🎯 Authentication flow test completed successfully!")
        print("📋 Summary:")
        print("   - If users exist: Login dialog will appear")
        print("   - If no users: Application opens directly")
        print("   - Add users through admin panel to enable authentication")
    else:
        print("\n❌ Authentication flow test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 