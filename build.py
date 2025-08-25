import os
import sys
import shutil
import PyInstaller.__main__

def build_executable():
    """Build the executable using PyInstaller."""
    # Clean up previous builds
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
    
    # PyInstaller configuration
    args = [
        'src/main.py',  # Script to package
        '--name=TalindaPOS',  # Name of the executable
        '--onedir',  # Create a directory containing the executable
        '--windowed',  # Windows: hide console window
        '--icon=resources/images/logo.ico',  # Application icon
        # Add resource files
        '--add-data=src/resources/styles;resources/styles',
        '--add-data=src/resources/translations;resources/translations',
        '--add-data=src/resources/images;resources/images',
        # Hidden imports for SQLAlchemy and other packages
        '--hidden-import=sqlalchemy.ext.baked',
        '--hidden-import=sqlalchemy.ext.declarative',
        '--hidden-import=pkg_resources.py2_warn',
    ]
    
    # Run PyInstaller
    PyInstaller.__main__.run(args)
    
    print("Build completed! Executable can be found in the 'dist' directory.")

if __name__ == "__main__":
    build_executable()
