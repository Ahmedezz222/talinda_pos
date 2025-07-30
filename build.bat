@echo off
REM Talinda POS - Build Executable
REM ==============================
REM This batch file builds the Talinda POS executable

echo.
echo ========================================
echo    TALINDA POS - BUILD EXECUTABLE
echo ========================================
echo.
echo This will build a standalone executable.
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher and try again.
    pause
    exit /b 1
)

REM Check if the build script exists
if not exist "build_executable.py" (
    echo ERROR: build_executable.py not found!
    echo Please ensure you are running this from the correct directory.
    pause
    exit /b 1
)

echo Starting build process...
echo.

REM Run the build script
python build_executable.py

echo.
echo Build process completed.
pause 