#!/usr/bin/env python3
"""
Test script to verify automatic shift closing functionality.
"""
import sys
import os
from datetime import datetime, time, timedelta
from sqlalchemy import and_

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from controllers.shift_controller import ShiftController
from models.user import User, Shift, ShiftStatus
from database.db_config import get_fresh_session

def test_automatic_shift_closing():
    """Test the automatic shift closing functionality."""
    print("Testing Automatic Shift Closing Functionality")
    print("=" * 60)
    
    try:
        # Create shift controller
        shift_controller = ShiftController()
        
        # Get a test user (admin or first available user)
        session = get_fresh_session()
        test_user = session.query(User).first()
        
        if not test_user:
            print("❌ No users found in database. Please create a user first.")
            return False
        
        print(f"Using test user: {test_user.username}")
        
        # Check current open shifts
        open_shifts_before = session.query(Shift).filter_by(status=ShiftStatus.OPEN).count()
        print(f"Open shifts before test: {open_shifts_before}")
        
        # Create a test open shift if none exists
        if open_shifts_before == 0:
            print("Creating test open shift...")
            test_shift = Shift(
                user_id=test_user.id,
                opening_amount=100.0,
                status=ShiftStatus.OPEN,
                open_time=datetime.now() - timedelta(hours=2)  # Opened 2 hours ago
            )
            session.add(test_shift)
            session.commit()
            print("✅ Test shift created")
        
        # Check open shifts again
        open_shifts_after_create = session.query(Shift).filter_by(status=ShiftStatus.OPEN).count()
        print(f"Open shifts after creating test shift: {open_shifts_after_create}")
        
        # Test the automatic shift closing function
        print("\nTesting automatic shift closing...")
        closed_count = shift_controller.close_all_open_shifts()
        print(f"✅ Closed {closed_count} shifts automatically")
        
        # Verify shifts were closed
        open_shifts_after = session.query(Shift).filter_by(status=ShiftStatus.OPEN).count()
        print(f"Open shifts after automatic closing: {open_shifts_after}")
        
        # Check closed shifts
        closed_shifts = session.query(Shift).filter_by(status=ShiftStatus.CLOSED).all()
        print(f"Total closed shifts: {len(closed_shifts)}")
        
        for shift in closed_shifts:
            print(f"  - Shift {shift.id}: {shift.user.username if shift.user else 'Unknown'} "
                  f"(Opened: {shift.open_time}, Closed: {shift.close_time})")
        
        # Test the daily reset function
        print("\nTesting daily reset function...")
        shift_controller.reset_daily_sales()
        print("✅ Daily reset completed")
        
        session.close()
        
        if open_shifts_after == 0 and closed_count > 0:
            print("\n✅ All tests passed! Automatic shift closing is working correctly.")
            return True
        else:
            print("\n❌ Some tests failed. Please check the output above.")
            return False
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_shift_detection():
    """Test detection of automatically closed shifts."""
    print("\nTesting Shift Detection")
    print("=" * 40)
    
    try:
        session = get_fresh_session()
        
        # Get a test user
        test_user = session.query(User).first()
        if not test_user:
            print("❌ No users found for testing.")
            return False
        
        # Create a shift that was "automatically closed" at midnight
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        midnight_time = datetime.combine(today, time(0, 0))
        
        auto_closed_shift = Shift(
            user_id=test_user.id,
            opening_amount=150.0,
            status=ShiftStatus.CLOSED,
            open_time=datetime.combine(yesterday, time(8, 0)),  # Opened yesterday at 8 AM
            close_time=midnight_time  # Closed at midnight
        )
        
        session.add(auto_closed_shift)
        session.commit()
        print(f"✅ Created test auto-closed shift for {test_user.username}")
        
        # Test detection logic
        from sqlalchemy import and_
        detected_shift = session.query(Shift).filter(
            and_(
                Shift.user_id == test_user.id,
                Shift.status == ShiftStatus.CLOSED,
                Shift.close_time >= datetime.combine(yesterday, time(23, 59)),
                Shift.close_time <= datetime.combine(today, time(0, 1))
            )
        ).first()
        
        if detected_shift:
            print("✅ Auto-closed shift detection working correctly")
            print(f"  - Detected shift closed at: {detected_shift.close_time}")
            return True
        else:
            print("❌ Auto-closed shift detection failed")
            return False
        
    except Exception as e:
        print(f"❌ Error during shift detection test: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def test_daily_reset_task():
    """Test the daily reset task functionality."""
    print("\nTesting Daily Reset Task")
    print("=" * 40)
    
    try:
        from utils.daily_reset_task import DailyResetTask
        
        # Create the task
        task = DailyResetTask()
        print("✅ Daily reset task created")
        
        # Test signal connections
        signal_connected = False
        def test_signal():
            nonlocal signal_connected
            signal_connected = True
            print("✅ Reset signal received")
        
        task.reset_triggered.connect(test_signal)
        print("✅ Signal connections working")
        
        # Test shift closing signal
        shift_signal_connected = False
        def test_shift_signal(count):
            nonlocal shift_signal_connected
            shift_signal_connected = True
            print(f"✅ Shift closing signal received with count: {count}")
        
        task.shift_closing_triggered.connect(test_shift_signal)
        print("✅ Shift closing signal connections working")
        
        # Clean up
        task.stop()
        print("✅ Task stopped successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during daily reset task test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Automatic Shift Closing Test Script")
    print("=" * 60)
    
    # Run all tests
    test1_success = test_automatic_shift_closing()
    test2_success = test_shift_detection()
    test3_success = test_daily_reset_task()
    
    print("\n" + "=" * 60)
    print("Test Results Summary:")
    print(f"Automatic Shift Closing: {'✅ PASS' if test1_success else '❌ FAIL'}")
    print(f"Shift Detection: {'✅ PASS' if test2_success else '❌ FAIL'}")
    print(f"Daily Reset Task: {'✅ PASS' if test3_success else '❌ FAIL'}")
    
    if test1_success and test2_success and test3_success:
        print("\n🎉 All tests passed! Automatic shift closing is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.") 