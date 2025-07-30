# Talinda POS - Uninstaller
# =========================
# This PowerShell script runs the uninstall script for Talinda POS

Write-Host ""
Write-Host "========================================" -ForegroundColor Red
Write-Host "    TALINDA POS - UNINSTALLER" -ForegroundColor Red
Write-Host "========================================" -ForegroundColor Red
Write-Host ""
Write-Host "This will completely remove the Talinda POS application." -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  WARNING: This action cannot be undone!" -ForegroundColor Red
Write-Host "All data, configurations, and files will be permanently deleted." -ForegroundColor Red
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

# Check if the uninstall script exists
if (-not (Test-Path "uninstall.py")) {
    Write-Host "ERROR: uninstall.py not found!" -ForegroundColor Red
    Write-Host "Please ensure you are running this from the correct directory." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Starting uninstall process..." -ForegroundColor Yellow
Write-Host ""

# Run the uninstall script
try {
    python uninstall.py
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✓ Uninstall completed successfully!" -ForegroundColor Green
    } else {
        Write-Host ""
        Write-Host "✗ Uninstall failed!" -ForegroundColor Red
    }
} catch {
    Write-Host ""
    Write-Host "✗ Error running uninstall script: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Uninstall process completed." -ForegroundColor Yellow
Read-Host "Press Enter to exit" 