@echo off
setlocal EnableDelayedExpansion

echo ===========================================
echo Talinda POS System Installation Setup
echo ===========================================

:: Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.8 or later.
    echo You can download Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    if errorlevel 1 (
        echo Failed to create virtual environment.
        pause
        exit /b 1
    )
)

:: Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Failed to upgrade pip.
    pause
    exit /b 1
)

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

:: Build the executable
echo Building Talinda POS executable...
python build.py
if errorlevel 1 (
    echo Failed to build the executable.
    pause
    exit /b 1
)

:: Create desktop shortcut
echo Creating desktop shortcut...
set "SCRIPT_DIR=%~dp0"
set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\Talinda POS.lnk"
set "TARGET=%SCRIPT_DIR%dist\TalindaPOS.exe"

powershell -Command "$WS = New-Object -ComObject WScript.Shell; $SC = $WS.CreateShortcut('%SHORTCUT%'); $SC.TargetPath = '%TARGET%'; $SC.WorkingDirectory = '%SCRIPT_DIR%dist'; $SC.Description = 'Talinda Point of Sale System'; $SC.Save()"

echo.
echo ===========================================
echo Installation completed successfully!
echo.
echo The Talinda POS executable has been created in the 'dist' folder
echo A shortcut has been created on your desktop
echo.
echo You can now run Talinda POS by:
echo 1. Double-clicking the desktop shortcut
echo 2. Running TalindaPOS.exe from the dist folder
echo ===========================================
echo.

pause
