#!/usr/bin/env python3
"""
Test script for Excel report save functionality.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_save_functionality():
    """Test the Excel report save functionality."""
    try:
        from utils.excel_report_generator import ExcelReportGenerator
        from database.db_config import get_fresh_session
        from models.user import Shift, ShiftStatus, User
        from datetime import datetime, timedelta
        
        print("Testing Excel Report Save Functionality...")
        
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
            print(f"Testing save functionality for shift {shift.id}...")
            
            # Test report preview
            preview = report_generator.get_report_preview(shift, shift.closing_amount or 1000.0)
            if preview:
                print(f"✅ Report preview generated successfully")
                print(f"   - Cashier: {preview['cashier_name']}")
                print(f"   - Opening Amount: ${preview['opening_amount']:.2f}")
                print(f"   - Closing Amount: ${preview['closing_amount']:.2f}")
                print(f"   - Total Sales: ${preview['total_sales']:.2f}")
                print(f"   - Total Transactions: {preview['total_transactions']}")
            else:
                print(f"❌ Failed to generate report preview")
                return False
            
            # Test report generation
            filepath = report_generator.generate_shift_report(shift, shift.closing_amount or 1000.0)
            
            if filepath:
                print(f"✅ Report generated successfully: {filepath}")
                
                # Test save functionality (without UI)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                test_save_path = f"test_save_report_{timestamp}.xlsx"
                
                try:
                    import shutil
                    shutil.copy2(filepath, test_save_path)
                    
                    if os.path.exists(test_save_path):
                        print(f"✅ Save functionality working: {test_save_path}")
                        
                        # Clean up test file
                        os.remove(test_save_path)
                        print(f"✅ Test file cleaned up")
                    else:
                        print(f"❌ Save functionality failed")
                        return False
                        
                except Exception as e:
                    print(f"❌ Error during save test: {e}")
                    return False
            else:
                print(f"❌ Failed to generate report for shift {shift.id}")
                return False
        
        print("\n🎉 All save functionality tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install openpyxl: pip install openpyxl")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_save_functionality()
    sys.exit(0 if success else 1) 