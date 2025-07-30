#!/usr/bin/env python3
"""
Verify Admin User Script
========================

This script verifies that the default admin user exists and can be used for login.
"""

import sys
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from database.db_config import Session
from models.user import User
from controllers.auth_controller import AuthController
import bcrypt

def verify_admin_user():
    """Verify that the default admin user exists and can be used."""
    print("=" * 50)
    print("VERIFYING DEFAULT ADMIN USER")
    print("=" * 50)
    
    try:
        session = Session()
        
        # Check if admin user exists
        admin_user = session.query(User).filter_by(username='admin').first()
        
        if admin_user:
            print("✅ Admin user found!")
            print(f"   Username: {admin_user.username}")
            print(f"   Role: {admin_user.role.value}")
            print(f"   Full Name: {admin_user.full_name}")
            print(f"   Active: {'Yes' if admin_user.active else 'No'}")
            
            # Test authentication
            auth_controller = AuthController()
            if auth_controller.login('admin', 'admin123'):
                print("✅ Authentication successful!")
                print("   You can login with:")
                print("   Username: admin")
                print("   Password: admin123")
            else:
                print("❌ Authentication failed!")
                print("   The password might be incorrect.")
                
        else:
            print("❌ Admin user not found!")
            print("   Please run the setup script first:")
            print("   python setup_for_new_device.py")
            
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("   Please check if the database is properly initialized.")
    
    print("\n" + "=" * 50)
    print("NEXT STEPS:")
    print("1. Run the application: python src/main.py")
    print("2. Login with the credentials above")
    print("3. Go to Admin Panel > User Management")
    print("4. Change the default passwords")
    print("=" * 50)

if __name__ == "__main__":
    verify_admin_user() 