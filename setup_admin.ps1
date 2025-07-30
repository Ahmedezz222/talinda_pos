# Talinda POS Setup with Admin Credentials - PowerShell Script
# Run this script in PowerShell with: .\setup_admin.ps1

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

Write-ColorOutput "========================================" "Cyan"
Write-ColorOutput "Talinda POS Setup with Admin Credentials" "Cyan"
Write-ColorOutput "========================================" "Cyan"
Write-ColorOutput ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
    Write-ColorOutput "Python found: $pythonVersion" "Green"
} catch {
    Write-ColorOutput "ERROR: Python is not installed or not in PATH" "Red"
    Write-ColorOutput "Please install Python 3.8 or later from https://python.org" "Yellow"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-ColorOutput ""
Write-ColorOutput "This will prompt you for admin username and password," "Yellow"
Write-ColorOutput "then build the application with these credentials embedded." "Yellow"
Write-ColorOutput ""

# Confirm before proceeding
$confirm = Read-Host "Do you want to continue? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-ColorOutput "Setup cancelled." "Yellow"
    exit 0
}

Write-ColorOutput ""
Write-ColorOutput "Running enhanced setup script..." "Green"

# Run the setup script
try {
    $process = Start-Process python -ArgumentList "setup_with_admin.py" -Wait -PassThru -NoNewWindow
    if ($process.ExitCode -eq 0) {
        Write-ColorOutput ""
        Write-ColorOutput "Setup completed successfully!" "Green"
        Write-ColorOutput "Check the build directory for your executable." "Cyan"
    } else {
        Write-ColorOutput ""
        Write-ColorOutput "Setup failed with exit code: $($process.ExitCode)" "Red"
    }
} catch {
    Write-ColorOutput ""
    Write-ColorOutput "Error running setup script: $($_.Exception.Message)" "Red"
}

Write-ColorOutput ""
Read-Host "Press Enter to exit" 