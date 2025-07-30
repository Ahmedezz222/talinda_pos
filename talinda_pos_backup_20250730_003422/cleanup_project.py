#!/usr/bin/env python3
"""
Talinda POS Project Cleanup Script
==================================

This script removes unnecessary files to optimize installer size and project cleanliness.
It identifies and removes:
- Test files
- Documentation files
- Build artifacts
- Cache files
- Database files (with backup option)
- Development-only files
- Temporary files
"""

import os
import sys
import shutil
import argparse
from pathlib import Path
from datetime import datetime
import zipfile

class ProjectCleaner:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.backup_dir = None
        self.removed_files = []
        self.removed_dirs = []
        self.total_size_removed = 0
        
    def create_backup(self):
        """Create a backup of the project before cleaning."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"talinda_pos_backup_{timestamp}"
        self.backup_dir = self.project_root.parent / backup_name
        
        print(f"Creating backup at: {self.backup_dir}")
        
        # Create backup directory
        self.backup_dir.mkdir(exist_ok=True)
        
        # Copy project files to backup
        for item in self.project_root.iterdir():
            if item.name not in ['.git', '__pycache__', '.pytest_cache', '.vscode', '.idea']:
                if item.is_file():
                    shutil.copy2(item, self.backup_dir / item.name)
                elif item.is_dir():
                    shutil.copytree(item, self.backup_dir / item.name, 
                                  ignore=shutil.ignore_patterns('__pycache__', '.pytest_cache'))
        
        print(f"Backup created successfully: {self.backup_dir}")
        
    def get_file_size(self, file_path):
        """Get file size in bytes."""
        try:
            return file_path.stat().st_size
        except:
            return 0
            
    def remove_file(self, file_path, reason=""):
        """Remove a file and track it."""
        try:
            size = self.get_file_size(file_path)
            file_path.unlink()
            self.removed_files.append((str(file_path), size, reason))
            self.total_size_removed += size
            print(f"Removed: {file_path} ({size} bytes) - {reason}")
            return True
        except Exception as e:
            print(f"Failed to remove {file_path}: {e}")
            return False
            
    def remove_directory(self, dir_path, reason=""):
        """Remove a directory and track it."""
        try:
            # Calculate total size of directory
            total_size = 0
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    total_size += self.get_file_size(file_path)
            
            shutil.rmtree(dir_path)
            self.removed_dirs.append((str(dir_path), total_size, reason))
            self.total_size_removed += total_size
            print(f"Removed directory: {dir_path} ({total_size} bytes) - {reason}")
            return True
        except Exception as e:
            print(f"Failed to remove directory {dir_path}: {e}")
            return False
    
    def clean_test_files(self):
        """Remove all test files and test-related documentation."""
        print("\n=== Cleaning Test Files ===")
        
        # Test files to remove
        test_patterns = [
            "test_*.py",
            "*_test.py",
            "test_*.md",
            "*_test.md"
        ]
        
        # Documentation files to remove
        doc_patterns = [
            "*_IMPLEMENTATION.md",
            "*_SUMMARY.md",
            "*_README.md",
            "*_FIX_*.md",
            "*_ENHANCEMENT_*.md",
            "*_IMPROVEMENTS.md",
            "*_FUNCTIONALITY.md",
            "*_MANAGEMENT.md",
            "*_AUTH.md",
            "*_REPORT.md",
            "*_FIXES.md",
            "*_SUPPORT.md",
            "*_LANGUAGE.md",
            "*_RESET.md",
            "*_MEMORY.md",
            "*_SIGNAL.md",
            "*_DUPLICATE.md",
            "*_VISIBILITY.md",
            "*_SIZING.md",
            "*_CHECKOUT.md",
            "*_COMPLETION.md",
            "*_SAVE.md",
            "*_EXCEL.md",
            "*_SHIFT.md",
            "*_ORDER.md",
            "*_SALES.md",
            "*_PAYMENT.md",
            "*_CLOSING.md",
            "*_STOCK.md",
            "*_IMPORT.md",
            "*_EXPORT.md",
            "*_DATA.md",
            "*_REPORT.md",
            "*_UI.md",
            "*_CSS.md",
            "*_FORM.md",
            "*_GRID.md",
            "*_RESPONSIVE.md",
            "*_CONTENT.md",
            "*_MESSAGE.md",
            "*_INDENTATION.md",
            "*_PARSING.md",
            "*_LOCK.md",
            "*_CREDENTIALS.md",
            "*_PLAN.md",
            "*_FIXES.md",
            "*_IMPROVEMENTS.md"
        ]
        
        # Remove test files
        for pattern in test_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "Test file")
        
        # Remove documentation files
        for pattern in doc_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "Documentation file")
    
    def clean_cache_files(self):
        """Remove cache and temporary files."""
        print("\n=== Cleaning Cache Files ===")
        
        cache_patterns = [
            "__pycache__",
            ".pytest_cache",
            "*.pyc",
            "*.pyo",
            "*.pyd",
            "*.so",
            "*.dll",
            "*.exe",
            "*.msi",
            "*.zip",
            "*.tar.gz",
            "*.whl",
            "build/",
            "dist/",
            "*.egg-info/",
            ".coverage",
            "htmlcov/",
            ".tox/",
            ".mypy_cache/",
            ".ruff_cache/",
            ".flake8_cache/",
            "*.log",
            "*.tmp",
            "*.temp",
            "*.bak",
            "*.backup",
            "*.old",
            "*.orig"
        ]
        
        for pattern in cache_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                dir_name = pattern[:-1]
                for dir_path in self.project_root.rglob(dir_name):
                    if dir_path.is_dir():
                        self.remove_directory(dir_path, "Cache directory")
            else:
                # File pattern
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        self.remove_file(file_path, "Cache file")
    
    def clean_database_files(self, keep_backup=True):
        """Remove database files (with optional backup)."""
        print("\n=== Cleaning Database Files ===")
        
        db_patterns = [
            "*.db",
            "*.db-shm",
            "*.db-wal",
            "*.sqlite",
            "*.sqlite3"
        ]
        
        for pattern in db_patterns:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    if keep_backup and self.backup_dir:
                        # Copy to backup before removing
                        backup_path = self.backup_dir / file_path.relative_to(self.project_root)
                        backup_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(file_path, backup_path)
                        print(f"Backed up: {file_path} -> {backup_path}")
                    
                    self.remove_file(file_path, "Database file")
    
    def clean_development_files(self):
        """Remove development-only files."""
        print("\n=== Cleaning Development Files ===")
        
        dev_patterns = [
            ".vscode/",
            ".idea/",
            ".git/",
            "*.sublime-*",
            ".editorconfig",
            ".gitignore",
            ".gitattributes",
            "pytest.ini",
            "tox.ini",
            ".flake8",
            ".pylintrc",
            "mypy.ini",
            "pyproject.toml",
            "setup.cfg",
            "MANIFEST.in",
            "requirements-dev.txt",
            "requirements-test.txt",
            "requirements-build.txt",
            "*.spec",
            "demo_*.py",
            "example_*.py",
            "sample_*.py"
        ]
        
        for pattern in dev_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                dir_name = pattern[:-1]
                for dir_path in self.project_root.rglob(dir_name):
                    if dir_path.is_dir():
                        self.remove_directory(dir_path, "Development directory")
            else:
                # File pattern
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        self.remove_file(file_path, "Development file")
    
    def clean_build_artifacts(self):
        """Remove build artifacts and temporary files."""
        print("\n=== Cleaning Build Artifacts ===")
        
        build_patterns = [
            "build/",
            "dist/",
            "*.egg-info/",
            "*.egg",
            "*.whl",
            "*.tar.gz",
            "*.zip",
            "*.exe",
            "*.msi",
            "*.dmg",
            "*.deb",
            "*.rpm",
            "*.app",
            "*.appimage",
            "*.snap",
            "*.flatpak",
            "*.spec",
            "*.manifest",
            "*.pdb",
            "*.map",
            "*.exp",
            "*.lib",
            "*.a",
            "*.o",
            "*.obj",
            "*.so",
            "*.dll",
            "*.dylib",
            "*.bundle",
            "*.framework"
        ]
        
        for pattern in build_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                dir_name = pattern[:-1]
                for dir_path in self.project_root.rglob(dir_name):
                    if dir_path.is_dir():
                        self.remove_directory(dir_path, "Build directory")
            else:
                # File pattern
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        self.remove_file(file_path, "Build artifact")
    
    def clean_report_files(self):
        """Remove generated report files."""
        print("\n=== Cleaning Report Files ===")
        
        report_patterns = [
            "reports/",
            "*.xlsx",
            "*.xls",
            "*.csv",
            "*.pdf",
            "*.html",
            "*.json",
            "*.xml",
            "*.txt"
        ]
        
        for pattern in report_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                dir_name = pattern[:-1]
                for dir_path in self.project_root.rglob(dir_name):
                    if dir_path.is_dir():
                        self.remove_directory(dir_path, "Report directory")
            else:
                # File pattern
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        # Skip important files
                        if file_path.name in ['requirements.txt', 'README.md', 'LICENSE']:
                            continue
                        self.remove_file(file_path, "Report file")
    
    def clean_logs(self):
        """Remove log files."""
        print("\n=== Cleaning Log Files ===")
        
        log_patterns = [
            "logs/",
            "*.log",
            "*.log.*",
            "*.out",
            "*.err",
            "*.trace",
            "*.dump",
            "*.crash",
            "*.stack"
        ]
        
        for pattern in log_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                dir_name = pattern[:-1]
                for dir_path in self.project_root.rglob(dir_name):
                    if dir_path.is_dir():
                        self.remove_directory(dir_path, "Log directory")
            else:
                # File pattern
                for file_path in self.project_root.rglob(pattern):
                    if file_path.is_file():
                        self.remove_file(file_path, "Log file")
    
    def clean_migration_files(self):
        """Remove database migration files (keep only essential ones)."""
        print("\n=== Cleaning Migration Files ===")
        
        migration_files = [
            "migrate_*.py",
            "fix_database.py",
            "init_database.py"
        ]
        
        for pattern in migration_files:
            for file_path in self.project_root.rglob(pattern):
                if file_path.is_file():
                    self.remove_file(file_path, "Migration file")
    
    def clean_duplicate_files(self):
        """Remove duplicate files in src directory."""
        print("\n=== Cleaning Duplicate Files ===")
        
        # Remove duplicate database files in src
        src_db_files = list(self.project_root.rglob("src/*.db*"))
        if len(src_db_files) > 1:
            # Keep the largest one, remove others
            src_db_files.sort(key=lambda x: x.stat().st_size, reverse=True)
            for db_file in src_db_files[1:]:
                self.remove_file(db_file, "Duplicate database file")
    
    def generate_cleanup_report(self):
        """Generate a report of what was cleaned."""
        print("\n" + "="*60)
        print("CLEANUP REPORT")
        print("="*60)
        
        print(f"\nTotal files removed: {len(self.removed_files)}")
        print(f"Total directories removed: {len(self.removed_dirs)}")
        print(f"Total size removed: {self.total_size_removed:,} bytes ({self.total_size_removed / 1024 / 1024:.2f} MB)")
        
        if self.removed_files:
            print(f"\nRemoved files:")
            for file_path, size, reason in self.removed_files:
                print(f"  - {file_path} ({size:,} bytes) - {reason}")
        
        if self.removed_dirs:
            print(f"\nRemoved directories:")
            for dir_path, size, reason in self.removed_dirs:
                print(f"  - {dir_path} ({size:,} bytes) - {reason}")
        
        if self.backup_dir:
            print(f"\nBackup created at: {self.backup_dir}")
        
        # Save report to file
        report_file = self.project_root / "cleanup_report.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("TALINDA POS CLEANUP REPORT\n")
            f.write("="*40 + "\n\n")
            f.write(f"Cleanup performed on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total files removed: {len(self.removed_files)}\n")
            f.write(f"Total directories removed: {len(self.removed_dirs)}\n")
            f.write(f"Total size removed: {self.total_size_removed:,} bytes ({self.total_size_removed / 1024 / 1024:.2f} MB)\n\n")
            
            if self.removed_files:
                f.write("REMOVED FILES:\n")
                for file_path, size, reason in self.removed_files:
                    f.write(f"  - {file_path} ({size:,} bytes) - {reason}\n")
                f.write("\n")
            
            if self.removed_dirs:
                f.write("REMOVED DIRECTORIES:\n")
                for dir_path, size, reason in self.removed_dirs:
                    f.write(f"  - {dir_path} ({size:,} bytes) - {reason}\n")
                f.write("\n")
            
            if self.backup_dir:
                f.write(f"Backup created at: {self.backup_dir}\n")
        
        print(f"\nCleanup report saved to: {report_file}")
    
    def clean_all(self, create_backup=True, keep_db_backup=True):
        """Perform complete cleanup."""
        print("Starting Talinda POS Project Cleanup...")
        print(f"Project root: {self.project_root}")
        
        if create_backup:
            self.create_backup()
        
        # Perform all cleanup operations
        self.clean_test_files()
        self.clean_cache_files()
        self.clean_database_files(keep_backup=keep_db_backup)
        self.clean_development_files()
        self.clean_build_artifacts()
        self.clean_report_files()
        self.clean_logs()
        self.clean_migration_files()
        self.clean_duplicate_files()
        
        # Generate report
        self.generate_cleanup_report()
        
        print("\nCleanup completed successfully!")
        print("Your project is now optimized for installer creation.")

def main():
    parser = argparse.ArgumentParser(description="Clean Talinda POS project for installer optimization")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup before cleanup")
    parser.add_argument("--no-db-backup", action="store_true", help="Don't backup database files")
    parser.add_argument("--project-root", default=".", help="Project root directory")
    
    args = parser.parse_args()
    
    cleaner = ProjectCleaner(args.project_root)
    cleaner.clean_all(
        create_backup=not args.no_backup,
        keep_db_backup=not args.no_db_backup
    )

if __name__ == "__main__":
    main() 