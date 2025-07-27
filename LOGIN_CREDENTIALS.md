# 🔐 Login Credentials

The POS system has been set up with the following default users for testing:

## 📋 Default Users

### 👨‍💼 Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator
- **Permissions:** Full system access

### 💰 Cashier User
- **Username:** `cashier`
- **Password:** `cashier123`
- **Role:** Cashier
- **Permissions:** Sales, shift management

### 👔 Manager User
- **Username:** `manager`
- **Password:** `manager123`
- **Role:** Manager
- **Permissions:** Management functions

## 🚀 Getting Started

1. **Run the application:**
   ```bash
   python src/main.py
   ```

2. **Login with any of the above credentials**

3. **For cashiers:** You'll be prompted for opening amount when starting a shift

## 🔧 Creating New Users

To create additional users, use the management command:
```bash
python src/manage.py create-default-users
```

## 📝 Notes

- All users are active by default
- Passwords are securely hashed using bcrypt
- Users can be deactivated by setting `active = 0` in the database
- Cashier users will have shift management features
- Admin users have access to all system functions 