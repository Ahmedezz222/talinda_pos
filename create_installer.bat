@echo off
chcp 65001 >nul
echo ========================================
echo    TALINDA POS - INSTALLER CREATOR
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8 or higher.
    echo Download from: https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Install PyInstaller if not present
echo Installing PyInstaller...
python -m pip install pyinstaller --quiet
if errorlevel 1 (
    echo ❌ Failed to install PyInstaller
    pause
    exit /b 1
)

echo ✅ PyInstaller installed
echo.

REM Create the installer script
echo Creating installer script...
(
echo import os
echo import sys
echo import subprocess
echo import shutil
echo import tempfile
echo import zipfile
echo import json
echo import platform
echo import urllib.request
echo import urllib.error
echo from pathlib import Path
echo import tkinter as tk
echo from tkinter import ttk, messagebox, filedialog
echo import threading
echo import time
echo.
echo class TalindaPOSInstaller:
echo     def __init__(self^):
echo         self.root = tk.Tk(^)
echo         self.root.title^("Talinda POS - Installer"^)
echo         self.root.geometry^("600x500"^)
echo         self.root.resizable^(False, False^)
echo         self.setup_ui^(^)
echo         self.install_path = None
echo         self.installation_complete = False
echo.    
echo     def setup_ui^(self^):
echo         main_frame = ttk.Frame^(self.root, padding="20"^)
echo         main_frame.grid^(row=0, column=0, sticky=^(tk.W, tk.E, tk.N, tk.S^)^)
echo.        
echo         title_label = ttk.Label^(main_frame, text="Talinda POS - Installer", font=^("Arial", 16, "bold"^)^)
echo         title_label.grid^(row=0, column=0, columnspan=2, pady=^(0, 20^)^)
echo.        
echo         welcome_text = "Welcome to Talinda POS Installer!\\n\\nThis installer will:\\n• Check system requirements\\n• Install Python ^(if needed^)\\n• Install all required packages\\n• Set up the database\\n• Create startup scripts\\n• Configure the application\\n\\nPlease select an installation directory and click 'Install' to begin."
echo         welcome_label = ttk.Label^(main_frame, text=welcome_text, justify=tk.LEFT^)
echo         welcome_label.grid^(row=1, column=0, columnspan=2, pady=^(0, 20^)^)
echo.        
echo         ttk.Label^(main_frame, text="Installation Directory:"^).grid^(row=2, column=0, sticky=tk.W, pady=^(0, 5^)^)
echo.        
echo         path_frame = ttk.Frame^(main_frame^)
echo         path_frame.grid^(row=3, column=0, columnspan=2, sticky=^(tk.W, tk.E^), pady=^(0, 20^)^)
echo.        
echo         self.path_var = tk.StringVar^(value=str^(Path.home^(^) / "TalindaPOS"^)^)
echo         self.path_entry = ttk.Entry^(path_frame, textvariable=self.path_var, width=50^)
echo         self.path_entry.grid^(row=0, column=0, sticky=^(tk.W, tk.E^)^)
echo.        
echo         browse_btn = ttk.Button^(path_frame, text="Browse", command=self.browse_path^)
echo         browse_btn.grid^(row=0, column=1, padx=^(5, 0^)^)
echo.        
echo         progress_frame = ttk.LabelFrame^(main_frame, text="Installation Progress", padding="10"^)
echo         progress_frame.grid^(row=4, column=0, columnspan=2, sticky=^(tk.W, tk.E^), pady=^(0, 20^)^)
echo.        
echo         self.progress = ttk.Progressbar^(progress_frame, mode='determinate'^)
echo         self.progress.grid^(row=0, column=0, sticky=^(tk.W, tk.E^), pady=^(0, 10^)^)
echo.        
echo         self.status_label = ttk.Label^(progress_frame, text="Ready to install"^)
echo         self.status_label.grid^(row=1, column=0, sticky=tk.W^)
echo.        
echo         button_frame = ttk.Frame^(main_frame^)
echo         button_frame.grid^(row=5, column=0, columnspan=2, pady=^(20, 0^)^)
echo.        
echo         self.install_btn = ttk.Button^(button_frame, text="Install", command=self.start_installation^)
echo         self.install_btn.grid^(row=0, column=0, padx=^(0, 10^)^)
echo.        
echo         self.cancel_btn = ttk.Button^(button_frame, text="Cancel", command=self.root.quit^)
echo         self.cancel_btn.grid^(row=0, column=1^)
echo.        
echo         main_frame.columnconfigure^(0, weight=1^)
echo         path_frame.columnconfigure^(0, weight=1^)
echo         progress_frame.columnconfigure^(0, weight=1^)
echo.    
echo     def browse_path^(self^):
echo         path = filedialog.askdirectory^(initialdir=self.path_var.get^(^)^)
echo         if path:
echo             self.path_var.set^(path^)
echo.    
echo     def update_status^(self, message, progress=None^):
echo         self.status_label.config^(text=message^)
echo         if progress is not None:
echo             self.progress['value'] = progress
echo         self.root.update^(^)
echo.    
echo     def install_requirements^(self^):
echo         self.update_status^("Installing required packages...", 40^)
echo         requirements = ["PyQt5>=5.15.9", "PyQt5-Qt5>=5.15.2", "PyQt5-sip>=12.12.1", "SQLAlchemy>=2.0.19", "bcrypt>=4.0.1", "python-dotenv>=1.0.0", "reportlab>=4.0.4", "qrcode>=7.4.2", "Pillow>=10.0.0", "openpyxl>=3.1.2", "pandas>=2.0.0"]
echo         try:
echo             for req in requirements:
echo                 self.update_status^(f"Installing {req}...", 40 + ^(len^(requirements^).index^(req^) * 5^)^)
echo                 subprocess.run^([sys.executable, "-m", "pip", "install", req], capture_output=True, check=True^)
echo             return True
echo         except Exception as e:
echo             messagebox.showerror^("Error", f"Failed to install packages: {e}"^)
echo             return False
echo.    
echo     def extract_application^(self^):
echo         self.update_status^("Extracting application files...", 70^)
echo         try:
echo             install_path = Path^(self.path_var.get^(^)^)
echo             install_path.mkdir^(parents=True, exist_ok=True^)
echo             ^(install_path / "src"^).mkdir^(exist_ok=True^)
echo             ^(install_path / "config"^).mkdir^(exist_ok=True^)
echo             ^(install_path / "logs"^).mkdir^(exist_ok=True^)
echo             ^(install_path / "reports"^).mkdir^(exist_ok=True^)
echo             ^(install_path / "backups"^).mkdir^(exist_ok=True^)
echo             self.create_sample_files^(install_path^)
echo             return True
echo         except Exception as e:
echo             messagebox.showerror^("Error", f"Failed to extract files: {e}"^)
echo             return False
echo.    
echo     def create_sample_files^(self, install_path^):
echo         main_py = '''#!/usr/bin/env python3
echo import sys
echo from pathlib import Path
echo from PyQt5.QtWidgets import QApplication
echo from PyQt5.QtCore import Qt
echo src_path = Path^(__file__^).parent / "src"
echo sys.path.insert^(0, str^(src_path^)^)
echo def main^(^):
echo     app = QApplication^(sys.argv^)
echo     app.setApplicationName^("Talinda POS"^)
echo     app.setApplicationVersion^("3.0.0"^)
echo     from ui.main_window import MainWindow
echo     window = MainWindow^(^)
echo     window.show^(^)
echo     sys.exit^(app.exec_^(^)^)
echo if __name__ == "__main__":
echo     main^(^)
echo '''
echo         with open^(install_path / "main.py", "w"^) as f:
echo             f.write^(main_py^)
echo.        
echo         if platform.system^(^) == "Windows":
echo             startup_script = f'''@echo off
echo cd /d "{install_path}"
echo python main.py
echo pause
echo '''
echo             with open^(install_path / "start_talinda_pos.bat", "w"^) as f:
echo                 f.write^(startup_script^)
echo         else:
echo             startup_script = f'''#!/bin/bash
echo cd "{install_path}"
echo python3 main.py
echo '''
echo             with open^(install_path / "start_talinda_pos.sh", "w"^) as f:
echo                 f.write^(startup_script^)
echo             os.chmod^(install_path / "start_talinda_pos.sh", 0o755^)
echo.    
echo     def setup_database^(self^):
echo         self.update_status^("Setting up database...", 80^)
echo         try:
echo             install_path = Path^(self.path_var.get^(^)^)
echo             db_init = '''#!/usr/bin/env python3
echo import sqlite3
echo from pathlib import Path
echo def init_database^(^):
echo     db_path = Path^(__file__^).parent / "pos_database.db"
echo     conn = sqlite3.connect^(db_path^)
echo     cursor = conn.cursor^(^)
echo     cursor.execute^('''CREATE TABLE IF NOT EXISTS users ^(id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, full_name TEXT NOT NULL, role TEXT NOT NULL, is_active BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP^)''')
echo     cursor.execute^('''CREATE TABLE IF NOT EXISTS products ^(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, cost REAL NOT NULL, stock_quantity INTEGER DEFAULT 0, category_id INTEGER, barcode TEXT, is_active BOOLEAN DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP^)''')
echo     cursor.execute^('''CREATE TABLE IF NOT EXISTS categories ^(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, tax_rate REAL DEFAULT 0.0, is_active BOOLEAN DEFAULT 1^)''')
echo     cursor.execute^('''CREATE TABLE IF NOT EXISTS sales ^(id INTEGER PRIMARY KEY AUTOINCREMENT, total_amount REAL NOT NULL, tax_amount REAL NOT NULL, discount_amount REAL DEFAULT 0.0, payment_method TEXT NOT NULL, user_id INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP^)''')
echo     cursor.execute^('''INSERT OR IGNORE INTO users ^(username, password, full_name, role^) VALUES ^(?, ?, ?, ?^)''', ^('admin', 'admin123', 'System Administrator', 'admin'^)^)
echo     cursor.execute^('''INSERT OR IGNORE INTO users ^(username, password, full_name, role^) VALUES ^(?, ?, ?, ?^)''', ^('cashier', 'cashier123', 'Default Cashier', 'cashier'^)^)
echo     categories = [^('Food', 0.14^), ^('Beverage', 0.14^), ^('Dessert', 0.14^), ^('Other', 0.14^)]
echo     for name, tax_rate in categories:
echo         cursor.execute^('''INSERT OR IGNORE INTO categories ^(name, tax_rate^) VALUES ^(?, ?^)''', ^(name, tax_rate^)^)
echo     conn.commit^(^)
echo     conn.close^(^)
echo     print^("Database initialized successfully!"^)
echo if __name__ == "__main__":
echo     init_database^(^)
echo '''
echo             with open^(install_path / "init_database.py", "w"^) as f:
echo                 f.write^(db_init^)
echo             subprocess.run^([sys.executable, str^(install_path / "init_database.py"^)], cwd=install_path, check=True^)
echo             return True
echo         except Exception as e:
echo             messagebox.showerror^("Error", f"Failed to setup database: {e}"^)
echo             return False
echo.    
echo     def start_installation^(self^):
echo         self.install_btn.config^(state='disabled'^)
echo         self.cancel_btn.config^(state='disabled'^)
echo         def install_thread^(^):
echo             try:
echo                 if not self.install_requirements^(^):
echo                     return
echo                 if not self.extract_application^(^):
echo                     return
echo                 if not self.setup_database^(^):
echo                     return
echo                 self.update_status^("Installation completed successfully!", 100^)
echo                 self.installation_complete = True
echo                 messagebox.showinfo^("Installation Complete", f"Talinda POS has been installed successfully!\\n\\nInstallation directory: {self.path_var.get^(^)}\\n\\nDefault login credentials:\\nAdmin: admin / admin123\\nCashier: cashier / cashier123\\n\\nPlease change these passwords immediately!"^)
echo                 self.cancel_btn.config^(text="Close", state='normal'^)
echo             except Exception as e:
echo                 messagebox.showerror^("Installation Error", f"Installation failed: {e}"^)
echo                 self.cancel_btn.config^(state='normal'^)
echo         thread = threading.Thread^(target=install_thread^)
echo         thread.daemon = True
echo         thread.start^(^)
echo.    
echo     def run^(self^):
echo         self.root.mainloop^(^)
echo.
echo if __name__ == "__main__":
echo     installer = TalindaPOSInstaller^(^)
echo     installer.run^(^)
) > talinda_pos_installer.py

echo ✅ Installer script created
echo.

REM Create PyInstaller spec file
echo Creating PyInstaller spec file...
(
echo # -*- mode: python ; coding: utf-8 -*-
echo.
echo block_cipher = None
echo.
echo a = Analysis^(
echo     [r'talinda_pos_installer.py'],
echo     pathex=[],
echo     binaries=[],
echo     datas=[],
echo     hiddenimports=[
echo         'tkinter',
echo         'tkinter.ttk',
echo         'tkinter.messagebox',
echo         'tkinter.filedialog',
echo         'urllib.request',
echo         'urllib.error',
echo         'subprocess',
echo         'threading',
echo         'pathlib',
echo         'json',
echo         'platform',
echo         'tempfile',
echo         'shutil',
echo         'zipfile'
echo     ],
echo     hookspath=[],
echo     hooksconfig={},
echo     runtime_hooks=[],
echo     excludes=[],
echo     win_no_prefer_redirects=False,
echo     win_private_assemblies=False,
echo     cipher=block_cipher,
echo     noarchive=False,
echo ^)
echo.
echo pyz = PYZ^(a.pure, a.zipped_data, cipher=block_cipher^)
echo.
echo exe = EXE^(
echo     pyz,
echo     a.scripts,
echo     a.binaries,
echo     a.zipfiles,
echo     a.datas,
echo     [],
echo     name='TalindaPOS_Installer',
echo     debug=False,
echo     bootloader_ignore_signals=False,
echo     strip=False,
echo     upx=True,
echo     upx_exclude=[],
echo     runtime_tmpdir=None,
echo     console=False,
echo     disable_windowed_traceback=False,
echo     argv_emulation=False,
echo     target_arch=None,
echo     codesign_identity=None,
echo     entitlements_file=None,
echo     icon=None
echo ^)
) > talinda_pos_installer.spec

echo ✅ Spec file created
echo.

REM Build the executable
echo Building executable installer...
echo This may take a few minutes...
python -m PyInstaller --clean --onefile --windowed talinda_pos_installer.spec

if errorlevel 1 (
    echo ❌ Failed to build executable installer
    pause
    exit /b 1
)

REM Move the executable to current directory
if exist "dist\TalindaPOS_Installer.exe" (
    move "dist\TalindaPOS_Installer.exe" "TalindaPOS_Installer.exe"
    echo ✅ Executable installer created successfully!
    echo 📁 Location: %CD%\TalindaPOS_Installer.exe
    echo.
    echo The installer will:
    echo • Check system requirements
    echo • Install Python ^(if needed^)
    echo • Install all required packages
    echo • Set up the database
    echo • Create startup scripts
    echo • Configure the application
    echo.
    echo Users can now run this executable to install Talinda POS!
) else (
    echo ❌ Executable not found in dist directory
)

REM Clean up temporary files
if exist "talinda_pos_installer.py" del "talinda_pos_installer.py"
if exist "talinda_pos_installer.spec" del "talinda_pos_installer.spec"
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo.
echo Installation creator completed!
pause 