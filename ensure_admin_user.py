#!/usr/bin/env python3
"""
Script to ensure admin user exists with admin/admin123 credentials.
This script creates the admin user if it doesn't exist, or updates the password if needed.
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

def ensure_admin_user():
    """Ensure admin user exists with admin/admin123 credentials."""
    try:
        session = Session()
        
        # Check if admin user exists
        admin_user = session.query(User).filter_by(username='admin').first()
        
        if admin_user:
            logger.info("Admin user already exists")
            
            # Check if password is correct (admin123)
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            if bcrypt.checkpw('admin123'.encode('utf-8'), admin_user.password_hash.encode('utf-8')):
                logger.info("Admin password is already correct")
            else:
                # Update password to admin123
                admin_user.password_hash = password_hash
                safe_commit(session)
                logger.info("Updated admin password to admin123")
        else:
            # Create admin user
            password_hash = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            admin_user = User(
                username='admin',
                password_hash=password_hash,
                role=UserRole.ADMIN,
                full_name='System Administrator',
                active=1
            )
            
            session.add(admin_user)
            safe_commit(session)
            logger.info("Created admin user with admin/admin123 credentials")
        
        session.close()
        return True
        
    except Exception as e:
        logger.error(f"Error ensuring admin user: {e}")
        return False

def main():
    """Main function."""
    print("🔧 Ensuring admin user exists with admin/admin123 credentials...")
    
    if ensure_admin_user():
        print("✅ Admin user setup completed successfully!")
        print("📋 Login credentials:")
        print("   Username: admin")
        print("   Password: admin123")
        print("\n🎯 The application will now auto-login with these credentials!")
    else:
        print("❌ Failed to setup admin user")
        sys.exit(1)

if __name__ == "__main__":
    main() 