# Talinda POS - Complete Setup and Uninstall Guide

## Overview

This comprehensive guide covers both setting up and uninstalling the Talinda POS application. The application is now fully functional with proper setup and uninstall capabilities.

## 🚀 Quick Start

### Setup the Application
```bash
# Windows (Batch)
fix_app_setup.bat

# Windows (PowerShell)
.\fix_app_setup.ps1

# All Platforms
python fix_app_setup.py
```

### Run the Application
```bash
python src/main.py
```

### Uninstall the Application
```bash
# Windows (Batch)
uninstall.bat

# Windows (PowerShell)
.\uninstall.ps1

# All Platforms
python uninstall.py
```

## 📋 Application Status

### ✅ Setup Complete
- **Database:** Initialized with default users and categories
- **Dependencies:** All required packages installed
- **Configuration:** Environment and logging configured
- **Directories:** All necessary folders created
- **Permissions:** File permissions set correctly

### ✅ Application Working
- **Startup:** Application launches successfully
- **Login:** Authentication system functional
- **Database:** All operations working
- **Reports:** Generation and export working
- **Background Tasks:** Running properly

## 🔧 Setup Process

### What the Setup Script Does

1. **System Verification**
   - Checks Python version (3.8+ required)
   - Validates system platform
   - Confirms file permissions

2. **Dependency Installation**
   - Installs all required Python packages
   - Verifies package installation
   - Handles installation errors

3. **Database Setup**
   - Creates SQLite database with proper schema
   - Seeds default categories (Food, Beverage, Dessert, Other)
   - Creates admin and cashier users

4. **Configuration**
   - Sets up logging system
   - Creates environment configuration
   - Configures application settings

5. **Directory Structure**
   - Creates logs, reports, and backups directories
   - Ensures proper file organization
   - Sets up resource directories

### Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Role: Administrator

**Cashier User:**
- Username: `cashier`
- Password: `cashier123`
- Role: Cashier

⚠️ **IMPORTANT:** Change these passwords after first login!

## 🗑️ Uninstall Process

### What the Uninstaller Does

1. **Data Backup**
   - Creates timestamped backup of database
   - Preserves reports and log files
   - Saves configuration files

2. **File Removal**
   - Removes application database files
   - Deletes log and report directories
   - Cleans configuration files

3. **System Cleanup**
   - Removes desktop shortcuts (Windows)
   - Cleans registry entries (Windows)
   - Removes Python cache files

4. **Verification**
   - Confirms all components removed
   - Provides detailed summary
   - Lists any remaining files

### Safety Features

- **Confirmation Required:** Asks for explicit confirmation
- **Automatic Backup:** Creates backup before deletion
- **Detailed Logging:** Records all actions
- **Graceful Handling:** Handles errors without crashing

## 📁 File Structure

```
talinda_pos/
├── src/                        # Main application code
│   ├── main.py                # Application entry point
│   ├── config.py              # Configuration management
│   ├── models/                # Database models
│   ├── controllers/           # Business logic
│   ├── ui/                    # User interface
│   └── resources/             # Styles and images
├── logs/                      # Application logs
├── reports/                   # Generated reports
├── backups/                   # Database backups
├── pos_database.db           # SQLite database
├── requirements.txt          # Python dependencies
├── fix_app_setup.py         # Setup script
├── fix_app_setup.bat        # Windows setup
├── fix_app_setup.ps1        # PowerShell setup
├── uninstall.py             # Uninstall script
├── uninstall.bat            # Windows uninstall
├── uninstall.ps1            # PowerShell uninstall
├── FIX_APP_SETUP_GUIDE.md   # Setup guide
├── UNINSTALL_GUIDE.md       # Uninstall guide
└── SETUP_COMPLETE.md        # Completion summary
```

## 🔄 Common Operations

### Reset Application
```bash
# Remove database and reinstall
rm pos_database.db
python fix_app_setup.py
```

### Backup Data
```bash
# Manual backup
cp pos_database.db backup_$(date +%Y%m%d_%H%M%S).db
cp -r reports/ backup_reports/
cp -r logs/ backup_logs/
```

### Restore Data
```bash
# Restore from backup
cp backup_*.db pos_database.db
cp -r backup_reports/ reports/
cp -r backup_logs/ logs/
```

### Check Application Status
```bash
# Verify installation
python -c "import PyQt5, sqlalchemy, bcrypt; print('Dependencies OK')"

# Check database
python -c "import sqlite3; sqlite3.connect('pos_database.db'); print('Database OK')"

# View logs
tail -f logs/talinda_pos.log
```

## 🛠️ Troubleshooting

### Setup Issues

**Problem:** "Module not found" errors
**Solution:** Run `python fix_app_setup.py`

**Problem:** Database connection errors
**Solution:** The setup script handles this automatically

**Problem:** Permission denied errors
**Solution:** Run with administrator privileges

### Uninstall Issues

**Problem:** Files still exist after uninstall
**Solution:** Close all applications and run uninstaller again

**Problem:** Database is locked
**Solution:** Close application and wait for locks to clear

**Problem:** Permission denied during uninstall
**Solution:** Run with administrator privileges

### Application Issues

**Problem:** Application won't start
**Solution:** 
1. Check logs in `logs/` directory
2. Run `python fix_app_setup.py`
3. Verify Python 3.8+ is installed

**Problem:** Login fails
**Solution:** 
1. Use default credentials (admin/admin123)
2. Check database exists
3. Run setup script again

## 📊 System Requirements

- **Python:** 3.8 or higher
- **OS:** Windows 10+, macOS 10.14+, or Linux
- **RAM:** 4GB minimum (8GB recommended)
- **Storage:** 1GB free space
- **Display:** 1024x768 minimum resolution

## 🔐 Security Notes

1. **Change Default Passwords:** Always change default credentials after first login
2. **Backup Regularly:** Create regular backups of your database
3. **Secure Environment:** Keep the application in a secure location
4. **User Management:** Create individual user accounts for each staff member

## 📞 Support

### Logs and Debugging
- **Application Logs:** `logs/talinda_pos.log`
- **Setup Logs:** `fix_setup.log`
- **Uninstall Logs:** `uninstall.log`

### Recovery Options
1. **From Backup:** Use the backup created by uninstaller
2. **Fresh Install:** Run setup script again
3. **Manual Recovery:** Restore database and configuration files

### Getting Help
1. Check the logs for error messages
2. Review the troubleshooting section
3. Run the appropriate setup/uninstall script
4. Ensure system meets requirements

## 🎯 Next Steps

### After Setup
1. **Login** with default credentials
2. **Change passwords** in admin panel
3. **Configure business settings**
4. **Add products and categories**
5. **Set up tax rates**
6. **Train users**

### Before Uninstall
1. **Backup important data**
2. **Close all application instances**
3. **Note any custom configurations**
4. **Prepare for data migration if needed**

---

## ✅ Summary

The Talinda POS application is now fully equipped with:

- **✅ Complete Setup System:** Automated installation and configuration
- **✅ Working Application:** All features tested and functional
- **✅ Safe Uninstaller:** Comprehensive removal with data backup
- **✅ Documentation:** Detailed guides for all operations
- **✅ Cross-Platform Support:** Works on Windows, macOS, and Linux
- **✅ Error Handling:** Robust error handling and recovery options

**The application is ready for production use!** 🚀

---

**Remember:** Always backup your data before making major changes, and change the default passwords for security! 