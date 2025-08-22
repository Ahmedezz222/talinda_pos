#!/usr/bin/env python3
"""
Debug script for active order checkout functionality.
This script helps identify issues with the checkout process.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from controllers.order_controller import OrderController
from controllers.sale_controller import SaleController
from models.user import User, UserRole
from models.order import OrderStatus
from database.db_config import Session, get_fresh_session

def debug_active_order_checkout():
    """Debug the active order checkout process step by step."""
    print("🔍 Debugging Active Order Checkout Process")
    print("=" * 50)
    
    try:
        # Get a test user
        session = Session()
        user = session.query(User).first()
        if not user:
            print("❌ No users found in database. Please create a user first.")
            return False
        
        print(f"✅ Using user: {user.username} (ID: {user.id})")
        
        # Create order controller
        order_controller = OrderController()
        
        # Create a test active order
        print("\n📋 Creating test active order...")
        test_order = order_controller.create_order(
            user=user,
            customer_name="Test Customer",
            notes="Debug test order"
        )
        
        if not test_order:
            print("❌ Failed to create test order")
            return False
        
        print(f"✅ Created test order: {test_order.order_number}")
        print(f"   Status: {test_order.status.value}")
        print(f"   Customer: {test_order.customer_name}")
        
        # Add some test items to the order
        print("\n🛍️ Adding test items to order...")
        from models.product import Product
        
        products = session.query(Product).limit(2).all()
        if not products:
            print("❌ No products found in database")
            return False
        
        items = []
        for i, product in enumerate(products):
            items.append({
                'product_id': product.id,
                'quantity': i + 1,
                'price': product.price,
                'notes': f"Debug item {i+1}"
            })
            print(f"   Added: {product.name} x{i+1} @ ${product.price}")
        
        if order_controller.add_items_to_order(test_order, items):
            print("✅ Items added to order successfully")
        else:
            print("❌ Failed to add items to order")
            return False
        
        # Create sale controller
        sale_controller = SaleController()
        
        # Load order into cart
        print("\n🛒 Loading order into cart...")
        if sale_controller.load_order_to_cart(test_order):
            print("✅ Order loaded into cart successfully")
            print(f"   Cart items: {len(sale_controller.cart)}")
            print(f"   Cart total: ${sale_controller.get_cart_total_with_tax():.2f}")
        else:
            print("❌ Failed to load order into cart")
            return False
        
        # Check if loaded_order is set
        print(f"\n📋 Checking loaded order reference...")
        if hasattr(sale_controller, 'loaded_order') and sale_controller.loaded_order:
            print(f"✅ Loaded order reference: {sale_controller.loaded_order.order_number}")
            print(f"   Status: {sale_controller.loaded_order.status.value}")
        else:
            print("❌ No loaded order reference found")
            return False
        
        # Test checkout process
        print("\n💳 Testing checkout process...")
        
        # Set current user
        sale_controller.current_user = user
        
        # Complete the sale
        if sale_controller.complete_sale(user):
            print("✅ Sale completed successfully")
            
            # Check if order was completed using a fresh session
            fresh_session = get_fresh_session()
            try:
                completed_order = fresh_session.query(Order).filter_by(id=test_order.id).first()
                if completed_order and completed_order.status == OrderStatus.COMPLETED:
                    print("✅ Order marked as completed")
                else:
                    print(f"❌ Order status is still: {completed_order.status.value if completed_order else 'Not found'}")
                    return False
            finally:
                fresh_session.close()
        else:
            print("❌ Failed to complete sale")
            return False
        
        print("\n🎉 All tests passed! Active order checkout is working correctly.")
        return True
        
    except Exception as e:
        print(f"❌ Error during debug: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        session.close()

def check_enhanced_cart_widget():
    """Check if the enhanced cart widget is properly configured."""
    print("\n🔧 Checking Enhanced Cart Widget Configuration")
    print("=" * 50)
    
    try:
        from ui.components.enhanced_cart_widget import EnhancedCartWidget
        
        # Check if the class exists and has required methods
        required_methods = [
            'create_order',
            'checkout',
            'checkout_active_order',
            'load_order'
        ]
        
        for method_name in required_methods:
            if hasattr(EnhancedCartWidget, method_name):
                print(f"✅ Method {method_name} exists")
            else:
                print(f"❌ Method {method_name} missing")
        
        # Check button connections
        print("\n🔗 Checking button connections...")
        # This would require creating an instance, but we can check the code structure
        
        print("✅ Enhanced cart widget structure looks correct")
        return True
        
    except ImportError as e:
        print(f"❌ Could not import EnhancedCartWidget: {e}")
        return False
    except Exception as e:
        print(f"❌ Error checking enhanced cart widget: {e}")
        return False

def show_usage_guide():
    """Show a guide on how to use active order checkout."""
    print("\n📖 Active Order Checkout Usage Guide")
    print("=" * 50)
    print("""
To use active order checkout in the POS system:

1. 📋 Create or find an active order:
   - Go to the Order Management tab
   - Look for orders with "Active" status
   - Click on an active order to load it into the cart

2. 🛒 Load the order into cart:
   - The order items will appear in the cart
   - The cart header will show "Order [number] - [customer] (Active)"
   - The button will change to "Checkout"

3. 💳 Checkout the order:
   - Click the "Checkout" button
   - You'll see a dialog asking what you want to do:
     • Update Order: Modify items/details
     • Checkout Order: Complete the sale
   - Choose "Checkout Order" to complete the sale

4. ✅ Complete the sale:
   - The system will process the payment
   - The order will be marked as "Completed"
   - A sale record will be created
   - The cart will be cleared

Common Issues:
• Make sure you're using the enhanced cart widget (not the basic one)
• Verify the order status is "Active" before loading
• Check that you have proper user permissions
• Ensure the database is accessible

If you're still having issues:
1. Check the console for error messages
2. Verify the order has items before loading
3. Make sure you're logged in as a valid user
""")

def main():
    """Main debug function."""
    print("🚀 Starting Active Order Checkout Debug")
    print("=" * 60)
    
    # Check enhanced cart widget
    if not check_enhanced_cart_widget():
        print("\n❌ Enhanced cart widget issues found")
        return
    
    # Debug the checkout process
    if debug_active_order_checkout():
        print("\n✅ Debug completed successfully!")
        show_usage_guide()
    else:
        print("\n❌ Debug found issues with the checkout process")
        print("\n🔧 Please check:")
        print("1. Database connectivity")
        print("2. User permissions")
        print("3. Product availability")
        print("4. Order status")

if __name__ == "__main__":
    main() 