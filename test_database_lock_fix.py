#!/usr/bin/env python3
"""
Test script to verify database lock fix for order creation.
"""

import sys
import os
import threading
import time
from pathlib import Path

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir / "src"))

from controllers.order_controller import OrderController
from controllers.auth_controller import AuthController
from models.user import User, UserRole
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_order_test(user, order_id):
    """Test function to create an order."""
    try:
        controller = OrderController()
        order = controller.create_order(user, f"Test Customer {order_id}", f"Test order {order_id}")
        logger.info(f"Order {order_id} created successfully: {order.order_number}")
        return True
    except Exception as e:
        logger.error(f"Failed to create order {order_id}: {e}")
        return False

def test_concurrent_order_creation():
    """Test concurrent order creation to verify database lock fix."""
    logger.info("Starting concurrent order creation test...")
    
    # Create a test user
    auth_controller = AuthController()
    test_user = User(
        username="test_user",
        password_hash="dummy_hash",
        role=UserRole.CASHIER,
        full_name="Test User",
        active=1
    )
    
    # Test single order creation first
    logger.info("Testing single order creation...")
    success = create_order_test(test_user, 1)
    if not success:
        logger.error("Single order creation failed!")
        return False
    
    # Test concurrent order creation
    logger.info("Testing concurrent order creation...")
    threads = []
    results = []
    
    def order_creation_worker(user, order_id, results_list):
        result = create_order_test(user, order_id)
        results_list.append((order_id, result))
    
    # Create 5 concurrent threads
    for i in range(2, 7):
        thread = threading.Thread(
            target=order_creation_worker,
            args=(test_user, i, results)
        )
        threads.append(thread)
        thread.start()
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()
    
    # Check results
    successful_orders = sum(1 for _, success in results if success)
    total_orders = len(results)
    
    logger.info(f"Concurrent order creation results: {successful_orders}/{total_orders} successful")
    
    if successful_orders == total_orders:
        logger.info("✅ Database lock fix test PASSED!")
        return True
    else:
        logger.error("❌ Database lock fix test FAILED!")
        return False

def test_database_connection():
    """Test basic database connectivity."""
    logger.info("Testing database connectivity...")
    
    try:
        from database.db_config import engine
        with engine.connect() as conn:
            result = conn.execute("SELECT 1")
            logger.info("✅ Database connectivity test PASSED!")
            return True
    except Exception as e:
        logger.error(f"❌ Database connectivity test FAILED: {e}")
        return False

if __name__ == "__main__":
    logger.info("Starting database lock fix verification...")
    
    # Test database connectivity first
    if not test_database_connection():
        sys.exit(1)
    
    # Test concurrent order creation
    if test_concurrent_order_creation():
        logger.info("All tests passed! Database lock issue has been resolved.")
        sys.exit(0)
    else:
        logger.error("Tests failed! Database lock issue persists.")
        sys.exit(1) 