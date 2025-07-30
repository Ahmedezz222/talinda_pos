#!/usr/bin/env python3
"""
Test script for No-Login functionality.
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

def test_no_login_setup():
    """Test the no-login setup functionality."""
    try:
        print("🧪 Testing No-Login Setup")
        print("=" * 50)
        
        session = Session()
        
        # Check if any users exist
        user_count = session.query(User).count()
        
        print(f"📊 Current user count: {user_count}")
        
        if user_count == 0:
            print("✅ No users exist - application will open without login")
            print("🎯 This is the expected state for no-login functionality")
            
            # Test the authentication flow
            from src.main import ApplicationManager
            app_manager = ApplicationManager()
            
            # Test the run_authentication method
            result = app_manager.run_authentication()
            
            if result:
                user, opening_amount = result
                print("✅ Authentication flow successful!")
                print(f"👤 Temporary user created: {user.username}")
                print(f"🏷️  Role: {user.role.value}")
                print(f"📛 Full Name: {user.full_name}")
                print(f"💰 Opening Amount: {opening_amount}")
            else:
                print("❌ Authentication flow failed")
                return False
                
        else:
            print("⚠️  Users exist in database")
            print("💡 Run 'python clear_users.py' to test no-login functionality")
            print(f"👥 Found {user_count} user(s):")
            
            users = session.query(User).all()
            for user in users:
                print(f"   - {user.username} ({user.role.value})")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logger.error(f"No-login test error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Starting No-Login Test")
    print("=" * 50)
    
    if test_no_login_setup():
        print("\n🎯 No-login test completed successfully!")
        print("📋 The application will open directly without login")
        print("💡 You can add users through the admin panel after first login")
    else:
        print("\n❌ No-login test failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 