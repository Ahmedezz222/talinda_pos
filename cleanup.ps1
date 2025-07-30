# Talinda POS Project Cleanup - PowerShell Script
# Run this script in PowerShell with: .\cleanup.ps1

param(
    [switch]$NoBackup,
    [switch]$NoDbBackup,
    [switch]$Help
)

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Show help if requested
if ($Help) {
    Write-ColorOutput "Talinda POS Project Cleanup Script" "Cyan"
    Write-ColorOutput "==================================" "Cyan"
    Write-ColorOutput ""
    Write-ColorOutput "Usage:" "Yellow"
    Write-ColorOutput "  .\cleanup.ps1                    # Run with backup (default)" "White"
    Write-ColorOutput "  .\cleanup.ps1 -NoBackup         # Run without backup" "White"
    Write-ColorOutput "  .\cleanup.ps1 -NoDbBackup       # Don't backup database files" "White"
    Write-ColorOutput "  .\cleanup.ps1 -Help             # Show this help" "White"
    Write-ColorOutput ""
    Write-ColorOutput "This script removes unnecessary files to optimize installer size:" "Yellow"
    Write-ColorOutput "  - Test files and documentation" "White"
    Write-ColorOutput "  - Cache and temporary files" "White"
    Write-ColorOutput "  - Development files" "White"
    Write-ColorOutput "  - Build artifacts" "White"
    Write-ColorOutput "  - Report and log files" "White"
    Write-ColorOutput "  - Database files (with backup)" "White"
    Write-ColorOutput ""
    exit 0
}

Write-ColorOutput "========================================" "Cyan"
Write-ColorOutput "Talinda POS Project Cleanup" "Cyan"
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
Write-ColorOutput "This will remove unnecessary files to optimize your installer size." "Yellow"
if (-not $NoBackup) {
    Write-ColorOutput "A backup will be created before cleaning." "Green"
} else {
    Write-ColorOutput "No backup will be created (--NoBackup specified)." "Red"
}
Write-ColorOutput ""

# Build command line arguments
$scriptArgs = @()
if ($NoBackup) { $scriptArgs += "--no-backup" }
if ($NoDbBackup) { $scriptArgs += "--no-db-backup" }

# Confirm before proceeding
$confirm = Read-Host "Do you want to continue? (y/N)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-ColorOutput "Cleanup cancelled." "Yellow"
    exit 0
}

Write-ColorOutput ""
Write-ColorOutput "Running cleanup script..." "Green"

# Run the cleanup script
try {
    $process = Start-Process python -ArgumentList @("cleanup_project.py") -ArgumentList $scriptArgs -Wait -PassThru -NoNewWindow
    if ($process.ExitCode -eq 0) {
        Write-ColorOutput ""
        Write-ColorOutput "Cleanup completed successfully!" "Green"
        Write-ColorOutput "Check cleanup_report.txt for details." "Cyan"
    } else {
        Write-ColorOutput ""
        Write-ColorOutput "Cleanup failed with exit code: $($process.ExitCode)" "Red"
    }
} catch {
    Write-ColorOutput ""
    Write-ColorOutput "Error running cleanup script: $($_.Exception.Message)" "Red"
}

Write-ColorOutput ""
Read-Host "Press Enter to exit" 