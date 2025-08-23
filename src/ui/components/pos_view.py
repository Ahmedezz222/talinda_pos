#!/usr/bin/env python3
"""
Modern POS View with Enhanced Items Lookup
==========================================

A completely redesigned POS interface with:
- Advanced search functionality
- Modern card-based UI
- Real-time filtering
- Responsive grid layout
- Category-based navigation
- Quick add to cart functionality

Author: Talinda POS Team
Version: 3.0.0
"""

import sys
import os
import logging
from typing import List, Dict, Optional, Callable
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(current_dir))

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, 
    QLabel, QScrollArea, QFrame, QSizePolicy, QComboBox, QSpacerItem,
    QGroupBox, QButtonGroup, QRadioButton, QCheckBox, QMessageBox,
    QProgressBar, QSlider, QSplitter, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QPropertyAnimation, QEasingCurve, QSize
from PyQt5.QtGui import QIcon, QFont, QPixmap, QPalette, QColor, QPainter

from controllers.pos_controller import POSController
from models.product import Product, Category

logger = logging.getLogger(__name__)


class ModernProductCard(QFrame):
    """Modern product card with enhanced styling and functionality."""
    
    product_selected = pyqtSignal(object)
    
    def __init__(self, product: Product, parent=None):
        super().__init__(parent)
        self.product = product
        self.is_hovered = False
        self.init_ui()
        self.setup_animations()
    
    def init_ui(self):
        """Initialize the modern product card UI."""
        self.setFixedSize(180, 200)
        self.setCursor(Qt.PointingHandCursor)
        self.setObjectName("productCard")
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(12, 12, 12, 12)
        
        # Product image placeholder (can be enhanced later)
        self.image_label = QLabel()
        self.image_label.setFixedSize(80, 80)
        self.image_label.setStyleSheet("""
            QLabel {
                background-color: #f8f9fa;
                border: 2px dashed #dee2e6;
                border-radius: 40px;
                color: #6c757d;
                font-size: 24px;
            }
        """)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setText("📦")
        layout.addWidget(self.image_label, alignment=Qt.AlignCenter)
        
        # Product name
        self.name_label = QLabel(self.product.name)
        self.name_label.setObjectName("productName")
        self.name_label.setAlignment(Qt.AlignCenter)
        self.name_label.setWordWrap(True)
        self.name_label.setMaximumHeight(40)
        layout.addWidget(self.name_label)
        
        # Price
        self.price_label = QLabel(f"${self.product.price:.2f}")
        self.price_label.setObjectName("productPrice")
        self.price_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.price_label)
        
        # Availability status
        self.availability_label = self.create_availability_label()
        layout.addWidget(self.availability_label)
        
        # Add to cart button
        self.add_button = QPushButton("Add to Cart")
        self.add_button.setObjectName("addButton")
        self.add_button.clicked.connect(self.on_add_clicked)
        layout.addWidget(self.add_button)
        
        # Apply modern styling
        self.apply_styling()
    
    def create_availability_label(self) -> QLabel:
        """Create availability label (always available)."""
        availability_label = QLabel()
        availability_label.setAlignment(Qt.AlignCenter)
        availability_label.setMaximumHeight(20)
        availability_label.setText("✅ Available")
        availability_label.setStyleSheet("color: #28a745; font-size: 10px; font-weight: bold;")
        return availability_label
    
    def apply_styling(self):
        """Apply modern styling to the product card."""
        self.setStyleSheet("""
            QFrame#productCard {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 12px;
                padding: 8px;
            }
            QFrame#productCard:hover {
                border-color: #007bff;
                background-color: #f8f9fa;
            }
            QLabel#productName {
                font-size: 14px;
                font-weight: bold;
                color: #212529;
                background-color: transparent;
            }
            QLabel#productPrice {
                font-size: 16px;
                font-weight: bold;
                color: #007bff;
                background-color: transparent;
            }
            QPushButton#addButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton#addButton:hover {
                background-color: #0056b3;
            }
            QPushButton#addButton:pressed {
                background-color: #004085;
            }
            QPushButton#addButton:disabled {
                background-color: #6c757d;
            }
        """)
    
    def setup_animations(self):
        """Setup hover animations."""
        self.hover_animation = QPropertyAnimation(self, b"geometry")
        self.hover_animation.setDuration(150)
        self.hover_animation.setEasingCurve(QEasingCurve.OutCubic)
    
    def enterEvent(self, event):
        """Handle mouse enter event."""
        self.is_hovered = True
        self.apply_hover_effect()
        super().enterEvent(event)
    
    def leaveEvent(self, event):
        """Handle mouse leave event."""
        self.is_hovered = False
        self.remove_hover_effect()
        super().leaveEvent(event)
    
    def apply_hover_effect(self):
        """Apply hover effect animation."""
        current_geometry = self.geometry()
        hover_geometry = current_geometry.adjusted(-2, -2, 2, 2)
        self.hover_animation.setStartValue(current_geometry)
        self.hover_animation.setEndValue(hover_geometry)
        self.hover_animation.start()
    
    def remove_hover_effect(self):
        """Remove hover effect animation."""
        current_geometry = self.geometry()
        normal_geometry = current_geometry.adjusted(2, 2, -2, -2)
        self.hover_animation.setStartValue(current_geometry)
        self.hover_animation.setEndValue(normal_geometry)
        self.hover_animation.start()
    
    def on_add_clicked(self):
        """Handle add to cart button click."""

        
        self.product_selected.emit(self.product)


class CategoryFilterWidget(QWidget):
    """Widget for filtering products by category."""
    
    category_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.categories = []
        self.selected_category = "All"
        self.init_ui()
    
    def init_ui(self):
        """Initialize the category filter UI."""
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Category label
        label = QLabel("Category:")
        label.setStyleSheet("font-weight: bold; color: #495057;")
        layout.addWidget(label)
        
        # Category combo box
        self.category_combo = QComboBox()
        self.category_combo.setMinimumWidth(150)
        self.category_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                padding: 8px 12px;
                background-color: white;
                font-size: 14px;
            }
            QComboBox:hover {
                border-color: #007bff;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
            }
        """)
        self.category_combo.currentTextChanged.connect(self.on_category_changed)
        layout.addWidget(self.category_combo)
        
        layout.addStretch()
    
    def set_categories(self, categories: List[Category]):
        """Set the available categories."""
        self.categories = categories
        self.category_combo.clear()
        self.category_combo.addItem("All Categories")
        
        for category in categories:
            self.category_combo.addItem(category.name)
    
    def on_category_changed(self, category_name: str):
        """Handle category selection change."""
        self.selected_category = category_name
        self.category_changed.emit(category_name)


class SearchWidget(QWidget):
    """Advanced search widget with real-time filtering."""
    
    search_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)
        self.search_timer.timeout.connect(self.perform_search)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the search widget UI."""
        layout = QHBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Search icon
        search_icon = QLabel("🔍")
        search_icon.setStyleSheet("font-size: 18px; color: #6c757d;")
        layout.addWidget(search_icon)
        
        # Search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search products by name, category, or price...")
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e9ecef;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #007bff;
                background-color: #f8f9fa;
            }
        """)
        self.search_input.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.search_input)
        
        # Clear button
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(80, 40)
        self.clear_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        self.clear_button.clicked.connect(self.clear_search)
        layout.addWidget(self.clear_button)
    
    def on_text_changed(self, text: str):
        """Handle search text changes with debouncing."""
        self.search_timer.stop()
        self.search_timer.start(300)  # 300ms delay
    
    def perform_search(self):
        """Perform the actual search."""
        search_text = self.search_input.text().strip()
        self.search_changed.emit(search_text)
    
    def clear_search(self):
        """Clear the search input."""
        self.search_input.clear()
        self.search_changed.emit("")


class ModernPOSView(QWidget):
    """Modern POS view with enhanced items lookup functionality."""
    
    def __init__(self, settings=None, database_manager=None, current_user=None, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.database_manager = database_manager
        self.current_user = current_user
        self.pos_controller = POSController(database_manager, current_user, settings)
        
        # Data storage
        self.all_products = []
        self.filtered_products = []
        self.categories = []
        
        # UI components
        self.search_widget = None
        self.category_filter = None
        self.products_grid = None
        self.products_container = None
        self.products_layout = None
        self.loading_indicator = None
        
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the modern POS interface."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        self.create_header_section(main_layout)
        
        # Search and filter section
        self.create_search_filter_section(main_layout)
        
        # Products grid section
        self.create_products_section(main_layout)
        
        # Loading indicator
        self.create_loading_indicator(main_layout)
        
        # Use responsive sizing
        from utils.responsive_ui import ResponsiveUI
        
        window_size = ResponsiveUI.get_responsive_window_size()
        # Scale down slightly for POS view
        pos_width = int(window_size.width() * 0.9)
        pos_height = int(window_size.height() * 0.9)
        
        self.setMinimumSize(pos_width, pos_height)
        self.resize(pos_width, pos_height)
    
    def create_header_section(self, parent_layout):
        """Create the header section."""
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_frame.setStyleSheet("""
            QFrame#headerFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        header_layout.setSpacing(5)
        
        # Title
        title_label = QLabel("🛒 Modern POS - Items Lookup")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Browse and search products with ease")
        subtitle_label.setStyleSheet("""
            font-size: 14px;
            color: #e3f2fd;
        """)
        subtitle_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(subtitle_label)
        
        parent_layout.addWidget(header_frame)
    
    def create_search_filter_section(self, parent_layout):
        """Create the search and filter section."""
        filter_frame = QFrame()
        filter_frame.setObjectName("filterFrame")
        filter_frame.setStyleSheet("""
            QFrame#filterFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        filter_layout = QVBoxLayout(filter_frame)
        filter_layout.setSpacing(15)
        
        # Search widget
        self.search_widget = SearchWidget()
        self.search_widget.search_changed.connect(self.filter_products)
        filter_layout.addWidget(self.search_widget)
        
        # Category filter
        self.category_filter = CategoryFilterWidget()
        self.category_filter.category_changed.connect(self.filter_products)
        filter_layout.addWidget(self.category_filter)
        
        parent_layout.addWidget(filter_frame)
    
    def create_products_section(self, parent_layout):
        """Create the products grid section."""
        products_frame = QFrame()
        products_frame.setObjectName("productsFrame")
        products_frame.setStyleSheet("""
            QFrame#productsFrame {
                background-color: white;
                border: 2px solid #e9ecef;
                border-radius: 10px;
            }
        """)
        
        products_layout = QVBoxLayout(products_frame)
        products_layout.setSpacing(10)
        products_layout.setContentsMargins(15, 15, 15, 15)
        
        # Products header
        products_header = QLabel("📦 Available Products")
        products_header.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #495057;
        """)
        products_layout.addWidget(products_header)
        
        # Products scroll area
        self.products_scroll = QScrollArea()
        self.products_scroll.setWidgetResizable(True)
        self.products_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.products_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.products_scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #f8f9fa;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #dee2e6;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #adb5bd;
            }
        """)
        
        # Products container
        self.products_container = QWidget()
        self.products_layout = QGridLayout(self.products_container)
        self.products_layout.setSpacing(15)
        self.products_layout.setContentsMargins(10, 10, 10, 10)
        
        self.products_scroll.setWidget(self.products_container)
        products_layout.addWidget(self.products_scroll)
        
        parent_layout.addWidget(products_frame, stretch=1)
    
    def create_loading_indicator(self, parent_layout):
        """Create the loading indicator."""
        self.loading_indicator = QProgressBar()
        self.loading_indicator.setVisible(False)
        self.loading_indicator.setStyleSheet("""
            QProgressBar {
                border: 2px solid #e9ecef;
                border-radius: 6px;
                text-align: center;
                background-color: #f8f9fa;
            }
            QProgressBar::chunk {
                background-color: #007bff;
                border-radius: 4px;
            }
        """)
        parent_layout.addWidget(self.loading_indicator)
    
    def load_data(self):
        """Load categories and products data."""
        self.show_loading(True)
        
        try:
            # Load categories
            self.categories = self.pos_controller.get_categories()
            self.category_filter.set_categories(self.categories)
            
            # Load products
            self.all_products = self.pos_controller.get_products()
            self.filtered_products = self.all_products.copy()
            
            # Display products
            self.display_products()
            
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to load data: {str(e)}")
        finally:
            self.show_loading(False)
    
    def show_loading(self, show: bool):
        """Show or hide the loading indicator."""
        self.loading_indicator.setVisible(show)
        if show:
            self.loading_indicator.setRange(0, 0)  # Indeterminate progress
    
    def filter_products(self):
        """Filter products based on search text and category."""
        search_text = self.search_widget.search_input.text().strip().lower()
        selected_category = self.category_filter.selected_category
        
        self.filtered_products = []
        
        for product in self.all_products:
            # Check if product matches search criteria
            matches_search = (
                search_text == "" or
                search_text in product.name.lower() or
                search_text in str(product.price).lower() or
                (hasattr(product, 'category') and product.category and 
                 search_text in product.category.name.lower())
            )
            
            # Check if product matches category filter
            matches_category = (
                selected_category == "All Categories" or
                (hasattr(product, 'category') and product.category and 
                 product.category.name == selected_category)
            )
            
            if matches_search and matches_category:
                self.filtered_products.append(product)
        
        self.display_products()
    
    def display_products(self):
        """Display the filtered products in the grid."""
        # Clear existing products
        self.clear_products_grid()
        
        if not self.filtered_products:
            self.show_no_products_message()
            return
        
        # Calculate grid layout
        available_width = self.products_scroll.width() - 40  # Account for margins
        card_width = 180
        max_cols = max(1, available_width // card_width)
        
        # Add product cards to grid
        for idx, product in enumerate(self.filtered_products):
            try:
                card = ModernProductCard(product)
                card.product_selected.connect(self.on_product_selected)
                
                row = idx // max_cols
                col = idx % max_cols
                self.products_layout.addWidget(card, row, col)
                
            except Exception as e:
                logger.error(f"Error creating product card for {product.name}: {str(e)}")
                continue
    
    def clear_products_grid(self):
        """Clear all products from the grid."""
        while self.products_layout.count():
            child = self.products_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def show_no_products_message(self):
        """Show a message when no products are found."""
        no_products_label = QLabel("No products found matching your criteria")
        no_products_label.setStyleSheet("""
            font-size: 16px;
            color: #6c757d;
            padding: 40px;
        """)
        no_products_label.setAlignment(Qt.AlignCenter)
        self.products_layout.addWidget(no_products_label, 0, 0)
    
    def on_product_selected(self, product: Product):
        """Handle product selection."""
        try:

            
            # Emit signal for cart integration
            # This can be connected to the cart widget
            logger.info(f"Product selected: {product.name}")
            
            # Show confirmation
            QMessageBox.information(self, "Added to Cart", f"{product.name} has been added to your cart!")
            
        except Exception as e:
            logger.error(f"Error handling product selection: {str(e)}")
            QMessageBox.critical(self, "Error", f"Failed to add product to cart: {str(e)}")
    
    def resizeEvent(self, event):
        """Handle resize events to adjust grid layout."""
        super().resizeEvent(event)
        # Redisplay products to adjust grid layout
        QTimer.singleShot(100, self.display_products)


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from database.database_manager import DatabaseManager
    
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create database manager
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    
    # Create and show POS view
    pos_view = ModernPOSView(database_manager=db_manager)
    pos_view.setWindowTitle("Modern POS - Items Lookup")
    pos_view.show()
    
    sys.exit(app.exec_()) 