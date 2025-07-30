#!/usr/bin/env python3
"""
Test script for Auto-Login functionality.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from controllers.auth_controller import AuthController
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_auto_login():
    """Test the auto-login functionality."""
    try:
        print("🧪 Testing Auto-Login Functionality")
        print("=" * 50)
        
        # Create auth controller
        auth_controller = AuthController()
        
        # Test login with admin/admin123
        print("📝 Attempting login with admin/admin123...")
        
        if auth_controller.login("admin", "admin123"):
            user = auth_controller.get_current_user()
            print("✅ Auto-login successful!")
            print(f"👤 Logged in as: {user.username}")
            print(f"🏷️  Role: {user.role.value}")
            print(f"📛 Full Name: {user.full_name}")
            print(f"✅ Active: {user.active}")
            
            # Test logout
            auth_controller.logout()
            print("🚪 Logout successful")
            
            return True
        else:
            print("❌ Auto-login failed!")
            print("🔍 Possible reasons:")
            print("   - Admin user doesn't exist")
            print("   - Password is incorrect")
            print("   - Database connection issues")
            
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        logger.error(f"Auto-login test error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Starting Auto-Login Test")
    print("=" * 50)
    
    if test_auto_login():
        print("\n🎯 Auto-login test completed successfully!")
        print("📋 The application will now automatically login with admin/admin123")
    else:
        print("\n❌ Auto-login test failed!")
        print("💡 Please run 'python ensure_admin_user.py' to create the admin user")
        sys.exit(1)

if __name__ == "__main__":
    main() 