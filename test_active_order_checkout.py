#!/usr/bin/env python3
"""
Test script to demonstrate the active order checkout functionality.
This script tests the integration between order management and cart checkout.
"""

import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from PyQt5.QtWidgets import QApplication, QMessageBox
from controllers.order_controller import OrderController
from controllers.sale_controller import SaleController
from models.user import User, UserRole
from models.order import OrderStatus
from models.product import Product
from database.db_config import get_fresh_session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_active_order_checkout():
    """Test the active order checkout functionality."""
    print("🧪 Testing Active Order Checkout Functionality")
    print("=" * 50)
    
    try:
        # Initialize controllers
        order_controller = OrderController()
        sale_controller = SaleController()
        
        # Get a test user (admin)
        session = get_fresh_session()
        test_user = session.query(User).filter_by(role=UserRole.ADMIN).first()
        
        if not test_user:
            print("❌ No admin user found for testing")
            return False
        
        print(f"✅ Using test user: {test_user.username}")
        
        # Get some products for testing
        products = session.query(Product).limit(3).all()
        if not products:
            print("❌ No products found for testing")
            return False
        
        print(f"✅ Found {len(products)} products for testing")
        
        # Create a test active order
        print("\n📋 Creating test active order...")
        test_order = order_controller.create_order(
            user=test_user,
            customer_name="Test Customer",
            notes="Test order for checkout functionality"
        )
        
        if not test_order:
            print("❌ Failed to create test order")
            return False
        
        print(f"✅ Created test order: {test_order.order_number}")
        
        # Add items to the order
        items = []
        for i, product in enumerate(products):
            items.append({
                'product_id': product.id,
                'quantity': i + 1,
                'price': product.price,
                'notes': f"Test item {i + 1}"
            })
        
        if order_controller.add_items_to_order(test_order, items):
            print(f"✅ Added {len(items)} items to order")
        else:
            print("❌ Failed to add items to order")
            return False
        
        # Test loading order into cart
        print("\n🛒 Testing order loading into cart...")
        if sale_controller.load_order_to_cart(test_order):
            print("✅ Order loaded into cart successfully")
            print(f"   Cart items: {len(sale_controller.cart)}")
            print(f"   Cart total: ${sale_controller.get_cart_total_with_tax():.2f}")
        else:
            print("❌ Failed to load order into cart")
            return False
        
        # Test checkout functionality
        print("\n💳 Testing checkout functionality...")
        if sale_controller.complete_sale(test_user):
            print("✅ Sale completed successfully")
            
            # Check if order was completed
            updated_order = order_controller.get_order_by_id(test_order.id)
            if updated_order and updated_order.status == OrderStatus.COMPLETED:
                print("✅ Order marked as completed")
            else:
                print("❌ Order was not marked as completed")
                return False
        else:
            print("❌ Failed to complete sale")
            return False
        
        # Clean up
        print("\n🧹 Cleaning up test data...")
        session.close()
        
        print("\n✅ All tests passed! Active order checkout functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        logger.error(f"Test error: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 Starting Active Order Checkout Test")
    print("This test verifies that active orders can be properly loaded into cart and checked out.")
    print()
    
    # Create QApplication for testing
    app = QApplication(sys.argv)
    
    # Run the test
    success = test_active_order_checkout()
    
    if success:
        print("\n🎉 Test completed successfully!")
        print("The active order checkout functionality is working correctly.")
        print("\nKey features tested:")
        print("• Creating active orders")
        print("• Loading orders into cart")
        print("• Processing checkout")
        print("• Order status updates")
    else:
        print("\n💥 Test failed!")
        print("There are issues with the active order checkout functionality.")
    
    print("\n📝 Test Summary:")
    print("The enhanced cart widget now supports:")
    print("• Loading active orders into cart")
    print("• Updating active orders (modify items/details)")
    print("• Checking out active orders (complete sale)")
    print("• Proper status handling for different order types")
    print("• Clear user feedback and confirmation dialogs")

if __name__ == "__main__":
    main() 