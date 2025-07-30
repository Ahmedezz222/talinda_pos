@echo off
echo ========================================
echo Talinda POS Installer Builder
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from https://python.org
    pause
    exit /b 1
)

echo Python found. Installing build dependencies...

REM Install cx_Freeze
pip install cx_Freeze

REM Install PyInstaller (alternative method)
pip install pyinstaller

echo.
echo Building executable with cx_Freeze...
python setup.py build

if errorlevel 1 (
    echo ERROR: Build failed with cx_Freeze
    echo Trying PyInstaller as alternative...
    echo.
    
    REM Try PyInstaller as alternative
    python -m PyInstaller --onefile --windowed --name "Talinda_POS" src/main.py
)

if errorlevel 1 (
    echo ERROR: Both build methods failed
    pause
    exit /b 1
)

echo.
echo ========================================
echo Build completed successfully!
echo ========================================
echo.
echo The executable can be found in:
echo - build/exe.win-amd64-3.8/ (cx_Freeze)
echo - dist/ (PyInstaller)
echo.
echo To create a simple installer:
echo 1. Copy the build folder to a USB drive
echo 2. Run Talinda_POS.exe from any computer
echo.
pause 