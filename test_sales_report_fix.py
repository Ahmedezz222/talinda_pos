#!/usr/bin/env python3
"""
Comprehensive test for sales report saving functionality.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_sales_report_saving():
    """Test the complete sales report saving functionality."""
    try:
        from utils.excel_report_generator import ExcelReportGenerator
        from database.db_config import get_fresh_session
        from models.user import Shift, ShiftStatus, User
        from models.sale import Sale, sale_products
        from models.product import Product, Category
        from datetime import datetime, timedelta
        import shutil
        
        print("Testing Sales Report Saving Functionality...")
        
        # Create a test session
        session = get_fresh_session()
        
        # Check if we have any shifts in the database
        shifts = session.query(Shift).filter_by(status=ShiftStatus.CLOSED).limit(1).all()
        
        if not shifts:
            print("No closed shifts found in database. Creating test data...")
            
            # Create test data
            test_user = session.query(User).first()
            if not test_user:
                print("No users found in database. Please run the application first.")
                return False
            
            # Create a test shift
            test_shift = Shift(
                user_id=test_user.id,
                opening_amount=1000.0,
                closing_amount=1500.0,
                open_time=datetime.now() - timedelta(hours=8),
                close_time=datetime.now(),
                status=ShiftStatus.CLOSED
            )
            session.add(test_shift)
            session.commit()
            shifts = [test_shift]
        
        # Test report generator
        report_generator = ExcelReportGenerator()
        
        for shift in shifts:
            print(f"Testing sales report saving for shift {shift.id}...")
            
            # Test 1: Report generation
            print("  Testing report generation...")
            filepath = report_generator.generate_shift_report(shift, shift.closing_amount or 1000.0)
            
            if filepath:
                print(f"  ✅ Report generated successfully: {filepath}")
                
                # Test 2: File existence
                if os.path.exists(filepath):
                    print(f"  ✅ File exists and is accessible")
                    
                    # Test 3: File size
                    file_size = os.path.getsize(filepath)
                    print(f"  ✅ File size: {file_size} bytes")
                    
                    # Test 4: Save functionality (copy to test location)
                    test_save_path = f"test_save_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                    
                    try:
                        shutil.copy2(filepath, test_save_path)
                        
                        if os.path.exists(test_save_path):
                            print(f"  ✅ Save functionality working: {test_save_path}")
                            
                            # Test 5: Verify copied file
                            copied_size = os.path.getsize(test_save_path)
                            if copied_size == file_size:
                                print(f"  ✅ Copied file size matches original: {copied_size} bytes")
                            else:
                                print(f"  ⚠️  Copied file size differs: {copied_size} vs {file_size}")
                            
                            # Clean up test file
                            os.remove(test_save_path)
                            print(f"  ✅ Test file cleaned up")
                        else:
                            print(f"  ❌ Save functionality failed")
                            return False
                            
                    except Exception as e:
                        print(f"  ❌ Error during save test: {e}")
                        return False
                    
                    # Test 6: Report preview
                    print("  Testing report preview...")
                    preview = report_generator.get_report_preview(shift, shift.closing_amount or 1000.0)
                    if preview:
                        print(f"  ✅ Report preview generated successfully")
                        print(f"    - Cashier: {preview['cashier_name']}")
                        print(f"    - Opening Amount: ${preview['opening_amount']:.2f}")
                        print(f"    - Closing Amount: ${preview['closing_amount']:.2f}")
                        print(f"    - Total Sales: ${preview['total_sales']:.2f}")
                        print(f"    - Total Transactions: {preview['total_transactions']}")
                    else:
                        print(f"  ❌ Failed to generate report preview")
                        return False
                    
                else:
                    print(f"  ❌ File was not created")
                    return False
            else:
                print(f"  ❌ Failed to generate report for shift {shift.id}")
                return False
        
        print("\n🎉 All sales report saving tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install openpyxl: pip install openpyxl")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_file_permissions():
    """Test file permissions and access."""
    try:
        print("\nTesting file permissions...")
        
        # Test reports directory
        reports_dir = Path("reports")
        if reports_dir.exists():
            print(f"  ✅ Reports directory exists: {reports_dir}")
            
            # Test write permission
            test_file = reports_dir / "test_permission.txt"
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                print(f"  ✅ Write permission to reports directory")
                
                # Clean up
                test_file.unlink()
                print(f"  ✅ Test file cleaned up")
            except Exception as e:
                print(f"  ❌ Write permission test failed: {e}")
                return False
        else:
            print(f"  ⚠️  Reports directory does not exist, will be created")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing file permissions: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("SALES REPORT SAVING COMPREHENSIVE TEST")
    print("=" * 60)
    
    # Test file permissions first
    permissions_ok = test_file_permissions()
    
    if permissions_ok:
        # Test sales report saving
        success = test_sales_report_saving()
    else:
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Sales report saving is working correctly.")
    else:
        print("❌ SOME TESTS FAILED! Please check the issues above.")
    print("=" * 60)
    
    sys.exit(0 if success else 1) 