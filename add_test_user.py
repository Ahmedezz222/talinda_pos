#!/usr/bin/env python3
"""
Script to add a test user for verifying authentication flow.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

import bcrypt
from database.db_config import Session, safe_commit
from models.user import User, UserRole
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_test_user():
    """Add a test user to verify authentication flow."""
    try:
        session = Session()
        
        # Check if test user already exists
        test_user = session.query(User).filter_by(username='testadmin').first()
        
        if test_user:
            print("✅ Test user already exists")
            print(f"👤 Username: {test_user.username}")
            print(f"🏷️  Role: {test_user.role.value}")
            print(f"📛 Full Name: {test_user.full_name}")
            print(f"✅ Active: {test_user.active}")
        else:
            # Create test user
            password_hash = bcrypt.hashpw('test123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            test_user = User(
                username='testadmin',
                password_hash=password_hash,
                role=UserRole.ADMIN,
                full_name='Test Administrator',
                active=1
            )
            
            session.add(test_user)
            safe_commit(session)
            
            print("✅ Test user created successfully!")
            print(f"👤 Username: {test_user.username}")
            print(f"🔑 Password: test123")
            print(f"🏷️  Role: {test_user.role.value}")
            print(f"📛 Full Name: {test_user.full_name}")
        
        # Show all users
        all_users = session.query(User).all()
        print(f"\n📊 Total users in database: {len(all_users)}")
        print("👥 All users:")
        for user in all_users:
            print(f"   - {user.username} ({user.role.value}) - Active: {user.active}")
        
        session.close()
        return True
        
    except Exception as e:
        logger.error(f"Error adding test user: {e}")
        print(f"❌ Error adding test user: {e}")
        return False

def main():
    """Main function."""
    print("🔧 Adding Test User for Authentication Flow")
    print("=" * 50)
    
    if add_test_user():
        print("\n🎯 Test user setup completed!")
        print("📋 Next steps:")
        print("   1. Start the application")
        print("   2. Login dialog should appear")
        print("   3. Login with testadmin/test123")
        print("   4. Or use any other existing user")
    else:
        print("\n❌ Failed to add test user")
        sys.exit(1)

if __name__ == "__main__":
    main() 