"""
Product card component for displaying products in the POS interface.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

# Import ResponsiveUI
from utils.responsive_ui import ResponsiveUI

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
        # Use responsive sizing
        from utils.responsive_ui import ResponsiveUI
        
        card_size = ResponsiveUI.get_responsive_card_size()
        self.setFixedSize(card_size.width(), card_size.height())
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
        # Use responsive image size
        card_size = ResponsiveUI.get_responsive_card_size()
        img_width = int(card_size.width() * 0.4)  # 40% of card width
        img_height = int(card_size.height() * 0.45)  # 45% of card height
        
        image_container.setFixedSize(img_width, img_height)
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
        """Create the information section of the product card."""
        self.info_container = QFrame(self)
        self.info_container.setObjectName("infoContainer")
        info_layout = QVBoxLayout(self.info_container)
        info_layout.setContentsMargins(4, 4, 4, 4)
        info_layout.setSpacing(2)

        # Product Name with fixed height and elided text
        self.name_label = QLabel(self.product.name, self.info_container)
        self.name_label.setObjectName("productName")
        self.name_label.setWordWrap(True)
        self.name_label.setFixedHeight(40)  # Fixed height for consistent sizing
        
        # Elide text if too long
        metrics = self.name_label.fontMetrics()
        elided_text = metrics.elidedText(
            self.product.name, Qt.ElideRight, self.name_label.width() - 10
        )
        self.name_label.setText(elided_text)
        info_layout.addWidget(self.name_label)
        
        # Add the price label
        price_label = QLabel(f"${self.product.price:.2f}", self.info_container)
        price_label.setObjectName("productPrice")
        price_label.setAlignment(Qt.AlignCenter)
        info_layout.addWidget(price_label)
        
        # Add the stock indicator
        stock_label = self.create_stock_label()
        info_layout.addWidget(stock_label, alignment=Qt.AlignCenter)
        
        # Add the info container to the main layout
        layout.addWidget(self.info_container)
    
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
                border: 2px solid #e0e0e0;
                border-radius: 10px;
                padding: 8px;
            }
            ProductCard:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #ffffff);
                border: 2px solid #2196F3;
            }
            QFrame#imageContainer {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2196F3, stop:1 #1976D2);
                border-radius: 8px;
                border: none;
                min-height: 60px;
                max-height: 60px;
                margin: 2px;
            }
            QFrame#imageContainer QLabel {
                font-size: 32px;
                color: white;
            }
            QFrame#infoContainer {
                background-color: transparent;
                border: none;
                margin-top: 12px;
                padding: 4px;
            }
            QLabel#productName {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                font-weight: bold;
                font-size: 12px;
                color: #2c3e50;
                background-color: #f8f9fa;
                padding: 4px 8px;
                border-radius: 6px;
                qproperty-alignment: AlignCenter;
                margin: 2px;
                min-height: 30px;
            }
            QLabel#productPrice {
                color: #00796B;
                font-size: 13px;
                font-weight: bold;
                background-color: #E0F2F1;
                padding: 4px 8px;
                border-radius: 6px;
                margin: 4px 2px;
            }
            QLabel#productStock {
                color: #43A047;
                font-size: 13px;
                font-weight: bold;
                background-color: #E8F5E9;
                padding: 6px;
                border-radius: 6px;
                margin: 4px;
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
