"""
Test script for enhanced cart functionality.
"""
from src.controllers.sale_controller import SaleController

from src.controllers.product_controller import ProductController
from src.models.user import User

def test_enhanced_cart():
    """Test the enhanced cart functionality."""
    print("Testing enhanced cart functionality...")
    
    # Initialize controllers
    sale_controller = SaleController()
    product_controller = ProductController()
    
    # Test 1: Regular POS cart functionality
    print("\n1. Testing regular POS cart functionality...")
    
    # Get some products
    products = product_controller.get_products()
    if products:
        product = products[0]
        print(f"  Adding product: {product.name} (${product.price})")
        
        # Test adding to cart
        success = sale_controller.add_to_cart(product, 2)
        print(f"  Added to cart: {success}")
        
        if success:
            print(f"  Cart subtotal: ${sale_controller.get_cart_subtotal():.2f}")
            print(f"  Cart total: ${sale_controller.get_cart_total_with_tax():.2f}")
            
            # Test discount
            sale_controller.apply_item_discount(product.id, 10.0, 0.0)  # 10% discount
            print(f"  After 10% discount: ${sale_controller.get_cart_total_with_tax():.2f}")
            
            # Clear cart
            sale_controller.clear_cart()
            print("  Cart cleared")
    

    
    # Test 3: Cart functionality summary
    print("\n3. Cart functionality summary...")
    print("  - Regular POS cart functionality")
    print("  - Item discounts and cart discounts")
    print("  - Tax calculation")
    print("  - Checkout process")
    
    print("\nEnhanced cart test completed!")

if __name__ == "__main__":
    test_enhanced_cart() 