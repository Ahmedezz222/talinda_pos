#!/usr/bin/env python3
"""
Test script to verify shift data creation and retrieval.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from controllers.auth_controller import AuthController
from models.user import User, UserRole, Shift, ShiftStatus
from database.db_config import get_fresh_session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_shift_data():
    """Test shift data creation and retrieval."""
    print("=" * 60)
    print("Testing Shift Data Creation and Retrieval...")
    print("=" * 60)
    
    try:
        # Initialize controllers
        session = get_fresh_session()
        auth_controller = AuthController()
        
        # Get test user
        test_user = session.query(User).filter_by(username="test_cashier").first()
        if not test_user:
            print("❌ Test user not found. Run test_cart_checkout.py first.")
            return
        
        print(f"✅ Using test user: {test_user.username} (ID: {test_user.id})")
        
        # Test 1: Check for existing open shifts
        print("\n1. Checking for existing open shifts...")
        existing_shifts = session.query(Shift).filter_by(user_id=test_user.id, status=ShiftStatus.OPEN).all()
        print(f"  Found {len(existing_shifts)} existing open shifts")
        
        for shift in existing_shifts:
            print(f"  - Shift ID: {shift.id}, Opening Amount: ${shift.opening_amount}, Open Time: {shift.open_time}")
        
        # Test 2: Open a new shift
        print("\n2. Opening a new shift...")
        opening_amount = 500.0
        new_shift = auth_controller.open_shift(test_user, opening_amount)
        
        if new_shift:
            print(f"  ✅ Shift opened successfully!")
            print(f"  - Shift ID: {new_shift.id}")
            print(f"  - Opening Amount: ${new_shift.opening_amount}")
            print(f"  - Status: {new_shift.status.value}")
            print(f"  - Open Time: {new_shift.open_time}")
        else:
            print("  ❌ Failed to open shift")
            return
        
        # Test 3: Verify shift was saved to database
        print("\n3. Verifying shift in database...")
        saved_shift = session.query(Shift).filter_by(id=new_shift.id).first()
        if saved_shift:
            print(f"  ✅ Shift found in database!")
            print(f"  - Shift ID: {saved_shift.id}")
            print(f"  - User ID: {saved_shift.user_id}")
            print(f"  - Status: {saved_shift.status.value}")
        else:
            print("  ❌ Shift not found in database")
            return
        
        # Test 4: Get open shift using auth controller
        print("\n4. Getting open shift using auth controller...")
        open_shift = auth_controller.get_open_shift(test_user)
        if open_shift:
            print(f"  ✅ Open shift retrieved successfully!")
            print(f"  - Shift ID: {open_shift.id}")
            print(f"  - Opening Amount: ${open_shift.opening_amount}")
            print(f"  - Status: {open_shift.status.value}")
        else:
            print("  ❌ No open shift found")
            return
        
        # Test 5: Test the exact query used in main.py
        print("\n5. Testing the exact query from main.py...")
        current_shift = auth_controller.session.query(Shift).filter_by(
            user_id=test_user.id, status=ShiftStatus.OPEN
        ).first()
        
        if current_shift:
            print(f"  ✅ Current shift found using main.py query!")
            print(f"  - Shift ID: {current_shift.id}")
            print(f"  - Opening Amount: ${current_shift.opening_amount}")
            print(f"  - Status: {current_shift.status.value}")
        else:
            print("  ❌ No current shift found using main.py query")
            return
        
        # Test 6: Test shift closing
        print("\n6. Testing shift closing...")
        closing_amount = 600.0
        closed_shift = auth_controller.close_shift(test_user, closing_amount)
        
        if closed_shift:
            print(f"  ✅ Shift closed successfully!")
            print(f"  - Shift ID: {closed_shift.id}")
            print(f"  - Closing Amount: ${closed_shift.closing_amount}")
            print(f"  - Status: {closed_shift.status.value}")
            print(f"  - Close Time: {closed_shift.close_time}")
        else:
            print("  ❌ Failed to close shift")
        
        # Test 7: Verify no open shifts remain
        print("\n7. Verifying no open shifts remain...")
        remaining_open_shifts = session.query(Shift).filter_by(user_id=test_user.id, status=ShiftStatus.OPEN).all()
        print(f"  Found {len(remaining_open_shifts)} remaining open shifts")
        
        if len(remaining_open_shifts) == 0:
            print("  ✅ No open shifts remain (correct)")
        else:
            print("  ❌ Open shifts still exist")
            for shift in remaining_open_shifts:
                print(f"    - Shift ID: {shift.id}")
        
        print("\n" + "=" * 60)
        print("🎉 Shift data test completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_shift_data() 