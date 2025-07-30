# Talinda POS - Fix App Setup Guide

## Overview

This guide provides comprehensive instructions for fixing common setup issues and properly configuring the Talinda POS application.

## Quick Fix

### For Windows Users

1. **Using Batch File (Recommended):**
   ```cmd
   fix_app_setup.bat
   ```

2. **Using PowerShell:**
   ```powershell
   .\fix_app_setup.ps1
   ```

3. **Using Python directly:**
   ```cmd
   python fix_app_setup.py
   ```

### For Linux/Mac Users

```bash
python3 fix_app_setup.py
```

## What the Fix Script Does

The `fix_app_setup.py` script automatically handles the following:

### 1. System Checks
- ✅ Verifies Python version (3.8+ required)
- ✅ Checks system platform and architecture
- ✅ Validates file paths and directories

### 2. Path and Directory Fixes
- ✅ Creates missing directories (logs, reports, backups)
- ✅ Fixes database path issues
- ✅ Ensures proper file structure

### 3. Database Management
- ✅ Backs up existing database (if any)
- ✅ Cleans corrupted database files (WAL/SHM)
- ✅ Initializes fresh database with proper schema
- ✅ Creates default admin and cashier users
- ✅ Seeds default categories (Food, Beverage, Dessert, Other)

### 4. Dependencies Installation
- ✅ Installs all required Python packages from `requirements.txt`
- ✅ Verifies package installation
- ✅ Handles installation errors gracefully

### 5. Configuration Setup
- ✅ Creates environment configuration file
- ✅ Sets up logging configuration
- ✅ Configures database settings

### 6. Permissions Fix
- ✅ Fixes file permissions on Unix-like systems
- ✅ Makes scripts executable where needed

### 7. Verification
- ✅ Tests application startup
- ✅ Verifies database connectivity
- ✅ Checks user creation
- ✅ Validates directory structure

## Default Credentials

After running the fix script, you'll have these default users:

### Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator

### Cashier User
- **Username:** `cashier`
- **Password:** `cashier123`
- **Role:** Cashier

⚠️ **IMPORTANT:** Change these passwords after first login!

## Manual Setup (If Fix Script Fails)

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 2. Initialize Database

```bash
cd src
python init_database.py
```

### 3. Create Default Users

```bash
python create_login_users.py
```

### 4. Run the Application

```bash
python src/main.py
```

## Common Issues and Solutions

### Issue: "Module not found" errors
**Solution:** Run the fix script to install dependencies:
```bash
python fix_app_setup.py
```

### Issue: Database connection errors
**Solution:** The fix script automatically handles database initialization and cleanup.

### Issue: Permission denied errors
**Solution:** On Unix-like systems, the fix script automatically fixes permissions.

### Issue: Missing directories
**Solution:** The fix script creates all necessary directories automatically.

### Issue: Application won't start
**Solution:** 
1. Run the fix script
2. Check the logs in the `logs/` directory
3. Ensure Python 3.8+ is installed

## File Structure After Setup

```
talinda_pos/
├── src/
│   ├── main.py                 # Main application
│   ├── config.py              # Configuration
│   ├── init_database.py       # Database initialization
│   ├── models/                # Database models
│   ├── controllers/           # Business logic
│   ├── ui/                    # User interface
│   └── resources/             # Resources (styles, images)
├── logs/                      # Application logs
├── reports/                   # Generated reports
├── backups/                   # Database backups
├── pos_database.db           # SQLite database
├── requirements.txt          # Python dependencies
├── fix_app_setup.py         # Fix script
├── fix_app_setup.bat        # Windows batch file
└── fix_app_setup.ps1        # PowerShell script
```

## Running the Application

After successful setup:

```bash
python src/main.py
```

## Next Steps

1. **Login** with the default credentials
2. **Change passwords** in the admin panel
3. **Configure business settings**
4. **Add your products and categories**
5. **Set up tax rates and pricing**

## Troubleshooting

### Check Logs
- Application logs: `logs/talinda_pos.log`
- Setup logs: `fix_setup.log`

### Verify Installation
```bash
python -c "import PyQt5, sqlalchemy, bcrypt; print('All dependencies installed')"
```

### Database Issues
```bash
python src/fix_database.py
```

### Reset Everything
1. Delete `pos_database.db`
2. Run `python fix_app_setup.py`

## Support

If you encounter issues:

1. Check the logs in the `logs/` directory
2. Run the fix script again
3. Ensure Python 3.8+ is installed
4. Check that all dependencies are installed

## System Requirements

- **Python:** 3.8 or higher
- **OS:** Windows 10+, macOS 10.14+, or Linux
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 1GB free space
- **Display:** 1024x768 minimum resolution

## Uninstallation

If you need to remove the Talinda POS application:

### Quick Uninstall
```bash
python uninstall.py
```

### Windows Users
```cmd
uninstall.bat
```

### PowerShell Users
```powershell
.\uninstall.ps1
```

**⚠️ Warning:** The uninstaller will permanently delete all data. Always backup important information first!

For detailed uninstallation instructions, see `UNINSTALL_GUIDE.md`.

---

**Note:** This fix script is designed to handle most common setup issues automatically. If you continue to experience problems, please check the logs and ensure your system meets the minimum requirements. 