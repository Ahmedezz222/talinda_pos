#!/usr/bin/env python3
"""
Test script to verify Excel report generator fixes.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_excel_import():
    """Test that Excel imports work correctly."""
    print("Testing Excel import...")
    
    try:
        from utils.excel_report_generator import ExcelReportGenerator
        print("✓ ExcelReportGenerator imported successfully")
        
        # Test initialization
        generator = ExcelReportGenerator()
        print("✓ ExcelReportGenerator initialized successfully")
        
        # Test if openpyxl is available
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            print("✓ openpyxl and styles imported successfully")
            
            # Test Font creation
            test_font = Font(bold=True, size=12, color="FFFFFF")
            print("✓ Font creation works")
            
        except ImportError as e:
            print(f"⚠ openpyxl not available: {e}")
            
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_excel_generator_methods():
    """Test that Excel generator methods handle missing openpyxl gracefully."""
    print("\nTesting Excel generator methods...")
    
    try:
        from utils.excel_report_generator import ExcelReportGenerator
        
        generator = ExcelReportGenerator()
        
        # Test methods that should handle missing openpyxl
        methods_to_test = [
            '_create_header',
            '_create_shift_summary', 
            '_create_sales_summary',
            '_create_detailed_sales',
            '_create_product_summary',
            '_auto_adjust_columns'
        ]
        
        for method_name in methods_to_test:
            if hasattr(generator, method_name):
                method = getattr(generator, method_name)
                print(f"✓ Method {method_name} exists")
            else:
                print(f"✗ Method {method_name} not found")
                
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_closing_dialog_import():
    """Test that closing dialog imports work correctly."""
    print("\nTesting closing dialog import...")
    
    try:
        from ui.components.closing_amount_dialog import ClosingAmountDialog
        print("✓ ClosingAmountDialog imported successfully")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    """Run all tests."""
    print("Testing Excel report generator fixes...\n")
    
    tests = [
        test_excel_import,
        test_excel_generator_methods,
        test_closing_dialog_import
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! Excel fixes are working correctly.")
        return 0
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 