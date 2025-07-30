# Talinda POS - Universal Setup Guide

This guide covers the comprehensive universal setup system for Talinda POS, designed to handle various deployment scenarios from simple new device setup to complex production environments.

## 🚀 Quick Start

### Windows Users
1. **Double-click** one of these files:
   - `setup_universal.bat` (Command Prompt)
   - `setup_universal.ps1` (PowerShell)

2. **Choose your setup mode and environment**
3. **Follow the on-screen instructions**

### All Platforms
```bash
python setup_universal.py [--mode <mode>] [--env <environment>]
```

## 📋 Setup Modes

### 1. New Device Setup (Default)
**Best for:** First-time installation on any device
- ✅ Installs all dependencies
- ✅ Creates database and users
- ✅ Sets up default categories
- ✅ Creates startup scripts
- ✅ Configures for local use

**Usage:**
```bash
python setup_universal.py --mode new-device --env local
```

### 2. Network Deployment
**Best for:** Multi-device network environments
- ✅ All new device features
- ✅ Network connectivity checks
- ✅ Server-optimized configuration
- ✅ Shared database setup (if configured)

**Usage:**
```bash
python setup_universal.py --mode network --env server
```

### 3. Production Environment
**Best for:** Live business environments
- ✅ Optimized for performance
- ✅ Enhanced security settings
- ✅ Minimal logging (ERROR level)
- ✅ Production-ready configuration

**Usage:**
```bash
python setup_universal.py --mode production --env server
```

### 4. Development Environment
**Best for:** Developers and testing
- ✅ Debug mode enabled
- ✅ Detailed logging (DEBUG level)
- ✅ Development-friendly settings
- ✅ Easy testing configuration

**Usage:**
```bash
python setup_universal.py --mode development --env local
```

### 5. Quick Setup
**Best for:** Rapid deployment
- ✅ Minimal configuration
- ✅ No user prompts
- ✅ Fast installation
- ✅ Basic setup only

**Usage:**
```bash
python setup_universal.py --mode quick --env local
```

## 🌍 Environment Types

### Local Environment
- **Host:** localhost
- **Port:** 5000
- **Debug:** Enabled
- **Log Level:** INFO
- **Best for:** Single device, personal use

### Server Environment
- **Host:** 0.0.0.0 (all interfaces)
- **Port:** 5000
- **Debug:** Disabled
- **Log Level:** WARNING
- **Best for:** Network deployment, business use

### Cloud Environment
- **Host:** 0.0.0.0 (all interfaces)
- **Port:** 8080
- **Debug:** Disabled
- **Log Level:** ERROR
- **Best for:** Cloud hosting, production servers

## 🔧 What the Setup Does

### System Checks
1. ✅ **Python version verification** (3.8+ required)
2. ✅ **Disk space check** (100MB minimum)
3. ✅ **Network connectivity** (for network/cloud modes)
4. ✅ **Platform detection** (Windows/Linux/macOS)

### Installation
1. ✅ **Dependency installation** from requirements files
2. ✅ **Directory creation** (logs, reports, backups, config)
3. ✅ **Database backup** (if existing)
4. ✅ **Database cleanup** (removes WAL/SHM files)

### Configuration
1. ✅ **Database initialization** with proper tables
2. ✅ **Admin user creation** (admin/admin123)
3. ✅ **Cashier user creation** (cashier/cashier123)
4. ✅ **Default categories** (Food, Beverage, Dessert, Other)
5. ✅ **Environment configuration** files
6. ✅ **Startup scripts** for different platforms

### Verification
1. ✅ **Database verification**
2. ✅ **Directory structure check**
3. ✅ **User authentication test**
4. ✅ **Configuration validation**

## 📁 Generated Files

After setup, you'll have:

```
talinda_pos/
├── pos_database.db              # Main database
├── config/                      # Configuration files
│   ├── config_local.json       # Local environment config
│   ├── config_server.json      # Server environment config
│   └── config_cloud.json       # Cloud environment config
├── logs/                        # Application logs
├── reports/                     # Generated reports
├── backups/                     # Database backups
├── start_talinda_pos.bat       # Windows startup script
├── start_talinda_pos.sh        # Unix startup script
├── setup_universal.log         # Setup log file
└── src/                        # Source code
    ├── main.py                 # Main application
    ├── logs/                   # Source logs
    └── reports/                # Source reports
```

## 🔐 Default Credentials

**⚠️ IMPORTANT: Change these passwords immediately after setup!**

### Admin User
- **Username:** `admin`
- **Password:** `admin123`
- **Role:** Administrator
- **Permissions:** Full system access

### Cashier User
- **Username:** `cashier`
- **Password:** `cashier123`
- **Role:** Cashier
- **Permissions:** Sales operations only

## 🚀 Starting the Application

### Windows
```bash
# Option 1: Double-click
start_talinda_pos.bat

# Option 2: Command line
python src/main.py
```

### Linux/macOS
```bash
# Option 1: Shell script
./start_talinda_pos.sh

# Option 2: Direct execution
python3 src/main.py
```

## 🔧 Configuration Files

### Environment Configuration
Each environment creates a JSON configuration file:

```json
{
  "database_type": "sqlite",
  "host": "localhost",
  "port": 5000,
  "debug": true,
  "log_level": "INFO"
}
```

### Customizing Configuration
1. Edit the appropriate config file in `config/`
2. Restart the application
3. Changes take effect immediately

## 🛠️ Troubleshooting

### Setup Fails

1. **Check Python version:**
   ```bash
   python --version
   ```
   Must be 3.8 or higher.

2. **Check internet connection:**
   Required for downloading packages.

3. **Check logs:**
   - Look for `setup_universal.log`
   - Check for specific error messages

4. **Manual dependency installation:**
   ```bash
   pip install -r requirements.txt
   ```

### Application Won't Start

1. **Verify setup completion:**
   ```bash
   ls pos_database.db
   ```

2. **Check Python path:**
   ```bash
   python -c "import sys; print(sys.path)"
   ```

3. **Check configuration:**
   ```bash
   cat config/config_local.json
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

### Network Issues

1. **Check firewall settings**
2. **Verify port availability**
3. **Test network connectivity**
4. **Check server configuration**

## 🔄 Upgrading

### From Previous Versions
1. **Backup your database:**
   ```bash
   cp pos_database.db backups/pos_database_backup_$(date +%Y%m%d_%H%M%S).db
   ```

2. **Run universal setup:**
   ```bash
   python setup_universal.py --mode new-device --env local
   ```

3. **Verify data integrity**
4. **Test application functionality**

## 📊 Performance Optimization

### Production Mode
- Disables debug features
- Optimizes logging
- Reduces memory usage
- Improves response times

### Development Mode
- Enables debug features
- Detailed logging
- Development tools
- Easy testing

## 🔒 Security Considerations

### Default Setup
- Change default passwords immediately
- Configure firewall rules
- Set up regular backups
- Monitor access logs

### Production Deployment
- Use strong passwords
- Enable SSL/TLS
- Configure user permissions
- Regular security updates
- Database encryption (if needed)

## 📞 Support

### Getting Help
1. **Check the logs** in `logs/` directory
2. **Review this guide** for troubleshooting
3. **Check setup log** for detailed information
4. **Verify system requirements**

### Common Issues
- **Python not found:** Install Python 3.8+
- **Permission denied:** Run as administrator
- **Port in use:** Change port in configuration
- **Database locked:** Restart application

## 🎯 Best Practices

### For New Devices
1. Use `new-device` mode
2. Choose `local` environment
3. Change passwords immediately
4. Configure business settings
5. Test all features

### For Network Deployment
1. Use `network` mode
2. Choose `server` environment
3. Configure network settings
4. Set up user permissions
5. Test multi-user access

### For Production
1. Use `production` mode
2. Choose appropriate environment
3. Configure security settings
4. Set up monitoring
5. Regular maintenance

---

**Happy selling with Talinda POS! 🛒**

*For additional support, check the main README.md and other documentation files.* 