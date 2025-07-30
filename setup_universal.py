#!/usr/bin/env python3
"""
Universal Setup Script for Talinda POS
======================================

This script provides a comprehensive setup solution for Talinda POS
across different deployment scenarios:
- New device setup
- Network deployment
- Production environment
- Development environment
- Quick deployment

Usage:
    python setup_universal.py [--mode <mode>] [--env <environment>]

Modes:
    - new-device: Setup for new device (default)
    - network: Setup for network deployment
    - production: Production environment setup
    - development: Development environment setup
    - quick: Quick setup with minimal configuration

Environments:
    - local: Local deployment (default)
    - server: Server deployment
    - cloud: Cloud deployment

Author: Talinda POS Team
Version: 3.0.0
"""

import os
import sys
import subprocess
import shutil
import sqlite3
import argparse
import json
import platform
import socket
from pathlib import Path
import logging
from datetime import datetime
import getpass

# Add src directory to path for imports
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('setup_universal.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class UniversalSetup:
    """Universal setup class for Talinda POS system."""
    
    def __init__(self, mode='new-device', environment='local'):
        self.current_dir = Path(__file__).parent.absolute()
        self.src_dir = self.current_dir / "src"
        self.database_path = self.current_dir / "pos_database.db"
        self.backup_dir = self.current_dir / "backups"
        self.config_dir = self.current_dir / "config"
        
        self.mode = mode
        self.environment = environment
        
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
        
        # Environment-specific configurations
        self.environment_configs = {
            'local': {
                'database_type': 'sqlite',
                'host': 'localhost',
                'port': 5000,
                'debug': True,
                'log_level': 'INFO'
            },
            'server': {
                'database_type': 'sqlite',
                'host': '0.0.0.0',
                'port': 5000,
                'debug': False,
                'log_level': 'WARNING'
            },
            'cloud': {
                'database_type': 'sqlite',
                'host': '0.0.0.0',
                'port': 8080,
                'debug': False,
                'log_level': 'ERROR'
            }
        }
    
    def print_banner(self):
        """Print setup banner."""
        print("=" * 70)
        print("              TALINDA POS - UNIVERSAL SETUP")
        print("=" * 70)
        print(f"Mode: {self.mode.upper()}")
        print(f"Environment: {self.environment.upper()}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version}")
        print("=" * 70)
        print()
    
    def check_system_requirements(self):
        """Check system requirements."""
        logger.info("Checking system requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            logger.error("Python 3.8 or higher is required!")
            return False
        
        # Check available disk space
        try:
            free_space = shutil.disk_usage(self.current_dir).free
            required_space = 100 * 1024 * 1024  # 100MB
            if free_space < required_space:
                logger.warning(f"Low disk space: {free_space // (1024*1024)}MB available")
        except Exception as e:
            logger.warning(f"Could not check disk space: {e}")
        
        # Check network connectivity (for network/cloud modes)
        if self.mode in ['network', 'cloud']:
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                logger.info("Network connectivity: OK")
            except OSError:
                logger.warning("No internet connection detected")
        
        logger.info("System requirements check completed")
        return True
    
    def install_dependencies(self):
        """Install required dependencies."""
        logger.info("Installing dependencies...")
        
        try:
            # Determine requirements file based on mode
            if self.mode == 'production':
                requirements_file = self.current_dir / "requirements_build.txt"
            else:
                requirements_file = self.current_dir / "requirements.txt"
            
            if not requirements_file.exists():
                logger.error(f"Requirements file not found: {requirements_file}")
                return False
            
            # Install dependencies
            result = subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("Dependencies installed successfully!")
                return True
            else:
                logger.error(f"Failed to install dependencies: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error installing dependencies: {e}")
            return False
    
    def create_directories(self):
        """Create necessary directories."""
        logger.info("Creating directories...")
        
        directories = [
            self.backup_dir,
            self.current_dir / "logs",
            self.current_dir / "reports",
            self.config_dir,
            self.src_dir / "logs",
            self.src_dir / "reports"
        ]
        
        for directory in directories:
            directory.mkdir(exist_ok=True)
            logger.info(f"Created directory: {directory}")
    
    def backup_existing_database(self):
        """Backup existing database if it exists."""
        if self.database_path.exists():
            logger.info("Backing up existing database...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"pos_database_backup_{timestamp}.db"
            
            try:
                shutil.copy2(self.database_path, backup_path)
                logger.info(f"Database backed up to: {backup_path}")
                return True
            except Exception as e:
                logger.error(f"Failed to backup database: {e}")
                return False
        return True
    
    def clean_database_files(self):
        """Clean corrupted database files."""
        logger.info("Cleaning database files...")
        
        # Remove WAL and SHM files
        wal_file = self.current_dir / "pos_database.db-wal"
        shm_file = self.current_dir / "pos_database.db-shm"
        
        for file_path in [wal_file, shm_file]:
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
            from database.database_manager import DatabaseManager
            from init_database import initialize_database
            
            # Initialize database
            initialize_database()
            logger.info("Database initialized successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            return False
    
    def create_admin_users(self):
        """Create admin users."""
        logger.info("Creating admin users...")
        
        try:
            from models.user import User
            from database.database_manager import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # Create admin user
            admin_user = User(
                username=self.default_admin['username'],
                password=self.default_admin['password'],
                full_name=self.default_admin['full_name'],
                role='admin',
                is_active=True
            )
            db_manager.add_user(admin_user)
            
            # Create cashier user
            cashier_user = User(
                username=self.default_cashier['username'],
                password=self.default_cashier['password'],
                full_name=self.default_cashier['full_name'],
                role='cashier',
                is_active=True
            )
            db_manager.add_user(cashier_user)
            
            logger.info("Admin users created successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to create admin users: {e}")
            return False
    
    def seed_default_data(self):
        """Seed default data."""
        logger.info("Seeding default data...")
        
        try:
            from models.product import Product, Category
            from database.database_manager import DatabaseManager
            
            db_manager = DatabaseManager()
            
            # Create default categories
            categories = [
                {'name': 'Food', 'tax_rate': 0.14},
                {'name': 'Beverage', 'tax_rate': 0.14},
                {'name': 'Dessert', 'tax_rate': 0.14},
                {'name': 'Other', 'tax_rate': 0.14}
            ]
            
            for cat_data in categories:
                category = Category(name=cat_data['name'], tax_rate=cat_data['tax_rate'])
                db_manager.add_category(category)
            
            logger.info("Default data seeded successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to seed default data: {e}")
            return False
    
    def create_environment_config(self):
        """Create environment-specific configuration."""
        logger.info("Creating environment configuration...")
        
        config = self.environment_configs.get(self.environment, self.environment_configs['local'])
        
        # Add mode-specific configurations
        if self.mode == 'production':
            config['debug'] = False
            config['log_level'] = 'ERROR'
        elif self.mode == 'development':
            config['debug'] = True
            config['log_level'] = 'DEBUG'
        
        # Create config file
        config_file = self.config_dir / f"config_{self.environment}.json"
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        logger.info(f"Configuration created: {config_file}")
        return True
    
    def create_startup_scripts(self):
        """Create startup scripts for different platforms."""
        logger.info("Creating startup scripts...")
        
        # Windows batch file
        if platform.system() == "Windows":
            batch_content = f"""@echo off
cd /d "{self.current_dir}"
python src/main.py
pause
"""
            batch_file = self.current_dir / "start_talinda_pos.bat"
            with open(batch_file, 'w') as f:
                f.write(batch_content)
            logger.info(f"Created startup script: {batch_file}")
        
        # Unix shell script
        shell_content = f"""#!/bin/bash
cd "{self.current_dir}"
python3 src/main.py
"""
        shell_file = self.current_dir / "start_talinda_pos.sh"
        with open(shell_file, 'w') as f:
            f.write(shell_content)
        
        # Make shell script executable
        if platform.system() != "Windows":
            os.chmod(shell_file, 0o755)
        logger.info(f"Created startup script: {shell_file}")
    
    def verify_setup(self):
        """Verify the setup."""
        logger.info("Verifying setup...")
        
        checks = [
            ("Database exists", self.database_path.exists()),
            ("Backup directory exists", self.backup_dir.exists()),
            ("Logs directory exists", (self.current_dir / "logs").exists()),
            ("Reports directory exists", (self.current_dir / "reports").exists()),
        ]
        
        all_passed = True
        for check_name, result in checks:
            if result:
                logger.info(f"✓ {check_name}")
            else:
                logger.error(f"✗ {check_name}")
                all_passed = False
        
        return all_passed
    
    def print_credentials(self):
        """Print login credentials."""
        print("\n" + "=" * 50)
        print("           LOGIN CREDENTIALS")
        print("=" * 50)
        print("⚠️  IMPORTANT: Change these passwords immediately!")
        print()
        print("ADMIN USER:")
        print(f"  Username: {self.default_admin['username']}")
        print(f"  Password: {self.default_admin['password']}")
        print()
        print("CASHIER USER:")
        print(f"  Username: {self.default_cashier['username']}")
        print(f"  Password: {self.default_cashier['password']}")
        print("=" * 50)
    
    def print_next_steps(self):
        """Print next steps."""
        print("\n" + "=" * 50)
        print("           NEXT STEPS")
        print("=" * 50)
        print("1. Start the application:")
        if platform.system() == "Windows":
            print("   Double-click: start_talinda_pos.bat")
        else:
            print("   Run: ./start_talinda_pos.sh")
        print("   Or run: python src/main.py")
        print()
        print("2. Login with the credentials above")
        print("3. Change default passwords immediately")
        print("4. Configure your business settings")
        print("5. Add your products and categories")
        print("=" * 50)
    
    def run_setup(self):
        """Run the complete setup process."""
        self.print_banner()
        
        # Check if user wants to continue
        if self.mode != 'quick':
            response = input("Do you want to continue with the setup? (y/N): ")
            if response.lower() not in ['y', 'yes']:
                print("Setup cancelled.")
                return False
        
        steps = [
            ("Checking system requirements", self.check_system_requirements),
            ("Installing dependencies", self.install_dependencies),
            ("Creating directories", self.create_directories),
            ("Backing up existing database", self.backup_existing_database),
            ("Cleaning database files", self.clean_database_files),
            ("Initializing database", self.initialize_database),
            ("Creating admin users", self.create_admin_users),
            ("Seeding default data", self.seed_default_data),
            ("Creating environment config", self.create_environment_config),
            ("Creating startup scripts", self.create_startup_scripts),
            ("Verifying setup", self.verify_setup),
        ]
        
        for step_name, step_func in steps:
            print(f"\n🔄 {step_name}...")
            if not step_func():
                logger.error(f"Setup failed at: {step_name}")
                return False
            print(f"✅ {step_name} completed")
        
        self.print_credentials()
        self.print_next_steps()
        
        logger.info("Setup completed successfully!")
        return True

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Universal Setup for Talinda POS")
    parser.add_argument('--mode', choices=['new-device', 'network', 'production', 'development', 'quick'],
                       default='new-device', help='Setup mode')
    parser.add_argument('--env', choices=['local', 'server', 'cloud'],
                       default='local', help='Environment type')
    
    args = parser.parse_args()
    
    setup = UniversalSetup(mode=args.mode, environment=args.env)
    success = setup.run_setup()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Setup failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 