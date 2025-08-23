"""
Test script to verify the enhanced cart widget styling and functionality.
This script can be run to test the visual enhancements made to the cart widget.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from ui.components.enhanced_cart_widget import EnhancedCartWidget
from controllers.sale_controller import SaleController
from models.user import User, UserRole

class TestWindow(QMainWindow):
    """Test window to display the enhanced cart widget."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Enhanced Cart Widget Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create a test user
        test_user = User(
            id=1,
            username="test_user",
            password_hash="test_hash",
            role=UserRole.ADMIN
        )
        
        # Create sale controller
        sale_controller = SaleController()
        
        # Create cart widget
        self.cart_widget = EnhancedCartWidget(sale_controller, test_user)
        
        # Set up main layout
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addWidget(self.cart_widget)
        self.setCentralWidget(central_widget)
        
        # Add some test items to the cart
        self.add_test_items()
    
    def add_test_items(self):
        """Add test items to the cart for demonstration."""
        from models.product import Product, ProductCategory
        
        # Create test products
        test_products = [
            Product(id=1, name="Test Product 1", price=10.99, stock_quantity=100, 
                   category=ProductCategory.FOOD, description="Test product 1"),
            Product(id=2, name="Test Product 2 with a longer name", price=5.50, stock_quantity=50,
                   category=ProductCategory.DRINK, description="Test product 2"),
            Product(id=3, name="Test Product 3", price=25.75, stock_quantity=25,
                   category=ProductCategory.OTHER, description="Test product 3")
        ]
        
        # Add products to cart
        for product in test_products:
            self.cart_widget.add_item(product)

def main():
    """Main function to run the test."""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show test window
    window = TestWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
