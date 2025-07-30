# Talinda POS - Uninstall Guide

## Overview

This guide provides comprehensive instructions for completely removing the Talinda POS application from your system.

## ⚠️ Important Warning

**This action cannot be undone!** The uninstaller will permanently delete:
- All application data and databases
- Configuration files
- Log files and reports
- Application directories and files

**Always backup your data before uninstalling!**

## Quick Uninstall

### For Windows Users

1. **Using Batch File (Recommended):**
   ```cmd
   uninstall.bat
   ```

2. **Using PowerShell:**
   ```powershell
   .\uninstall.ps1
   ```

3. **Using Python directly:**
   ```cmd
   python uninstall.py
   ```

### For Linux/Mac Users

```bash
python3 uninstall.py
```

## What the Uninstaller Does

The `uninstall.py` script automatically handles the following:

### 1. Data Backup
- ✅ Creates a timestamped backup of your database
- ✅ Backs up reports and log files
- ✅ Preserves configuration files
- ✅ Stores backup in a safe location

### 2. File Removal
- ✅ Removes application database files
- ✅ Deletes log directories and files
- ✅ Removes report directories and files
- ✅ Cleans up configuration files
- ✅ Removes build artifacts

### 3. Directory Cleanup
- ✅ Removes application directories
- ✅ Cleans Python cache files
- ✅ Removes temporary files
- ✅ Deletes backup directories

### 4. System Cleanup
- ✅ Removes desktop shortcuts (Windows)
- ✅ Removes start menu entries (Windows)
- ✅ Cleans registry entries (Windows)
- ✅ Optionally removes Python packages

### 5. Verification
- ✅ Verifies all components are removed
- ✅ Confirms cleanup completion
- ✅ Provides detailed summary

## Manual Uninstall (If Uninstaller Fails)

### 1. Backup Your Data

```bash
# Create backup directory
mkdir talinda_pos_backup_$(date +%Y%m%d_%H%M%S)

# Backup database
cp pos_database.db talinda_pos_backup_*/ 2>/dev/null || echo "No database found"

# Backup reports
cp -r reports/ talinda_pos_backup_*/ 2>/dev/null || echo "No reports found"

# Backup logs
cp -r logs/ talinda_pos_backup_*/ 2>/dev/null || echo "No logs found"
```

### 2. Remove Application Files

```bash
# Remove main application files
rm -f pos_database.db*
rm -f env_example.txt
rm -f timezone_settings.json
rm -f *.log

# Remove directories
rm -rf logs/
rm -rf reports/
rm -rf backups/
rm -rf build/
rm -rf dist/
rm -rf __pycache__/
```

### 3. Remove Source Files

```bash
# Remove source-specific files
rm -f src/pos_database.db*
rm -rf src/logs/
rm -rf src/reports/
rm -rf src/__pycache__/
```

### 4. Clean Python Cache

```bash
# Remove all Python cache files
find . -name "__pycache__" -type d -exec rm -rf {} +
find . -name "*.pyc" -type f -delete
```

### 5. Remove Python Packages (Optional)

```bash
# Uninstall build tools
pip uninstall -y cx_Freeze PyInstaller

# Note: Core dependencies (PyQt5, SQLAlchemy, etc.) are kept
# as they might be used by other applications
```

## Windows-Specific Cleanup

### Remove Shortcuts

```cmd
# Remove desktop shortcut
del "%USERPROFILE%\Desktop\Talinda POS.lnk" 2>nul

# Remove start menu shortcut
del "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Talinda POS.lnk" 2>nul
```

### Remove Registry Entries

```cmd
# Remove uninstall registry entry (requires admin)
reg delete "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Talinda POS" /f
```

## Recovery Options

### Restore from Backup

If you need to restore your data:

1. **Restore Database:**
   ```bash
   cp talinda_pos_backup_*/pos_database.db ./
   ```

2. **Restore Reports:**
   ```bash
   cp -r talinda_pos_backup_*/reports/ ./
   ```

3. **Restore Logs:**
   ```bash
   cp -r talinda_pos_backup_*/logs/ ./
   ```

4. **Reinstall Application:**
   ```bash
   python fix_app_setup.py
   ```

### Complete Reinstall

If you want to start fresh:

1. **Run the fix script:**
   ```bash
   python fix_app_setup.py
   ```

2. **Or use the setup script:**
   ```bash
   python setup_for_new_device.py
   ```

## Troubleshooting

### Issue: "Permission denied" errors
**Solution:** Run the uninstaller with administrator privileges.

### Issue: Files still exist after uninstall
**Solution:** 
1. Check if any processes are using the files
2. Close any running instances of the application
3. Run the uninstaller again

### Issue: Database is locked
**Solution:**
1. Close any applications using the database
2. Wait a few minutes for locks to clear
3. Try the uninstall again

### Issue: Python packages not removed
**Solution:** 
1. Run the uninstaller with the package removal option
2. Or manually uninstall packages:
   ```bash
   pip uninstall -y cx_Freeze PyInstaller
   ```

## Post-Uninstall Checklist

After uninstalling, verify the following:

- ✅ Application no longer starts
- ✅ Database files are removed
- ✅ Log and report directories are gone
- ✅ Shortcuts are removed (Windows)
- ✅ Backup is created and accessible
- ✅ No error messages in uninstall log

## File Locations to Check

### Windows
```
C:\Users\[Username]\Desktop\Talinda POS.lnk
C:\Users\[Username]\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Talinda POS.lnk
```

### Linux/Mac
```
~/.local/share/applications/talinda-pos.desktop
~/.config/talinda-pos/
```

## Support

If you encounter issues during uninstallation:

1. **Check the logs:** Look in `uninstall.log` for detailed information
2. **Manual cleanup:** Use the manual uninstall steps above
3. **Contact support:** If problems persist, check the backup and reinstall

## Safety Tips

1. **Always backup first** - The uninstaller creates a backup, but you can create additional backups
2. **Close the application** - Ensure no instances are running
3. **Check dependencies** - Don't remove Python packages used by other applications
4. **Keep the backup** - Store the backup in a safe location for potential recovery

---

**Note:** The uninstaller is designed to be safe and thorough. It will ask for confirmation before proceeding and create backups of important data. If you're unsure, always backup your data manually before proceeding. 