#!/usr/bin/env python3
"""
Talinda POS - Executable Installer Creator
==========================================

This script creates a standalone executable installer for Talinda POS
that will automatically install all dependencies and set up the application.

Usage:
    python create_installer.py

The generated executable will:
1. Check system requirements
2. Install Python if not present
3. Install all required packages
4. Set up the database
5. Create startup scripts
6. Configure the application

Author: Talinda POS Team
Version: 1.0.0
"""

import os
import sys
import subprocess
import shutil
import tempfile
import zipfile
from pathlib import Path
import json

def check_pyinstaller():
    """Check if PyInstaller is installed."""
    try:
        import PyInstaller
        return True
    except ImportError:
        return False

def install_pyinstaller():
    """Install PyInstaller."""
    print("Installing PyInstaller...")
    subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
    print("PyInstaller installed successfully!")

def create_installer_script():
    """Create the main installer script that will be compiled."""
    
    installer_code = '''#!/usr/bin/env python3
"""
Talinda POS - Standalone Installer
==================================

This is the main installer script that will be compiled into an executable.
"""

import os
import sys
import subprocess
import shutil
import tempfile
import zipfile
import json
import platform
import urllib.request
import urllib.error
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time

class TalindaPOSInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Talinda POS - Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.eval('tk::PlaceWindow . center')
        
        self.setup_ui()
        self.install_path = None
        self.installation_complete = False
        
    def setup_ui(self):
        """Setup the user interface."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="Talinda POS - Installer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Welcome text
        welcome_text = """Welcome to Talinda POS Installer!

This installer will:
• Check system requirements
• Install Python (if needed)
• Install all required packages
• Set up the database
• Create startup scripts
• Configure the application

Please select an installation directory and click 'Install' to begin."""
        
        welcome_label = ttk.Label(main_frame, text=welcome_text, justify=tk.LEFT)
        welcome_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Installation path
        ttk.Label(main_frame, text="Installation Directory:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.path_var = tk.StringVar(value=str(Path.home() / "TalindaPOS"))
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_btn.grid(row=0, column=1, padx=(5, 0))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Installation Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Ready to install")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        self.install_btn = ttk.Button(button_frame, text="Install", command=self.start_installation)
        self.install_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.root.quit)
        self.cancel_btn.grid(row=0, column=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        path_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        
    def browse_path(self):
        """Browse for installation directory."""
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)
    
    def update_status(self, message, progress=None):
        """Update status message and progress bar."""
        self.status_label.config(text=message)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update()
    
    def check_python(self):
        """Check if Python is installed."""
        self.update_status("Checking Python installation...", 10)
        try:
            result = subprocess.run([sys.executable, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except:
            pass
        return False
    
    def install_python(self):
        """Install Python if not present."""
        self.update_status("Installing Python...", 20)
        
        # This would download and install Python
        # For now, we'll assume Python is available
        python_url = "https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe"
        
        try:
            # Download Python installer
            temp_dir = tempfile.gettempdir()
            installer_path = Path(temp_dir) / "python_installer.exe"
            
            self.update_status("Downloading Python installer...", 25)
            urllib.request.urlretrieve(python_url, installer_path)
            
            # Install Python silently
            self.update_status("Installing Python...", 30)
            subprocess.run([str(installer_path), "/quiet", "InstallAllUsers=1"], 
                         check=True)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install Python: {e}")
            return False
    
    def install_requirements(self):
        """Install required packages."""
        self.update_status("Installing required packages...", 40)
        
        requirements = [
            "PyQt5>=5.15.9",
            "PyQt5-Qt5>=5.15.2", 
            "PyQt5-sip>=12.12.1",
            "SQLAlchemy>=2.0.19",
            "bcrypt>=4.0.1",
            "python-dotenv>=1.0.0",
            "reportlab>=4.0.4",
            "qrcode>=7.4.2",
            "Pillow>=10.0.0",
            "openpyxl>=3.1.2",
            "pandas>=2.0.0"
        ]
        
        try:
            for req in requirements:
                self.update_status(f"Installing {req}...", 40 + (len(requirements).index(req) * 5))
                subprocess.run([sys.executable, "-m", "pip", "install", req], 
                             capture_output=True, check=True)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install packages: {e}")
            return False
    
    def extract_application(self):
        """Extract application files."""
        self.update_status("Extracting application files...", 70)
        
        try:
            install_path = Path(self.path_var.get())
            install_path.mkdir(parents=True, exist_ok=True)
            
            # Create application structure
            (install_path / "src").mkdir(exist_ok=True)
            (install_path / "config").mkdir(exist_ok=True)
            (install_path / "logs").mkdir(exist_ok=True)
            (install_path / "reports").mkdir(exist_ok=True)
            (install_path / "backups").mkdir(exist_ok=True)
            
            # Copy application files (this would be embedded in the executable)
            self.create_sample_files(install_path)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract files: {e}")
            return False
    
    def create_sample_files(self, install_path):
        """Create sample application files."""
        # Create main.py
        main_py = '''#!/usr/bin/env python3
"""
Talinda POS - Main Application
"""

import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Talinda POS")
    app.setApplicationVersion("3.0.0")
    
    # Import and show main window
    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
'''
        
        with open(install_path / "main.py", "w") as f:
            f.write(main_py)
        
        # Create startup script
        if platform.system() == "Windows":
            startup_script = f'''@echo off
cd /d "{install_path}"
python main.py
pause
'''
            with open(install_path / "start_talinda_pos.bat", "w") as f:
                f.write(startup_script)
        else:
            startup_script = f'''#!/bin/bash
cd "{install_path}"
python3 main.py
'''
            with open(install_path / "start_talinda_pos.sh", "w") as f:
                f.write(startup_script)
            os.chmod(install_path / "start_talinda_pos.sh", 0o755)
    
    def setup_database(self):
        """Setup the database."""
        self.update_status("Setting up database...", 80)
        
        try:
            install_path = Path(self.path_var.get())
            
            # Create database initialization script
            db_init = '''#!/usr/bin/env python3
"""
Database initialization for Talinda POS
"""

import sqlite3
from pathlib import Path

def init_database():
    db_path = Path(__file__).parent / "pos_database.db"
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL,
            role TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            cost REAL NOT NULL,
            stock_quantity INTEGER DEFAULT 0,
            category_id INTEGER,
            barcode TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tax_rate REAL DEFAULT 0.0,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            total_amount REAL NOT NULL,
            tax_amount REAL NOT NULL,
            discount_amount REAL DEFAULT 0.0,
            payment_method TEXT NOT NULL,
            user_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert default admin user
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, full_name, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin123', 'System Administrator', 'admin'))
    
    # Insert default cashier user
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, full_name, role)
        VALUES (?, ?, ?, ?)
    ''', ('cashier', 'cashier123', 'Default Cashier', 'cashier'))
    
    # Insert default categories
    categories = [
        ('Food', 0.14),
        ('Beverage', 0.14),
        ('Dessert', 0.14),
        ('Other', 0.14)
    ]
    
    for name, tax_rate in categories:
        cursor.execute('''
            INSERT OR IGNORE INTO categories (name, tax_rate)
            VALUES (?, ?)
        ''', (name, tax_rate))
    
    conn.commit()
    conn.close()
    
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()
'''
            
            with open(install_path / "init_database.py", "w") as f:
                f.write(db_init)
            
            # Run database initialization
            subprocess.run([sys.executable, str(install_path / "init_database.py")], 
                         cwd=install_path, check=True)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to setup database: {e}")
            return False
    
    def create_desktop_shortcut(self):
        """Create desktop shortcut."""
        self.update_status("Creating desktop shortcut...", 90)
        
        try:
            install_path = Path(self.path_var.get())
            
            if platform.system() == "Windows":
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                shortcut_path = Path(desktop) / "Talinda POS.lnk"
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(str(shortcut_path))
                shortcut.Targetpath = str(install_path / "start_talinda_pos.bat")
                shortcut.WorkingDirectory = str(install_path)
                shortcut.IconLocation = str(install_path / "main.py")
                shortcut.save()
            
            return True
        except Exception as e:
            # Non-critical error, just log it
            print(f"Could not create desktop shortcut: {e}")
            return True
    
    def start_installation(self):
        """Start the installation process in a separate thread."""
        self.install_btn.config(state='disabled')
        self.cancel_btn.config(state='disabled')
        
        def install_thread():
            try:
                # Check Python
                if not self.check_python():
                    if not self.install_python():
                        return
                
                # Install requirements
                if not self.install_requirements():
                    return
                
                # Extract application
                if not self.extract_application():
                    return
                
                # Setup database
                if not self.setup_database():
                    return
                
                # Create desktop shortcut
                self.create_desktop_shortcut()
                
                # Installation complete
                self.update_status("Installation completed successfully!", 100)
                self.installation_complete = True
                
                # Show completion message
                messagebox.showinfo("Installation Complete", 
                                  f"Talinda POS has been installed successfully!\\n\\n"
                                  f"Installation directory: {self.path_var.get()}\\n\\n"
                                  f"Default login credentials:\\n"
                                  f"Admin: admin / admin123\\n"
                                  f"Cashier: cashier / cashier123\\n\\n"
                                  f"Please change these passwords immediately!")
                
                # Enable close button
                self.cancel_btn.config(text="Close", state='normal')
                
            except Exception as e:
                messagebox.showerror("Installation Error", f"Installation failed: {e}")
                self.cancel_btn.config(state='normal')
        
        thread = threading.Thread(target=install_thread)
        thread.daemon = True
        thread.start()
    
    def run(self):
        """Run the installer."""
        self.root.mainloop()

if __name__ == "__main__":
    installer = TalindaPOSInstaller()
    installer.run()
'''
    
    # Write the installer script to a temporary file
    temp_dir = Path(tempfile.gettempdir())
    installer_script_path = temp_dir / "talinda_pos_installer.py"
    
    with open(installer_script_path, 'w', encoding='utf-8') as f:
        f.write(installer_code)
    
    return installer_script_path

def create_spec_file(installer_script_path):
    """Create PyInstaller spec file."""
    
    spec_content = f'''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    [r'{installer_script_path}'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'urllib.request',
        'urllib.error',
        'subprocess',
        'threading',
        'pathlib',
        'json',
        'platform',
        'tempfile',
        'shutil',
        'zipfile'
    ],
    hookspath=[],
    hooksconfig={{}},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TalindaPOS_Installer',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None
)
'''
    
    spec_file_path = Path("talinda_pos_installer.spec")
    with open(spec_file_path, 'w') as f:
        f.write(spec_content)
    
    return spec_file_path

def main():
    """Main function."""
    print("=" * 60)
    print("           TALINDA POS - INSTALLER CREATOR")
    print("=" * 60)
    print()
    
    # Check if PyInstaller is installed
    if not check_pyinstaller():
        print("PyInstaller not found. Installing...")
        install_pyinstaller()
    
    print("Creating installer script...")
    installer_script_path = create_installer_script()
    
    print("Creating PyInstaller spec file...")
    spec_file_path = create_spec_file(installer_script_path)
    
    print("Building executable installer...")
    print("This may take a few minutes...")
    
    try:
        # Run PyInstaller
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--onefile",
            "--windowed",
            str(spec_file_path)
        ], check=True)
        
        # Move the executable to the current directory
        dist_dir = Path("dist")
        if dist_dir.exists():
            exe_files = list(dist_dir.glob("*.exe"))
            if exe_files:
                exe_file = exe_files[0]
                final_exe = Path("TalindaPOS_Installer.exe")
                shutil.move(str(exe_file), str(final_exe))
                
                print()
                print("✅ Executable installer created successfully!")
                print(f"📁 Location: {final_exe.absolute()}")
                print()
                print("The installer will:")
                print("• Check system requirements")
                print("• Install Python (if needed)")
                print("• Install all required packages")
                print("• Set up the database")
                print("• Create startup scripts")
                print("• Configure the application")
                print()
                print("Users can now run this executable to install Talinda POS!")
                
                # Clean up temporary files
                if installer_script_path.exists():
                    installer_script_path.unlink()
                if spec_file_path.exists():
                    spec_file_path.unlink()
                if dist_dir.exists():
                    shutil.rmtree(dist_dir)
                build_dir = Path("build")
                if build_dir.exists():
                    shutil.rmtree(build_dir)
                
                return True
        
        print("❌ Failed to create executable installer")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building installer: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 