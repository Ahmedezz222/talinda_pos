# Talinda POS - New Device Setup Script
# PowerShell version for Windows

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "           TALINDA POS - NEW DEVICE SETUP" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This script will prepare the Talinda POS application" -ForegroundColor White
Write-Host "to run on this device." -ForegroundColor White
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Checking Python installation..." -ForegroundColor Green

try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Python found: $pythonVersion" -ForegroundColor Green
    } else {
        throw "Python not found"
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH!" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher from https://python.org" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Python found. Running setup..." -ForegroundColor Green
Write-Host ""

# Run the Python setup script
python setup_for_new_device.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Setup completed successfully!" -ForegroundColor Green
    Write-Host "You can now run the application with: python src/main.py" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "Setup failed! Check the logs for details." -ForegroundColor Red
}

Read-Host "Press Enter to exit" 