#!/usr/bin/env python3
"""
Simple User Reset Script for Talinda POS
========================================

This script resets user passwords to simple defaults without interactive prompts.
Use this when you can't use the interactive create_login_users.py script.

Usage:
    python reset_users.py
"""

import os
import sys
import bcrypt
from pathlib import Path

# Add src directory to path for imports
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def reset_users():
    """Reset users with simple passwords."""
    try:
        from database.db_config import Session
        from models.user import User, UserRole
        
        session = Session()
        
        # Simple passwords that are easy to type
        simple_password = "123456"
        password_hash = bcrypt.hashpw(simple_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Users to create/reset
        users_data = [
            {
                'username': 'admin',
                'password_hash': password_hash,
                'role': UserRole.ADMIN,
                'full_name': 'System Administrator',
                'active': 1
            },
            {
                'username': 'cashier',
                'password_hash': password_hash,
                'role': UserRole.CASHIER,
                'full_name': 'Default Cashier',
                'active': 1
            },
            {
                'username': 'manager',
                'password_hash': password_hash,
                'role': UserRole.MANAGER,
                'full_name': 'Store Manager',
                'active': 1
            }
        ]
        
        print("Resetting users with simple passwords...")
        
        for user_data in users_data:
            # Check if user exists
            existing_user = session.query(User).filter_by(username=user_data['username']).first()
            
            if existing_user:
                # Update existing user
                existing_user.password_hash = user_data['password_hash']
                existing_user.role = user_data['role']
                existing_user.full_name = user_data['full_name']
                existing_user.active = user_data['active']
                print(f"✓ Updated user: {user_data['username']}")
            else:
                # Create new user
                user = User(**user_data)
                session.add(user)
                print(f"✓ Created user: {user_data['username']}")
        
        session.commit()
        session.close()
        
        print("\n" + "=" * 50)
        print("           LOGIN CREDENTIALS")
        print("=" * 50)
        print("All users now use the same simple password:")
        print("Password: 123456")
        print()
        print("Available users:")
        print("- admin (Administrator)")
        print("- cashier (Cashier)")
        print("- manager (Manager)")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("Talinda POS - Simple User Reset")
    print("=" * 40)
    
    if reset_users():
        print("\n✅ Users reset successfully!")
        print("You can now login with username and password: 123456")
    else:
        print("\n❌ Failed to reset users!")
        sys.exit(1) 