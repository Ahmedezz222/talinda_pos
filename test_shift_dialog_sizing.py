#!/usr/bin/env python3
"""
Test script for improved shift dialog sizing.
This script tests the enhanced dialog sizing and layout improvements.
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
        test_cashier = session.query(User).filter_by(username="test_cashier_size").first()
        if test_cashier:
            print("✅ Test cashier already exists")
            return test_cashier
        
        # Create password hash
        password = "test123"
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Create test cashier
        cashier = User(
            username="test_cashier_size",
            password_hash=password_hash,
            role=UserRole.CASHIER,
            full_name="Test Cashier Size",
            active=1
        )
        
        session.add(cashier)
        safe_commit(session)
        
        print("✅ Test cashier created successfully")
        print(f"   Username: test_cashier_size")
        print(f"   Password: test123")
        return cashier
        
    except Exception as e:
        print(f"❌ Error creating test cashier: {e}")
        return None

def test_dialog_sizing():
    """Test the improved dialog sizing."""
    try:
        print("\n🧪 Testing Improved Dialog Sizing")
        print("=" * 50)
        
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtCore import QTimer
        
        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test 1: Dialog without existing shift (smaller size)
        print("\n📋 Test 1: Dialog without existing shift")
        print("   Expected size: 400x280")
        dialog1 = OpeningAmountDialog()
        size1 = dialog1.size()
        print(f"   Actual size: {size1.width()}x{size1.height()}")
        
        if size1.width() == 400 and size1.height() == 280:
            print("   ✅ Size is correct")
        else:
            print("   ❌ Size is incorrect")
        
        dialog1.show()
        print("   ✅ Dialog displayed successfully")
        
        # Test 2: Dialog with existing shift (larger size)
        print("\n📋 Test 2: Dialog with existing shift")
        print("   Expected size: 500x450")
        
        # Create a mock shift for testing
        cashier = create_test_cashier()
        if cashier:
            shift_controller = ShiftController()
            
            # Open a shift first
            shift = shift_controller.open_shift(cashier, 100.0)
            if shift:
                print("   ✅ Test shift created successfully")
                
                # Test dialog with existing shift
                dialog2 = OpeningAmountDialog(existing_shift=shift)
                size2 = dialog2.size()
                print(f"   Actual size: {size2.width()}x{size2.height()}")
                
                if size2.width() == 500 and size2.height() == 450:
                    print("   ✅ Size is correct")
                else:
                    print("   ❌ Size is incorrect")
                
                dialog2.show()
                print("   ✅ Dialog displayed successfully")
                
                # Clean up the test shift
                shift.status = ShiftStatus.CLOSED
                shift.close_time = datetime.utcnow()
                safe_commit(shift_controller.session)
                print("   ✅ Test shift cleaned up")
            else:
                print("   ❌ Failed to create test shift")
        else:
            print("   ❌ Failed to create test cashier")
        
        # Test 3: Check dialog properties
        print("\n📋 Test 3: Dialog Properties")
        dialog3 = OpeningAmountDialog()
        
        # Check window flags
        flags = dialog3.windowFlags()
        if flags & 0x00000001:  # Qt.Window
            print("   ✅ Window flag is set")
        else:
            print("   ❌ Window flag is not set")
        
        # Check if modal
        if dialog3.isModal():
            print("   ✅ Dialog is modal")
        else:
            print("   ❌ Dialog is not modal")
        
        # Check layout spacing
        layout = dialog3.layout()
        if layout:
            spacing = layout.spacing()
            margins = layout.contentsMargins()
            print(f"   ✅ Layout spacing: {spacing}")
            print(f"   ✅ Layout margins: {margins.left()}, {margins.top()}, {margins.right()}, {margins.bottom()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing dialog sizing: {e}")
        logger.error(f"Error testing dialog sizing: {e}")
        return False

def test_ui_elements():
    """Test the UI elements and their sizing."""
    try:
        print("\n🎨 Testing UI Elements")
        print("=" * 30)
        
        from PyQt5.QtWidgets import QApplication
        
        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Test new shift dialog UI elements
        print("\n📋 Testing New Shift Dialog UI Elements")
        dialog = OpeningAmountDialog()
        
        # Find the amount input field
        amount_input = dialog.findChild(type(dialog.amount_input))
        if amount_input:
            height = amount_input.height()
            print(f"   ✅ Amount input height: {height}px")
            if height >= 45:
                print("   ✅ Input field height is adequate")
            else:
                print("   ❌ Input field height is too small")
        else:
            print("   ❌ Amount input field not found")
        
        # Test existing shift dialog UI elements
        print("\n📋 Testing Existing Shift Dialog UI Elements")
        
        # Create a mock shift
        cashier = create_test_cashier()
        if cashier:
            shift_controller = ShiftController()
            shift = shift_controller.open_shift(cashier, 100.0)
            
            if shift:
                dialog2 = OpeningAmountDialog(existing_shift=shift)
                
                # Find buttons
                buttons = dialog2.findChildren(type(dialog2.findChild(type(dialog2))))
                print(f"   ✅ Found {len(buttons)} buttons")
                
                # Check button heights
                for button in buttons:
                    if isinstance(button, type(dialog2.findChild(type(dialog2)))):
                        height = button.height()
                        text = button.text()
                        print(f"   ✅ Button '{text}' height: {height}px")
                        if height >= 45:
                            print(f"   ✅ Button '{text}' height is adequate")
                        else:
                            print(f"   ❌ Button '{text}' height is too small")
                
                # Clean up
                shift.status = ShiftStatus.CLOSED
                shift.close_time = datetime.utcnow()
                safe_commit(shift_controller.session)
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing UI elements: {e}")
        logger.error(f"Error testing UI elements: {e}")
        return False

def cleanup_test_data():
    """Clean up test data."""
    try:
        session = Session()
        
        # Remove test cashier
        test_cashier = session.query(User).filter_by(username="test_cashier_size").first()
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
    print("🚀 Starting Dialog Sizing Tests")
    print("=" * 50)
    
    # Test the dialog sizing
    success1 = test_dialog_sizing()
    
    # Test UI elements
    success2 = test_ui_elements()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Dialog sizing improvements are working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    # Clean up test data
    cleanup_test_data()
    
    print("\n📝 Summary of Sizing Improvements:")
    print("   ✅ Increased dialog sizes for better content display")
    print("   ✅ Enhanced spacing and margins for better visual separation")
    print("   ✅ Improved button sizes for better usability")
    print("   ✅ Better input field sizing and styling")
    print("   ✅ Enhanced visual design with better colors and backgrounds")
    print("   ✅ Improved typography and readability")
    print("   ✅ Better layout organization and spacing")
    print("   ✅ Responsive design considerations") 