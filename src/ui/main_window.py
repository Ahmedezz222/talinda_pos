#!/usr/bin/env python3
"""
Talinda POS System - Main Window
================================

Modern, professional main window for the POS system with enhanced UI/UX.
"""

import sys
import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(current_dir))

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QGridLayout, QStackedWidget, QDialog, QMessageBox,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox, QListWidget, 
    QListWidgetItem, QSizePolicy, QFrame, QSplitter, QToolBar, QStatusBar,
    QProgressBar, QSpacerItem, QButtonGroup, QRadioButton, QCheckBox,
    QTabWidget, QGroupBox, QFormLayout, QSpinBox, QDoubleSpinBox,
    QTextEdit, QDateEdit, QTimeEdit, QCalendarWidget, QMenu, QAction,
    QToolButton, QSlider, QProgressDialog, QInputDialog, QFileDialog
)
from PyQt5.QtGui import (
    QPixmap, QFont, QIcon, QPalette, QColor, QPainter, QBrush, 
    QLinearGradient, QRadialGradient, QPen, QFontMetrics
)
from PyQt5.QtCore import (
    Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve,
    QSize, QRect, QPoint, QDate, QTime, QDateTime, QUrl
)

import bcrypt
from controllers.auth_controller import AuthController
from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController
from database.database_manager import DatabaseManager
from ui.components.enhanced_cart_widget import EnhancedCartWidget
from ui.components.product_card import ProductCard
from ui.components.add_product_page import AddProductPage
from ui.components.order_widget import OrderManagementWidget
from ui.components import ShowProductsWindow
from ui.components.pos_view import ModernPOSView
from ui.components.language_selector import LanguageSelectorDialog
from models.user import UserRole, User
from utils.localization import tr, set_language, is_rtl


class ModernPOSWidget(QWidget):
    """Modern POS widget with enhanced UI and functionality."""
    
    def __init__(self, user, product_controller, sale_controller):
        super().__init__()
        self.user = user
        self.product_controller = product_controller
        self.sale_controller = sale_controller
        self.current_category = None
        self.category_buttons = {}
        self.product_cards = {}
        self.logger = logging.getLogger(__name__)
        
        self.init_ui()
        self.setup_connections()
        self.load_data()
    
    def init_ui(self):
        """Initialize the modern POS interface."""
        # Main layout with splitter for better resizing
        main_layout = QHBoxLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable sections
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)
        splitter.setHandleWidth(2)
        splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #e0e0e0;
                border: none;
            }
            QSplitter::handle:hover {
                background-color: #1976d2;
            }
        """)
        
        # Left panel - Categories and Products
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Cart
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter proportions (70% left, 30% right)
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter)
    
    def create_left_panel(self) -> QWidget:
        """Create the left panel with categories and products."""
        panel = QWidget()
        panel.setObjectName("leftPanel")
        panel.setStyleSheet("""
            QWidget#leftPanel {
                background-color: #f8f9fa;
                border-right: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        header = self.create_header_section()
        layout.addWidget(header)
        
        # Products section (will show categories or products)
        products_section = self.create_products_section()
        layout.addWidget(products_section, 1)  # Take remaining space
        
        return panel
    
    def create_header_section(self) -> QWidget:
        """Create the header section with title and user info."""
        header = QFrame()
        header.setObjectName("headerSection")
        header.setStyleSheet("""
            QFrame#headerSection {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #1976d2, stop:1 #42a5f5);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        header.setFixedHeight(80)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(20, 15, 20, 15)
        
        # Title and subtitle
        title_layout = QVBoxLayout()
        title = QLabel("🛒 Point of Sale")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: white;
        """)
        
        self.subtitle = QLabel(f"Welcome, {self.user.username} ({self.user.role.value.title()})")
        self.subtitle.setStyleSheet("""
            font-size: 12px;
            color: rgba(255, 255, 255, 0.8);
        """)
        
        title_layout.addWidget(title)
        title_layout.addWidget(self.subtitle)
        layout.addLayout(title_layout)
        
        layout.addStretch()
        
        # Current time display
        self.time_label = QLabel()
        self.time_label.setStyleSheet("""
            font-size: 14px;
            color: white;
            font-weight: bold;
        """)
        layout.addWidget(self.time_label)
        
        # Update time every second
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
        
        return header
    
    def create_categories_section(self) -> QWidget:
        """Create the categories section with modern buttons."""
        section = QGroupBox("📂 Categories")
        section.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 25, 15, 15)
        
        # Categories scroll area
        self.categories_scroll = QScrollArea()
        self.categories_scroll.setWidgetResizable(True)
        self.categories_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.categories_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.categories_scroll.setMaximumHeight(120)
        self.categories_scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
            }
            QScrollBar:vertical {
                width: 8px;
                background: #f0f0f0;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 4px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
        """)
        
        # Categories container
        self.categories_container = QWidget()
        self.categories_layout = QGridLayout(self.categories_container)
        self.categories_layout.setSpacing(8)
        self.categories_layout.setContentsMargins(10, 10, 10, 10)
        
        self.categories_scroll.setWidget(self.categories_container)
        layout.addWidget(self.categories_scroll)
        
        return section
    
    def create_products_section(self) -> QWidget:
        """Create the products section with improved grid layout."""
        section = QGroupBox("🛍️ Items")
        section.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 25, 15, 15)
        
        # Back button (hidden initially) with improved styling
        self.back_btn = QPushButton("← Back to Categories")
        self.back_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: 2px solid #7f8c8d;
                border-radius: 8px;
                padding: 10px 20px;
                font-size: 13px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #7f8c8d, stop:1 #95a5a6);
                border: 2px solid #6c7b7d;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6c7b7d, stop:1 #7f8c8d);
            }
        """)
        self.back_btn.clicked.connect(self.show_categories)
        self.back_btn.hide()
        layout.addWidget(self.back_btn)
        
        # Items scroll area with improved styling
        self.products_scroll = QScrollArea()
        self.products_scroll.setWidgetResizable(True)
        self.products_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.products_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.products_scroll.setStyleSheet("""
            QScrollArea {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
            QScrollBar:vertical {
                width: 10px;
                background: #f0f0f0;
                border-radius: 5px;
                margin: 2px;
            }
            QScrollBar::handle:vertical {
                background: #c0c0c0;
                border-radius: 5px;
                min-height: 30px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: #a0a0a0;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Items container with improved grid layout
        self.products_container = QWidget()
        self.products_layout = QGridLayout(self.products_container)
        self.products_layout.setSpacing(15)
        self.products_layout.setContentsMargins(20, 20, 20, 20)
        
        self.products_scroll.setWidget(self.products_container)
        layout.addWidget(self.products_scroll)
        
        return section
    
    def create_right_panel(self) -> QWidget:
        """Create the right panel with cart."""
        panel = QWidget()
        panel.setObjectName("rightPanel")
        panel.setStyleSheet("""
            QWidget#rightPanel {
                background-color: white;
                border-left: 1px solid #e0e0e0;
            }
        """)
        
        layout = QVBoxLayout(panel)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Enhanced cart widget
        self.cart_widget = EnhancedCartWidget(self.sale_controller, self.user)
        layout.addWidget(self.cart_widget)
        
        return panel
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect cart signals
        if hasattr(self.cart_widget, 'product_added'):
            self.cart_widget.product_added.connect(self.on_product_added)
        if hasattr(self.cart_widget, 'product_removed'):
            self.cart_widget.product_removed.connect(self.on_product_removed)
        # Connect order saved signal to refresh order management
        if hasattr(self.cart_widget, 'order_saved'):
            self.cart_widget.order_saved.connect(self.on_order_saved)
    
    def load_data(self):
        """Load categories and products."""
        try:
            self.show_categories()
        except Exception as e:
            self.logger.error(f"Error loading data: {str(e)}")
    
    def show_categories(self):
        """Show categories as clickable items."""
        # Clear existing items safely
        self.clear_all_widgets()
        
        # Update header
        self.subtitle.setText(f"Welcome, {self.user.username} ({self.user.role.value.title()}) - Browse Categories")
        
        try:
            categories = self.product_controller.get_categories()
        except Exception as e:
            self.logger.error(f"Failed to load categories: {str(e)}")
            return
        
        # Category color scheme with Arabic categories
        category_colors = {
            'FOOD': {'bg': '#ff6b6b', 'text': 'white'},
            'DRINKS': {'bg': '#4ecdc4', 'text': 'white'},
            'SETS': {'bg': '#45b7d1', 'text': 'white'},
            'MAKIS': {'bg': '#96ceb4', 'text': 'white'},
            'NIGIRIS': {'bg': '#feca57', 'text': 'black'},
            'SASHIMI': {'bg': '#ff9ff3', 'text': 'white'},
            'GUNKANS': {'bg': '#54a0ff', 'text': 'white'},
            'FINGER FOOD': {'bg': '#5f27cd', 'text': 'white'},
            'HANDROLLS': {'bg': '#00d2d3', 'text': 'white'},
            'DESERTS': {'bg': '#ff9f43', 'text': 'white'},
            'SIDE DISHES': {'bg': '#10ac84', 'text': 'white'},
            'SPECIAL MAKIS': {'bg': '#ee5a24', 'text': 'white'},
            'ALCOHOL': {'bg': '#2f3542', 'text': 'white'},
            'FRIS': {'bg': '#747d8c', 'text': 'white'},
            'HOT DRINKS': {'bg': '#a55eea', 'text': 'white'},
            'CUSTOM FOOD PRICE': {'bg': '#26de81', 'text': 'white'},
        }
        
        # Calculate responsive grid columns using helper function
        card_width = 180  # Slightly smaller for better fit
        card_height = 140  # Consistent height
        spacing = 15  # Consistent spacing
        
        # Calculate max columns with proper spacing
        max_cols = self.calculate_optimal_grid_columns(card_width, spacing)
        
        row = 0
        col = 0
        
        for category in categories:
            category_name = category.name  # Use exact name, no uppercase conversion
            
            if category_name in category_colors:
                colors = category_colors[category_name]
                btn = self.create_category_card(
                    category.name, 
                    colors['bg'], 
                    colors['text'], 
                    card_width,
                    card_height
                )
            else:
                btn = self.create_category_card(
                    category.name, 
                    '#95a5a6', 
                    'white', 
                    card_width,
                    card_height
                )
            
            self.products_layout.addWidget(btn, row, col)
            self.category_buttons[category.name] = btn
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Hide back button when showing categories
        self.back_btn.hide()
        self.current_category = None
    
    def create_category_card(self, text: str, bg_color: str, text_color: str, width: int, height: int) -> QPushButton:
        """Create a category card with improved styling and layout."""
        btn = QPushButton()
        btn.setFixedSize(width, height)
        btn.setCursor(Qt.PointingHandCursor)
        
        # Create simple text without icon
        btn.setText(text)
        
        # Enhanced styling with better visual hierarchy (Qt-compatible)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {bg_color}, stop:1 {self.darken_color(bg_color)});
                color: {text_color};
                border: 2px solid {self.lighten_color(bg_color)};
                border-radius: 12px;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
                text-align: center;
                margin: 2px;
            }}
            QPushButton:hover {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.lighten_color(bg_color)}, stop:1 {bg_color});
                border: 3px solid white;
            }}
            QPushButton:pressed {{
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 {self.darken_color(bg_color)}, stop:1 {bg_color});
                border: 2px solid {self.darken_color(bg_color)};
            }}
        """)
        
        btn.clicked.connect(lambda: self.select_category(text))
        return btn
    
    def load_products(self):
        """Load and display products in a responsive grid."""
        # Clear existing products safely
        self.clear_all_widgets()
        
        try:
            if self.current_category:
                # Find the category object
                categories = self.product_controller.get_categories()
                category_obj = None
                for cat in categories:
                    if cat.name == self.current_category:
                        category_obj = cat
                        break
                products = self.product_controller.get_products(category_obj)
            else:
                products = self.product_controller.get_products()
        except Exception as e:
            self.logger.error(f"Failed to load products: {str(e)}")
            return
        
        # Calculate responsive grid columns using helper function
        card_width = 200  # Product cards can be larger
        spacing = 15
        max_cols = self.calculate_optimal_grid_columns(card_width, spacing)
        
        row = 0
        col = 0
        
        for product in products:
            try:
                card = ProductCard(product)
                # Connect the product_selected signal to the cart widget
                card.product_selected.connect(self.cart_widget.add_item)
                self.products_layout.addWidget(card, row, col)
                self.product_cards[product.id] = card
                
                col += 1
                if col >= max_cols:
                    col = 0
                    row += 1
            except Exception as e:
                self.logger.error(f"Error creating product card for {product.name}: {str(e)}")
                continue
    
    def select_category(self, category_name: str):
        """Handle category selection and show products."""
        self.current_category = category_name
        
        # Update header
        self.subtitle.setText(f"Welcome, {self.user.username} ({self.user.role.value.title()}) - {category_name}")
        
        # Show back button
        self.back_btn.show()
        
        # Load products for this category
        self.load_products()
    
    def update_time(self):
        """Update the time display."""
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.time_label.setText(f"🕐 {current_time}")
    
    def on_product_added(self, product_id: int):
        """Handle product added to cart."""
        self.logger.info(f"Product {product_id} added to cart")
    
    def on_product_removed(self, product_id: int):
        """Handle product removed from cart."""
        self.logger.info(f"Product {product_id} removed from cart")
    
    def on_order_saved(self, order):
        """Handle order saved signal from cart widget."""
        if order is None:
            self.logger.warning("Order saved signal received with None order")
            return
        
        self.logger.info(f"Order saved from POS widget: {order.order_number}")
        # Forward the signal to the main window if it exists
        if hasattr(self, 'parent') and self.parent():
            main_window = self.parent()
            while main_window and not hasattr(main_window, 'on_order_saved'):
                main_window = main_window.parent()
            if main_window and hasattr(main_window, 'on_order_saved'):
                main_window.on_order_saved(order)
    
    def resizeEvent(self, event):
        """Handle resize events for responsive design."""
        super().resizeEvent(event)
        # Reload current view to adjust grid layout with a slight delay
        QTimer.singleShot(150, self.reload_current_view)
    
    def reload_current_view(self):
        """Reload the current view (categories or products)."""
        try:
            if self.current_category:
                self.load_products()
            else:
                self.show_categories()
        except Exception as e:
            self.logger.error(f"Error reloading current view: {str(e)}")
    
    def calculate_optimal_grid_columns(self, card_width: int, spacing: int = 15) -> int:
        """Calculate optimal number of columns for the current window size."""
        available_width = max(400, self.width() - 400)
        max_cols = max(3, min(5, int((available_width - spacing) / (card_width + spacing))))
        return max_cols
    
    def lighten_color(self, color: str) -> str:
        """Lighten a hex color."""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            lightened = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"
        except:
            return color
    
    def darken_color(self, color: str) -> str:
        """Darken a hex color."""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        except:
            return color

    def clear_all_widgets(self):
        """Safely clear all widgets from the products layout."""
        # Disconnect signals from stored widgets before clearing
        for btn in self.category_buttons.values():
            if btn and not btn.isHidden():
                try:
                    btn.clicked.disconnect()
                except (TypeError, RuntimeError):
                    pass  # Signal already disconnected
        
        for card in self.product_cards.values():
            if card and not card.isHidden():
                try:
                    # Disconnect any signals from product cards
                    card.deleteLater()
                except (TypeError, RuntimeError):
                    pass  # Widget already deleted
        
        # Clear stored references
        self.category_buttons.clear()
        self.product_cards.clear()
        
        # Clear layout safely
        while self.products_layout.count():
            item = self.products_layout.takeAt(0)
            if item.widget():
                widget = item.widget()
                try:
                    widget.setParent(None)
                    widget.deleteLater()
                except (TypeError, RuntimeError):
                    pass  # Widget already deleted or invalid


class ModernAdminPanelWidget(QWidget):
    """Modern admin panel with enhanced functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.logger = logging.getLogger(__name__)
        self.init_ui()
        self.load_users()
    
    def init_ui(self):
        """Initialize the admin panel UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header
        header = QLabel("⚙️ Admin Panel")
        header.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(header)
        
        # Reports section
        reports_section = self.create_reports_section()
        layout.addWidget(reports_section)
        
        # User management section
        user_section = self.create_user_management_section()
        layout.addWidget(user_section)
        
        # System info section
        system_section = self.create_system_info_section()
        layout.addWidget(system_section)
    
    def create_user_management_section(self) -> QWidget:
        """Create user management section."""
        section = QGroupBox("👥 User Management")
        section.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("➕ Add User")
        add_btn.setStyleSheet(self.get_button_style("#27ae60"))
        add_btn.clicked.connect(self.add_user)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Edit User")
        edit_btn.setStyleSheet(self.get_button_style("#3498db"))
        edit_btn.clicked.connect(self.edit_user)
        buttons_layout.addWidget(edit_btn)
        
        change_password_btn = QPushButton("🔐 Change Password")
        change_password_btn.setStyleSheet(self.get_button_style("#f39c12"))
        change_password_btn.clicked.connect(self.change_password)
        buttons_layout.addWidget(change_password_btn)
        
        delete_btn = QPushButton("🗑️ Delete User")
        delete_btn.setStyleSheet(self.get_button_style("#e74c3c"))
        delete_btn.clicked.connect(self.delete_user)
        buttons_layout.addWidget(delete_btn)
        
        layout.addLayout(buttons_layout)
        
        # User count display
        user_count_layout = QHBoxLayout()
        user_count_label = QLabel("Total Users:")
        user_count_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.users_count_label = QLabel("0")
        self.users_count_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 14px;")
        user_count_layout.addWidget(user_count_label)
        user_count_layout.addWidget(self.users_count_label)
        user_count_layout.addStretch(1)
        layout.addLayout(user_count_layout)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels([
            "ID", "Username", "Role", "Status", "Actions"
        ])
        
        # Set column widths
        self.users_table.setColumnWidth(0, 50)   # ID
        self.users_table.setColumnWidth(1, 120)  # Username
        self.users_table.setColumnWidth(2, 100)  # Role
        self.users_table.setColumnWidth(3, 80)   # Status
        self.users_table.setColumnWidth(4, 100)  # Actions
        
        self.users_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #e0e0e0;
                border-radius: 6px;
                background-color: white;
                gridline-color: #f0f0f0;
                selection-background-color: #e3f2fd;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #e0e0e0;
                font-weight: bold;
                color: #2c3e50;
            }
            QTableWidget::item {
                padding: 4px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #2c3e50;
            }
        """)
        layout.addWidget(self.users_table)
        
        return section
    
    def create_system_info_section(self) -> QWidget:
        """Create system information section."""
        section = QGroupBox("💻 System Information")
        section.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # System info
        info_layout = QFormLayout()
        
        self.db_status_label = QLabel("🟢 Connected")
        self.db_status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
        info_layout.addRow("Database Status:", self.db_status_label)
        
        self.users_count_label = QLabel("0")
        info_layout.addRow("Total Users:", self.users_count_label)
        
        layout.addLayout(info_layout)
        
        return section
    
    def create_reports_section(self) -> QWidget:
        """Create reports section."""
        section = QGroupBox("📊 Reports & Analytics")
        section.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        layout = QVBoxLayout(section)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 25, 20, 20)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        daily_report_btn = QPushButton("📈 Daily Sales Report")
        daily_report_btn.setStyleSheet(self.get_button_style("#9b59b6"))
        daily_report_btn.clicked.connect(self.show_daily_sales_report)
        buttons_layout.addWidget(daily_report_btn)
        
        shift_report_btn = QPushButton("🕐 Shift Reports")
        shift_report_btn.setStyleSheet(self.get_button_style("#f39c12"))
        shift_report_btn.clicked.connect(self.show_shift_reports)
        buttons_layout.addWidget(shift_report_btn)
        
        layout.addLayout(buttons_layout)
        
        return section
    
    def show_daily_sales_report(self):
        """Show the simple daily sales report dialog."""
        try:
            from controllers.shift_controller import ShiftController
            from ui.components.simple_sale_report_dialog import SimpleSaleReportDialog
            
            shift_controller = ShiftController()
            report_data = shift_controller.get_daily_sales_report()
            
            dialog = SimpleSaleReportDialog(self, report_data)
            dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"Error showing daily sales report: {e}")
    
    def show_shift_reports(self):
        """Show shift reports dialog."""
        try:
            from controllers.shift_controller import ShiftController
            from ui.components.simple_sale_report_dialog import SimpleSaleReportDialog
            
            shift_controller = ShiftController()
            # For now, show the same dialog but could be enhanced for shift-specific reports
            report_data = shift_controller.get_daily_sales_report()
            
            dialog = SimpleSaleReportDialog(self, report_data)
            dialog.exec_()
            
        except Exception as e:
            self.logger.error(f"Error showing shift reports: {e}")
    
    def get_button_style(self, color: str) -> str:
        """Get button styling."""
        return f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background-color: {self.lighten_color(color)};
            }}
            QPushButton:pressed {{
                background-color: {self.darken_color(color)};
            }}
        """
    
    def load_users(self):
        """Load users into the table."""
        try:
            if not hasattr(self, 'users_table') or not self.users_table:
                return
                
            users = self.auth_controller.session.query(User).all()
            self.users_table.setRowCount(len(users))
            
            for row, user in enumerate(users):
                # ID
                id_item = QTableWidgetItem(str(user.id))
                id_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(row, 0, id_item)
                
                # Username
                username_item = QTableWidgetItem(user.username)
                self.users_table.setItem(row, 1, username_item)
                
                # Role
                role_item = QTableWidgetItem(user.role.value.title())
                role_item.setTextAlignment(Qt.AlignCenter)
                self.users_table.setItem(row, 2, role_item)
                
                # Status
                status_text = "Active" if user.active else "Inactive"
                status_item = QTableWidgetItem(status_text)
                status_item.setTextAlignment(Qt.AlignCenter)
                if user.active:
                    status_item.setBackground(QColor("#d4edda"))
                    status_item.setForeground(QColor("#155724"))
                else:
                    status_item.setBackground(QColor("#f8d7da"))
                    status_item.setForeground(QColor("#721c24"))
                self.users_table.setItem(row, 3, status_item)
                
                # Actions button
                actions_btn = QPushButton("Actions")
                actions_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 5px 10px;
                        font-size: 12px;
                        min-width: 60px;
                    }
                    QPushButton:hover {
                        background-color: #7f8c8d;
                    }
                """)
                self.users_table.setCellWidget(row, 4, actions_btn)
            
            # Update user count
            if hasattr(self, 'users_count_label'):
                self.users_count_label.setText(str(len(users)))
            
        except Exception as e:
            self.logger.error(f"Failed to load users: {str(e)}")
    
    def add_user(self):
        """Add a new user."""
        try:
            from ui.components.user_edit_dialog import UserEditDialog
            dialog = UserEditDialog(parent=self)
            if dialog.exec_() == QDialog.Accepted:
                self.load_users()
        except Exception as e:
            self.logger.error(f"Failed to add user: {str(e)}")
    
    def edit_user(self):
        """Edit selected user."""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            try:
                user_id = int(self.users_table.item(current_row, 0).text())
                user = self.auth_controller.session.query(User).filter_by(id=user_id).first()
                
                if user:
                    from ui.components.user_edit_dialog import UserEditDialog
                    dialog = UserEditDialog(user=user, parent=self)
                    if dialog.exec_() == QDialog.Accepted:
                        self.load_users()
                else:
                    pass  # User not found
            except Exception as e:
                self.logger.error(f"Failed to edit user: {str(e)}")
        else:
            pass  # No user selected
    
    def change_password(self):
        """Change password for selected user."""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            try:
                user_id = int(self.users_table.item(current_row, 0).text())
                username = self.users_table.item(current_row, 1).text()
                user = self.auth_controller.session.query(User).filter_by(id=user_id).first()
                
                if user:
                    from ui.components.user_edit_dialog import UserEditDialog
                    dialog = UserEditDialog(user=user, parent=self)
                    # Focus on password fields
                    dialog.password_input.setFocus()
                    if dialog.exec_() == QDialog.Accepted:
                        self.load_users()
                else:
                    pass  # User not found
            except Exception as e:
                self.logger.error(f"Failed to change password: {str(e)}")
        else:
            pass  # No user selected
    
    def delete_user(self):
        """Delete selected user."""
        current_row = self.users_table.currentRow()
        if current_row >= 0:
            user_id = int(self.users_table.item(current_row, 0).text())
            username = self.users_table.item(current_row, 1).text()
            
            try:
                user = self.auth_controller.session.query(User).filter_by(id=user_id).first()
                if user:
                    self.auth_controller.session.delete(user)
                    self.auth_controller.session.commit()
                    self.load_users()
                else:
                    pass  # User not found
            except Exception as e:
                self.logger.error(f"Failed to delete user: {str(e)}")
    
    def lighten_color(self, color: str) -> str:
        """Lighten a hex color."""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            lightened = tuple(min(255, int(c * 1.2)) for c in rgb)
            return f"#{lightened[0]:02x}{lightened[1]:02x}{lightened[2]:02x}"
        except:
            return color
    
    def darken_color(self, color: str) -> str:
        """Darken a hex color."""
        try:
            color = color.lstrip('#')
            rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            darkened = tuple(max(0, int(c * 0.8)) for c in rgb)
            return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
        except:
            return color


class ModernMainWindow(QMainWindow):
    """Modern main window with enhanced UI and functionality."""
    
    def __init__(self, user, opening_amount=None):
        super().__init__()
        self.user = user
        self.opening_amount = opening_amount
        self.product_controller = ProductController()
        self.sale_controller = SaleController()
        self.logger = logging.getLogger(__name__)
        
        # Add missing attributes for the new POS view
        self.settings = None  # Can be enhanced later with proper settings
        self.database_manager = DatabaseManager()  # Initialize database manager
        
        self.init_ui()
        self.setup_menu()
        self.setup_status_bar()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the main window UI."""
        self.setWindowTitle(tr("main_window.title", "Talinda POS System"))
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # Set window icon and properties
        self.setWindowIcon(QIcon("resources/styles/logo.png"))
        self.setWindowState(Qt.WindowMaximized)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create sidebar
        self.sidebar = self.create_sidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create stacked widget
        self.stacked_widget = QStackedWidget()
        self.stacked_widget.setStyleSheet("""
            QStackedWidget {
                background-color: #f8f9fa;
                border: none;
            }
        """)
        
        # Initialize pages
        self.init_pages()
        
        main_layout.addWidget(self.stacked_widget, 1)
        
        # Set initial page
        self.sidebar.setCurrentRow(0)
    
    def create_sidebar(self) -> QListWidget:
        """Create the modern sidebar."""
        sidebar = QListWidget()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QListWidget#sidebar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #2c3e50, stop:1 #34495e);
                border: none;
                color: white;
                font-size: 14px;
                font-weight: bold;
                outline: none;
            }
            QListWidget#sidebar::item {
                padding: 15px 20px;
                border-bottom: 1px solid #34495e;
                background-color: transparent;
            }
            QListWidget#sidebar::item:selected {
                background-color: #3498db;
                color: white;
                border-left: 4px solid #2980b9;
            }
            QListWidget#sidebar::item:hover {
                background-color: #34495e;
                border-left: 4px solid #3498db;
            }
        """)
        
        # Add menu items
        menu_items = [
            ("🛒", tr("pos.title", "Point of Sale"), "Main point of sale interface"),
            ("📋", tr("orders.title", "Orders"), "Manage orders and transactions"),
        ]
        
        if self.user.role.value == 'admin':
            menu_items.extend([
                ("⚙️", tr("main_window.admin_panel", "Admin Panel"), "User and system management"),
                ("➕", tr("products.add_product", "Add Product"), "Add new products to inventory"),
                ("📦", tr("products.title", "Products"), "View and manage products"),
            ])
        
        for icon, text, tooltip in menu_items:
            item = QListWidgetItem(f"{icon} {text}")
            item.setToolTip(tooltip)
            sidebar.addItem(item)
        
        sidebar.currentRowChanged.connect(self.switch_page)
        return sidebar
    
    def init_pages(self):
        """Initialize all pages."""
        # POS System page - Using the Modern POS Widget with cart functionality
        self.pos_widget = ModernPOSWidget(
            user=self.user,
            product_controller=self.product_controller,
            sale_controller=self.sale_controller
        )
        self.stacked_widget.addWidget(self.pos_widget)
        
        # Order Management page
        self.order_management_widget = OrderManagementWidget(self.user)
        self.stacked_widget.addWidget(self.order_management_widget)
        
        # Admin pages (if admin user)
        if self.user.role.value == 'admin':
            # Admin Panel page
            self.admin_panel_widget = ModernAdminPanelWidget()
            self.stacked_widget.addWidget(self.admin_panel_widget)
            
            # Add Product page
            try:
                categories = self.product_controller.get_categories()
                cat_list = [{'id': cat.id, 'name': cat.name} for cat in categories]
                self.add_product_page = AddProductPage(categories=cat_list)
                self.add_product_page.product_added.connect(self.handle_add_product)
                self.stacked_widget.addWidget(self.add_product_page)
            except Exception as e:
                self.logger.error(f"Failed to initialize Add Product page: {str(e)}")
    
    def setup_menu(self):
        """Setup the application menu."""
        menubar = self.menuBar()
        menubar.setStyleSheet("""
            QMenuBar {
                background-color: #2c3e50;
                color: white;
                font-weight: bold;
            }
            QMenuBar::item {
                background-color: transparent;
                padding: 8px 12px;
            }
            QMenuBar::item:selected {
                background-color: #34495e;
            }
        """)
        
        # File menu
        file_menu = menubar.addMenu('📁 File')
        
        new_sale_action = QAction('🆕 New Sale', self)
        new_sale_action.setShortcut('Ctrl+N')
        new_sale_action.triggered.connect(self.new_sale)
        file_menu.addAction(new_sale_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction('🚪 Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Tools menu
        tools_menu = menubar.addMenu('🔧 Tools')
        
        if self.user.role.value == 'admin':
            admin_action = QAction('⚙️ Admin Panel', self)
            admin_action.triggered.connect(lambda: self.switch_page(2))
            tools_menu.addAction(admin_action)
        
        # Change Password menu
        change_password_action = QAction('🔐 Change My Password', self)
        change_password_action.triggered.connect(self.change_my_password)
        tools_menu.addAction(change_password_action)
        
        # Language menu
        language_action = QAction('🌐 Language', self)
        language_action.triggered.connect(self.show_language_selector)
        tools_menu.addAction(language_action)
        
        # Help menu
        help_menu = menubar.addMenu('❓ Help')
        
        about_action = QAction('ℹ️ About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_status_bar(self):
        """Setup the status bar."""
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.setStyleSheet("""
            QStatusBar {
                background-color: #ecf0f1;
                color: #2c3e50;
                border-top: 1px solid #bdc3c7;
            }
        """)
        
        # User info
        user_info = QLabel(f"👤 {self.user.username} ({self.user.role.value.title()})")
        status_bar.addWidget(user_info)
        
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Opening amount (for cashiers)
        if self.opening_amount is not None:
            opening_info = QLabel(f"💰 Opening Amount: ${self.opening_amount:.2f}")
            status_bar.addPermanentWidget(opening_info)
        
        status_bar.addPermanentWidget(QLabel("|"))
        
        # Current time
        self.time_label = QLabel()
        status_bar.addPermanentWidget(self.time_label)
        
        # Update time
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()
    
    def setup_connections(self):
        """Setup signal connections."""
        # Connect cart signals
        if hasattr(self.pos_widget, 'cart_widget'):
            cart = self.pos_widget.cart_widget
            if hasattr(cart, 'sale_completed'):
                cart.sale_completed.connect(self.on_sale_completed)
        # Connect order saved signal to refresh order management
        if hasattr(self.pos_widget.cart_widget, 'order_saved'):
            self.pos_widget.cart_widget.order_saved.connect(self.on_order_saved)
    
    def switch_page(self, index):
        """Switch to the specified page."""
        try:
            if index == 0:  # POS System
                self.stacked_widget.setCurrentIndex(0)
            elif index == 1:  # Order Management
                self.stacked_widget.setCurrentIndex(1)
            elif self.user.role.value == 'admin':
                if index == 2:  # Admin Panel
                    self.stacked_widget.setCurrentIndex(2)
                elif index == 3:  # Add Product
                    self.stacked_widget.setCurrentIndex(3)
                elif index == 4:  # Show Products
                    self.show_products_window()
                    return
        except Exception as e:
            self.logger.error(f"Error switching page: {str(e)}")
    
    def show_products_window(self):
        """Show the products window."""
        try:
            dialog = ShowProductsWindow(self)
            dialog.exec_()
            self.sidebar.setCurrentRow(2)  # Go back to Admin Panel
        except Exception as e:
            self.logger.error(f"Failed to show products: {str(e)}")

    def handle_add_product(self, product_data):
        """Handle product addition."""
        try:
            self.product_controller.add_product(**product_data)
        except ValueError as e:
            self.logger.error(f"Validation error: {str(e)}")
        except Exception as e:
            self.logger.error(f"Failed to add product: {str(e)}")
    
    def new_sale(self):
        """Start a new sale."""
        self.sidebar.setCurrentRow(0)  # Switch to POS
        # Clear cart if available
        if hasattr(self.pos_widget, 'cart_widget'):
            cart = self.pos_widget.cart_widget
            if hasattr(cart, 'clear_cart'):
                cart.clear_cart()
    
    def on_sale_completed(self, sale_data):
        """Handle sale completion."""
        self.logger.info("Sale completed")
    
    def on_order_saved(self, order):
        """Handle order saved signal from cart widget."""
        if order is None:
            self.logger.warning("Order saved signal received with None order")
            return
        
        self.logger.info(f"Order saved: {order.order_number}")
        # Refresh the order management widget to show the latest order
        if hasattr(self, 'order_management_widget') and self.order_management_widget:
            self.order_management_widget.refresh_orders()
        # Note: Success message is already shown by the cart widget, so we don't show it again here
    
    def show_about(self):
        """Show about dialog."""
        pass  # About dialog removed
    
    def show_language_selector(self):
        """Show language selector dialog."""
        dialog = LanguageSelectorDialog(self)
        dialog.language_selector.language_changed.connect(self.on_language_changed)
        dialog.exec()
    
    def change_my_password(self):
        """Change current user's password."""
        try:
            from ui.components.user_edit_dialog import UserEditDialog
            dialog = UserEditDialog(user=self.user, parent=self)
            # Focus on password fields
            dialog.password_input.setFocus()
            if dialog.exec_() == QDialog.Accepted:
                pass  # Password changed successfully
        except Exception as e:
            self.logger.error(f"Failed to change password: {str(e)}")
    
    def on_language_changed(self, language: str):
        """Handle language change."""
        try:
            # Update the application language
            set_language(language)
            
            # Refresh all UI elements
            self.refresh_ui_for_language_change()
            
        except Exception as e:
            self.logger.error(f"Error changing language: {str(e)}")
    
    def refresh_ui_for_language_change(self):
        """Refresh all UI elements after language change."""
        try:
            # Update window title
            self.setWindowTitle(tr("main_window.title", "Talinda POS System"))
            
            # Update menu items
            self.refresh_menu_items()
            
            # Update sidebar items
            self.refresh_sidebar_items()
            
            # Update status bar
            self.refresh_status_bar()
            
            # Update current page content
            self.refresh_current_page()
            
        except Exception as e:
            self.logger.error(f"Error refreshing UI for language change: {str(e)}")
    
    def refresh_menu_items(self):
        """Refresh menu items with new language."""
        try:
            menubar = self.menuBar()
            
            # Update File menu
            file_menu = menubar.actions()[0].menu()  # First menu is File
            if file_menu:
                file_menu.setTitle(f"📁 {tr('main_window.file_menu', 'File')}")
                for action in file_menu.actions():
                    if "Exit" in action.text():
                        action.setText(f"🚪 {tr('main_window.exit', 'Exit')}")
                    elif "New Sale" in action.text():
                        action.setText(f"🆕 {tr('pos.new_sale', 'New Sale')}")
            
            # Update Tools menu
            tools_menu = menubar.actions()[1].menu()  # Second menu is Tools
            if tools_menu:
                tools_menu.setTitle(f"🔧 {tr('common.tools', 'Tools')}")
                for action in tools_menu.actions():
                    if "Language" in action.text():
                        action.setText(f"🌐 {tr('common.language', 'Language')}")
                    elif "Admin Panel" in action.text():
                        action.setText(f"⚙️ {tr('main_window.admin_panel', 'Admin Panel')}")
            
            # Update Help menu
            help_menu = menubar.actions()[2].menu()  # Third menu is Help
            if help_menu:
                help_menu.setTitle(f"❓ {tr('main_window.help_menu', 'Help')}")
                for action in help_menu.actions():
                    if "About" in action.text():
                        action.setText(f"ℹ️ {tr('main_window.about', 'About')}")
                
        except Exception as e:
            self.logger.error(f"Error refreshing menu items: {str(e)}")
            # If menu refresh fails, try to recreate the entire menu
            try:
                menubar.clear()
                self.setup_menu()
            except Exception as e2:
                self.logger.error(f"Error recreating menu: {str(e2)}")
    
    def refresh_sidebar_items(self):
        """Refresh sidebar items with new language."""
        try:
            if hasattr(self, 'sidebar'):
                # Clear and recreate sidebar items with new translations
                self.sidebar.clear()
                
                # Add menu items with updated translations
                menu_items = [
                    ("🛒", tr("pos.title", "Point of Sale"), "Main point of sale interface"),
                    ("📋", tr("orders.title", "Orders"), "Manage orders and transactions"),
                ]
                
                if self.user.role.value == 'admin':
                    menu_items.extend([
                        ("⚙️", tr("main_window.admin_panel", "Admin Panel"), "User and system management"),
                        ("➕", tr("products.add_product", "Add Product"), "Add new products to inventory"),
                        ("📦", tr("products.title", "Products"), "View and manage products"),
                    ])
                
                for icon, text, tooltip in menu_items:
                    item = QListWidgetItem(f"{icon} {text}")
                    item.setToolTip(tooltip)
                    self.sidebar.addItem(item)
                
                # Restore the current selection
                current_index = min(self.sidebar.count() - 1, 0)  # Default to first item
                self.sidebar.setCurrentRow(current_index)
                        
        except Exception as e:
            self.logger.error(f"Error refreshing sidebar items: {str(e)}")
    
    def refresh_status_bar(self):
        """Refresh status bar with new language."""
        try:
            status_bar = self.statusBar()
            if status_bar:
                # Clear and recreate status bar
                status_bar.clearMessage()
                
                # Remove all widgets
                for widget in status_bar.findChildren(QLabel):
                    widget.deleteLater()
                
                # Recreate status bar content
                # User info
                user_info = QLabel(f"👤 {self.user.username} ({self.user.role.value.title()})")
                status_bar.addWidget(user_info)
                
                status_bar.addPermanentWidget(QLabel("|"))
                
                # Opening amount (for cashiers)
                if self.opening_amount is not None:
                    opening_info = QLabel(f"💰 {tr('shifts.opening_amount', 'Opening Amount')}: ${self.opening_amount:.2f}")
                    status_bar.addPermanentWidget(opening_info)
                
                status_bar.addPermanentWidget(QLabel("|"))
                
                # Current time
                self.time_label = QLabel()
                status_bar.addPermanentWidget(self.time_label)
                self.update_time()
                    
        except Exception as e:
            self.logger.error(f"Error refreshing status bar: {str(e)}")
    
    def refresh_current_page(self):
        """Refresh the current page content."""
        try:
            current_index = self.sidebar.currentRow()
            
            # Refresh based on current page
            if current_index == 0:  # POS
                if hasattr(self, 'pos_widget'):
                    self.refresh_pos_widget()
            elif current_index == 1:  # Orders
                if hasattr(self, 'order_management_widget'):
                    self.refresh_order_widget()
            elif current_index == 2:  # Admin Panel
                if hasattr(self, 'admin_panel_widget'):
                    self.refresh_admin_widget()
            elif current_index == 3:  # Add Product
                if hasattr(self, 'add_product_page'):
                    self.refresh_add_product_page()
            elif current_index == 4:  # Show Products
                # This is handled by the dialog, no need to refresh
                pass
                    
        except Exception as e:
            self.logger.error(f"Error refreshing current page: {str(e)}")
    
    def refresh_add_product_page(self):
        """Refresh add product page elements."""
        try:
            if hasattr(self, 'add_product_page'):
                # Update form labels and buttons
                for widget in self.add_product_page.findChildren(QLabel):
                    if "Product Name" in widget.text():
                        widget.setText(tr("products.product_name", "Product Name"))
                    elif "Product Code" in widget.text():
                        widget.setText(tr("products.product_code", "Product Code"))
                    elif "Price" in widget.text():
                        widget.setText(tr("products.price", "Price"))
                    elif "Category" in widget.text():
                        widget.setText(tr("products.category", "Category"))
                    elif "Stock" in widget.text():
                        widget.setText(tr("products.stock", "Stock"))
                    elif "Description" in widget.text():
                        widget.setText(tr("products.description", "Description"))
                
                for widget in self.add_product_page.findChildren(QPushButton):
                    if "Save" in widget.text():
                        widget.setText(tr("common.save", "Save"))
                    elif "Cancel" in widget.text():
                        widget.setText(tr("common.cancel", "Cancel"))
                        
        except Exception as e:
            self.logger.error(f"Error refreshing add product page: {str(e)}")
    
    def refresh_pos_widget(self):
        """Refresh POS widget elements."""
        try:
            if hasattr(self, 'pos_widget'):
                # Update POS widget title and labels
                for widget in self.pos_widget.findChildren(QLabel):
                    if "Point of Sale" in widget.text():
                        widget.setText(tr("pos.title", "Point of Sale"))
                    elif "Total" in widget.text() and ":" in widget.text():
                        widget.setText(f"{tr('pos.total', 'Total')}:")
                    elif "Subtotal" in widget.text() and ":" in widget.text():
                        widget.setText(f"{tr('pos.subtotal', 'Subtotal')}:")
                    elif "Tax" in widget.text() and ":" in widget.text():
                        widget.setText(f"{tr('pos.tax', 'Tax')}:")
                    elif "Discount" in widget.text() and ":" in widget.text():
                        widget.setText(f"{tr('pos.discount', 'Discount')}:")
                    elif "Grand Total" in widget.text() and ":" in widget.text():
                        widget.setText(f"{tr('pos.grand_total', 'Grand Total')}:")
                
                # Update buttons
                for widget in self.pos_widget.findChildren(QPushButton):
                    if "Add to Cart" in widget.text():
                        widget.setText(tr("pos.add_to_cart", "Add to Cart"))
                    elif "Clear Cart" in widget.text():
                        widget.setText(tr("pos.clear_cart", "Clear Cart"))
                    elif "Checkout" in widget.text():
                        widget.setText(tr("pos.checkout", "Checkout"))
                    elif "Complete Sale" in widget.text():
                        widget.setText(tr("pos.complete_sale", "Complete Sale"))
                    elif "Cancel Sale" in widget.text():
                        widget.setText(tr("pos.cancel_sale", "Cancel Sale"))
                    
        except Exception as e:
            self.logger.error(f"Error refreshing POS widget: {str(e)}")
    
    def refresh_order_widget(self):
        """Refresh order management widget elements."""
        try:
            if hasattr(self, 'order_management_widget'):
                # Update order widget title and labels
                for widget in self.order_management_widget.findChildren(QLabel):
                    if "Orders" in widget.text() and "Management" in widget.text():
                        widget.setText(tr("orders.title", "Orders"))
                    elif "Order ID" in widget.text():
                        widget.setText(tr("orders.order_id", "Order ID"))
                    elif "Date" in widget.text():
                        widget.setText(tr("orders.date", "Date"))
                    elif "Time" in widget.text():
                        widget.setText(tr("orders.time", "Time"))
                    elif "Status" in widget.text():
                        widget.setText(tr("orders.status", "Status"))
                    elif "Total" in widget.text():
                        widget.setText(tr("orders.total", "Total"))
                    elif "Actions" in widget.text():
                        widget.setText(tr("orders.actions", "Actions"))
                
                # Update buttons
                for widget in self.order_management_widget.findChildren(QPushButton):
                    if "View" in widget.text():
                        widget.setText(tr("orders.view", "View"))
                    elif "Edit" in widget.text():
                        widget.setText(tr("orders.edit", "Edit"))
                    elif "Delete" in widget.text():
                        widget.setText(tr("orders.delete", "Delete"))
                    elif "Complete" in widget.text():
                        widget.setText(tr("orders.complete", "Complete"))
                    elif "Cancel" in widget.text():
                        widget.setText(tr("orders.cancel", "Cancel"))
                    
        except Exception as e:
            self.logger.error(f"Error refreshing order widget: {str(e)}")
    
    def refresh_admin_widget(self):
        """Refresh admin panel widget elements."""
        try:
            if hasattr(self, 'admin_panel_widget'):
                # Update admin widget title and labels
                for widget in self.admin_panel_widget.findChildren(QLabel):
                    if "Admin Panel" in widget.text():
                        widget.setText(tr("main_window.admin_panel", "Admin Panel"))
                    elif "User Management" in widget.text():
                        widget.setText(tr("admin.user_management", "User Management"))
                    elif "System Information" in widget.text():
                        widget.setText(tr("admin.system_info", "System Information"))
                    elif "Reports" in widget.text():
                        widget.setText(tr("reports.title", "Reports"))
                
                # Update buttons
                for widget in self.admin_panel_widget.findChildren(QPushButton):
                    if "Add User" in widget.text():
                        widget.setText(tr("admin.add_user", "Add User"))
                    elif "Edit User" in widget.text():
                        widget.setText(tr("admin.edit_user", "Edit User"))
                    elif "Delete User" in widget.text():
                        widget.setText(tr("admin.delete_user", "Delete User"))
                    elif "Daily Sales Report" in widget.text():
                        widget.setText(tr("reports.daily_report", "Daily Report"))
                    elif "Shift Reports" in widget.text():
                        widget.setText(tr("reports.shift_reports", "Shift Reports"))
                    
        except Exception as e:
            self.logger.error(f"Error refreshing admin widget: {str(e)}")
    
    def refresh_reports_widget(self):
        """Refresh reports widget elements."""
        try:
            if hasattr(self, 'reports_widget'):
                # Update reports widget title and labels
                if hasattr(self.reports_widget, 'title_label'):
                    self.reports_widget.title_label.setText(tr("reports.title", "Reports"))
                    
        except Exception as e:
            self.logger.error(f"Error refreshing reports widget: {str(e)}")
    
    def update_time(self):
        """Update the time display."""
        current_time = QDateTime.currentDateTime().toString("hh:mm:ss")
        self.time_label.setText(f"🕐 {current_time}")
    
    def closeEvent(self, event):
        """Handle window close event."""
        # Close the application directly without closing amount dialog
        event.accept()


# Alias for backward compatibility
MainWindow = ModernMainWindow
