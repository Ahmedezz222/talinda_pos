#!/usr/bin/env python3
"""
Test to verify that the import issues are completely resolved.
"""

import sys
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_imports():
    """Test that all imports work correctly."""
    try:
        print("Testing imports...")
        
        # Test basic imports
        from utils.excel_report_generator import ExcelReportGenerator
        print("✅ ExcelReportGenerator imported successfully")
        
        # Test openpyxl availability
        try:
            import openpyxl
            print("✅ openpyxl imported successfully")
        except ImportError:
            print("❌ openpyxl not available")
            return False
        
        # Test Worksheet import
        try:
            from openpyxl.worksheet.worksheet import Worksheet
            print("✅ Worksheet imported successfully")
        except ImportError:
            print("❌ Worksheet import failed")
            return False
        
        # Test creating ExcelReportGenerator instance
        try:
            generator = ExcelReportGenerator()
            print("✅ ExcelReportGenerator instance created successfully")
        except Exception as e:
            print(f"❌ Failed to create ExcelReportGenerator instance: {e}")
            return False
        
        print("\n🎉 All import tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1) 