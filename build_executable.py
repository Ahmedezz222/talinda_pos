#!/usr/bin/env python3
"""
Build Executable for Talinda POS
================================

This script creates a standalone executable using cx_Freeze with improved
error handling and compatibility checks.

Usage:
    python build_executable.py

Author: Talinda POS Team
Version: 2.0.0
"""

import sys
import os
import shutil
import subprocess
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('build.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class ExecutableBuilder:
    """Builder class for creating Talinda POS executable."""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.src_dir = self.base_dir / "src"
        self.build_dir = self.base_dir / "build"
        self.dist_dir = self.base_dir / "dist"
        
        # Application information
        self.app_name = "Talinda POS"
        self.app_version = "2.0.0"
        
    def print_banner(self):
        """Print build banner."""
        print("=" * 60)
        print("           TALINDA POS - BUILD EXECUTABLE")
        print("=" * 60)
        print(f"Building {self.app_name} v{self.app_version}")
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
    
    def check_dependencies(self):
        """Check if required dependencies are installed."""
        logger.info("Checking dependencies...")
        
        required_packages = [
            "cx_Freeze",
            "PyQt5",
            "SQLAlchemy",
            "bcrypt",
            "reportlab",
            "openpyxl"
        ]
        
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                logger.info(f"✓ {package}")
            except ImportError:
                missing_packages.append(package)
                logger.error(f"✗ {package} - Not installed")
        
        if missing_packages:
            logger.error(f"Missing packages: {', '.join(missing_packages)}")
            logger.info("Install missing packages with: pip install " + " ".join(missing_packages))
            return False
        
        return True
    
    def clean_build_directories(self):
        """Clean previous build directories."""
        logger.info("Cleaning build directories...")
        
        directories_to_clean = [self.build_dir, self.dist_dir]
        
        for directory in directories_to_clean:
            if directory.exists():
                try:
                    shutil.rmtree(directory)
                    logger.info(f"Cleaned: {directory}")
                except Exception as e:
                    logger.warning(f"Could not clean {directory}: {e}")
    
    def create_directories(self):
        """Create necessary directories."""
        logger.info("Creating directories...")
        
        directories = [self.build_dir, self.dist_dir]
        
        for directory in directories:
            try:
                directory.mkdir(exist_ok=True)
                logger.info(f"Created: {directory}")
            except Exception as e:
                logger.error(f"Could not create {directory}: {e}")
                return False
        
        return True
    
    def check_source_files(self):
        """Check if required source files exist."""
        logger.info("Checking source files...")
        
        required_files = [
            self.src_dir / "main.py",
            self.src_dir / "config.py",
            self.src_dir / "init_database.py",
            self.src_dir / "manage.py",
        ]
        
        missing_files = []
        
        for file_path in required_files:
            if not file_path.exists():
                missing_files.append(str(file_path))
                logger.error(f"Missing: {file_path}")
            else:
                logger.info(f"✓ {file_path.name}")
        
        if missing_files:
            logger.error(f"Missing source files: {', '.join(missing_files)}")
            return False
        
        return True
    
    def run_build(self):
        """Run the cx_Freeze build process."""
        logger.info("Starting build process...")
        
        try:
            # Import cx_Freeze
            from cx_Freeze import setup, Executable
            
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
                    (str(self.src_dir / "resources"), "resources"),
                    (str(self.src_dir / "config.py"), "config.py"),
                    (str(self.src_dir / "init_database.py"), "init_database.py"),
                    (str(self.src_dir / "manage.py"), "manage.py"),
                    (str(self.src_dir / "fix_database.py"), "fix_database.py"),
                ],
                "include_msvcr": True,
                "optimize": 2,
                "zip_include_packages": ["*"],
                "zip_exclude_packages": [],
            }
            
            # Add migration files
            migration_files = list(self.src_dir.glob("migrate_*.py"))
            for migration_file in migration_files:
                build_exe_options["include_files"].append(
                    (str(migration_file), migration_file.name)
                )
            
            # Executable definition
            base = None
            if sys.platform == "win32":
                base = "Win32GUI"
            
            # Check if icon exists
            icon_path = self.src_dir / "resources" / "images" / "logo.ico"
            if not icon_path.exists():
                icon_path = None
            
            executables = [
                Executable(
                    script=str(self.src_dir / "main.py"),
                    base=base,
                    target_name=f"{self.app_name.replace(' ', '_')}.exe",
                    icon=str(icon_path) if icon_path else None,
                    shortcut_name=self.app_name,
                    shortcut_dir="DesktopFolder",
                )
            ]
            
            # Run setup
            setup(
                name=self.app_name,
                version=self.app_version,
                description="A comprehensive Point of Sale system built with PyQt5",
                author="Talinda POS Team",
                options={"build_exe": build_exe_options},
                executables=executables,
            )
            
            logger.info("Build completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Build failed: {e}")
            return False
    
    def copy_additional_files(self):
        """Copy additional files to the build directory."""
        logger.info("Copying additional files...")
        
        # Find the build directory
        build_dirs = list(self.build_dir.glob("exe.*"))
        if not build_dirs:
            logger.error("Build directory not found!")
            return False
        
        build_dir = build_dirs[0]
        
        # Copy additional files
        additional_files = [
            "README.md",
            "requirements.txt",
            "USER_SETUP_GUIDE.md",
            "create_login_users.py",
        ]
        
        for file_name in additional_files:
            file_path = self.base_dir / file_name
            if file_path.exists():
                try:
                    shutil.copy2(file_path, build_dir)
                    logger.info(f"Copied: {file_name}")
                except Exception as e:
                    logger.warning(f"Could not copy {file_name}: {e}")
        
        return True
    
    def verify_build(self):
        """Verify that the build was successful."""
        logger.info("Verifying build...")
        
        # Find the build directory
        build_dirs = list(self.build_dir.glob("exe.*"))
        if not build_dirs:
            logger.error("Build directory not found!")
            return False
        
        build_dir = build_dirs[0]
        exe_file = build_dir / f"{self.app_name.replace(' ', '_')}.exe"
        
        if not exe_file.exists():
            logger.error(f"Executable not found: {exe_file}")
            return False
        
        logger.info(f"✓ Executable created: {exe_file}")
        logger.info(f"✓ Build directory: {build_dir}")
        
        # Show build size
        try:
            size_mb = exe_file.stat().st_size / (1024 * 1024)
            logger.info(f"✓ Executable size: {size_mb:.1f} MB")
        except Exception:
            pass
        
        return True
    
    def print_success_message(self):
        """Print success message with next steps."""
        build_dirs = list(self.build_dir.glob("exe.*"))
        if build_dirs:
            build_dir = build_dirs[0]
            exe_file = build_dir / f"{self.app_name.replace(' ', '_')}.exe"
            
            print("\n" + "=" * 60)
            print("                    BUILD SUCCESSFUL!")
            print("=" * 60)
            print(f"Executable: {exe_file}")
            print(f"Build directory: {build_dir}")
            print()
            print("Next steps:")
            print("1. Test the executable by running it")
            print("2. Create an installer if needed")
            print("3. Distribute the build directory")
            print("=" * 60)
    
    def run(self):
        """Run the complete build process."""
        self.print_banner()
        
        # Check Python version
        if not self.check_python_version():
            return False
        
        # Check dependencies
        if not self.check_dependencies():
            return False
        
        # Check source files
        if not self.check_source_files():
            return False
        
        # Clean build directories
        self.clean_build_directories()
        
        # Create directories
        if not self.create_directories():
            return False
        
        # Run build
        if not self.run_build():
            return False
        
        # Copy additional files
        self.copy_additional_files()
        
        # Verify build
        if not self.verify_build():
            return False
        
        # Print success message
        self.print_success_message()
        
        return True


def main():
    """Main entry point."""
    try:
        builder = ExecutableBuilder()
        success = builder.run()
        
        if success:
            print("\n🎉 Build completed successfully!")
            return 0
        else:
            print("\n❌ Build failed! Check the logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nBuild interrupted by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during build: {e}")
        print(f"\n❌ Build failed with unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 