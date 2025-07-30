@echo off
REM Talinda POS - Fix App Setup
REM ===========================
REM This batch file runs the fix setup script for Talinda POS

echo.
echo ========================================
echo    TALINDA POS - FIX APP SETUP
echo ========================================
echo.
echo This will fix common issues and set up the application.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

REM Check if the fix script exists
if not exist "fix_app_setup.py" (
    echo ERROR: fix_app_setup.py not found!
    echo Please ensure you are running this from the correct directory.
    pause
    exit /b 1
)

echo Starting fix and setup process...
echo.

REM Run the fix script
python fix_app_setup.py

echo.
echo Fix and setup process completed.
pause 