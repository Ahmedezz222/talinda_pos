#!/usr/bin/env python3
"""
Test script for Shift Details Report functionality
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from database.database_manager import DatabaseManager
from controllers.shift_controller import ShiftController
from models.user import User, Shift, ShiftStatus
from models.sale import Sale, sale_products
from models.order import Order, OrderStatus
from models.product import Product, Category
from database.db_config import get_fresh_session, safe_commit
from datetime import datetime, timedelta

def test_shift_details_report():
    """Test the shift details report functionality."""
    print("🧪 Testing Shift Details Report Functionality")
    print("=" * 50)
    
    try:
        # Initialize controllers
        db_manager = DatabaseManager()
        shift_controller = ShiftController()
        
        # Get all shifts
        print("📋 Getting all shifts...")
        shifts = db_manager.get_all_shifts()
        print(f"Found {len(shifts)} shifts")
        
        if not shifts:
            print("❌ No shifts found in database. Please create some shifts first.")
            return False
        
        # Test with the first shift
        test_shift_id = shifts[0]['shift_id']
        print(f"🔍 Testing with shift ID: {test_shift_id}")
        
        # Get shift details
        print("📊 Getting shift details...")
        shift_details = db_manager.get_shift_details(test_shift_id)
        if shift_details:
            print(f"✅ Shift details retrieved successfully")
            print(f"   - User: {shift_details['username']}")
            print(f"   - Open Time: {shift_details['open_time']}")
            print(f"   - Status: {shift_details['status']}")
        else:
            print("❌ Failed to get shift details")
            return False
        
        # Get sales by payment method
        print("💳 Getting sales by payment method...")
        sales_by_payment = db_manager.get_shift_sales_by_payment(test_shift_id)
        print(f"✅ Found {len(sales_by_payment)} payment methods")
        for payment in sales_by_payment:
            print(f"   - {payment['payment_method']}: ${payment['total_amount']:.2f}")
        
        # Get product sales
        print("📦 Getting product sales...")
        product_sales = db_manager.get_shift_product_sales(test_shift_id)
        print(f"✅ Found {len(product_sales)} products sold")
        for product in product_sales[:5]:  # Show first 5
            print(f"   - {product['product_name']}: {product['quantity']} units, ${product['total_amount']:.2f}")
        
        # Get orders
        print("📋 Getting orders...")
        orders = db_manager.get_shift_orders(test_shift_id)
        print(f"✅ Found {len(orders)} orders")
        for order in orders[:3]:  # Show first 3
            print(f"   - Order #{order['order_number']}: ${order['total_amount']:.2f}")
        
        # Get complete report
        print("📊 Getting complete shift details report...")
        report = shift_controller.get_shift_details_report(test_shift_id)
        if report:
            print("✅ Complete report generated successfully")
            print(f"   - Total Sales: ${report['summary']['total_sales']:.2f}")
            print(f"   - Total Products Sold: {report['summary']['total_products_sold']}")
            print(f"   - Total Orders: {report['summary']['total_orders']}")
            print(f"   - Unique Products: {report['summary']['unique_products']}")
        else:
            print("❌ Failed to generate complete report")
            return False
        
        print("\n🎉 All tests passed! Shift Details Report is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def create_test_data():
    """Create some test data if needed."""
    print("🔧 Creating test data...")
    
    try:
        session = get_fresh_session()
        
        # Check if we have any shifts
        existing_shifts = session.query(Shift).count()
        if existing_shifts > 0:
            print(f"✅ Found {existing_shifts} existing shifts")
            session.close()
            return True
        
        # Create test user if needed
        test_user = session.query(User).filter_by(username="test_user").first()
        if not test_user:
            import bcrypt
            password_hash = bcrypt.hashpw("password123".encode('utf-8'), bcrypt.gensalt())
            test_user = User(
                username="test_user",
                password_hash=password_hash.decode('utf-8'),
                role=UserRole.CASHIER,
                full_name="Test User",
                active=1
            )
            session.add(test_user)
            safe_commit(session)
            print("✅ Created test user")
        
        # Create test shift
        test_shift = Shift(
            user_id=test_user.id,
            opening_amount=100.0,
            status=ShiftStatus.CLOSED,
            open_time=datetime.now() - timedelta(hours=8),
            close_time=datetime.now()
        )
        session.add(test_shift)
        safe_commit(session)
        print("✅ Created test shift")
        
        session.close()
        return True
        
    except Exception as e:
        print(f"❌ Failed to create test data: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Shift Details Report Test")
    print("=" * 50)
    
    # Create test data if needed
    if not create_test_data():
        print("❌ Failed to create test data")
        sys.exit(1)
    
    # Run the test
    if test_shift_details_report():
        print("\n✅ All tests completed successfully!")
        sys.exit(0)
    else:
        print("\n❌ Tests failed!")
        sys.exit(1) 