#!/usr/bin/env python3
"""
Test script to debug sale completion issues.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from controllers.sale_controller import SaleController
from models.user import User, UserRole
from models.product import Product, Category
from database.db_config import get_fresh_session
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def test_sale_completion():
    """Test sale completion specifically."""
    print("=" * 60)
    print("Testing Sale Completion...")
    print("=" * 60)
    
    try:
        # Initialize controllers
        session = get_fresh_session()
        sale_controller = SaleController()
        
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
        
        # Clear any existing cart
        sale_controller.clear_cart()
        print("✅ Cleared existing cart")
        
        # Add product to cart
        success = sale_controller.add_to_cart(test_product, 1)
        if success:
            print(f"✅ Added {test_product.name} to cart")
        else:
            print(f"❌ Failed to add {test_product.name} to cart")
            return
        
        # Check cart contents
        print(f"✅ Cart has {len(sale_controller.cart)} items")
        for product_id, cart_item in sale_controller.cart.items():
            print(f"  - {cart_item.product.name}: {cart_item.quantity} x ${cart_item.price:.2f}")
        
        # Check totals
        subtotal = sale_controller.get_cart_subtotal()
        total_with_tax = sale_controller.get_cart_total_with_tax()
        print(f"✅ Subtotal: ${subtotal:.2f}")
        print(f"✅ Total with tax: ${total_with_tax:.2f}")
        
        # Test sale completion
        print("\n🔄 Attempting sale completion...")
        success = sale_controller.complete_sale(test_user)
        
        if success:
            print("✅ Sale completed successfully!")
            
            # Check if cart is cleared
            if not sale_controller.cart:
                print("✅ Cart cleared after sale")
            else:
                print("❌ Cart not cleared after sale")
            
            # Check if stock was updated
            updated_product = session.query(Product).filter_by(id=test_product.id).first()
            print(f"✅ Product stock after sale: {updated_product.stock}")
            
            # Check if sale was recorded
            from models.sale import Sale
            recent_sales = session.query(Sale).order_by(Sale.timestamp.desc()).limit(1).all()
            if recent_sales:
                sale = recent_sales[0]
                print(f"✅ Sale recorded: ID={sale.id}, Amount=${sale.total_amount:.2f}, User={sale.user_id}")
            else:
                print("❌ No sale recorded in database")
                
        else:
            print("❌ Sale completion failed")
            
            # Check if current_user is set
            if sale_controller.current_user:
                print(f"✅ Current user is set: {sale_controller.current_user.username}")
            else:
                print("❌ Current user is not set")
            
            # Check cart contents
            print(f"✅ Cart still has {len(sale_controller.cart)} items")
        
        print("\n" + "=" * 60)
        print("🎉 Sale completion test completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_sale_completion() 