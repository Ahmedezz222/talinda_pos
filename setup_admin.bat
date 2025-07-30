@echo off
echo ========================================
echo Talinda POS Setup with Admin Credentials
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

echo Python found. Starting setup with admin configuration...
echo.
echo This will prompt you for admin username and password,
echo then build the application with these credentials embedded.
echo.

set /p confirm="Do you want to continue? (y/N): "
if /i not "%confirm%"=="y" (
    echo Setup cancelled.
    pause
    exit /b 0
)

echo.
echo Running enhanced setup script...
python setup_with_admin.py

echo.
echo Setup completed!
echo Check the build directory for your executable.
echo.
pause 