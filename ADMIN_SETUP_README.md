# Talinda POS Setup with Admin Credentials

## Overview

This enhanced setup system allows you to set admin username and password during the build process. The credentials are securely embedded in the application and the database is pre-configured with the admin user.

## Features

- **Interactive Setup**: Prompts for admin username and password
- **Secure Password Hashing**: Uses bcrypt for password security
- **Pre-configured Database**: Creates initial database with admin user
- **Embedded Credentials**: Admin credentials are built into the executable
- **Multiple Interfaces**: Batch, PowerShell, and Python scripts available

## Quick Start

### Option 1: Windows Batch Script (Recommended)
```batch
setup_admin.bat
```

### Option 2: PowerShell Script
```powershell
.\setup_admin.ps1
```

### Option 3: Python Script
```bash
python setup_with_admin.py
```

## Setup Process

### 1. Admin Credentials Setup
The setup will prompt you for:
- **Admin Username**: Must be at least 3 characters
- **Admin Password**: Must be at least 6 characters
- **Password Confirmation**: To ensure accuracy

### 2. Security Features
- Passwords are hashed using bcrypt
- Salt is automatically generated
- Credentials are embedded securely in the application
- Database is pre-configured with admin user

### 3. Build Process
- Creates `admin_config.py` with embedded credentials
- Creates `initial_database.sql` with admin user
- Builds executable using cx_Freeze
- Includes all necessary files and dependencies

## Files Created

### `admin_config.py`
Contains the default admin credentials:
```python
DEFAULT_ADMIN_USERNAME = "your_username"
DEFAULT_ADMIN_PASSWORD_HASH = b'$2b$12$...'

def get_default_admin_credentials():
    return DEFAULT_ADMIN_USERNAME, DEFAULT_ADMIN_PASSWORD_HASH

def verify_admin_credentials(username, password):
    # Verification logic
```

### `initial_database.sql`
Contains SQL to create database with admin user:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, password_hash, role) 
VALUES ('your_username', 'hashed_password', 'admin');
```

## Usage Examples

### Basic Setup
```bash
# Run the setup
python setup_with_admin.py

# Follow the prompts:
# Admin Username: admin
# Admin Password: ********
# Confirm Password: ********
# Proceed with build? (y/N): y
```

### Batch Script
```batch
# Double-click setup_admin.bat
# Or run from command line:
setup_admin.bat
```

### PowerShell Script
```powershell
# Run in PowerShell:
.\setup_admin.ps1
```

## Security Considerations

### Password Requirements
- **Username**: Minimum 3 characters
- **Password**: Minimum 6 characters
- **Confirmation**: Must match password

### Built-in Security
- Passwords are hashed with bcrypt
- Salt is automatically generated
- Credentials are embedded in the application
- No plain text passwords stored

### Best Practices
1. **Use strong passwords**: Mix letters, numbers, symbols
2. **Keep credentials secure**: Don't share the executable
3. **Change default credentials**: After first login
4. **Backup credentials**: Store them securely

## Integration with Application

### Login Process
The application will use the embedded credentials for initial login:
1. Check if database exists
2. If not, create database with admin user
3. Allow login with embedded credentials
4. After first login, recommend changing password

### Database Initialization
The application will automatically:
1. Create database if it doesn't exist
2. Insert admin user with embedded credentials
3. Set up all necessary tables
4. Allow immediate login

## Troubleshooting

### Common Issues

**"cx_Freeze is not installed"**
```bash
pip install cx_Freeze
```

**"Password too short"**
- Ensure password is at least 6 characters

**"Passwords don't match"**
- Carefully retype the password and confirmation

**"Username too short"**
- Ensure username is at least 3 characters

### Error Messages

**"Admin Username: "**
- Enter a username (minimum 3 characters)

**"Admin Password: "**
- Enter a password (minimum 6 characters)
- Password will be hidden for security

**"Confirm Password: "**
- Re-enter the same password

**"Proceed with build? (y/N): "**
- Type 'y' to continue, 'n' to cancel

## Build Output

After successful setup, you'll find:

### Executable
- `build/exe.win-amd64-3.8/Talinda_POS.exe`
- Ready to run on any Windows PC
- Includes embedded admin credentials

### Configuration Files
- `src/admin_config.py` - Admin credentials
- `src/initial_database.sql` - Database setup

### Build Directory
- `build/` - Contains all build artifacts
- `dist/` - Distribution-ready files

## Deployment

### Single PC Installation
1. Run the setup with admin credentials
2. Copy the executable to target PC
3. Run the executable
4. Login with the credentials you set

### Network Deployment
1. Run setup on build machine
2. Copy executable to network location
3. Users can run from network location
4. Each user gets their own database

### USB Deployment
1. Run setup with admin credentials
2. Copy executable to USB drive
3. Run from any PC with USB drive
4. Portable installation

## Customization

### Changing Default Credentials
To change the default admin credentials:
1. Edit `src/admin_config.py`
2. Update `DEFAULT_ADMIN_USERNAME`
3. Update `DEFAULT_ADMIN_PASSWORD_HASH`
4. Rebuild the application

### Adding More Users
After first login:
1. Use admin account to create additional users
2. Set appropriate roles and permissions
3. Users can change their own passwords

## Support

### Getting Help
1. Check the error messages
2. Verify Python and cx_Freeze are installed
3. Ensure sufficient disk space
4. Check file permissions

### Common Solutions
- **Install cx_Freeze**: `pip install cx_Freeze`
- **Update Python**: Install Python 3.8 or later
- **Check disk space**: Ensure 500MB+ available
- **Run as administrator**: If permission issues

---

**Note**: This setup creates a secure, pre-configured Talinda POS application with embedded admin credentials. The credentials are hashed and embedded in the application for immediate use after installation. 