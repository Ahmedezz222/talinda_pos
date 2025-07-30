#!/usr/bin/env python3
"""
Setup Script for Talinda POS - New Device Deployment
====================================================

This script prepares the Talinda POS application to run on any new device.
It handles database initialization, admin user creation, default data seeding,
and configuration setup.

Usage:
    python setup_for_new_device.py

Author: Talinda POS Team
Version: 2.0.0
"""

import os
import sys
import subprocess
import shutil
import sqlite3
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
        logging.FileHandler('setup.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TalindaPOSSetup:
    """Setup class for Talinda POS system."""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent.absolute()
        self.src_dir = self.current_dir / "src"
        self.database_path = self.current_dir / "pos_database.db"
        self.backup_dir = self.current_dir / "backups"
        
        # Default admin credentials
        self.default_admin = {
            'username': 'admin',
            'password': 'admin123',
            'full_name': 'System Administrator'
        }
        
        # Default cashier credentials
        self.default_cashier = {
            'username': 'cashier',
            'password': 'cashier123',
            'full_name': 'Default Cashier'
        }
    
    def print_banner(self):
        """Print setup banner."""
        print("=" * 60)
        print("           TALINDA POS - NEW DEVICE SETUP")
        print("=" * 60)
        print("This script will prepare the Talinda POS application")
        print("to run on this device.")
        print("=" * 60)
        print()
    
    def check_python_version(self):
        """Check if Python version is compatible."""
        logger.info("Checking Python version...")
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 or higher is required!")
            return False
        logger.info(f"Python version: {sys.version}")
        return True
    
    def install_dependencies(self):
        """Install required dependencies."""
        logger.info("Installing dependencies...")
        try:
            # Check if requirements.txt exists
            requirements_file = self.current_dir / "requirements.txt"
            if not requirements_file.exists():
                logger.error("requirements.txt not found!")
                return False
            
            # Install dependencies
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], check=True)
            
            logger.info("Dependencies installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            return False
        except Exception as e:
            logger.error(f"Error installing dependencies: {e}")
            return False
    
    def backup_existing_database(self):
        """Backup existing database if it exists."""
        if self.database_path.exists():
            logger.info("Backing up existing database...")
            
            # Create backup directory
            self.backup_dir.mkdir(exist_ok=True)
            
            # Create backup filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"pos_database_backup_{timestamp}.db"
            
            try:
                shutil.copy2(self.database_path, backup_path)
                logger.info(f"Database backed up to: {backup_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to backup database: {e}")
                return False
        else:
            logger.info("No existing database found.")
            return True
    
    def clean_database_files(self):
        """Clean up any corrupted database files."""
        logger.info("Cleaning up database files...")
        
        # Remove WAL and SHM files if they exist
        wal_file = self.current_dir / "pos_database.db-wal"
        shm_file = self.current_dir / "pos_database.db-shm"
        
        files_to_remove = [wal_file, shm_file]
        
        for file_path in files_to_remove:
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(f"Removed: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {file_path}: {e}")
        
        # Also clean files in src directory
        src_wal = self.src_dir / "pos_database.db-wal"
        src_shm = self.src_dir / "pos_database.db-shm"
        
        for file_path in [src_wal, src_shm]:
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(f"Removed: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {file_path}: {e}")
    
    def initialize_database(self):
        """Initialize the database."""
        logger.info("Initializing database...")
        try:
            # Import database initialization
            from init_database import init_database
            init_database()
            logger.info("Database initialized successfully!")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
    
    def create_admin_users(self):
        """Create default admin and cashier users."""
        logger.info("Creating default users...")
        try:
            # Import required modules
            from database.db_config import Session
            from models.user import User, UserRole
            import bcrypt
            
            session = Session()
            
            # Create admin user
            if not session.query(User).filter_by(username=self.default_admin['username']).first():
                password_hash = bcrypt.hashpw(
                    self.default_admin['password'].encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                admin = User(
                    username=self.default_admin['username'],
                    password_hash=password_hash,
                    role=UserRole.ADMIN,
                    full_name=self.default_admin['full_name'],
                    active=1
                )
                session.add(admin)
                logger.info("Admin user created successfully!")
            else:
                logger.info("Admin user already exists.")
            
            # Create cashier user
            if not session.query(User).filter_by(username=self.default_cashier['username']).first():
                password_hash = bcrypt.hashpw(
                    self.default_cashier['password'].encode('utf-8'), 
                    bcrypt.gensalt()
                ).decode('utf-8')
                
                cashier = User(
                    username=self.default_cashier['username'],
                    password_hash=password_hash,
                    role=UserRole.CASHIER,
                    full_name=self.default_cashier['full_name'],
                    active=1
                )
                session.add(cashier)
                logger.info("Cashier user created successfully!")
            else:
                logger.info("Cashier user already exists.")
            
            session.commit()
            session.close()
            
            logger.info("Default users created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create users: {e}")
            return False
    
    def seed_default_data(self):
        """Seed the database with default categories and data."""
        logger.info("Seeding default data...")
        try:
            from database.db_config import Session
            from models.product import Category
            
            session = Session()
            initial_categories = ["Food", "Beverage", "Dessert", "Other"]
            
            for cat_name in initial_categories:
                # Check if category already exists
                if not session.query(Category).filter_by(name=cat_name).first():
                    category = Category(name=cat_name, description=f"{cat_name} category", tax_rate=14.0)
                    session.add(category)
                    logger.info(f"Created category: {cat_name}")
                else:
                    # Update existing category to have 14% tax rate
                    existing_category = session.query(Category).filter_by(name=cat_name).first()
                    if existing_category and (not hasattr(existing_category, 'tax_rate') or existing_category.tax_rate == 0.0):
                        existing_category.tax_rate = 14.0
                        logger.info(f"Updated category: {cat_name}")
            
            session.commit()
            session.close()
            
            logger.info("Default data seeded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to seed default data: {e}")
            return False
    
    def create_directories(self):
        """Create necessary directories."""
        logger.info("Creating necessary directories...")
        
        directories = [
            self.current_dir / "logs",
            self.current_dir / "reports",
            self.src_dir / "logs",
            self.src_dir / "reports",
            self.current_dir / "backups"
        ]
        
        for directory in directories:
            try:
                directory.mkdir(exist_ok=True)
                logger.info(f"Created directory: {directory}")
            except Exception as e:
                logger.warning(f"Could not create directory {directory}: {e}")
    
    def create_env_file(self):
        """Create environment file with default settings."""
        logger.info("Creating environment configuration...")
        
        env_content = """# Talinda POS Environment Configuration
# Copy this file to .env and modify as needed

# Application settings
APP_NAME=Talinda POS
APP_VERSION=2.0.0
APP_AUTHOR=Talinda POS Team

# Database settings
DATABASE_URL=sqlite:///pos_database.db
DATABASE_ECHO=false

# Logging settings
LOG_LEVEL=INFO
LOG_FILE=logs/talinda_pos.log
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# UI settings
WINDOW_WIDTH=1200
WINDOW_HEIGHT=800
THEME=default

# Security settings
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=3
PASSWORD_MIN_LENGTH=8

# File paths
CSS_FILE=resources/styles/main.qss
LOGO_FILE=resources/images/logo.png

# Colors
PRIMARY_COLOR=#1976d2
SECONDARY_COLOR=#424242
SUCCESS_COLOR=#4caf50
ERROR_COLOR=#f44336
WARNING_COLOR=#ff9800

# Environment
ENVIRONMENT=production
"""
        
        env_file = self.current_dir / "env_example.txt"
        try:
            with open(env_file, 'w', encoding='utf-8') as f:
                f.write(env_content)
            logger.info(f"Environment file created: {env_file}")
        except Exception as e:
            logger.warning(f"Could not create environment file: {e}")
    
    def verify_setup(self):
        """Verify that the setup was successful."""
        logger.info("Verifying setup...")
        
        checks = [
            ("Database file exists", self.database_path.exists()),
            ("Requirements installed", self.check_requirements_installed()),
            ("Admin user exists", self.check_admin_user_exists()),
            ("Categories exist", self.check_categories_exist()),
        ]
        
        all_passed = True
        for check_name, passed in checks:
            if passed:
                logger.info(f"[OK] {check_name}")
            else:
                logger.error(f"[FAIL] {check_name}")
                all_passed = False
        
        return all_passed
    
    def check_requirements_installed(self):
        """Check if required packages are installed."""
        try:
            import PyQt5
            import sqlalchemy
            import bcrypt
            import reportlab
            import openpyxl
            return True
        except ImportError:
            return False
    
    def check_admin_user_exists(self):
        """Check if admin user exists in database."""
        try:
            from database.db_config import Session
            from models.user import User
            
            session = Session()
            admin = session.query(User).filter_by(username='admin').first()
            session.close()
            return admin is not None
        except Exception:
            return False
    
    def check_categories_exist(self):
        """Check if default categories exist."""
        try:
            from database.db_config import Session
            from models.product import Category
            
            session = Session()
            categories = session.query(Category).all()
            session.close()
            return len(categories) > 0
        except Exception:
            return False
    
    def print_credentials(self):
        """Print default credentials."""
        print("\n" + "=" * 60)
        print("                    DEFAULT CREDENTIALS")
        print("=" * 60)
        print("Admin User:")
        print(f"  Username: {self.default_admin['username']}")
        print(f"  Password: {self.default_admin['password']}")
        print()
        print("Cashier User:")
        print(f"  Username: {self.default_cashier['username']}")
        print(f"  Password: {self.default_cashier['password']}")
        print()
        print("⚠️  IMPORTANT: Change these passwords after first login!")
        print("=" * 60)
    
    def print_next_steps(self):
        """Print next steps for the user."""
        print("\n" + "=" * 60)
        print("                      NEXT STEPS")
        print("=" * 60)
        print("1. Run the application:")
        print("   python src/main.py")
        print()
        print("2. Login with the default credentials above")
        print()
        print("3. Change default passwords in the admin panel")
        print()
        print("4. Configure your business settings")
        print()
        print("5. Add your products and categories")
        print("=" * 60)
    
    def run_setup(self):
        """Run the complete setup process."""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Install dependencies
        if not self.install_dependencies():
            logger.error("Failed to install dependencies. Please install them manually.")
            return False
        
        # Create directories
        self.create_directories()
        
        # Backup existing database
        if not self.backup_existing_database():
            logger.warning("Failed to backup existing database. Continuing...")
        
        # Clean database files
        self.clean_database_files()
        
        # Initialize database
        if not self.initialize_database():
            logger.error("Failed to initialize database.")
            return False
        
        # Create admin users
        if not self.create_admin_users():
            logger.error("Failed to create admin users.")
            return False
        
        # Seed default data
        if not self.seed_default_data():
            logger.error("Failed to seed default data.")
            return False
        
        # Create environment file
        self.create_env_file()
        
        # Verify setup
        if not self.verify_setup():
            logger.error("Setup verification failed!")
            return False
        
        # Print credentials and next steps
        self.print_credentials()
        self.print_next_steps()
        
        logger.info("Setup completed successfully!")
        return True


def main():
    """Main entry point."""
    try:
        setup = TalindaPOSSetup()
        success = setup.run_setup()
        
        if success:
            print("\n🎉 Setup completed successfully!")
            print("You can now run the application with: python src/main.py")
        else:
            print("\n❌ Setup failed! Check the logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nSetup interrupted by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during setup: {e}")
        print(f"\n❌ Setup failed with unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 