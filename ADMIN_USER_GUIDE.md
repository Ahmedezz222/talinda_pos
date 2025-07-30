# Talinda POS - Admin User Guide

## Default Admin User Setup

The Talinda POS system comes with a pre-configured default admin user that allows you to access the system immediately and manage all aspects of the application.

### Default Credentials

**Admin User:**
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator
- **Full Name:** System Administrator

**Cashier User:**
- **Username:** `cashier`
- **Password:** `cashier123`
- **Role:** Cashier
- **Full Name:** Default Cashier

## First Time Setup

### 1. Run the Setup Script
If you haven't already, run the setup script to initialize the database and create default users:

```bash
python setup_for_new_device.py
```

### 2. Verify Admin User
Run the verification script to confirm the admin user is properly set up:

```bash
python verify_admin_user.py
```

### 3. Start the Application
Launch the Talinda POS application:

```bash
python src/main.py
```

### 4. Login with Default Credentials
- Enter username: `admin`
- Enter password: `admin123`
- Click "Login"

## Changing Passwords

### Option 1: Change Your Own Password (Recommended for First Login)

1. **Login as admin** with the default credentials
2. **Go to Tools menu** → **🔐 Change My Password**
3. **Enter your new password** (minimum 6 characters)
4. **Confirm the new password**
5. **Click Save**

### Option 2: Change Passwords via Admin Panel

1. **Login as admin**
2. **Go to Admin Panel** (from the sidebar)
3. **Navigate to User Management section**
4. **Select a user** from the table
5. **Click "🔐 Change Password"** button
6. **Enter and confirm the new password**
7. **Click Save**

### Option 3: Edit User Details

1. **Login as admin**
2. **Go to Admin Panel** → **User Management**
3. **Select a user** from the table
4. **Click "✏️ Edit User"** button
5. **Modify user information** including password
6. **Click Save**

## User Management Features

### Adding New Users

1. **Go to Admin Panel** → **User Management**
2. **Click "➕ Add User"** button
3. **Fill in the required information:**
   - Username (unique)
   - Full Name
   - Role (Admin/Cashier/Manager)
   - Password (minimum 6 characters)
   - Active status
4. **Click Save**

### Editing Users

1. **Select a user** from the User Management table
2. **Click "✏️ Edit User"** button
3. **Modify any user information** (except username for existing users)
4. **Click Save**

### Deleting Users

1. **Select a user** from the User Management table
2. **Click "🗑️ Delete User"** button
3. **Confirm the deletion**

## Security Best Practices

### 1. Change Default Passwords Immediately
- Change the default admin password on first login
- Change the default cashier password
- Use strong, unique passwords

### 2. Regular Password Updates
- Update passwords regularly (every 3-6 months)
- Use different passwords for different users
- Avoid common passwords

### 3. User Access Management
- Only create user accounts for authorized personnel
- Deactivate unused accounts
- Regularly review user permissions

### 4. Admin Account Security
- Keep admin credentials secure
- Don't share admin passwords
- Use admin account only for administrative tasks

## Password Requirements

- **Minimum length:** 6 characters
- **Recommended:** 8+ characters with mix of:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters

## Troubleshooting

### Can't Login with Default Credentials?

1. **Verify the setup:**
   ```bash
   python verify_admin_user.py
   ```

2. **Re-run the setup script:**
   ```bash
   python setup_for_new_device.py
   ```

3. **Check database file:**
   - Ensure `pos_database.db` exists in the project root
   - Check file permissions

### Forgot Admin Password?

1. **Stop the application**
2. **Delete the database file:**
   ```bash
   rm pos_database.db
   ```
3. **Re-run the setup script:**
   ```bash
   python setup_for_new_device.py
   ```
4. **Use default credentials again**

### User Management Not Working?

1. **Ensure you're logged in as admin**
2. **Check if the admin panel is accessible**
3. **Verify database permissions**
4. **Check application logs for errors**

## Command Line User Management

You can also manage users via command line:

### Create Admin User
```bash
python src/manage.py create-admin
```

### Create User Non-Interactively
```bash
python src/manage.py create-admin-noninteractive --username newadmin --password newpass123 --full-name "New Admin"
```

### List All Users
```bash
python src/manage.py list-users
```

## Support

If you encounter any issues:

1. **Check the application logs** in the `logs/` directory
2. **Verify database integrity**
3. **Review this guide**
4. **Contact system administrator**

---

**Important:** Always change the default passwords after first login to ensure system security! 