#!/usr/bin/env python3
"""
Script to clear all users from the database for testing no-login functionality.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from database.db_config import Session, safe_commit
from models.user import User
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def clear_all_users():
    """Clear all users from the database."""
    try:
        session = Session()
        
        # Get count of users before deletion
        user_count = session.query(User).count()
        
        if user_count == 0:
            print("✅ No users exist in the database")
            return True
        
        # Delete all users
        session.query(User).delete()
        safe_commit(session)
        
        print(f"✅ Successfully deleted {user_count} users from the database")
        print("🎯 The application will now open without any login")
        print("📋 You can add users through the admin panel after first login")
        
        session.close()
        return True
        
    except Exception as e:
        logger.error(f"Error clearing users: {e}")
        print(f"❌ Error clearing users: {e}")
        return False

def main():
    """Main function."""
    print("🧹 Clearing all users from database...")
    print("=" * 50)
    
    # Confirmation prompt
    response = input("Are you sure you want to delete ALL users? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("❌ Operation cancelled")
        return
    
    if clear_all_users():
        print("\n🎯 Database cleared successfully!")
        print("📋 Next steps:")
        print("   1. Start the application")
        print("   2. It will open directly without login")
        print("   3. Add users through the admin panel")
    else:
        print("\n❌ Failed to clear users")
        sys.exit(1)

if __name__ == "__main__":
    main() 