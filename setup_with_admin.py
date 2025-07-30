#!/usr/bin/env python3
"""
Enhanced Setup script for Talinda POS with Admin Configuration
=============================================================

This script creates a standalone executable and installer using cx_Freeze,
with the ability to set admin username and password during build.
"""

import sys
import os
import getpass
import hashlib
import sqlite3
from pathlib import Path

# Try to import cx_Freeze, provide helpful error if not available
try:
    from cx_Freeze import setup, Executable
    CX_FREEZE_AVAILABLE = True
except ImportError:
    CX_FREEZE_AVAILABLE = False
    print("ERROR: cx_Freeze is not installed.")
    print("Please install it using: pip install cx_Freeze")
    print("Or use the alternative build script: python build_installer.py")
    sys.exit(1)

def get_admin_credentials():
    """Prompt user for admin credentials."""
    print("\n" + "="*60)
    print("ADMIN CREDENTIALS SETUP")
    print("="*60)
    print("Please enter the admin credentials for Talinda POS:")
    print("(These will be embedded in the application)")
    print()
    
    while True:
        username = input("Admin Username: ").strip()
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
        if len(username) < 3:
            print("Username must be at least 3 characters long.")
            continue
        break
    
    while True:
        password = getpass.getpass("Admin Password: ")
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
        if len(password) < 6:
            print("Password must be at least 6 characters long.")
            continue
        
        confirm_password = getpass.getpass("Confirm Password: ")
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue
        break
    
    return username, password

def create_admin_config(username, password):
    """Create admin configuration file."""
    import bcrypt
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Create admin config content
    config_content = f'''#!/usr/bin/env python3
"""
Admin Configuration for Talinda POS
==================================

This file contains the default admin credentials for Talinda POS.
Generated during build process.
"""

# Default admin credentials
DEFAULT_ADMIN_USERNAME = "{username}"
DEFAULT_ADMIN_PASSWORD_HASH = {hashed_password}

def get_default_admin_credentials():
    """Get default admin credentials."""
    return DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD_HASH

def verify_admin_credentials(username, password):
    """Verify admin credentials."""
    import bcrypt
    return (username == DEFAULT_ADMIN_USERNAME and 
            bcrypt.checkpw(password.encode('utf-8'), DEFAULT_ADMIN_PASSWORD_HASH))
'''
    
    return config_content

def create_database_with_admin(username, password):
    """Create initial database with admin user."""
    import bcrypt
    
    # Hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Create database content
    db_content = f'''-- Talinda POS Database with Admin User
-- Generated during build process

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert default admin user
INSERT OR REPLACE INTO users (username, password_hash, role) 
VALUES ('{username}', '{hashed_password.decode()}', 'admin');

-- Create other necessary tables (simplified)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER DEFAULT 0,
    category TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_number TEXT UNIQUE NOT NULL,
    total_amount REAL NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
'''
    
    return db_content

def main():
    """Main setup function."""
    print("Talinda POS Setup with Admin Configuration")
    print("="*50)
    
    # Get admin credentials
    username, password = get_admin_credentials()
    
    print(f"\nAdmin credentials set:")
    print(f"Username: {username}")
    print(f"Password: {'*' * len(password)}")
    
    # Confirm
    confirm = input("\nProceed with build? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Build cancelled.")
        sys.exit(0)
    
    # Create admin config file
    admin_config_content = create_admin_config(username, password)
    admin_config_path = Path("src") / "admin_config.py"
    
    with open(admin_config_path, 'w', encoding='utf-8') as f:
        f.write(admin_config_content)
    
    print(f"Admin config created: {admin_config_path}")
    
    # Create initial database
    db_content = create_database_with_admin(username, password)
    db_path = Path("src") / "initial_database.sql"
    
    with open(db_path, 'w', encoding='utf-8') as f:
        f.write(db_content)
    
    print(f"Initial database created: {db_path}")
    
    # Application information
    APP_NAME = "Talinda POS"
    APP_VERSION = "2.0.0"
    APP_AUTHOR = "Talinda POS Team"
    APP_DESCRIPTION = "A comprehensive Point of Sale system built with PyQt5"

    # Base directory
    BASE_DIR = Path(__file__).parent
    SRC_DIR = BASE_DIR / "src"

    # Build options
    build_exe_options = {
        "packages": [
            "PyQt5",
            "PyQt5.QtCore",
            "PyQt5.QtGui", 
            "PyQt5.QtWidgets",
            "sqlalchemy",
            "sqlalchemy.orm",
            "sqlalchemy.ext.declarative",
            "bcrypt",
            "dotenv",
            "reportlab",
            "qrcode",
            "PIL",
            "openpyxl",
            "logging",
            "datetime",
            "pathlib",
            "typing",
            "traceback",
            "zipfile",
            "json",
            "csv",
            "xml",
            "xml.etree",
            "xml.etree.ElementTree",
        ],
        "excludes": [
            "tkinter",
            "matplotlib",
            "numpy",
            "scipy",
            "pandas",
            "jupyter",
            "IPython",
            "notebook",
            "sphinx",
            "docutils",
            "pydoc",
            "doctest",
            "unittest",
            "test",
            "tests",
            "distutils",
            "setuptools",
            "pip",
            "wheel",
            "virtualenv",
            "venv",
        ],
        "include_files": [
            (str(SRC_DIR / "resources"), "resources"),
            (str(SRC_DIR / "config.py"), "config.py"),
            (str(SRC_DIR / "admin_config.py"), "admin_config.py"),
            (str(SRC_DIR / "initial_database.sql"), "initial_database.sql"),
            (str(SRC_DIR / "init_database.py"), "init_database.py"),
            (str(SRC_DIR / "manage.py"), "manage.py"),
            (str(SRC_DIR / "fix_database.py"), "fix_database.py"),
        ],
        "include_msvcr": True,
        "optimize": 2,
        "build_exe": str(BASE_DIR / "build" / "exe.win-amd64-3.8"),
    }

    # Add migration files
    migration_files = list(SRC_DIR.glob("migrate_*.py"))
    for migration_file in migration_files:
        build_exe_options["include_files"].append(
            (str(migration_file), migration_file.name)
        )

    # Executable definition
    base = None
    if sys.platform == "win32":
        base = "Win32GUI"  # Use Win32GUI for Windows GUI applications

    executables = [
        Executable(
            script=str(SRC_DIR / "main.py"),
            base=base,
            target_name=f"{APP_NAME.replace(' ', '_')}.exe",
            icon=str(SRC_DIR / "resources" / "images" / "logo.ico") if (SRC_DIR / "resources" / "images" / "logo.ico").exists() else None,
            shortcut_name=APP_NAME,
            shortcut_dir="DesktopFolder",
        )
    ]

    # Setup configuration
    if CX_FREEZE_AVAILABLE:
        print("\nBuilding executable with admin credentials...")
        setup(
            name=APP_NAME,
            version=APP_VERSION,
            description=APP_DESCRIPTION,
            author=APP_AUTHOR,
            options={"build_exe": build_exe_options},
            executables=executables,
            requires=[
                "PyQt5>=5.15.9",
                "SQLAlchemy>=2.0.19",
                "bcrypt>=4.0.1",
                "python-dotenv>=1.0.0",
                "reportlab>=4.0.4",
                "qrcode>=7.4.2",
                "Pillow>=10.0.0",
                "openpyxl>=3.1.2",
            ],
        )
        print("\nBuild completed successfully!")
        print(f"Admin username: {username}")
        print("Please save these credentials securely.")
    else:
        print("cx_Freeze is not available. Cannot proceed with setup.")
        sys.exit(1)

if __name__ == "__main__":
    main() 