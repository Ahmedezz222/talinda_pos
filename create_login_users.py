#!/usr/bin/env python3
"""
Create Login Users for Talinda POS - New Device Setup
====================================================

This script creates login users for new devices in the Talinda POS system.
It provides an interactive interface to create admin, cashier, and manager users
with secure passwords and proper role assignments.

Usage:
    python create_login_users.py

Features:
- Interactive user creation
- Secure password hashing
- Role-based user management
- Validation and error handling
- Default user creation options

Author: Talinda POS Team
Version: 2.0.0
"""

import os
import sys
import getpass
import bcrypt
from pathlib import Path
import logging
from datetime import datetime

# Add src directory to path for imports
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('user_setup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class UserCreationManager:
    """Manager for creating login users in the POS system."""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent.absolute()
        self.src_dir = self.current_dir / "src"
        
        # Default users configuration
        self.default_users = {
            'admin': {
                'username': 'admin',
                'password': 'admin123',
                'role': 'admin',
                'full_name': 'System Administrator',
                'description': 'Full system access and management'
            },
            'cashier': {
                'username': 'cashier',
                'password': 'cashier123',
                'role': 'cashier',
                'full_name': 'Default Cashier',
                'description': 'Basic POS operations'
            },
            'manager': {
                'username': 'manager',
                'password': 'manager123',
                'role': 'manager',
                'full_name': 'Store Manager',
                'description': 'Management and reporting access'
            }
        }
    
    def print_banner(self):
        """Print application banner."""
        print("=" * 70)
        print("           TALINDA POS - LOGIN USER CREATION")
        print("=" * 70)
        print("This tool helps you create login users for new devices.")
        print("You can create admin, cashier, and manager users.")
        print("=" * 70)
        print()
    
    def check_database_connection(self):
        """Check if database is accessible."""
        try:
            from database.db_config import Session
            from models.user import User
            session = Session()
            session.close()
            logger.info("Database connection successful")
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
    
    def validate_username(self, username):
        """Validate username format and uniqueness."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters long"
        
        if not username.replace('_', '').replace('-', '').isalnum():
            return False, "Username can only contain letters, numbers, underscores, and hyphens"
        
        # Check if username already exists
        try:
            from database.db_config import Session
            from models.user import User
            session = Session()
            existing_user = session.query(User).filter_by(username=username).first()
            session.close()
            
            if existing_user:
                return False, "Username already exists"
        except Exception as e:
            logger.warning(f"Could not check username uniqueness: {e}")
        
        return True, "Username is valid"
    
    def validate_password(self, password):
        """Validate password strength."""
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        
        if len(password) > 50:
            return False, "Password is too long (maximum 50 characters)"
        
        return True, "Password is valid"
    
    def get_user_input(self, prompt, password=False, validation_func=None):
        """Get user input with validation."""
        while True:
            if password:
                user_input = getpass.getpass(prompt)
            else:
                user_input = input(prompt).strip()
            
            if validation_func:
                is_valid, message = validation_func(user_input)
                if not is_valid:
                    print(f"❌ {message}")
                    continue
            
            return user_input
    
    def create_user(self, username, password, role, full_name):
        """Create a new user in the database."""
        try:
            from database.db_config import Session
            from models.user import User, UserRole
            
            session = Session()
            
            # Hash the password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Create user object
            user = User(
                username=username,
                password_hash=password_hash,
                role=UserRole(role),
                full_name=full_name,
                active=1
            )
            
            session.add(user)
            session.commit()
            session.close()
            
            logger.info(f"User '{username}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create user '{username}': {e}")
            return False
    
    def create_custom_user(self):
        """Create a custom user with user input."""
        print("\n" + "=" * 50)
        print("              CREATE CUSTOM USER")
        print("=" * 50)
        
        # Get username
        username = self.get_user_input(
            "Enter username: ",
            validation_func=self.validate_username
        )
        
        # Get password
        password = self.get_user_input(
            "Enter password: ",
            password=True,
            validation_func=self.validate_password
        )
        
        # Confirm password
        confirm_password = self.get_user_input(
            "Confirm password: ",
            password=True
        )
        
        if password != confirm_password:
            print("❌ Passwords do not match!")
            return False
        
        # Get full name
        full_name = self.get_user_input("Enter full name: ").strip()
        if not full_name:
            full_name = username
        
        # Get role
        print("\nAvailable roles:")
        print("1. admin - Full system access and management")
        print("2. manager - Management and reporting access")
        print("3. cashier - Basic POS operations")
        
        role_choice = self.get_user_input("Select role (1-3): ").strip()
        role_map = {'1': 'admin', '2': 'manager', '3': 'cashier'}
        
        if role_choice not in role_map:
            print("❌ Invalid role choice!")
            return False
        
        role = role_map[role_choice]
        
        # Create the user
        if self.create_user(username, password, role, full_name):
            print(f"✅ User '{username}' created successfully!")
            return True
        else:
            print("❌ Failed to create user!")
            return False
    
    def create_default_users(self):
        """Create default users for the system."""
        print("\n" + "=" * 50)
        print("            CREATE DEFAULT USERS")
        print("=" * 50)
        
        created_count = 0
        
        for user_type, user_data in self.default_users.items():
            print(f"\nCreating {user_type} user...")
            print(f"Username: {user_data['username']}")
            print(f"Role: {user_data['role']}")
            print(f"Full Name: {user_data['full_name']}")
            print(f"Description: {user_data['description']}")
            
            # Check if user already exists
            try:
                from database.db_config import Session
                from models.user import User
                session = Session()
                existing_user = session.query(User).filter_by(username=user_data['username']).first()
                session.close()
                
                if existing_user:
                    print(f"⚠️  User '{user_data['username']}' already exists, skipping...")
                    continue
            except Exception as e:
                logger.warning(f"Could not check existing user: {e}")
            
            # Create the user
            if self.create_user(
                user_data['username'],
                user_data['password'],
                user_data['role'],
                user_data['full_name']
            ):
                created_count += 1
                print(f"✅ {user_type.capitalize()} user created successfully!")
            else:
                print(f"❌ Failed to create {user_type} user!")
        
        print(f"\n📊 Created {created_count} default users")
        return created_count
    
    def list_existing_users(self):
        """List all existing users in the system."""
        try:
            from database.db_config import Session
            from models.user import User
            
            session = Session()
            users = session.query(User).all()
            session.close()
            
            if not users:
                print("No users found in the system.")
                return
            
            print("\n" + "=" * 70)
            print("                    EXISTING USERS")
            print("=" * 70)
            print(f"{'Username':<15} {'Role':<10} {'Full Name':<25} {'Status':<10}")
            print("-" * 70)
            
            for user in users:
                status = "Active" if user.active else "Inactive"
                print(f"{user.username:<15} {user.role.value:<10} {user.full_name:<25} {status:<10}")
            
            print("=" * 70)
            
        except Exception as e:
            logger.error(f"Failed to list users: {e}")
            print("❌ Failed to retrieve user list!")
    
    def show_default_credentials(self):
        """Show default user credentials."""
        print("\n" + "=" * 70)
        print("                    DEFAULT CREDENTIALS")
        print("=" * 70)
        
        for user_type, user_data in self.default_users.items():
            print(f"\n{user_type.upper()} USER:")
            print(f"  Username: {user_data['username']}")
            print(f"  Password: {user_data['password']}")
            print(f"  Role: {user_data['role']}")
            print(f"  Full Name: {user_data['full_name']}")
            print(f"  Description: {user_data['description']}")
        
        print("\n⚠️  IMPORTANT: Change these passwords after first login!")
        print("=" * 70)
    
    def interactive_menu(self):
        """Show interactive menu for user creation."""
        while True:
            print("\n" + "=" * 50)
            print("              USER CREATION MENU")
            print("=" * 50)
            print("1. Create custom user")
            print("2. Create default users (admin, cashier, manager)")
            print("3. List existing users")
            print("4. Show default credentials")
            print("5. Exit")
            print("=" * 50)
            
            choice = input("Select an option (1-5): ").strip()
            
            if choice == '1':
                self.create_custom_user()
            elif choice == '2':
                self.create_default_users()
            elif choice == '3':
                self.list_existing_users()
            elif choice == '4':
                self.show_default_credentials()
            elif choice == '5':
                print("Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please select 1-5.")
    
    def run_quick_setup(self):
        """Run quick setup for new devices."""
        print("\n🚀 Quick Setup for New Device")
        print("This will create default users for immediate use.")
        
        confirm = input("Continue with quick setup? (y/N): ").strip().lower()
        if confirm != 'y':
            print("Quick setup cancelled.")
            return False
        
        # Create default users
        created_count = self.create_default_users()
        
        if created_count > 0:
            print(f"\n✅ Quick setup completed! Created {created_count} users.")
            self.show_default_credentials()
            return True
        else:
            print("\n❌ Quick setup failed!")
            return False
    
    def run(self):
        """Run the user creation manager."""
        self.print_banner()
        
        # Check database connection
        if not self.check_database_connection():
            print("❌ Cannot connect to database. Please ensure the database is initialized.")
            return False
        
        # Check if any users exist
        try:
            from database.db_config import Session
            from models.user import User
            session = Session()
            user_count = session.query(User).count()
            session.close()
            
            if user_count == 0:
                print("⚠️  No users found in the system.")
                print("This appears to be a new device setup.")
                return self.run_quick_setup()
            else:
                print(f"Found {user_count} existing user(s) in the system.")
                return self.interactive_menu()
                
        except Exception as e:
            logger.error(f"Error checking existing users: {e}")
            print("❌ Error checking existing users.")
            return False


def main():
    """Main entry point."""
    try:
        manager = UserCreationManager()
        success = manager.run()
        
        if success:
            print("\n🎉 User creation completed successfully!")
        else:
            print("\n❌ User creation failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nOperation interrupted by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"\n❌ Unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 