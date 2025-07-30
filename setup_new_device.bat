@echo off
echo ============================================================
echo           TALINDA POS - NEW DEVICE SETUP
echo ============================================================
echo.
echo This script will prepare the Talinda POS application
echo to run on this device.
echo.
echo Press any key to continue...
pause >nul

echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH!
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python found. Running setup...
echo.

python setup_for_new_device.py

if errorlevel 1 (
    echo.
    echo Setup failed! Check the logs for details.
    pause
    exit /b 1
) else (
    echo.
    echo Setup completed successfully!
    echo You can now run the application with: python src/main.py
    pause
) 