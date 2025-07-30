# Talinda POS - User Setup Guide for New Devices

This guide explains how to create login users for new devices in the Talinda POS system.

## 📋 Overview

The user setup system provides multiple ways to create login users for new devices:

1. **Interactive User Creation** - Create custom users with specific roles
2. **Default User Setup** - Quick setup with pre-configured users
3. **Command Line Tools** - Use existing management commands

## 🚀 Quick Start

### Option 1: Use the Interactive Script (Recommended)

#### Windows Users:
```bash
# Double-click the batch file
create_users.bat

# Or run PowerShell script
.\create_users.ps1

# Or run Python directly
python create_login_users.py
```

#### Linux/Mac Users:
```bash
# Make script executable (first time only)
chmod +x create_login_users.py

# Run the script
python create_login_users.py
```

### Option 2: Use Command Line Tools

```bash
# Create default users
python src/manage.py create-default-users

# Create admin user interactively
python src/manage.py create-admin

# Create admin user non-interactively
python src/manage.py create-admin-noninteractive --username admin --password admin123 --full-name "System Admin"
```

## 📝 Available User Roles

### 1. Admin User
- **Access Level**: Full system access
- **Capabilities**: 
  - User management
  - System configuration
  - Reports and analytics
  - Product and category management
  - Order management
- **Default Credentials**: `admin` / `admin123`

### 2. Manager User
- **Access Level**: Management access
- **Capabilities**:
  - Reports and analytics
  - Product management
  - Order management
  - Limited user management
- **Default Credentials**: `manager` / `manager123`

### 3. Cashier User
- **Access Level**: Basic POS operations
- **Capabilities**:
  - Process sales
  - View products
  - Basic reporting
  - Shift management
- **Default Credentials**: `cashier` / `cashier123`

## 🔧 Interactive Script Features

The `create_login_users.py` script provides:

### 1. Quick Setup Mode
- Automatically detects if no users exist
- Offers to create default users immediately
- Perfect for new device deployment

### 2. Interactive Menu
- **Create Custom User**: Create users with custom credentials
- **Create Default Users**: Create admin, cashier, and manager users
- **List Existing Users**: View all current users in the system
- **Show Default Credentials**: Display default login information

### 3. Validation Features
- Username format validation
- Password strength requirements
- Duplicate username checking
- Database connection verification

## 📊 Default User Configuration

When using the quick setup or default user creation, the following users are created:

| Username | Password | Role | Full Name | Description |
|----------|----------|------|-----------|-------------|
| `admin` | `admin123` | Admin | System Administrator | Full system access |
| `cashier` | `cashier123` | Cashier | Default Cashier | Basic POS operations |
| `manager` | `manager123` | Manager | Store Manager | Management access |

## 🔒 Security Best Practices

### 1. Change Default Passwords
After first login, immediately change the default passwords:
- Go to Admin Panel → User Management
- Select each user and change their password
- Use strong passwords (8+ characters, mix of letters, numbers, symbols)

### 2. Create Custom Users
Instead of using default users, create custom users with:
- Unique usernames
- Strong passwords
- Specific role assignments
- Full names for accountability

### 3. Regular Password Updates
- Implement a password change policy
- Regularly update user passwords
- Deactivate unused accounts

## 🛠️ Troubleshooting

### Common Issues

#### 1. Database Connection Error
```
ERROR: Cannot connect to database
```
**Solution**: Ensure the database is initialized first:
```bash
python src/manage.py init-db
```

#### 2. Python Not Found
```
ERROR: Python is not installed or not in PATH
```
**Solution**: Install Python 3.8+ and ensure it's in your system PATH

#### 3. Permission Denied
```
ERROR: Permission denied
```
**Solution**: Run as administrator (Windows) or use sudo (Linux/Mac)

#### 4. Username Already Exists
```
ERROR: Username already exists
```
**Solution**: Choose a different username or use the existing user

### Log Files
Check the following log files for detailed error information:
- `user_setup.log` - User creation script logs
- `logs/talinda_pos.log` - Application logs

## 📋 Step-by-Step Setup for New Device

### Step 1: Prepare the System
1. Ensure Python 3.8+ is installed
2. Install required dependencies: `pip install -r requirements.txt`
3. Initialize the database: `python src/manage.py init-db`

### Step 2: Create Users
1. Run the user creation script: `python create_login_users.py`
2. Choose "Quick Setup" for new devices
3. Note down the default credentials

### Step 3: Test Login
1. Start the application: `python src/main.py`
2. Login with default credentials
3. Verify all features work correctly

### Step 4: Secure the System
1. Change default passwords
2. Create custom users if needed
3. Configure business settings
4. Add products and categories

## 🔄 Updating Existing Users

### Add New Users
```bash
# Use interactive script
python create_login_users.py

# Or use command line
python src/manage.py create-admin
```

### Modify Existing Users
- Use the Admin Panel in the application
- Go to User Management section
- Edit user details, roles, or passwords

### Deactivate Users
- Use the Admin Panel
- Set user status to "Inactive"
- Users cannot login when inactive

## 📞 Support

If you encounter issues:

1. Check the log files for error details
2. Verify database connection and permissions
3. Ensure all dependencies are installed
4. Contact system administrator for assistance

## 📄 File Structure

```
talinda_pos/
├── create_login_users.py      # Main user creation script
├── create_users.bat          # Windows batch file
├── create_users.ps1          # PowerShell script
├── USER_SETUP_GUIDE.md       # This guide
├── src/
│   ├── manage.py             # Command line management tools
│   ├── models/user.py        # User model definitions
│   └── controllers/auth_controller.py  # Authentication logic
└── logs/
    └── user_setup.log        # User creation logs
```

---

**Note**: Always keep default credentials secure and change them immediately after first use. The default passwords are for initial setup only and should not be used in production environments. 