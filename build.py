import os
import sys
import shutil
import PyInstaller.__main__

def clean_build_directories():
    """Clean up previous build directories safely."""
    import time
    import psutil

    # Try to close any running instances of the application
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if 'TalindaPOS' in proc.info['name']:
                proc.kill()
                time.sleep(1)  # Give the process time to close
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # Clean up previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
            except PermissionError:
                print(f"Could not remove {dir_name}. Please close any running instances of the application.")
                sys.exit(1)

def build_executable():
    """Build the executable using PyInstaller."""
    # Clean up previous builds
    clean_build_directories()
    
    # PyInstaller configuration
    args = [
        'src\\main.py',  # Script to package
        '--name=TalindaPOS',  # Name of the executable
        '--onedir',  # Create a directory containing the executable
        '--windowed',  # Windows: hide console window
        '--noconsole',  # Hide console on Windows
        '--clean',  # Clean PyInstaller cache
        '--add-data=resources/translations;resources/translations',  # Translations
        '--add-data=logs;logs',  # Logs directory
        # Database files
        '--add-data=src/database;database',
        # Add the source directory to Python path
        '--paths=.',
        '--paths=src',
        # Hidden imports
        '--hidden-import=PyQt5.QtCore',
        '--hidden-import=PyQt5.QtGui',
        '--hidden-import=PyQt5.QtWidgets',
        '--hidden-import=sqlalchemy.ext.baked',
        '--hidden-import=sqlalchemy.ext.declarative',
        '--hidden-import=sqlalchemy.orm',
        '--hidden-import=bcrypt',
        '--hidden-import=openpyxl',
        '--hidden-import=PIL',
        # Add all project modules
        '--hidden-import=ui.main_window',
        '--hidden-import=ui.components',
        '--hidden-import=models',
        '--hidden-import=controllers',
        '--hidden-import=utils',
        # Exclude unnecessary packages
        '--exclude-module=tkinter',
        '--exclude-module=matplotlib',
        '--exclude-module=notebook',
        '--exclude-module=jupyter',
        # Create a single file
        '--onefile',
        # Add version info
        '--version-file=version_info.txt'
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Build completed! Executable can be found in the 'dist' directory.")

if __name__ == "__main__":
    build_executable()
