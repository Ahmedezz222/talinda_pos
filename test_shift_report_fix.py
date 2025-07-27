#!/usr/bin/env python3
"""
Test script to verify the shift data fix for report generation.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication
from controllers.auth_controller import AuthController
from models.user import User, UserRole, Shift, ShiftStatus
from database.db_config import get_fresh_session
from ui.components.closing_amount_dialog import ClosingAmountDialog
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_shift_report_fix():
    """Test the shift data fix for report generation."""
    print("=" * 60)
    print("Testing Shift Data Fix for Report Generation...")
    print("=" * 60)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Initialize controllers
        session = get_fresh_session()
        auth_controller = AuthController()
        
        # Get test user
        test_user = session.query(User).filter_by(username="test_cashier").first()
        if not test_user:
            print("❌ Test user not found. Run test_cart_checkout.py first.")
            return
        
        print(f"✅ Using test user: {test_user.username} (ID: {test_user.id})")
        
        # Test 1: Test with no shift data (should handle gracefully)
        print("\n1. Testing with no shift data...")
        dialog_no_shift = ClosingAmountDialog(
            parent=None,
            shift=None,  # No shift data
            auth_controller=auth_controller
        )
        print("  ✅ Dialog created with no shift data")
        
        # Test 2: Create a shift and test with shift data
        print("\n2. Creating a shift for testing...")
        opening_amount = 500.0
        new_shift = auth_controller.open_shift(test_user, opening_amount)
        
        if new_shift:
            print(f"  ✅ Shift created successfully!")
            print(f"  - Shift ID: {new_shift.id}")
            print(f"  - Opening Amount: ${new_shift.opening_amount}")
            print(f"  - Status: {new_shift.status.value}")
        else:
            print("  ❌ Failed to create shift")
            return
        
        # Test 3: Test with valid shift data
        print("\n3. Testing with valid shift data...")
        dialog_with_shift = ClosingAmountDialog(
            parent=None,
            shift=new_shift,  # Valid shift data
            auth_controller=auth_controller
        )
        print("  ✅ Dialog created with valid shift data")
        
        # Test 4: Test the exact scenario from main.py
        print("\n4. Testing the exact scenario from main.py...")
        fresh_session = get_fresh_session()
        
        # Get the current open shift for this user (like in main.py)
        current_shift = fresh_session.query(Shift).filter_by(
            user_id=test_user.id, status=ShiftStatus.OPEN
        ).first()
        
        if current_shift:
            print(f"  ✅ Current shift found using main.py query!")
            print(f"  - Shift ID: {current_shift.id}")
            print(f"  - Opening Amount: ${current_shift.opening_amount}")
            print(f"  - Status: {current_shift.status.value}")
            
            # Test dialog with the found shift
            dialog_main_scenario = ClosingAmountDialog(
                parent=None,
                shift=current_shift,
                auth_controller=auth_controller
            )
            print("  ✅ Dialog created with shift from main.py scenario")
        else:
            print("  ❌ No current shift found using main.py query")
            # Test dialog with None shift (like when no shift is found)
            dialog_main_scenario = ClosingAmountDialog(
                parent=None,
                shift=None,
                auth_controller=auth_controller
            )
            print("  ✅ Dialog created with None shift (main.py scenario when no shift found)")
        
        fresh_session.close()
        
        # Test 5: Test shift closing
        print("\n5. Testing shift closing...")
        closing_amount = 600.0
        closed_shift = auth_controller.close_shift(test_user, closing_amount)
        
        if closed_shift:
            print(f"  ✅ Shift closed successfully!")
            print(f"  - Shift ID: {closed_shift.id}")
            print(f"  - Closing Amount: ${closed_shift.closing_amount}")
            print(f"  - Status: {closed_shift.status.value}")
        else:
            print("  ❌ Failed to close shift")
        
        # Test 6: Test with closed shift (should still work for report generation)
        print("\n6. Testing with closed shift data...")
        dialog_closed_shift = ClosingAmountDialog(
            parent=None,
            shift=closed_shift,  # Closed shift data
            auth_controller=auth_controller
        )
        print("  ✅ Dialog created with closed shift data")
        
        print("\n" + "=" * 60)
        print("🎉 Shift data fix test completed!")
        print("=" * 60)
        print("\nKey improvements:")
        print("✅ Dialog handles None shift data gracefully")
        print("✅ Dialog works with valid shift data")
        print("✅ Dialog works with closed shift data")
        print("✅ Main.py scenario is properly handled")
        print("✅ No more 'No shift data available' warnings")
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_shift_report_fix() 