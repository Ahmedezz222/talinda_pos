# Talinda POS - New Device Setup Guide

This guide will help you set up the Talinda POS application on any new device.

## Prerequisites

- **Python 3.8 or higher** - Download from [python.org](https://python.org)
- **Windows 10/11** (for Windows users)
- **Internet connection** (for downloading dependencies)

## Quick Setup (Recommended)

### Windows Users

1. **Double-click** one of these files:
   - `setup_new_device.bat` (Command Prompt)
   - `setup_new_device.ps1` (PowerShell)

2. **Follow the on-screen instructions**

3. **Wait for the setup to complete**

### Manual Setup (All Platforms)

1. **Open a terminal/command prompt** in the project directory

2. **Run the setup script:**
   ```bash
   python setup_for_new_device.py
   ```

3. **Follow the on-screen instructions**

## What the Setup Does

The setup script will automatically:

1. ✅ **Check Python version** (requires 3.8+)
2. ✅ **Install all dependencies** from `requirements.txt`
3. ✅ **Create necessary directories** (logs, reports, backups)
4. ✅ **Backup existing database** (if any)
5. ✅ **Clean corrupted database files** (WAL/SHM files)
6. ✅ **Initialize the database** with proper tables
7. ✅ **Create default users:**
   - **Admin:** username=`admin`, password=`admin123`
   - **Cashier:** username=`cashier`, password=`cashier123`
8. ✅ **Seed default categories** (Food, Beverage, Dessert, Other)
9. ✅ **Create environment configuration**
10. ✅ **Verify everything works**

## After Setup

### 1. Run the Application

```bash
python src/main.py
```

### 2. Login with Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Cashier User:**
- Username: `cashier`
- Password: `cashier123`

### 3. Important Security Steps

⚠️ **CHANGE DEFAULT PASSWORDS IMMEDIATELY!**

1. Login as admin
2. Go to Admin Panel
3. Change both admin and cashier passwords
4. Create additional users as needed

### 4. Configure Your Business

1. **Add your products** and categories
2. **Configure tax rates** and business settings
3. **Set up payment methods**
4. **Customize the interface** as needed

## Troubleshooting

### Setup Fails

1. **Check Python version:**
   ```bash
   python --version
   ```
   Must be 3.8 or higher.

2. **Check internet connection** - required for downloading packages

3. **Check logs:**
   - Look for `setup.log` file
   - Check for specific error messages

4. **Manual dependency installation:**
   ```bash
   pip install -r requirements.txt
   ```

### Application Won't Start

1. **Check if setup completed successfully**
2. **Verify database exists:**
   ```bash
   ls pos_database.db
   ```
3. **Check Python path:**
   ```bash
   python -c "import sys; print(sys.path)"
   ```

### Database Issues

1. **Reset database:**
   ```bash
   python src/manage.py reset-system
   ```

2. **Reinitialize database:**
   ```bash
   python src/init_database.py
   ```

## File Structure After Setup

```
talinda_pos/
├── pos_database.db          # Main database
├── logs/                    # Application logs
├── reports/                 # Generated reports
├── backups/                 # Database backups
├── src/                     # Source code
│   ├── main.py             # Main application
│   ├── logs/               # Source logs
│   └── reports/            # Source reports
├── setup.log               # Setup log file
└── env_example.txt         # Environment configuration
```

## Default Configuration

The setup creates a production-ready configuration:

- **Database:** SQLite (local file)
- **Logging:** INFO level
- **Security:** Standard timeout and attempt limits
- **UI:** Default theme with responsive design
- **Categories:** Food, Beverage, Dessert, Other (14% tax rate)

## Support

If you encounter issues:

1. **Check the logs** in the `logs/` directory
2. **Review this guide** for troubleshooting steps
3. **Check the main README.md** for additional information
4. **Look at setup.log** for detailed setup information

## Security Notes

- Default passwords are for initial setup only
- Change passwords immediately after first login
- Keep the database file secure
- Regular backups are recommended
- Consider using a virtual environment for production

---

**Happy selling with Talinda POS! 🛒** 