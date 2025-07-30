@echo off
REM Talinda POS - Uninstaller
REM =========================
REM This batch file runs the uninstall script for Talinda POS

echo.
echo ========================================
echo    TALINDA POS - UNINSTALLER
echo ========================================
echo.
echo This will completely remove the Talinda POS application.
echo.
echo ⚠️  WARNING: This action cannot be undone!
echo All data, configurations, and files will be permanently deleted.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

REM Check if the uninstall script exists
if not exist "uninstall.py" (
    echo ERROR: uninstall.py not found!
    echo Please ensure you are running this from the correct directory.
    pause
    exit /b 1
)

echo Starting uninstall process...
echo.

REM Run the uninstall script
python uninstall.py

echo.
echo Uninstall process completed.
pause 