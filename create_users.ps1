# Talinda POS - Create Login Users
# ===============================
# This PowerShell script runs the user creation script for new devices

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TALINDA POS - CREATE LOGIN USERS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will help you create login users for new devices." -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-Host "Found Python: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if the script exists
if (-not (Test-Path "create_login_users.py")) {
    Write-Host "ERROR: create_login_users.py not found!" -ForegroundColor Red
    Write-Host "Please ensure you are running this from the correct directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting user creation script..." -ForegroundColor Green
Write-Host ""

# Run the Python script
try {
    python create_login_users.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "Script executed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "Script execution failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "ERROR: Failed to execute the script: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "Script execution completed." -ForegroundColor Yellow
Read-Host "Press Enter to exit" 