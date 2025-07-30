# Talinda POS - Universal Setup PowerShell Script
# ================================================

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    TALINDA POS - UNIVERSAL SETUP" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found! Please install Python 3.8 or higher." -ForegroundColor Red
    Write-Host "Download from: https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Choose setup mode:" -ForegroundColor Yellow
Write-Host "1. New Device Setup (default)" -ForegroundColor White
Write-Host "2. Network Deployment" -ForegroundColor White
Write-Host "3. Production Environment" -ForegroundColor White
Write-Host "4. Development Environment" -ForegroundColor White
Write-Host "5. Quick Setup" -ForegroundColor White
Write-Host ""

$choice = Read-Host "Enter your choice (1-5, default=1)"

switch ($choice) {
    "" { $mode = "new-device" }
    "1" { $mode = "new-device" }
    "2" { $mode = "network" }
    "3" { $mode = "production" }
    "4" { $mode = "development" }
    "5" { $mode = "quick" }
    default { 
        Write-Host "Invalid choice. Using default: new-device" -ForegroundColor Yellow
        $mode = "new-device"
    }
}

Write-Host ""
Write-Host "Choose environment:" -ForegroundColor Yellow
Write-Host "1. Local (default)" -ForegroundColor White
Write-Host "2. Server" -ForegroundColor White
Write-Host "3. Cloud" -ForegroundColor White
Write-Host ""

$env_choice = Read-Host "Enter your choice (1-3, default=1)"

switch ($env_choice) {
    "" { $env = "local" }
    "1" { $env = "local" }
    "2" { $env = "server" }
    "3" { $env = "cloud" }
    default { 
        Write-Host "Invalid choice. Using default: local" -ForegroundColor Yellow
        $env = "local"
    }
}

Write-Host ""
Write-Host "Starting setup with mode: $mode and environment: $env" -ForegroundColor Green
Write-Host ""

# Run the setup script
try {
    $setupScript = "setup_universal.py"
    
    if (-not (Test-Path $setupScript)) {
        Write-Host "❌ Setup script not found: $setupScript" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    $arguments = @("--mode", $mode, "--env", $env)
    $process = Start-Process -FilePath "python" -ArgumentList $arguments -Wait -PassThru -NoNewWindow
    
    if ($process.ExitCode -eq 0) {
        Write-Host ""
        Write-Host "✅ Setup completed successfully!" -ForegroundColor Green
        Write-Host "You can now start the application." -ForegroundColor Green
        Write-Host ""
        Write-Host "To start the application:" -ForegroundColor Yellow
        Write-Host "  - Double-click: start_talinda_pos.bat" -ForegroundColor White
        Write-Host "  - Or run: python src/main.py" -ForegroundColor White
    } else {
        Write-Host ""
        Write-Host "❌ Setup failed! Check the logs for details." -ForegroundColor Red
        Write-Host "Log file: setup_universal.log" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error running setup: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit" 