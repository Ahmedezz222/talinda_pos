@echo off
echo ========================================
echo Talinda POS Project Cleanup
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

echo Python found. Starting cleanup process...
echo.
echo This will remove unnecessary files to optimize your installer size.
echo A backup will be created before cleaning.
echo.

set /p confirm="Do you want to continue? (y/N): "
if /i not "%confirm%"=="y" (
    echo Cleanup cancelled.
    pause
    exit /b 0
)

echo.
echo Running cleanup script...
python cleanup_project.py

echo.
echo Cleanup completed!
echo Check cleanup_report.txt for details.
echo.
pause 