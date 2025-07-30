#!/usr/bin/env python3
"""
Verification script for Talinda POS setup.
This script checks that everything is properly configured.
"""

import sys
import os
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def check_python_version():
    """Check Python version."""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires 3.8+")
        return False

def check_dependencies():
    """Check if required dependencies are installed."""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'PyQt5', 'sqlalchemy', 'bcrypt', 'reportlab', 
        'openpyxl', 'qrcode', 'PIL'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - Missing")
            all_ok = False
    
    return all_ok

def check_database():
    """Check if database exists and is accessible."""
    print("\n🗄️  Checking database...")
    
    db_path = current_dir / "pos_database.db"
    if not db_path.exists():
        print("❌ Database file not found")
        return False
    
    try:
        from database.db_config import Session
        from models.user import User
        from models.product import Category
        
        session = Session()
        
        # Check users
        users = session.query(User).all()
        print(f"✅ Database accessible - {len(users)} users found")
        
        # Check categories
        categories = session.query(Category).all()
        print(f"✅ Categories found - {len(categories)} categories")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def check_directories():
    """Check if required directories exist."""
    print("\n📁 Checking directories...")
    
    required_dirs = [
        current_dir / "logs",
        current_dir / "reports", 
        current_dir / "backups",
        src_dir / "logs",
        src_dir / "reports"
    ]
    
    all_ok = True
    for directory in required_dirs:
        if directory.exists():
            print(f"✅ {directory.name} - OK")
        else:
            print(f"❌ {directory.name} - Missing")
            all_ok = False
    
    return all_ok

def check_users():
    """Check if default users exist."""
    print("\n👥 Checking users...")
    
    try:
        from database.db_config import Session
        from models.user import User, UserRole
        
        session = Session()
        
        # Check admin user
        admin = session.query(User).filter_by(username='admin').first()
        if admin and admin.role == UserRole.ADMIN:
            print("✅ Admin user - OK")
        else:
            print("❌ Admin user - Missing or incorrect role")
            return False
        
        # Check cashier user
        cashier = session.query(User).filter_by(username='cashier').first()
        if cashier and cashier.role == UserRole.CASHIER:
            print("✅ Cashier user - OK")
        else:
            print("❌ Cashier user - Missing or incorrect role")
            return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ User check error: {e}")
        return False

def check_categories():
    """Check if default categories exist."""
    print("\n🏷️  Checking categories...")
    
    try:
        from database.db_config import Session
        from models.product import Category
        
        session = Session()
        
        expected_categories = ["Food", "Beverage", "Dessert", "Other"]
        categories = session.query(Category).all()
        
        if len(categories) >= 4:
            print(f"✅ Categories found - {len(categories)} categories")
            for cat in categories:
                print(f"   • {cat.name} (Tax: {cat.tax_rate}%)")
        else:
            print(f"❌ Categories - Expected 4+, found {len(categories)}")
            return False
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Category check error: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 50)
    print("           TALINDA POS - SETUP VERIFICATION")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Database", check_database),
        ("Directories", check_directories),
        ("Users", check_users),
        ("Categories", check_categories)
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ {check_name} - Error: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("                    SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{check_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n🎉 All checks passed! The application is ready to run.")
        print("Run: python src/main.py")
        return 0
    else:
        print(f"\n⚠️  {total - passed} check(s) failed. Please review the setup.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 