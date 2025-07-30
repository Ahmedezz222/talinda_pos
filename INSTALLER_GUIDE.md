# Talinda POS - Executable Installer Guide

## Overview

This guide explains how to create a standalone executable installer for Talinda POS that will automatically install all dependencies and set up the application on any Windows system.

## What the Installer Does

The generated executable installer will:

1. **Check System Requirements** - Verify Python installation and system compatibility
2. **Install Python** - Download and install Python if not present
3. **Install Dependencies** - Install all required packages (PyQt5, SQLAlchemy, etc.)
4. **Set Up Database** - Create and initialize the SQLite database
5. **Create Startup Scripts** - Generate batch files for easy application startup
6. **Configure Application** - Set up default users and categories
7. **Create Desktop Shortcut** - Add a desktop shortcut for easy access

## Creating the Installer

### Prerequisites

- Python 3.8 or higher installed
- Internet connection for downloading packages
- Windows operating system

### Method 1: Using PowerShell Script (Recommended)

1. **Open PowerShell as Administrator**
2. **Navigate to the project directory**
   ```powershell
   cd "path\to\talinda_pos"
   ```
3. **Run the installer creator**
   ```powershell
   .\create_installer.ps1
   ```

### Method 2: Using Batch File

1. **Open Command Prompt as Administrator**
2. **Navigate to the project directory**
   ```cmd
   cd "path\to\talinda_pos"
   ```
3. **Run the installer creator**
   ```cmd
   create_installer.bat
   ```

### Method 3: Using Python Script

1. **Open Command Prompt or PowerShell**
2. **Navigate to the project directory**
   ```bash
   cd "path\to\talinda_pos"
   ```
3. **Run the installer creator**
   ```bash
   python create_installer.py
   ```

## What Happens During Creation

1. **Check Python** - Verifies Python is installed
2. **Install PyInstaller** - Installs PyInstaller if not present
3. **Create Installer Script** - Generates the main installer Python script
4. **Create Spec File** - Creates PyInstaller configuration
5. **Build Executable** - Compiles the installer into a standalone .exe file
6. **Clean Up** - Removes temporary files

## Output

After successful creation, you'll find:
- `TalindaPOS_Installer.exe` - The standalone installer executable

## Using the Installer

### For End Users

1. **Download the installer** - `TalindaPOS_Installer.exe`
2. **Run as Administrator** - Right-click and select "Run as administrator"
3. **Choose Installation Directory** - Select where to install Talinda POS
4. **Click Install** - The installer will handle everything automatically
5. **Wait for Completion** - Monitor progress in the installer window

### Default Credentials

After installation, users can log in with:

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Cashier User:**
- Username: `cashier`
- Password: `cashier123`

⚠️ **Important:** Users should change these passwords immediately after first login.

## Installation Directory Structure

The installer creates the following structure:

```
TalindaPOS/
├── main.py                 # Main application entry point
├── start_talinda_pos.bat   # Windows startup script
├── init_database.py        # Database initialization script
├── pos_database.db         # SQLite database
├── src/                    # Application source code
├── config/                 # Configuration files
├── logs/                   # Application logs
├── reports/                # Generated reports
└── backups/                # Database backups
```

## Starting the Application

After installation, users can start Talinda POS by:

1. **Double-clicking** `start_talinda_pos.bat`
2. **Using the desktop shortcut** (if created)
3. **Running** `python main.py` from the installation directory

## Troubleshooting

### Common Issues

1. **"Python not found"**
   - Ensure Python 3.8+ is installed
   - Add Python to PATH environment variable

2. **"Failed to install packages"**
   - Check internet connection
   - Try running as administrator
   - Verify pip is working: `python -m pip --version`

3. **"Permission denied"**
   - Run installer as administrator
   - Check antivirus software settings

4. **"PyInstaller not found"**
   - The installer creator will install it automatically
   - Manual install: `python -m pip install pyinstaller`

### Manual Installation

If the installer fails, users can manually install:

1. **Install Python** from https://python.org
2. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run setup**:
   ```bash
   python setup_universal.py
   ```

## Customization

### Modifying the Installer

To customize the installer behavior:

1. **Edit `create_installer.ps1`** - Modify the installer script generation
2. **Update requirements** - Modify the package list in the installer
3. **Change default settings** - Update default paths and configurations

### Adding Custom Files

To include additional files in the installer:

1. **Modify the installer script** to copy additional files
2. **Update the PyInstaller spec** to include data files
3. **Rebuild the installer**

## Security Considerations

1. **Default Passwords** - Always change default credentials
2. **Network Security** - Configure firewall settings if needed
3. **Database Security** - Consider encrypting the database
4. **User Permissions** - Use appropriate user roles and permissions

## Distribution

### Single File Distribution

The generated `TalindaPOS_Installer.exe` is completely self-contained and can be distributed as a single file.

### Distribution Methods

1. **Direct Download** - Host the .exe file on a website
2. **USB Drive** - Copy to USB for offline installation
3. **Network Share** - Share on local network
4. **Email** - Send as attachment (check size limits)

### File Size

The installer typically ranges from 50-100 MB depending on included dependencies.

## Support

For issues with the installer:

1. **Check the logs** in the installation directory
2. **Verify system requirements**
3. **Try manual installation**
4. **Contact support** with error details

## Version History

- **v1.0.0** - Initial installer creation
- **v2.0.0** - Added GUI installer interface
- **v3.0.0** - Enhanced error handling and user experience

---

**Note:** This installer is designed for Windows systems. For other operating systems, use the appropriate setup scripts provided in the project. 