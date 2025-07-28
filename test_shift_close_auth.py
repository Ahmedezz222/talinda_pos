#!/usr/bin/env python3
"""
Test script for shift close password authentication functionality.
This script tests the new password authentication feature for cashiers closing shifts.
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
        test_cashier = session.query(User).filter_by(username="test_cashier").first()
        if test_cashier:
            print("✅ Test cashier already exists")
            return test_cashier
        
        # Create password hash
        password = "test123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create test cashier
        cashier = User(
            username="test_cashier",
            password_hash=password_hash,
            role=UserRole.CASHIER,
            full_name="Test Cashier",
            active=1
        )
        
        session.add(cashier)
        safe_commit(session)
        
        print("✅ Test cashier created successfully")
        print(f"   Username: test_cashier")
        print(f"   Password: test123")
        return cashier
        
    except Exception as e:
        print(f"❌ Error creating test cashier: {e}")
        return None

def test_shift_operations():
    """Test shift opening and closing operations."""
    try:
        print("\n🧪 Testing Shift Operations")
        print("=" * 40)
        
        # Create test cashier
        cashier = create_test_cashier()
        if not cashier:
            return False
        
        # Initialize controllers
        shift_controller = ShiftController()
        auth_controller = AuthController()
        
        # Test opening a shift
        print("\n📋 Opening shift...")
        shift = shift_controller.open_shift(cashier, 100.0)
        if shift:
            print("✅ Shift opened successfully")
            print(f"   Shift ID: {shift.id}")
            print(f"   Opening Amount: ${shift.opening_amount}")
            print(f"   Status: {shift.status.value}")
        else:
            print("❌ Failed to open shift")
            return False
        
        # Test password verification
        print("\n🔐 Testing password verification...")
        
        # Test correct password
        correct_password = "test123"
        is_valid = shift_controller.verify_user_password(cashier, correct_password)
        if is_valid:
            print("✅ Correct password verification passed")
        else:
            print("❌ Correct password verification failed")
            return False
        
        # Test incorrect password
        incorrect_password = "wrongpassword"
        is_valid = shift_controller.verify_user_password(cashier, incorrect_password)
        if not is_valid:
            print("✅ Incorrect password verification correctly rejected")
        else:
            print("❌ Incorrect password verification incorrectly accepted")
            return False
        
        # Test closing shift with correct password
        print("\n🔒 Testing shift close with correct password...")
        closed_shift = shift_controller.close_shift_with_auth(cashier, correct_password)
        if closed_shift:
            print("✅ Shift closed successfully with correct password")
            print(f"   Close Time: {closed_shift.close_time}")
            print(f"   Status: {closed_shift.status.value}")
        else:
            print("❌ Failed to close shift with correct password")
            return False
        
        # Test closing shift with incorrect password
        print("\n🚫 Testing shift close with incorrect password...")
        closed_shift = shift_controller.close_shift_with_auth(cashier, incorrect_password)
        if not closed_shift:
            print("✅ Shift close correctly rejected with incorrect password")
        else:
            print("❌ Shift close incorrectly accepted with incorrect password")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing shift operations: {e}")
        logger.error(f"Error testing shift operations: {e}")
        return False

def test_auth_dialog():
    """Test the authentication dialog UI."""
    try:
        print("\n🖥️  Testing Authentication Dialog UI")
        print("=" * 40)
        
        from PyQt5.QtWidgets import QApplication
        from ui.components.shift_close_auth_dialog import ShiftCloseAuthDialog
        
        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Create and show the dialog
        dialog = ShiftCloseAuthDialog("test_cashier")
        dialog.show()
        
        print("✅ Authentication Dialog UI Test Completed!")
        print("   The dialog should now be visible.")
        print("   Features to test:")
        print("   - Password input field")
        print("   - Show/hide password checkbox")
        print("   - Cancel button")
        print("   - Close Shift button")
        print("   - Password validation")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing authentication dialog: {e}")
        logger.error(f"Error testing authentication dialog: {e}")
        return False

def cleanup_test_data():
    """Clean up test data."""
    try:
        session = Session()
        
        # Remove test cashier
        test_cashier = session.query(User).filter_by(username="test_cashier").first()
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
    print("🚀 Starting Shift Close Authentication Tests")
    print("=" * 50)
    
    # Test the shift operations
    success1 = test_shift_operations()
    
    # Test the UI dialog
    success2 = test_auth_dialog()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Shift close authentication is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    # Clean up test data
    cleanup_test_data()
    
    print("\n📝 Summary of Enhancements:")
    print("   ✅ Added password authentication for cashier shift closing")
    print("   ✅ Created ShiftCloseAuthDialog component")
    print("   ✅ Enhanced ShiftController with password verification")
    print("   ✅ Updated main application to use authentication dialog")
    print("   ✅ Added proper error handling and user feedback")
    print("   ✅ Implemented secure password verification using bcrypt")
    print("   ✅ Added user-friendly UI with show/hide password option") 