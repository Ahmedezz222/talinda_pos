"""
Product card component for displaying products in the POS interface.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel,
                           QPushButton, QFrame, QHBoxLayout)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QFont, QPainter, QColor, QLinearGradient
from models.product import Product

class ProductCard(QFrame):
    """Widget for displaying a product in the grid."""
    
    # Signal emitted when product is selected
    product_selected = pyqtSignal(object)
    
    def __init__(self, product: Product):
        """Initialize the product card."""
        super().__init__()
        self.product = product
        self.is_hovered = False
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setFrameStyle(QFrame.NoFrame)
        self.setFixedSize(200, 160)
        self.setCursor(Qt.PointingHandCursor)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Product image/icon section
        self.create_image_section(layout)
        
        # Product info section
        self.create_info_section(layout)
        
        # Apply modern styling
        self.apply_styling()
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
    
    def create_image_section(self, layout):
        """Create the product image/icon section."""
        # Image container
        image_container = QFrame()
        image_container.setFixedSize(80, 60)
        image_container.setObjectName("imageContainer")
        
        # Product icon/emoji based on category
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 32px; color: #ffffff;")
        
        # Set icon based on product name or category
        icon = self.get_product_icon()
        icon_label.setText(icon)
        
        image_layout = QVBoxLayout(image_container)
        image_layout.addWidget(icon_label)
        layout.addWidget(image_container, alignment=Qt.AlignCenter)
    
    def get_product_icon(self):
        """Get appropriate icon for the product."""
        name_lower = self.product.name.lower()
        
        # Food items
        if any(word in name_lower for word in ['sushi', 'maki', 'nigiri', 'sashimi']):
            return '🍣'
        elif any(word in name_lower for word in ['pizza', 'burger', 'sandwich']):
            return '🍕'
        elif any(word in name_lower for word in ['salad', 'vegetable']):
            return '🥗'
        elif any(word in name_lower for word in ['chicken', 'meat', 'beef']):
            return '🍖'
        elif any(word in name_lower for word in ['fish', 'seafood']):
            return '🐟'
        
        # Drinks
        elif any(word in name_lower for word in ['coffee', 'tea', 'hot']):
            return '☕'
        elif any(word in name_lower for word in ['juice', 'soda', 'drink']):
            return '🥤'
        elif any(word in name_lower for word in ['beer', 'wine', 'alcohol']):
            return '🍺'
        
        # Desserts
        elif any(word in name_lower for word in ['cake', 'dessert', 'sweet']):
            return '🍰'
        elif any(word in name_lower for word in ['ice cream']):
            return '🍦'
        
        # Default
        else:
            return '📦'
    
    def create_info_section(self, layout):
        """Create the product information section."""
        # Product name
        name_label = QLabel(self.product.name)
        name_label.setObjectName('productName')
        name_label.setAlignment(Qt.AlignCenter)
        name_label.setWordWrap(True)
        name_label.setMaximumHeight(40)
        layout.addWidget(name_label)
        
        # Price and stock row
        info_layout = QHBoxLayout()
        
        # Price
        price_label = QLabel(f"${self.product.price:.2f}")
        price_label.setObjectName('productPrice')
        price_label.setAlignment(Qt.AlignLeft)
        info_layout.addWidget(price_label)
        
        # Stock indicator
        stock_label = self.create_stock_label()
        stock_label.setAlignment(Qt.AlignRight)
        info_layout.addWidget(stock_label)
        
        layout.addLayout(info_layout)
    
    def create_stock_label(self) -> QLabel:
        """Create availability label (always available)."""
        stock_label = QLabel()
        stock_label.setObjectName('productStock')
        stock_label.setText("✅")
        stock_label.setToolTip("Available")
        return stock_label
    
    def apply_styling(self):
        """Apply modern styling to the product card."""
        self.setStyleSheet('''
            ProductCard {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #f8f9fa);
                border: 2px solid #e9ecef;
                border-radius: 16px;
                padding: 8px;
            }
            ProductCard:hover {
                border-color: #007bff;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:1 #e3f2fd);
                transform: translateY(-2px);
            }
            QFrame#imageContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 12px;
                border: none;
            }
            QLabel#productName {
                font-weight: bold;
                font-size: 14px;
                color: #212529;
                background-color: transparent;
                margin: 4px 0;
            }
            QLabel#productPrice {
                color: #28a745;
                font-size: 18px;
                font-weight: bold;
                background-color: transparent;
            }
            QLabel#productStock {
                color: #6c757d;
                font-size: 12px;
                font-weight: bold;
                background-color: transparent;
            }
        ''')
    
    def mousePressEvent(self, event):
        """Handle mouse press events to select the product."""
        if event.button() == Qt.LeftButton:
            try:
                self.product_selected.emit(self.product)
            except Exception as e:
                print(f"Error selecting product: {str(e)}")
        super().mousePressEvent(event)
    
    def enterEvent(self, event):
        """Handle mouse enter events for hover effects."""
        self.is_hovered = True
        self.update()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave events to reset hover effects."""
        self.is_hovered = False
        self.update()
        super().leaveEvent(event)
    
    def paintEvent(self, event):
        """Custom paint event for enhanced visual effects."""
        super().paintEvent(event)
        
        if self.is_hovered:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing)
            
            # Create subtle shadow effect
            shadow_color = QColor(0, 123, 255, 30)
            painter.setPen(Qt.NoPen)
            painter.setBrush(shadow_color)
            painter.drawRoundedRect(self.rect().adjusted(2, 2, 2, 2), 16, 16)
