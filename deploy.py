#!/usr/bin/env python3
"""
Talinda POS Deployment Script
=============================

This script helps deploy the built Talinda POS application to various locations.
"""

import os
import sys
import shutil
import zipfile
import argparse
from pathlib import Path
from datetime import datetime

class Deployer:
    """Deploys the Talinda POS application."""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.app_name = "Talinda POS"
        self.app_version = "2.0.0"
        
        # Possible build locations
        self.build_locations = [
            self.project_root / "build" / "exe.win-amd64-3.8",
            self.project_root / "dist",
            self.project_root / "installer"
        ]
        
    def find_built_application(self):
        """Find the built application."""
        for location in self.build_locations:
            if location.exists():
                # Look for the main executable
                exe_name = f"{self.app_name.replace(' ', '_')}.exe"
                exe_path = location / exe_name
                
                if exe_path.exists():
                    return location, exe_path
                    
                # Check if it's a single executable
                if location.is_file() and location.suffix == '.exe':
                    return location.parent, location
                    
        return None, None
        
    def create_deployment_package(self, output_dir: Path, include_installer=True):
        """Create a deployment package."""
        build_dir, exe_path = self.find_built_application()
        
        if not build_dir or not exe_path:
            print("✗ No built application found!")
            print("Please run the build script first.")
            return False
            
        print(f"✓ Found built application: {exe_path}")
        
        # Create output directory
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if build_dir.is_dir():
            # Copy entire directory
            target_dir = output_dir / f"{self.app_name.replace(' ', '_')}_v{self.app_version}_{timestamp}"
            shutil.copytree(build_dir, target_dir)
            print(f"✓ Copied application to: {target_dir}")
            
            # Create zip file
            zip_file = output_dir / f"{self.app_name.replace(' ', '_')}_v{self.app_version}_{timestamp}.zip"
            self.create_zip_archive(build_dir, zip_file)
            print(f"✓ Created zip archive: {zip_file}")
            
        else:
            # Single file
            target_file = output_dir / f"{self.app_name.replace(' ', '_')}_v{self.app_version}_{timestamp}.exe"
            shutil.copy2(build_dir, target_file)
            print(f"✓ Copied executable to: {target_file}")
            
        # Include installer if requested
        if include_installer:
            installer_dir = self.project_root / "installer"
            if installer_dir.exists():
                installer_files = list(installer_dir.glob("*.exe"))
                for installer_file in installer_files:
                    target_installer = output_dir / installer_file.name
                    shutil.copy2(installer_file, target_installer)
                    print(f"✓ Copied installer: {target_installer}")
                    
        return True
        
    def create_zip_archive(self, source_dir: Path, zip_file: Path):
        """Create a zip archive of the application."""
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(source_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_name = file_path.relative_to(source_dir)
                    zipf.write(file_path, arc_name)
                    
    def deploy_to_usb(self, usb_drive: str):
        """Deploy to USB drive."""
        usb_path = Path(usb_drive)
        
        if not usb_path.exists():
            print(f"✗ USB drive not found: {usb_drive}")
            return False
            
        print(f"Deploying to USB drive: {usb_path}")
        
        # Create deployment package
        deploy_dir = usb_path / f"{self.app_name.replace(' ', '_')}_Deployment"
        return self.create_deployment_package(deploy_dir)
        
    def deploy_to_network(self, network_path: str):
        """Deploy to network location."""
        network_dir = Path(network_path)
        
        if not network_dir.exists():
            print(f"✗ Network path not found: {network_path}")
            return False
            
        print(f"Deploying to network: {network_dir}")
        
        # Create deployment package
        deploy_dir = network_dir / f"{self.app_name.replace(' ', '_')}_Deployment"
        return self.create_deployment_package(deploy_dir)
        
    def create_self_extracting_package(self, output_dir: Path):
        """Create a self-extracting package."""
        build_dir, exe_path = self.find_built_application()
        
        if not build_dir or not exe_path:
            print("✗ No built application found!")
            return False
            
        # Create a simple batch file that extracts and runs
        batch_content = f"""@echo off
echo ========================================
echo {self.app_name} v{self.app_version}
echo ========================================
echo.

REM Check if already extracted
if exist "app\\{self.app_name.replace(' ', '_')}.exe" (
    echo Application already extracted.
    goto run
)

echo Extracting application...
mkdir app 2>nul

REM Copy files (simplified - in real scenario you'd use a proper archiver)
xcopy /E /I /Y "files\\*" "app\\"

:run
echo Starting {self.app_name}...
cd app
start "" "{self.app_name.replace(' ', '_')}.exe"
cd ..

echo.
echo {self.app_name} started successfully!
pause
"""
        
        # Create deployment structure
        deploy_dir = output_dir / f"{self.app_name.replace(' ', '_')}_SelfExtracting"
        deploy_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy application files
        app_dir = deploy_dir / "files"
        if build_dir.is_dir():
            shutil.copytree(build_dir, app_dir, dirs_exist_ok=True)
        else:
            app_dir.mkdir(exist_ok=True)
            shutil.copy2(build_dir, app_dir)
            
        # Create batch file
        batch_file = deploy_dir / f"Run_{self.app_name.replace(' ', '_')}.bat"
        with open(batch_file, 'w', encoding='utf-8') as f:
            f.write(batch_content)
            
        print(f"✓ Created self-extracting package: {deploy_dir}")
        print(f"✓ Run script: {batch_file}")
        
        return True
        
    def create_readme(self, output_dir: Path):
        """Create a README file for deployment."""
        readme_content = f"""# {self.app_name} v{self.app_version} - Deployment Package

## Quick Start

### For End Users:
1. **Extract** this folder to any location
2. **Run** `{self.app_name.replace(' ', '_')}.exe`
3. The application will create its database automatically

### For Administrators:
- Copy the entire folder to the target computer
- Create shortcuts to the executable as needed
- The application is portable and doesn't require installation

## System Requirements
- Windows 10 or later
- 4GB RAM minimum
- 500MB free disk space
- No Python installation required

## Features
- Complete Point of Sale system
- Product management
- Sales tracking
- Reports generation
- Multi-language support (English/Arabic)
- User authentication
- Shift management

## Support
For technical support, contact the development team.

## License
This software is provided under the MIT License.

---
Generated on: {datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")}
"""
        
        readme_file = output_dir / "README.txt"
        with open(readme_file, 'w', encoding='utf-8') as f:
            f.write(readme_content)
            
        print(f"✓ Created README: {readme_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Deploy Talinda POS application")
    parser.add_argument("--output", "-o", default="./deployment", 
                       help="Output directory for deployment package")
    parser.add_argument("--usb", "-u", help="USB drive letter (e.g., E:)")
    parser.add_argument("--network", "-n", help="Network path")
    parser.add_argument("--self-extracting", "-s", action="store_true",
                       help="Create self-extracting package")
    parser.add_argument("--no-installer", action="store_true",
                       help="Don't include installer in deployment")
    
    args = parser.parse_args()
    
    deployer = Deployer()
    
    if args.usb:
        success = deployer.deploy_to_usb(args.usb)
    elif args.network:
        success = deployer.deploy_to_network(args.network)
    elif args.self_extracting:
        output_dir = Path(args.output)
        success = deployer.create_self_extracting_package(output_dir)
    else:
        output_dir = Path(args.output)
        success = deployer.create_deployment_package(output_dir, not args.no_installer)
        
    if success:
        # Create README
        output_dir = Path(args.output)
        deployer.create_readme(output_dir)
        
        print("\n" + "=" * 50)
        print("Deployment completed successfully!")
        print("=" * 50)
    else:
        print("\nDeployment failed!")
        sys.exit(1)


if __name__ == "__main__":
    main() 