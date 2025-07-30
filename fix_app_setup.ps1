# Talinda POS - Fix App Setup
# ===========================
# This PowerShell script runs the fix setup script for Talinda POS

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TALINDA POS - FIX APP SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will fix common issues and set up the application." -ForegroundColor Yellow
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or higher and try again." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if the fix script exists
if (-not (Test-Path "fix_app_setup.py")) {
    Write-Host "ERROR: fix_app_setup.py not found!" -ForegroundColor Red
    Write-Host "Please ensure you are running this from the correct directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting fix and setup process..." -ForegroundColor Yellow
Write-Host ""

# Run the fix script
try {
    python fix_app_setup.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Fix and setup completed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "✗ Fix and setup failed!" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "✗ Error running fix script: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Fix and setup process completed." -ForegroundColor Yellow
Read-Host "Press Enter to exit" 