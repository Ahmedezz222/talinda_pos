#!/usr/bin/env python3
"""
Test script for Excel report generation functionality.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_excel_report_generation():
    """Test the Excel report generation functionality."""
    try:
        from utils.excel_report_generator import ExcelReportGenerator
        from database.db_config import get_fresh_session
        from models.user import Shift, ShiftStatus, User
        from models.sale import Sale
        from models.product import Product, Category
        from datetime import datetime, timedelta
        
        print("Testing Excel Report Generation...")
        
        # Create a test session
        session = get_fresh_session()
        
        # Check if we have any shifts in the database
        shifts = session.query(Shift).filter_by(status=ShiftStatus.CLOSED).limit(5).all()
        
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
        
        # Test report generation
        report_generator = ExcelReportGenerator()
        
        for shift in shifts:
            print(f"Generating report for shift {shift.id}...")
            
            # Generate the report
            filepath = report_generator.generate_shift_report(shift, shift.closing_amount or 1000.0)
            
            if filepath:
                print(f"✅ Report generated successfully: {filepath}")
                
                # Check if file exists
                if os.path.exists(filepath):
                    print(f"✅ File exists and is accessible")
                    
                    # Try to open the file
                    if report_generator.open_excel_file(filepath):
                        print(f"✅ Excel file opened successfully")
                    else:
                        print(f"⚠️  File generated but could not open automatically")
                else:
                    print(f"❌ File was not created")
                    return False
            else:
                print(f"❌ Failed to generate report for shift {shift.id}")
                return False
        
        print("\n🎉 All tests passed! Excel report generation is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install openpyxl: pip install openpyxl")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

if __name__ == "__main__":
    success = test_excel_report_generation()
    sys.exit(0 if success else 1) 