# Talinda POS Installer Builder - PowerShell Script
# Run this script in PowerShell with: .\build.ps1

param(
    [switch]$NoInstaller,
    [switch]$NoPortable,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
Talinda POS Installer Builder

Usage:
    .\build.ps1                    # Build everything
    .\build.ps1 -NoInstaller       # Skip installer creation
    .\build.ps1 -NoPortable        # Skip portable package
    .\build.ps1 -Help              # Show this help

Options:
    -NoInstaller    Skip creating Windows installer
    -NoPortable     Skip creating portable package
    -Help           Show this help message
"@
    exit 0
}

# Set execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Talinda POS Installer Builder" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8 or later from https://python.org" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Install build dependencies
Write-Host "Installing build dependencies..." -ForegroundColor Yellow

$dependencies = @(
    "cx_Freeze",
    "pyinstaller",
    "pyinstaller-hooks-contrib"
)

foreach ($dep in $dependencies) {
    try {
        Write-Host "Installing $dep..." -ForegroundColor Yellow
        pip install $dep
        Write-Host "✓ Installed $dep" -ForegroundColor Green
    } catch {
        Write-Host "✗ Failed to install $dep" -ForegroundColor Red
        Write-Host "Continuing with other methods..." -ForegroundColor Yellow
    }
}

Write-Host ""

# Try cx_Freeze first
Write-Host "Building executable with cx_Freeze..." -ForegroundColor Yellow
try {
    python setup.py build
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ cx_Freeze build completed successfully" -ForegroundColor Green
        $buildMethod = "cx_Freeze"
    } else {
        throw "cx_Freeze failed"
    }
} catch {
    Write-Host "✗ cx_Freeze build failed, trying PyInstaller..." -ForegroundColor Yellow
    
    # Try PyInstaller as alternative
    try {
        python -m PyInstaller --onefile --windowed --name "Talinda_POS" --distpath "dist" src/main.py
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ PyInstaller build completed successfully" -ForegroundColor Green
            $buildMethod = "PyInstaller"
        } else {
            throw "PyInstaller failed"
        }
    } catch {
        Write-Host "✗ Both build methods failed" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Create installer if requested
if (-not $NoInstaller) {
    Write-Host ""
    Write-Host "Creating installer..." -ForegroundColor Yellow
    
    try {
        python build_installer.py --no-portable
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Installer created successfully" -ForegroundColor Green
        } else {
            Write-Host "⚠ Installer creation failed, but executable was built" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠ Installer creation failed, but executable was built" -ForegroundColor Yellow
    }
}

# Create portable package if requested
if (-not $NoPortable) {
    Write-Host ""
    Write-Host "Creating portable package..." -ForegroundColor Yellow
    
    try {
        python build_installer.py --no-installer
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Portable package created successfully" -ForegroundColor Green
        } else {
            Write-Host "⚠ Portable package creation failed" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "⚠ Portable package creation failed" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Build completed successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Show output locations
if ($buildMethod -eq "cx_Freeze") {
    Write-Host "Executable location: build/exe.win-amd64-3.8/" -ForegroundColor White
    Write-Host "Main executable: build/exe.win-amd64-3.8/Talinda_POS.exe" -ForegroundColor White
} else {
    Write-Host "Executable location: dist/" -ForegroundColor White
    Write-Host "Main executable: dist/Talinda_POS.exe" -ForegroundColor White
}

if (-not $NoInstaller) {
    Write-Host "Installer location: installer/" -ForegroundColor White
}

if (-not $NoPortable) {
    Write-Host "Portable package location: installer/" -ForegroundColor White
}

Write-Host ""
Write-Host "Deployment instructions:" -ForegroundColor Yellow
Write-Host "1. Copy the entire build folder to any computer" -ForegroundColor White
Write-Host "2. Run Talinda_POS.exe from the folder" -ForegroundColor White
Write-Host "3. The application will create its database automatically" -ForegroundColor White

Write-Host ""
Read-Host "Press Enter to exit" 