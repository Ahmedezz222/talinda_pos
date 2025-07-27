#!/usr/bin/env python3
"""
Test script for UI checkout functionality.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication
from controllers.sale_controller import SaleController
from controllers.product_controller import ProductController
from models.user import User, UserRole
from models.product import Product, Category
from database.db_config import get_fresh_session
from ui.components.enhanced_cart_widget import EnhancedCartWidget
from ui.components.payment_dialog import PaymentDialog
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_ui_checkout():
    """Test the complete UI checkout flow."""
    print("=" * 60)
    print("Testing UI Checkout Functionality...")
    print("=" * 60)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Initialize controllers
        session = get_fresh_session()
        sale_controller = SaleController()
        product_controller = ProductController()
        
        # Get test user
        test_user = session.query(User).filter_by(username="test_cashier").first()
        if not test_user:
            print("❌ Test user not found. Run test_cart_checkout.py first.")
            return
        
        # Get test product
        test_product = session.query(Product).filter_by(name="Test Product 1").first()
        if not test_product:
            print("❌ Test product not found. Run test_cart_checkout.py first.")
            return
        
        print(f"✅ Using test user: {test_user.username}")
        print(f"✅ Using test product: {test_product.name} (stock: {test_product.stock})")
        
        # Test 1: Create enhanced cart widget
        print("\n1. Testing Enhanced Cart Widget...")
        cart_widget = EnhancedCartWidget(sale_controller, test_user)
        print("  ✅ Enhanced cart widget created successfully")
        
        # Test 2: Add item to cart via UI
        print("\n2. Testing add item to cart...")
        cart_widget.add_item(test_product)
        print(f"  ✅ Added {test_product.name} to cart")
        print(f"  ✅ Cart has {len(sale_controller.cart)} items")
        
        # Test 3: Check cart totals
        print("\n3. Testing cart totals...")
        subtotal = sale_controller.get_cart_subtotal()
        total_with_tax = sale_controller.get_cart_total_with_tax()
        print(f"  ✅ Subtotal: ${subtotal:.2f}")
        print(f"  ✅ Total with tax: ${total_with_tax:.2f}")
        
        # Test 4: Test payment dialog
        print("\n4. Testing payment dialog...")
        payment_dialog = PaymentDialog(sale_controller, cart_widget)
        print("  ✅ Payment dialog created successfully")
        
        # Check payment dialog totals
        dialog_total = payment_dialog.total_amount.text()
        print(f"  ✅ Payment dialog total: {dialog_total}")
        
        # Test 5: Test checkout process
        print("\n5. Testing checkout process...")
        try:
            # Simulate checkout without showing dialog
            success = sale_controller.complete_sale(test_user)
            if success:
                print("  ✅ Checkout completed successfully!")
                
                # Check if cart is cleared
                if not sale_controller.cart:
                    print("  ✅ Cart cleared after checkout")
                else:
                    print("  ❌ Cart not cleared after checkout")
                
                # Check if stock was updated
                updated_product = session.query(Product).filter_by(id=test_product.id).first()
                print(f"  ✅ Product stock after checkout: {updated_product.stock}")
                
            else:
                print("  ❌ Checkout failed")
                
        except Exception as e:
            print(f"  ❌ Checkout error: {str(e)}")
        
        # Test 6: Test cart widget methods
        print("\n6. Testing cart widget methods...")
        
        # Test clear cart
        cart_widget.clear_cart()
        if not sale_controller.cart:
            print("  ✅ Cart cleared successfully")
        else:
            print("  ❌ Cart not cleared")
        
        # Test button states
        cart_widget.update_button_states()
        print("  ✅ Button states updated")
        
        print("\n" + "=" * 60)
        print("🎉 UI checkout functionality test completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ui_checkout() 