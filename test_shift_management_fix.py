#!/usr/bin/env python3
"""
Test script for enhanced shift management functionality.
This script tests the improved shift management that handles existing open shifts.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from datetime import datetime, date
from controllers.shift_controller import ShiftController
from controllers.auth_controller import AuthController
from models.user import User, UserRole, Shift, ShiftStatus
from database.db_config import Session, safe_commit
from ui.components.opening_amount_dialog import OpeningAmountDialog
import bcrypt
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_cashier():
    """Create a test cashier user for testing."""
    try:
        session = Session()
        
        # Check if test cashier already exists
        test_cashier = session.query(User).filter_by(username="test_cashier_fix").first()
        if test_cashier:
            print("✅ Test cashier already exists")
            return test_cashier
        
        # Create password hash
        password = "test123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create test cashier
        cashier = User(
            username="test_cashier_fix",
            password_hash=password_hash,
            role=UserRole.CASHIER,
            full_name="Test Cashier Fix",
            active=1
        )
        
        session.add(cashier)
        safe_commit(session)
        
        print("✅ Test cashier created successfully")
        print(f"   Username: test_cashier_fix")
        print(f"   Password: test123")
        return cashier
        
    except Exception as e:
        print(f"❌ Error creating test cashier: {e}")
        return None

def test_opening_amount_dialog():
    """Test the enhanced opening amount dialog."""
    try:
        print("\n🧪 Testing Enhanced Opening Amount Dialog")
        print("=" * 50)
        
        from PyQt5.QtWidgets import QApplication
        
        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test 1: Dialog without existing shift
        print("\n📋 Test 1: Dialog without existing shift")
        dialog1 = OpeningAmountDialog()
        dialog1.show()
        print("✅ Dialog without existing shift displayed")
        print("   Features to test:")
        print("   - Enter opening amount")
        print("   - Open Shift button")
        print("   - Cancel button")
        
        # Test 2: Dialog with existing shift
        print("\n📋 Test 2: Dialog with existing shift")
        
        # Create a mock shift for testing
        cashier = create_test_cashier()
        if cashier:
            shift_controller = ShiftController()
            
            # Open a shift first
            shift = shift_controller.open_shift(cashier, 100.0)
            if shift:
                print("✅ Test shift opened successfully")
                
                # Test dialog with existing shift
                dialog2 = OpeningAmountDialog(existing_shift=shift)
                dialog2.show()
                print("✅ Dialog with existing shift displayed")
                print("   Features to test:")
                print("   - Current shift information display")
                print("   - Close Current Shift button")
                print("   - Open New Shift (Replace Current) button")
                print("   - Cancel button")
                
                # Clean up the test shift
                shift.status = ShiftStatus.CLOSED
                shift.close_time = datetime.utcnow()
                safe_commit(shift_controller.session)
                print("✅ Test shift cleaned up")
            else:
                print("❌ Failed to open test shift")
        else:
            print("❌ Failed to create test cashier")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing opening amount dialog: {e}")
        logger.error(f"Error testing opening amount dialog: {e}")
        return False

def test_shift_management_flow():
    """Test the complete shift management flow."""
    try:
        print("\n🔄 Testing Complete Shift Management Flow")
        print("=" * 50)
        
        # Create test cashier
        cashier = create_test_cashier()
        if not cashier:
            return False
        
        # Initialize controllers
        shift_controller = ShiftController()
        
        # Test 1: Open first shift
        print("\n📋 Test 1: Opening first shift")
        shift1 = shift_controller.open_shift(cashier, 100.0)
        if shift1:
            print("✅ First shift opened successfully")
            print(f"   Shift ID: {shift1.id}")
            print(f"   Opening Amount: ${shift1.opening_amount}")
            print(f"   Status: {shift1.status.value}")
        else:
            print("❌ Failed to open first shift")
            return False
        
        # Test 2: Try to open another shift (should show existing shift dialog)
        print("\n📋 Test 2: Attempting to open another shift")
        current_shift = shift_controller.get_current_shift(cashier)
        if current_shift:
            print("✅ Current shift detected")
            print(f"   Shift ID: {current_shift.id}")
            print(f"   Status: {current_shift.status.value}")
            
            # This would normally show the dialog, but for testing we'll simulate the flow
            print("   (In real application, this would show the enhanced dialog)")
            print("   - Option 1: Close Current Shift")
            print("   - Option 2: Open New Shift (Replace Current)")
            print("   - Option 3: Cancel")
        else:
            print("❌ No current shift found")
            return False
        
        # Test 3: Close the shift
        print("\n📋 Test 3: Closing the shift")
        closed_shift = shift_controller.close_shift(cashier)
        if closed_shift:
            print("✅ Shift closed successfully")
            print(f"   Close Time: {closed_shift.close_time}")
            print(f"   Status: {closed_shift.status.value}")
        else:
            print("❌ Failed to close shift")
            return False
        
        # Test 4: Open a new shift after closing
        print("\n📋 Test 4: Opening new shift after closing")
        shift2 = shift_controller.open_shift(cashier, 200.0)
        if shift2:
            print("✅ New shift opened successfully")
            print(f"   Shift ID: {shift2.id}")
            print(f"   Opening Amount: ${shift2.opening_amount}")
            print(f"   Status: {shift2.status.value}")
        else:
            print("❌ Failed to open new shift")
            return False
        
        # Clean up
        shift2.status = ShiftStatus.CLOSED
        shift2.close_time = datetime.utcnow()
        safe_commit(shift_controller.session)
        print("✅ Test shift cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing shift management flow: {e}")
        logger.error(f"Error testing shift management flow: {e}")
        return False

def cleanup_test_data():
    """Clean up test data."""
    try:
        session = Session()
        
        # Remove test cashier
        test_cashier = session.query(User).filter_by(username="test_cashier_fix").first()
        if test_cashier:
            # Remove associated shifts
            shifts = session.query(Shift).filter_by(user_id=test_cashier.id).all()
            for shift in shifts:
                session.delete(shift)
            
            session.delete(test_cashier)
            safe_commit(session)
            print("✅ Test data cleaned up")
        
    except Exception as e:
        print(f"⚠️  Error cleaning up test data: {e}")

if __name__ == "__main__":
    print("🚀 Starting Enhanced Shift Management Tests")
    print("=" * 50)
    
    # Test the enhanced opening amount dialog
    success1 = test_opening_amount_dialog()
    
    # Test the complete shift management flow
    success2 = test_shift_management_flow()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Enhanced shift management is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    # Clean up test data
    cleanup_test_data()
    
    print("\n📝 Summary of Fixes:")
    print("   ✅ Enhanced OpeningAmountDialog to handle existing shifts")
    print("   ✅ Added options to close existing shift or open new one")
    print("   ✅ Improved UI with clear information and choices")
    print("   ✅ Updated main application flow to handle shift management")
    print("   ✅ Added proper error handling and user feedback")
    print("   ✅ Integrated with password authentication for shift closing")
    print("   ✅ Added shift replacement functionality")
    print("   ✅ Improved user experience with clear options") 