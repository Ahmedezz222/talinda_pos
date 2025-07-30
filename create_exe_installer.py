#!/usr/bin/env python3
"""
Create Talinda POS Executable Installer
=======================================

This script creates a standalone executable installer for Talinda POS.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def main():
    print("=" * 60)
    print("    TALINDA POS - EXECUTABLE INSTALLER CREATOR")
    print("=" * 60)
    print()
    
    # Check Python
    try:
        result = subprocess.run([sys.executable, "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Python found: {result.stdout.strip()}")
        else:
            print("❌ Python not found!")
            return False
    except:
        print("❌ Python not found!")
        return False
    
    # Install PyInstaller
    print("Installing PyInstaller...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], 
                      check=True, capture_output=True)
        print("✅ PyInstaller installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install PyInstaller")
        return False
    
    # Create installer script
    print("Creating installer script...")
    
    installer_code = '''#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
import tempfile
import json
import platform
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading

class TalindaPOSInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Talinda POS - Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        self.setup_ui()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title_label = ttk.Label(main_frame, text="Talinda POS - Installer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        welcome_text = "Welcome to Talinda POS Installer!\\n\\nThis installer will:\\n• Install all required packages\\n• Set up the database\\n• Create startup scripts\\n• Configure the application\\n\\nPlease select an installation directory and click 'Install' to begin."
        
        welcome_label = ttk.Label(main_frame, text=welcome_text, justify=tk.LEFT)
        welcome_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        ttk.Label(main_frame, text="Installation Directory:").grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        
        path_frame = ttk.Frame(main_frame)
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.path_var = tk.StringVar(value=str(Path.home() / "TalindaPOS"))
        self.path_entry = ttk.Entry(path_frame, textvariable=self.path_var, width=50)
        self.path_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        browse_btn = ttk.Button(path_frame, text="Browse", command=self.browse_path)
        browse_btn.grid(row=0, column=1, padx=(5, 0))
        
        progress_frame = ttk.LabelFrame(main_frame, text="Installation Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, text="Ready to install")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        self.install_btn = ttk.Button(button_frame, text="Install", command=self.start_installation)
        self.install_btn.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_btn = ttk.Button(button_frame, text="Cancel", command=self.root.quit)
        self.cancel_btn.grid(row=0, column=1)
        
        main_frame.columnconfigure(0, weight=1)
        path_frame.columnconfigure(0, weight=1)
        progress_frame.columnconfigure(0, weight=1)
        
    def browse_path(self):
        path = filedialog.askdirectory(initialdir=self.path_var.get())
        if path:
            self.path_var.set(path)
    
    def update_status(self, message, progress=None):
        self.status_label.config(text=message)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update()
    
    def install_requirements(self):
        self.update_status("Installing required packages...", 30)
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
                self.update_status(f"Installing {req}...", 30 + (len(requirements).index(req) * 5))
                subprocess.run([sys.executable, "-m", "pip", "install", req], 
                             capture_output=True, check=True)
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install packages: {e}")
            return False
    
    def create_application_files(self):
        self.update_status("Creating application files...", 60)
        try:
            install_path = Path(self.path_var.get())
            install_path.mkdir(parents=True, exist_ok=True)
            
            (install_path / "src").mkdir(exist_ok=True)
            (install_path / "config").mkdir(exist_ok=True)
            (install_path / "logs").mkdir(exist_ok=True)
            (install_path / "reports").mkdir(exist_ok=True)
            (install_path / "backups").mkdir(exist_ok=True)
            
            # Create main.py
            main_py = '''#!/usr/bin/env python3
import sys
from pathlib import Path
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

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
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create files: {e}")
            return False
    
    def setup_database(self):
        self.update_status("Setting up database...", 80)
        try:
            install_path = Path(self.path_var.get())
            
            db_init = '''#!/usr/bin/env python3
import sqlite3
from pathlib import Path

def init_database():
    db_path = Path(__file__).parent / "pos_database.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
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
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tax_rate REAL DEFAULT 0.0,
            is_active BOOLEAN DEFAULT 1
        )
    ''')
    
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
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, full_name, role)
        VALUES (?, ?, ?, ?)
    ''', ('admin', 'admin123', 'System Administrator', 'admin'))
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (username, password, full_name, role)
        VALUES (?, ?, ?, ?)
    ''', ('cashier', 'cashier123', 'Default Cashier', 'cashier'))
    
    categories = [('Food', 0.14), ('Beverage', 0.14), ('Dessert', 0.14), ('Other', 0.14)]
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
            
            subprocess.run([sys.executable, str(install_path / "init_database.py")], 
                         cwd=install_path, check=True)
            
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Failed to setup database: {e}")
            return False
    
    def start_installation(self):
        self.install_btn.config(state='disabled')
        self.cancel_btn.config(state='disabled')
        
        def install_thread():
            try:
                if not self.install_requirements():
                    return
                if not self.create_application_files():
                    return
                if not self.setup_database():
                    return
                
                self.update_status("Installation completed successfully!", 100)
                messagebox.showinfo("Installation Complete", 
                                  f"Talinda POS has been installed successfully!\\n\\n"
                                  f"Installation directory: {self.path_var.get()}\\n\\n"
                                  f"Default login credentials:\\n"
                                  f"Admin: admin / admin123\\n"
                                  f"Cashier: cashier / cashier123\\n\\n"
                                  f"Please change these passwords immediately!")
                self.cancel_btn.config(text="Close", state='normal')
                
            except Exception as e:
                messagebox.showerror("Installation Error", f"Installation failed: {e}")
                self.cancel_btn.config(state='normal')
        
        thread = threading.Thread(target=install_thread)
        thread.daemon = True
        thread.start()
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    installer = TalindaPOSInstaller()
    installer.run()
'''
    
    with open("talinda_pos_installer.py", "w", encoding="utf-8") as f:
        f.write(installer_code)
    
    print("✅ Installer script created")
    
    # Create spec file
    print("Creating PyInstaller spec file...")
    
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['talinda_pos_installer.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[
        'tkinter',
        'tkinter.ttk',
        'tkinter.messagebox',
        'tkinter.filedialog',
        'subprocess',
        'threading',
        'pathlib',
        'json',
        'platform',
        'tempfile',
        'shutil'
    ],
    hookspath=[],
    hooksconfig={},
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
    
    with open("talinda_pos_installer.spec", "w") as f:
        f.write(spec_content)
    
    print("✅ Spec file created")
    
    # Build executable
    print("Building executable installer...")
    print("This may take a few minutes...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "PyInstaller",
            "--clean",
            "--onefile",
            "--windowed",
            "talinda_pos_installer.spec"
        ], check=True)
        
        # Move executable to current directory
        if Path("dist/TalindaPOS_Installer.exe").exists():
            shutil.move("dist/TalindaPOS_Installer.exe", "TalindaPOS_Installer.exe")
            print("✅ Executable installer created successfully!")
            print(f"📁 Location: {Path.cwd() / 'TalindaPOS_Installer.exe'}")
        else:
            print("❌ Executable not found in dist directory")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Error building installer: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Cleanup
    print("Cleaning up temporary files...")
    
    files_to_remove = [
        "talinda_pos_installer.py",
        "talinda_pos_installer.spec"
    ]
    
    dirs_to_remove = [
        "dist",
        "build"
    ]
    
    for file in files_to_remove:
        if Path(file).exists():
            Path(file).unlink()
    
    for dir_path in dirs_to_remove:
        if Path(dir_path).exists():
            shutil.rmtree(dir_path)
    
    print("✅ Cleanup completed")
    
    print()
    print("The installer will:")
    print("• Install all required packages")
    print("• Set up the database")
    print("• Create startup scripts")
    print("• Configure the application")
    print()
    print("Users can now run TalindaPOS_Installer.exe to install Talinda POS!")
    print()
    print("Installation creator completed!")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 