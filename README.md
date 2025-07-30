# Talinda POS System

A modern, feature-rich Point of Sale system built with Python and PyQt5.

## Features

- Modern and beautiful UI using PyQt5
- Multi-language support (Arabic & English)
- User role management (admin, cashier, etc.)
- Shift management
- Sales and inventory management
- Report generation
- SQLite database integration
- Touch-friendly design

## Requirements

- Python 3.8+
- Dependencies listed in requirements.txt

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows:
     ```
     .\venv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source venv/bin/activate
     ```
4. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Quick Start

### 1. Setup (First Time Only)
```bash
python setup_for_new_device.py
```

### 2. Verify Setup
```bash
python verify_admin_user.py
```

### 3. Run the Application
```bash
python src/main.py
```

### 4. Login with Default Credentials
- **Username:** `admin`
- **Password:** `admin123`

## Default Users

The system comes with pre-configured default users:

**Admin User:**
- Username: `admin`
- Password: `admin123`
- Role: Administrator

**Cashier User:**
- Username: `cashier`
- Password: `cashier123`
- Role: Cashier

⚠️ **Important:** Change these default passwords after first login!

For detailed instructions, see [ADMIN_USER_GUIDE.md](ADMIN_USER_GUIDE.md)

## Development

The project follows a modular architecture:

- `src/ui/`: User interface components
- `src/database/`: Database models and operations
- `src/models/`: Business logic models
- `src/controllers/`: Application controllers
- `src/utils/`: Utility functions
- `src/resources/`: Application resources (images, translations, etc.)

## License

MIT License
