#!/usr/bin/env python3
"""
Test script to verify category grid improvements
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from ui.main_window import ModernPOSWidget
from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController
from models.user import User, UserRole

def test_category_grid():
    """Test the improved category grid layout."""
    app = QApplication(sys.argv)
    
    # Create a test user
    test_user = User(
        id=1,
        username="test_user",
        role=UserRole.CASHIER,
        active=True
    )
    
    # Create controllers
    product_controller = ProductController()
    sale_controller = SaleController()
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Category Grid Test")
    main_window.resize(1200, 800)
    
    # Create central widget
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    
    # Create layout
    layout = QVBoxLayout(central_widget)
    
    # Create POS widget
    pos_widget = ModernPOSWidget(test_user, product_controller, sale_controller)
    layout.addWidget(pos_widget)
    
    # Show the window
    main_window.show()
    
    print("Category grid test window opened.")
    print("Features to test:")
    print("1. Responsive grid layout (resize window)")
    print("2. Category cards with icons and gradients")
    print("3. Hover effects and animations")
    print("4. Proper spacing and alignment")
    
    return app.exec_()

if __name__ == "__main__":
    test_category_grid() 