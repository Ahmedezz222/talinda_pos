#!/usr/bin/env python3
"""
Test script for auto-close orders functionality.
"""
import sys
import os
from pathlib import Path
from datetime import datetime, timedelta, timezone

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from database.db_config import get_fresh_session
from models.order import Order, OrderStatus
from models.user import User
from utils.background_tasks import BackgroundTaskManager
from PyQt5.QtWidgets import QApplication
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_order(session, user, hours_old=25):
    """Create a test order that's older than 24 hours."""
    from controllers.order_controller import OrderController
    import uuid
    
    order_controller = OrderController()
    
    # Create order with old timestamp and unique number
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    order_number = f"TEST-{timestamp}-{unique_id}"
    
    order = Order(
        order_number=order_number,
        customer_name="Test Customer",
        user_id=user.id,
        status=OrderStatus.ACTIVE,
        created_at=datetime.now(timezone.utc) - timedelta(hours=hours_old),
        updated_at=datetime.now(timezone.utc) - timedelta(hours=hours_old)
    )
    
    session.add(order)
    session.commit()
    
    logger.info(f"Created test order {order.order_number} with age {hours_old} hours")
    return order

def test_auto_close_functionality():
    """Test the auto-close functionality."""
    print("Testing Auto-Close Orders Functionality")
    print("=" * 50)
    
    # Create QApplication for PyQt signals
    app = QApplication(sys.argv)
    
    try:
        # Get a fresh session
        session = get_fresh_session()
        
        # Get or create a test user
        user = session.query(User).first()
        if not user:
            print("No users found in database. Please create a user first.")
            return False
        
        print(f"Using user: {user.username}")
        
        # Create test orders
        print("\n1. Creating test orders...")
        
        # Create an order that's 25 hours old (should be auto-closed)
        old_order = create_test_order(session, user, hours_old=25)
        
        # Create an order that's 23 hours old (should NOT be auto-closed)
        recent_order = create_test_order(session, user, hours_old=23)
        
        # Create an order that's 1 hour old (should NOT be auto-closed)
        new_order = create_test_order(session, user, hours_old=1)
        
        session.close()
        
        print(f"Created orders:")
        print(f"  - Old order: {old_order.order_number} (25 hours old)")
        print(f"  - Recent order: {recent_order.order_number} (23 hours old)")
        print(f"  - New order: {new_order.order_number} (1 hour old)")
        
        # Test the background task manager
        print("\n2. Testing background task manager...")
        
        task_manager = BackgroundTaskManager(check_interval_minutes=1)
        
        # Connect signals for testing
        def on_orders_closed(count):
            print(f"✓ Auto-closed {count} orders")
        
        def on_error(error_msg):
            print(f"✗ Error: {error_msg}")
        
        task_manager.orders_auto_closed.connect(on_orders_closed)
        task_manager.task_error.connect(on_error)
        
        # Force an immediate check
        print("Running immediate check for old orders...")
        task_manager.force_check_now()
        
        # Wait a moment for the check to complete
        app.processEvents()
        
        # Wait a moment for the check to complete and process events
        import time
        time.sleep(1)
        app.processEvents()
        
        # Verify results
        print("\n3. Verifying results...")
        session = get_fresh_session()
        
        # Check old order status
        old_order_check = session.query(Order).filter_by(order_number=old_order.order_number).first()
        if old_order_check and old_order_check.status == OrderStatus.COMPLETED:
            print(f"✓ Old order {old_order_check.order_number} was auto-closed")
        else:
            print(f"✗ Old order {old_order.order_number} was NOT auto-closed")
        
        # Check recent order status
        recent_order_check = session.query(Order).filter_by(order_number=recent_order.order_number).first()
        if recent_order_check and recent_order_check.status == OrderStatus.ACTIVE:
            print(f"✓ Recent order {recent_order_check.order_number} remains active")
        else:
            print(f"✗ Recent order {recent_order.order_number} was incorrectly closed")
        
        # Check new order status
        new_order_check = session.query(Order).filter_by(order_number=new_order.order_number).first()
        if new_order_check and new_order_check.status == OrderStatus.ACTIVE:
            print(f"✓ New order {new_order_check.order_number} remains active")
        else:
            print(f"✗ New order {new_order.order_number} was incorrectly closed")
        
        session.close()
        
        # Clean up test orders
        print("\n4. Cleaning up test orders...")
        session = get_fresh_session()
        test_orders = session.query(Order).filter(
            Order.order_number.like("TEST-%")
        ).all()
        
        for order in test_orders:
            session.delete(order)
        
        session.commit()
        session.close()
        
        print(f"Cleaned up {len(test_orders)} test orders")
        
        print("\n✓ Auto-close functionality test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        logger.error(f"Test error: {e}")
        return False
    
    finally:
        app.quit()

if __name__ == "__main__":
    success = test_auto_close_functionality()
    sys.exit(0 if success else 1) 