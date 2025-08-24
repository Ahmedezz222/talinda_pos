# Talinda POS

A modern Point of Sale system built with PyQt5 and SQLAlchemy.

## Features

- Modern and responsive UI with PyQt5
- Secure user authentication
- Multi-language support (English and Arabic)
- Product and category management
- Order processing and tracking
- Sales reporting and analytics
- Shift management
- Background task automation

## Installation

### Method 1: Using the Batch Installer (Recommended)

1. Download the latest release from the releases page
2. Extract the files to your desired location
3. Run `install.bat` by double-clicking it
4. Wait for the installation to complete
5. Launch Talinda POS from the Desktop shortcut or from the `dist` folder

The batch installer will:
- Set up a Python virtual environment
- Install all required dependencies
- Build the executable
- Create a desktop shortcut
- Configure everything automatically

### Method 2: Manual Installation

1. Ensure you have Python 3.8 or higher installed
2. Clone the repository:
   ```bash
   git clone https://github.com/Ahmedezz222/talinda_pos.git
   cd talinda_pos
   ```

3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

4. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the application:
   ```bash
   python src/main.py
   ```

### Method 3: Building from Source

1. Follow steps 1-3 from Method 2
2. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Build the executable:
   ```bash
   python build.py
   ```

4. The executable will be available in the `dist` directory

## Default Credentials

- Username: admin
- Password: admin123

It is highly recommended to change these credentials after first login.

## System Requirements

- Operating System: Windows 7/8/10/11, Linux, or macOS
- RAM: 4GB minimum (8GB recommended)
- Storage: 500MB free space
- Display: 1280x720 minimum resolution

## Support

For support, please create an issue on the GitHub repository or contact support@talindapos.com
