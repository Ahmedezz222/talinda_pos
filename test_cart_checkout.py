#!/usr/bin/env python3
"""
Test script for cart checkout functionality.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from controllers.sale_controller import SaleController, CartItem
from controllers.product_controller import ProductController
from controllers.auth_controller import AuthController
from models.user import User, UserRole
from models.product import Product, Category
from database.db_config import get_fresh_session
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_cart_checkout():
    """Test the complete cart checkout process."""
    print("=" * 60)
    print("Testing Cart Checkout Functionality...")
    print("=" * 60)
    
    try:
        # Initialize controllers
        session = get_fresh_session()
        sale_controller = SaleController()
        product_controller = ProductController()
        auth_controller = AuthController()
        
        # Create test user if not exists
        test_user = session.query(User).filter_by(username="test_cashier").first()
        if not test_user:
            import bcrypt
            password_hash = bcrypt.hashpw("test123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            test_user = User(
                username="test_cashier",
                password_hash=password_hash,
                role=UserRole.CASHIER,
                full_name="Test Cashier",
                active=1
            )
            session.add(test_user)
            session.commit()
            print("✅ Created test user")
        else:
            print("✅ Test user already exists")
        
        # Create test category if not exists
        test_category = session.query(Category).filter_by(name="Test Category").first()
        if not test_category:
            test_category = Category(
                name="Test Category",
                description="Test category for checkout testing",
                tax_rate=10.0
            )
            session.add(test_category)
            session.commit()
            print("✅ Created test category")
        else:
            print("✅ Test category already exists")
        
        # Create test products if not exist
        test_products = []
        product_names = ["Test Product 1", "Test Product 2", "Test Product 3"]
        
        for i, name in enumerate(product_names):
            product = session.query(Product).filter_by(name=name).first()
            if not product:
                product = Product(
                    name=name,
                    description=f"Test product {i+1} for checkout testing",
                    price=10.0 + (i * 5.0),  # 10, 15, 20
                    category_id=test_category.id,
                    stock=50
                )
                session.add(product)
                test_products.append(product)
            else:
                test_products.append(product)
        
        session.commit()
        print("✅ Test products ready")
        
        # Test 1: Add items to cart
        print("\n1. Testing cart operations...")
        for product in test_products:
            success = sale_controller.add_to_cart(product, 2)
            if success:
                print(f"  ✅ Added {product.name} to cart")
            else:
                print(f"  ❌ Failed to add {product.name} to cart")
        
        # Test 2: Check cart totals
        print("\n2. Testing cart totals...")
        subtotal = sale_controller.get_cart_subtotal()
        discount_total = sale_controller.get_cart_discount_total()
        tax_total = sale_controller.get_cart_tax_total()
        total_with_tax = sale_controller.get_cart_total_with_tax()
        
        print(f"  ✅ Subtotal: ${subtotal:.2f}")
        print(f"  ✅ Discount: ${discount_total:.2f}")
        print(f"  ✅ Tax: ${tax_total:.2f}")
        print(f"  ✅ Total with tax: ${total_with_tax:.2f}")
        
        # Test 3: Test discount application
        print("\n3. Testing discount application...")
        success = sale_controller.apply_item_discount(test_products[0].id, 10.0, 0.0)
        if success:
            print(f"  ✅ Applied 10% discount to {test_products[0].name}")
        else:
            print(f"  ❌ Failed to apply discount to {test_products[0].name}")
        
        # Test 4: Test cart discount
        print("\n4. Testing cart discount...")
        sale_controller.apply_cart_discount(5.0, 2.0)
        print("  ✅ Applied 5% + $2.0 cart discount")
        
        # Recalculate totals
        new_subtotal = sale_controller.get_cart_subtotal()
        new_discount_total = sale_controller.get_cart_discount_total()
        new_tax_total = sale_controller.get_cart_tax_total()
        new_total_with_tax = sale_controller.get_cart_total_with_tax()
        
        print(f"  ✅ New subtotal: ${new_subtotal:.2f}")
        print(f"  ✅ New discount: ${new_discount_total:.2f}")
        print(f"  ✅ New tax: ${new_tax_total:.2f}")
        print(f"  ✅ New total with tax: ${new_total_with_tax:.2f}")
        
        # Test 5: Test sale completion
        print("\n5. Testing sale completion...")
        success = sale_controller.complete_sale(test_user)
        if success:
            print("  ✅ Sale completed successfully!")
            
            # Verify cart is cleared
            if not sale_controller.cart:
                print("  ✅ Cart cleared after sale")
            else:
                print("  ❌ Cart not cleared after sale")
                
            # Verify stock was updated
            for product in test_products:
                updated_product = session.query(Product).filter_by(id=product.id).first()
                if updated_product.stock == 48:  # 50 - 2
                    print(f"  ✅ Stock updated for {product.name}: {updated_product.stock}")
                else:
                    print(f"  ❌ Stock not updated correctly for {product.name}: {updated_product.stock}")
        else:
            print("  ❌ Sale completion failed")
        
        # Test 6: Test with insufficient stock
        print("\n6. Testing insufficient stock scenario...")
        # Add a product with low stock
        low_stock_product = session.query(Product).filter_by(name="Test Product 1").first()
        if low_stock_product:
            # Try to add more than available stock
            success = sale_controller.add_to_cart(low_stock_product, 100)
            if not success:
                print("  ✅ Correctly prevented adding more than available stock")
            else:
                print("  ❌ Should have prevented adding more than available stock")
        
        print("\n" + "=" * 60)
        print("🎉 Cart checkout functionality test completed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_cart_checkout() 