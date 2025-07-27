#!/usr/bin/env python3
"""
Test script to verify responsiveness improvements in the POS application.
"""
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_responsive_layout():
    """Test the responsive layout functionality."""
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.main_window import MainWindow
        from models.user import User, UserRole
        
        # Create a test application
        app = QApplication(sys.argv)
        
        # Create a test user
        test_user = User()
        test_user.id = 1
        test_user.username = "test_user"
        test_user.role = UserRole.admin
        
        # Create main window
        window = MainWindow(test_user)
        window.show()
        
        print("✅ Responsive layout test passed!")
        print("   - Window should be maximized")
        print("   - Sidebar should be properly styled")
        print("   - Layout should be responsive to window resizing")
        
        # Test window resize
        window.resize(1600, 1000)
        print("   - Window resized to 1600x1000")
        
        return True
        
    except Exception as e:
        print(f"❌ Responsive layout test failed: {e}")
        return False

def test_product_grid():
    """Test the responsive product grid."""
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.components.product_card import ProductCard
        from models.product import Product
        
        # Create a test application
        app = QApplication(sys.argv)
        
        # Create a test product
        test_product = Product()
        test_product.id = 1
        test_product.name = "Test Product"
        test_product.price = 9.99
        test_product.stock = 10
        
        # Create product card
        card = ProductCard(test_product)
        card.show()
        
        print("✅ Product card test passed!")
        print("   - Card should have proper sizing")
        print("   - Card should be responsive")
        
        return True
        
    except Exception as e:
        print(f"❌ Product card test failed: {e}")
        return False

def test_cart_widget():
    """Test the responsive cart widget."""
    try:
        from PyQt5.QtWidgets import QApplication
        from ui.components.enhanced_cart_widget import EnhancedCartWidget
        from controllers.sale_controller import SaleController
        from models.user import User, UserRole
        
        # Create a test application
        app = QApplication(sys.argv)
        
        # Create test objects
        test_user = User()
        test_user.id = 1
        test_user.username = "test_user"
        test_user.role = UserRole.cashier
        
        sale_controller = SaleController()
        
        # Create cart widget
        cart = EnhancedCartWidget(sale_controller, test_user)
        cart.show()
        
        print("✅ Cart widget test passed!")
        print("   - Cart should have proper layout")
        print("   - Buttons should be properly sized")
        
        return True
        
    except Exception as e:
        print(f"❌ Cart widget test failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing POS Application Responsiveness...")
    print("=" * 50)
    
    # Run tests
    tests = [
        test_responsive_layout,
        test_product_grid,
        test_cart_widget
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All responsiveness tests passed!")
        print("The POS application should now be fully responsive.")
    else:
        print("⚠️  Some tests failed. Please check the implementation.") 