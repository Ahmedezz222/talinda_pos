#!/usr/bin/env python3
"""
Setup script for Talinda POS
============================

This script creates a standalone executable and installer using cx_Freeze.
"""

import sys
import os
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
        "getpass",
        "enum",
        "collections",
        "itertools",
        "functools",
        "operator",
        "re",
        "hashlib",
        "base64",
        "urllib",
        "urllib.parse",
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
        "pytest",
        "pytest_qt",
        "pytest_cov",
    ],
    "include_files": [
        (str(SRC_DIR / "resources"), "resources"),
        (str(SRC_DIR / "config.py"), "config.py"),
        (str(SRC_DIR / "init_database.py"), "init_database.py"),
        (str(SRC_DIR / "manage.py"), "manage.py"),
        (str(SRC_DIR / "fix_database.py"), "fix_database.py"),
    ],
    "include_msvcr": True,
    "optimize": 2,
    "zip_include_packages": ["*"],
    "zip_exclude_packages": [],
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

# Check if icon exists
icon_path = SRC_DIR / "resources" / "images" / "logo.ico"
if not icon_path.exists():
    icon_path = None

executables = [
    Executable(
        script=str(SRC_DIR / "main.py"),
        base=base,
        target_name=f"{APP_NAME.replace(' ', '_')}.exe",
        icon=str(icon_path) if icon_path else None,
        shortcut_name=APP_NAME,
        shortcut_dir="DesktopFolder",
    )
]

# Setup configuration
if CX_FREEZE_AVAILABLE:
    setup(
        name=APP_NAME,
        version=APP_VERSION,
        description=APP_DESCRIPTION,
        author=APP_AUTHOR,
        options={"build_exe": build_exe_options},
        executables=executables,
    )
else:
    print("cx_Freeze is not available. Cannot proceed with setup.")
    sys.exit(1) 