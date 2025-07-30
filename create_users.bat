@echo off
REM Talinda POS - Create Login Users
REM ================================
REM This batch file runs the user creation script for new devices

echo.
echo ========================================
echo    TALINDA POS - CREATE LOGIN USERS
echo ========================================
echo.
echo This will help you create login users for new devices.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

REM Check if the script exists
if not exist "create_login_users.py" (
    echo ERROR: create_login_users.py not found!
    echo Please ensure you are running this from the correct directory.
    pause
    exit /b 1
)

echo Starting user creation script...
echo.

REM Run the Python script
python create_login_users.py

echo.
echo Script execution completed.
pause 