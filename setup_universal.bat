@echo off
echo ========================================
echo    TALINDA POS - UNIVERSAL SETUP
echo ========================================
echo.
echo Choose setup mode:
echo 1. New Device Setup (default)
echo 2. Network Deployment
echo 3. Production Environment
echo 4. Development Environment
echo 5. Quick Setup
echo.
set /p choice="Enter your choice (1-5, default=1): "

if "%choice%"=="" set choice=1
if "%choice%"=="1" set mode=new-device
if "%choice%"=="2" set mode=network
if "%choice%"=="3" set mode=production
if "%choice%"=="4" set mode=development
if "%choice%"=="5" set mode=quick

echo.
echo Choose environment:
echo 1. Local (default)
echo 2. Server
echo 3. Cloud
echo.
set /p env_choice="Enter your choice (1-3, default=1): "

if "%env_choice%"=="" set env_choice=1
if "%env_choice%"=="1" set env=local
if "%env_choice%"=="2" set env=server
if "%env_choice%"=="3" set env=cloud

echo.
echo Starting setup with mode: %mode% and environment: %env%
echo.

python setup_universal.py --mode %mode% --env %env%

if %errorlevel% equ 0 (
    echo.
    echo Setup completed successfully!
    echo You can now start the application.
) else (
    echo.
    echo Setup failed! Check the logs for details.
)

pause 