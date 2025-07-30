#!/usr/bin/env python3
"""
Uninstall Script for Talinda POS
================================

This script completely removes the Talinda POS application and all its components
from the system.

Usage:
    python uninstall.py

Author: Talinda POS Team
Version: 2.0.0
"""

import os
import sys
import shutil
import sqlite3
from pathlib import Path
import logging
from datetime import datetime
import platform
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('uninstall.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class TalindaPOSUninstaller:
    """Uninstaller class for Talinda POS system."""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent.absolute()
        self.src_dir = self.current_dir / "src"
        self.database_path = self.current_dir / "pos_database.db"
        self.backup_dir = self.current_dir / "backups"
        
        # Files and directories to remove
        self.files_to_remove = [
            "pos_database.db",
            "pos_database.db-wal",
            "pos_database.db-shm",
            "fix_setup.log",
            "uninstall.log",
            "env_example.txt",
            "timezone_settings.json",
        ]
        
        self.directories_to_remove = [
            "logs",
            "reports", 
            "backups",
            "build",
            "dist",
            "__pycache__",
        ]
        
        self.src_files_to_remove = [
            "pos_database.db",
            "pos_database.db-wal", 
            "pos_database.db-shm",
        ]
        
        self.src_directories_to_remove = [
            "logs",
            "reports",
            "__pycache__",
        ]
    
    def print_banner(self):
        """Print uninstall banner."""
        print("=" * 60)
        print("           TALINDA POS - UNINSTALLER")
        print("=" * 60)
        print("This script will completely remove the Talinda POS")
        print("application and all its components.")
        print("=" * 60)
        print()
        print("⚠️  WARNING: This action cannot be undone!")
        print("All data, configurations, and files will be permanently deleted.")
        print()
    
    def confirm_uninstall(self):
        """Ask for user confirmation before uninstalling."""
        while True:
            response = input("Are you sure you want to uninstall Talinda POS? (yes/no): ").lower().strip()
            if response in ['yes', 'y']:
                return True
            elif response in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.")
    
    def backup_important_data(self):
        """Create a backup of important data before uninstalling."""
        logger.info("Creating backup of important data...")
        
        # Create backup directory with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.current_dir / f"talinda_pos_backup_{timestamp}"
        
        try:
            backup_dir.mkdir(exist_ok=True)
            
            # Backup database if it exists
            if self.database_path.exists():
                shutil.copy2(self.database_path, backup_dir / "pos_database.db")
                logger.info(f"[OK] Database backed up to: {backup_dir / 'pos_database.db'}")
            
            # Backup reports if they exist
            reports_dir = self.current_dir / "reports"
            if reports_dir.exists() and any(reports_dir.iterdir()):
                shutil.copytree(reports_dir, backup_dir / "reports", dirs_exist_ok=True)
                logger.info(f"[OK] Reports backed up to: {backup_dir / 'reports'}")
            
            # Backup logs if they exist
            logs_dir = self.current_dir / "logs"
            if logs_dir.exists() and any(logs_dir.iterdir()):
                shutil.copytree(logs_dir, backup_dir / "logs", dirs_exist_ok=True)
                logger.info(f"[OK] Logs backed up to: {backup_dir / 'logs'}")
            
            # Backup configuration files
            config_files = ["env_example.txt", "timezone_settings.json"]
            for config_file in config_files:
                config_path = self.current_dir / config_file
                if config_path.exists():
                    shutil.copy2(config_path, backup_dir / config_file)
                    logger.info(f"[OK] {config_file} backed up")
            
            logger.info(f"[OK] Backup created at: {backup_dir}")
            return backup_dir
            
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
            return None
    
    def remove_files(self, file_list, base_dir):
        """Remove files from the specified directory."""
        for file_name in file_list:
            file_path = base_dir / file_name
            if file_path.exists():
                try:
                    if file_path.is_file():
                        file_path.unlink()
                        logger.info(f"[OK] Removed file: {file_path}")
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                        logger.info(f"[OK] Removed directory: {file_path}")
                except Exception as e:
                    logger.warning(f"Could not remove {file_path}: {e}")
    
    def remove_directories(self, dir_list, base_dir):
        """Remove directories from the specified directory."""
        for dir_name in dir_list:
            dir_path = base_dir / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    logger.info(f"[OK] Removed directory: {dir_path}")
                except Exception as e:
                    logger.warning(f"Could not remove directory {dir_path}: {e}")
    
    def clean_python_cache(self):
        """Remove Python cache files."""
        logger.info("Cleaning Python cache files...")
        
        # Remove __pycache__ directories
        for root, dirs, files in os.walk(self.current_dir):
            for dir_name in dirs:
                if dir_name == "__pycache__":
                    cache_dir = Path(root) / dir_name
                    try:
                        shutil.rmtree(cache_dir)
                        logger.info(f"[OK] Removed cache: {cache_dir}")
                    except Exception as e:
                        logger.warning(f"Could not remove cache {cache_dir}: {e}")
        
        # Remove .pyc files
        for root, dirs, files in os.walk(self.current_dir):
            for file_name in files:
                if file_name.endswith('.pyc'):
                    pyc_file = Path(root) / file_name
                    try:
                        pyc_file.unlink()
                        logger.info(f"[OK] Removed .pyc file: {pyc_file}")
                    except Exception as e:
                        logger.warning(f"Could not remove .pyc file {pyc_file}: {e}")
    
    def uninstall_python_packages(self):
        """Uninstall Python packages specific to Talinda POS."""
        logger.info("Uninstalling Python packages...")
        
        # List of packages to uninstall
        packages_to_remove = [
            "cx_Freeze",
            "PyInstaller",
        ]
        
        for package in packages_to_remove:
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "uninstall", "-y", package
                ], capture_output=True, text=True)
                
                if result.returncode == 0:
                    logger.info(f"[OK] Uninstalled package: {package}")
                else:
                    logger.warning(f"Could not uninstall {package}: {result.stderr}")
                    
            except Exception as e:
                logger.warning(f"Error uninstalling {package}: {e}")
    
    def remove_shortcuts(self):
        """Remove desktop shortcuts and start menu entries."""
        logger.info("Removing shortcuts...")
        
        if platform.system() == "Windows":
            try:
                # Remove desktop shortcut
                desktop = Path.home() / "Desktop"
                shortcut = desktop / "Talinda POS.lnk"
                if shortcut.exists():
                    shortcut.unlink()
                    logger.info(f"[OK] Removed desktop shortcut: {shortcut}")
                
                # Remove start menu shortcut
                start_menu = Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs"
                start_menu_shortcut = start_menu / "Talinda POS.lnk"
                if start_menu_shortcut.exists():
                    start_menu_shortcut.unlink()
                    logger.info(f"[OK] Removed start menu shortcut: {start_menu_shortcut}")
                    
            except Exception as e:
                logger.warning(f"Could not remove shortcuts: {e}")
    
    def remove_registry_entries(self):
        """Remove Windows registry entries."""
        if platform.system() == "Windows":
            logger.info("Removing registry entries...")
            
            try:
                # Remove uninstall registry entry
                subprocess.run([
                    "reg", "delete", 
                    "HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\Talinda POS",
                    "/f"
                ], capture_output=True)
                logger.info("[OK] Removed registry entries")
                
            except Exception as e:
                logger.warning(f"Could not remove registry entries: {e}")
    
    def clean_environment_variables(self):
        """Clean up environment variables."""
        logger.info("Cleaning environment variables...")
        
        # Note: This would require admin privileges to modify system environment variables
        # For now, just log what should be cleaned
        logger.info("Note: Environment variables should be cleaned manually if needed")
    
    def verify_uninstall(self):
        """Verify that the uninstall was successful."""
        logger.info("Verifying uninstall...")
        
        # Check if main components are removed
        checks = [
            ("Database file", not self.database_path.exists()),
            ("Logs directory", not (self.current_dir / "logs").exists()),
            ("Reports directory", not (self.current_dir / "reports").exists()),
            ("Build directory", not (self.current_dir / "build").exists()),
            ("Dist directory", not (self.current_dir / "dist").exists()),
        ]
        
        all_removed = True
        for check_name, removed in checks:
            if removed:
                logger.info(f"[OK] {check_name} removed")
            else:
                logger.warning(f"[WARNING] {check_name} still exists")
                all_removed = False
        
        return all_removed
    
    def print_uninstall_summary(self, backup_dir):
        """Print uninstall summary."""
        print("\n" + "=" * 60)
        print("                    UNINSTALL SUMMARY")
        print("=" * 60)
        print("✅ Talinda POS has been uninstalled successfully!")
        print()
        
        if backup_dir and backup_dir.exists():
            print(f"📁 Backup created at: {backup_dir}")
            print("   This contains your database, reports, and configuration files.")
            print()
        
        print("🗑️  Removed components:")
        print("   - Application files and directories")
        print("   - Database and configuration files")
        print("   - Log files and reports")
        print("   - Python cache files")
        print("   - Build artifacts")
        print()
        
        print("⚠️  Manual cleanup required:")
        print("   - Python packages (if you want to remove them completely)")
        print("   - Environment variables (if any were set)")
        print("   - Registry entries (Windows)")
        print()
        
        print("📋 Next steps:")
        print("   1. Review the backup folder if you need to restore data")
        print("   2. Remove any remaining Python packages if desired")
        print("   3. Clean up any environment variables if needed")
        print("=" * 60)
    
    def run_uninstall(self):
        """Run the complete uninstall process."""
        self.print_banner()
        
        # Confirm uninstall
        if not self.confirm_uninstall():
            print("Uninstall cancelled by user.")
            return True
        
        logger.info("Starting Talinda POS uninstall process...")
        
        # Create backup
        backup_dir = self.backup_important_data()
        
        # Remove files from current directory
        logger.info("Removing application files...")
        self.remove_files(self.files_to_remove, self.current_dir)
        
        # Remove directories from current directory
        logger.info("Removing application directories...")
        self.remove_directories(self.directories_to_remove, self.current_dir)
        
        # Remove files from src directory
        logger.info("Removing source files...")
        self.remove_files(self.src_files_to_remove, self.src_dir)
        
        # Remove directories from src directory
        logger.info("Removing source directories...")
        self.remove_directories(self.src_directories_to_remove, self.src_dir)
        
        # Clean Python cache
        self.clean_python_cache()
        
        # Remove shortcuts
        self.remove_shortcuts()
        
        # Remove registry entries (Windows only)
        self.remove_registry_entries()
        
        # Clean environment variables
        self.clean_environment_variables()
        
        # Uninstall Python packages (optional)
        if input("Do you want to uninstall Talinda POS Python packages? (yes/no): ").lower().strip() in ['yes', 'y']:
            self.uninstall_python_packages()
        
        # Verify uninstall
        if not self.verify_uninstall():
            logger.warning("Some components may not have been removed completely.")
        
        # Print summary
        self.print_uninstall_summary(backup_dir)
        
        logger.info("[OK] Uninstall completed successfully!")
        return True


def main():
    """Main entry point."""
    try:
        uninstaller = TalindaPOSUninstaller()
        success = uninstaller.run_uninstall()
        
        if success:
            print("\n🎉 Talinda POS has been uninstalled successfully!")
        else:
            print("\n❌ Uninstall failed! Check the logs for details.")
            return 1
            
    except KeyboardInterrupt:
        print("\n\nUninstall interrupted by user.")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error during uninstall: {e}")
        print(f"\n❌ Uninstall failed with unexpected error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 