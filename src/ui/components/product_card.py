"""
Product card component for displaying products in the POS interface.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                           QPushButton, QFrame)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from models.product import Product

class ProductCard(QFrame):
    """Widget for displaying a product in the grid."""
    
    # Signal emitted when product is selected
    product_selected = pyqtSignal(object)
    
    def __init__(self, product: Product):
        """Initialize the product card."""
        super().__init__()
        self.product = product
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('''
            ProductCard, QFrame {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 12px 8px 12px 8px;
                min-width: 140px;
                max-width: 180px;
                min-height: 120px;
                max-height: 140px;
            }
            ProductCard:hover, QFrame:hover {
                border-color: #7c4dff;
                background-color: #f8f4ff;
            }
            QLabel#productName {
                font-weight: bold;
                font-size: 13px;
                color: #2d224c;
                margin-bottom: 8px;
                min-height: 40px;
                max-height: 60px;
                background-color: transparent;
            }
            QLabel#productPrice {
                color: #d500f9;
                font-size: 16px;
                font-weight: bold;
                margin-bottom: 4px;
                background-color: transparent;
            }
            QLabel#productStock {
                color: #6d6d6d;
                font-size: 11px;
                margin-bottom: 4px;
                background-color: transparent;
            }
        ''')
        
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(8, 8, 8, 8)
        
        try:
            # Product name
            name_label = QLabel(self.product.name)
            name_label.setObjectName('productName')
            name_label.setAlignment(Qt.AlignCenter)
            name_label.setWordWrap(True)
            name_label.setMinimumHeight(40)
            name_label.setMaximumHeight(60)
            layout.addWidget(name_label)
            
            # Price
            price_label = QLabel(f"${self.product.price:.2f}")
            price_label.setObjectName('productPrice')
            price_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(price_label)
            
            # Stock (small indicator)
            if hasattr(self.product, 'stock') and self.product.stock is not None:
                if self.product.stock <= 0:
                    stock_label = QLabel("OUT OF STOCK")
                    stock_label.setStyleSheet("color: #e74c3c; font-size: 10px; font-weight: bold; background-color: transparent;")
                elif self.product.stock <= 5:
                    stock_label = QLabel(f"Low Stock: {self.product.stock}")
                    stock_label.setStyleSheet("color: #f39c12; font-size: 10px; font-weight: bold; background-color: transparent;")
                else:
                    stock_label = QLabel(f"In Stock: {self.product.stock}")
                    stock_label.setStyleSheet("color: #27ae60; font-size: 10px; font-weight: bold; background-color: transparent;")
            else:
                stock_label = QLabel("Stock: N/A")
                stock_label.setStyleSheet("color: #95a5a6; font-size: 10px; font-weight: bold; background-color: transparent;")
            
            stock_label.setObjectName('productStock')
            stock_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(stock_label)
            
        except Exception as e:
            # Fallback display if there's an error
            error_label = QLabel("Product Error")
            error_label.setStyleSheet("color: #e74c3c; font-size: 12px; font-weight: bold; background-color: transparent;")
            error_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(error_label)
            print(f"Error creating product card: {str(e)}")
        
        # Add stretch to push everything to the top
        layout.addStretch()
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
    def mousePressEvent(self, event):
        """Handle mouse press events to select the product."""
        if event.button() == Qt.LeftButton:
            try:
                # Check if product is in stock before allowing selection
                if hasattr(self.product, 'stock') and self.product.stock is not None and self.product.stock > 0:
                    self.product_selected.emit(self.product)
                else:
                    from PyQt5.QtWidgets import QMessageBox
                    QMessageBox.warning(self, "Out of Stock", f"{self.product.name} is currently out of stock!")
            except Exception as e:
                print(f"Error selecting product: {str(e)}")
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse enter events for hover effects."""
        self.setStyleSheet(self.styleSheet().replace(
            'border: 2px solid #e0e0e0;',
            'border: 2px solid #7c4dff;'
        ))
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave events to reset hover effects."""
        self.setStyleSheet(self.styleSheet().replace(
            'border: 2px solid #7c4dff;',
            'border: 2px solid #e0e0e0;'
        ))
        super().leaveEvent(event)
