#!/usr/bin/env python3
"""
Fix App Setup for Talinda POS
=============================

This script fixes common setup issues and provides a comprehensive setup solution
for the Talinda POS application.

Usage:
    python fix_app_setup.py

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
import platform

# Add src directory to path for imports
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('fix_setup.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TalindaPOSFixSetup:
    """Fix and setup class for Talinda POS system."""
    
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
        print("           TALINDA POS - FIX APP SETUP")
        print("=" * 60)
        print("This script will fix common issues and set up the")
        print("Talinda POS application properly.")
        print("=" * 60)
        print()
    
    def check_system_info(self):
        """Check system information."""
        logger.info("Checking system information...")
        logger.info(f"Platform: {platform.system()} {platform.release()}")
        logger.info(f"Python version: {sys.version}")
        logger.info(f"Current directory: {self.current_dir}")
        logger.info(f"Source directory: {self.src_dir}")
        return True
    
    def check_python_version(self):
        """Check if Python version is compatible."""
        logger.info("Checking Python version...")
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 or higher is required!")
            logger.error(f"Current version: {sys.version}")
            return False
        logger.info(f"[OK] Python version: {sys.version}")
        return True
    
    def fix_path_issues(self):
        """Fix common path and directory issues."""
        logger.info("Fixing path and directory issues...")
        
        # Create necessary directories
        directories = [
            self.current_dir / "logs",
            self.current_dir / "reports",
            self.current_dir / "backups",
            self.src_dir / "logs",
            self.src_dir / "reports",
            self.src_dir / "resources" / "images",
            self.src_dir / "resources" / "styles",
            self.src_dir / "resources" / "translations",
        ]
        
        for directory in directories:
            try:
                directory.mkdir(parents=True, exist_ok=True)
                logger.info(f"[OK] Created directory: {directory}")
            except Exception as e:
                logger.warning(f"Could not create directory {directory}: {e}")
        
        # Fix database path issues
        if not self.database_path.exists():
            # Check if database exists in src directory
            src_db = self.src_dir / "pos_database.db"
            if src_db.exists():
                try:
                    shutil.copy2(src_db, self.database_path)
                    logger.info(f"[OK] Moved database from {src_db} to {self.database_path}")
                except Exception as e:
                    logger.warning(f"Could not move database: {e}")
        
        return True
    
    def clean_database_files(self):
        """Clean up corrupted database files."""
        logger.info("Cleaning up database files...")
        
        # Remove WAL and SHM files if they exist
        wal_file = self.current_dir / "pos_database.db-wal"
        shm_file = self.current_dir / "pos_database.db-shm"
        
        files_to_remove = [wal_file, shm_file]
        
        for file_path in files_to_remove:
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(f"[OK] Removed: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {file_path}: {e}")
        
        # Also clean files in src directory
        src_wal = self.src_dir / "pos_database.db-wal"
        src_shm = self.src_dir / "pos_database.db-shm"
        
        for file_path in [src_wal, src_shm]:
            if file_path.exists():
                try:
                    file_path.unlink()
                    logger.info(f"[OK] Removed: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {file_path}: {e}")
    
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
            logger.info("Installing Python packages...")
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True, check=True)
            
            logger.info("[OK] Dependencies installed successfully!")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e}")
            logger.error(f"Error output: {e.stderr}")
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
                logger.info(f"[OK] Database backed up to: {backup_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to backup database: {e}")
                return False
        else:
            logger.info("No existing database found.")
            return True
    
    def initialize_database(self):
        """Initialize the database."""
        logger.info("Initializing database...")
        try:
            # Import database initialization
            from init_database import init_database
            init_database()
            logger.info("[OK] Database initialized successfully!")
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
                logger.info("[OK] Admin user created successfully!")
            else:
                logger.info("[OK] Admin user already exists.")
            
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
                logger.info("[OK] Cashier user created successfully!")
            else:
                logger.info("[OK] Cashier user already exists.")
            
            session.commit()
            session.close()
            
            logger.info("[OK] Default users created successfully!")
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
                    logger.info(f"[OK] Created category: {cat_name}")
                else:
                    # Update existing category to have 14% tax rate
                    existing_category = session.query(Category).filter_by(name=cat_name).first()
                    if existing_category and (not hasattr(existing_category, 'tax_rate') or existing_category.tax_rate == 0.0):
                        existing_category.tax_rate = 14.0
                        logger.info(f"[OK] Updated category: {cat_name}")
            
            session.commit()
            session.close()
            
            logger.info("[OK] Default data seeded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to seed default data: {e}")
            return False
    
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
            logger.info(f"[OK] Environment file created: {env_file}")
        except Exception as e:
            logger.warning(f"Could not create environment file: {e}")
    
    def fix_permissions(self):
        """Fix file permissions on Unix-like systems."""
        if platform.system() in ['Linux', 'Darwin']:
            logger.info("Fixing file permissions...")
            try:
                # Make main.py executable
                main_py = self.src_dir / "main.py"
                if main_py.exists():
                    os.chmod(main_py, 0o755)
                    logger.info("[OK] Made main.py executable")
                
                # Make setup scripts executable
                setup_scripts = [
                    "setup_for_new_device.py",
                    "fix_app_setup.py",
                    "build_executable.py"
                ]
                
                for script in setup_scripts:
                    script_path = self.current_dir / script
                    if script_path.exists():
                        os.chmod(script_path, 0o755)
                        logger.info(f"[OK] Made {script} executable")
                
            except Exception as e:
                logger.warning(f"Could not fix permissions: {e}")
    
    def verify_setup(self):
        """Verify that the setup was successful."""
        logger.info("Verifying setup...")
        
        checks = [
            ("Database file exists", self.database_path.exists()),
            ("Requirements installed", self.check_requirements_installed()),
            ("Admin user exists", self.check_admin_user_exists()),
            ("Categories exist", self.check_categories_exist()),
            ("Directories created", self.check_directories_exist()),
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
    
    def check_directories_exist(self):
        """Check if necessary directories exist."""
        required_dirs = [
            self.current_dir / "logs",
            self.current_dir / "reports",
            self.current_dir / "backups",
            self.src_dir / "logs",
            self.src_dir / "reports",
        ]
        
        return all(directory.exists() for directory in required_dirs)
    
    def test_application(self):
        """Test if the application can start."""
        logger.info("Testing application startup...")
        try:
            # Try to import main modules
            from config import config
            from database.db_config import Session
            from models.user import User
            
            logger.info("[OK] Core modules imported successfully")
            
            # Test database connection
            session = Session()
            session.execute("SELECT 1")
            session.close()
            logger.info("[OK] Database connection successful")
            
            return True
            
        except Exception as e:
            logger.error(f"Application test failed: {e}")
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
    
    def run_fix_setup(self):
        """Run the complete fix and setup process."""
        self.print_banner()
        
        # Check system info
        self.check_system_info()
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Fix path issues
        self.fix_path_issues()
        
        # Clean database files
        self.clean_database_files()
        
        # Install dependencies
        if not self.install_dependencies():
            logger.error("Failed to install dependencies. Please install them manually.")
            return False
        
        # Backup existing database
        if not self.backup_existing_database():
            logger.warning("Failed to backup existing database. Continuing...")
        
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
        
        # Fix permissions
        self.fix_permissions()
        
        # Test application
        if not self.test_application():
            logger.warning("Application test failed, but setup may still work.")
        
        # Verify setup
        if not self.verify_setup():
            logger.error("Setup verification failed!")
            return False
        
        # Print credentials and next steps
        self.print_credentials()
        self.print_next_steps()
        
        logger.info("[OK] Fix and setup completed successfully!")
        return True


def main():
    """Main entry point."""
    try:
        setup = TalindaPOSFixSetup()
        success = setup.run_fix_setup()
        
        if success:
            print("\n🎉 Fix and setup completed successfully!")
            print("You can now run the application with: python src/main.py")
        else:
            print("\n❌ Fix and setup failed! Check the logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nFix and setup interrupted by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during fix and setup: {e}")
        print(f"\n❌ Fix and setup failed with unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 