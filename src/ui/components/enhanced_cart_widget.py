"""
Enhanced cart widget that supports both regular POS sales and table orders.
"""
import sys
import os
import logging

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from typing import Dict, Optional
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                           QScrollArea, QFrame, QHBoxLayout, QLineEdit, 
                           QDialog, QFormLayout, QDoubleSpinBox, QMessageBox,
                           QComboBox, QTextEdit, QTabWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from controllers.sale_controller import SaleController, CartItem

# Set up logging
logger = logging.getLogger(__name__)


class DiscountDialog(QDialog):
    """Dialog for applying discounts to cart items."""
    
    def __init__(self, parent=None, item_name="", current_discount_percent=0.0, current_discount_amount=0.0):
        super().__init__(parent)
        self.setWindowTitle(f"Apply Discount - {item_name}")
        # Use responsive sizing
        from utils.responsive_ui import ResponsiveUI
        
        dialog_size = ResponsiveUI.get_responsive_dialog_size('standard')
        self.setFixedSize(dialog_size.width(), dialog_size.height())
        self.discount_percentage = current_discount_percent
        self.discount_amount = current_discount_amount
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Percentage discount
        self.percent_spin = QDoubleSpinBox()
        self.percent_spin.setRange(0.0, 100.0)
        self.percent_spin.setValue(self.discount_percentage)
        self.percent_spin.setSuffix("%")
        self.percent_spin.setMinimumHeight(35)
        layout.addRow("Discount Percentage:", self.percent_spin)
        
        # Fixed amount discount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.0, 9999.99)
        self.amount_spin.setValue(self.discount_amount)
        self.amount_spin.setPrefix("$")
        self.amount_spin.setDecimals(2)
        self.amount_spin.setMinimumHeight(35)
        layout.addRow("Discount Amount:", self.amount_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        apply_btn = QPushButton("Apply")
        apply_btn.setMinimumHeight(35)
        apply_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        apply_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
    
    def get_discounts(self):
        return self.percent_spin.value(), self.amount_spin.value()

class CartDiscountDialog(QDialog):
    """Dialog for applying cart-wide discounts."""
    
    def __init__(self, parent=None, current_percent=0.0, current_amount=0.0):
        super().__init__(parent)
        self.setWindowTitle("Apply Cart Discount")
        # Use responsive sizing
        from utils.responsive_ui import ResponsiveUI
        
        dialog_size = ResponsiveUI.get_responsive_dialog_size('standard')
        self.setFixedSize(dialog_size.width(), dialog_size.height())
        self.discount_percentage = current_percent
        self.discount_amount = current_amount
        self.init_ui()
    
    def init_ui(self):
        layout = QFormLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Percentage discount
        self.percent_spin = QDoubleSpinBox()
        self.percent_spin.setRange(0.0, 100.0)
        self.percent_spin.setValue(self.discount_percentage)
        self.percent_spin.setSuffix("%")
        self.percent_spin.setMinimumHeight(35)
        layout.addRow("Cart Discount Percentage:", self.percent_spin)
        
        # Fixed amount discount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.0, 9999.99)
        self.amount_spin.setValue(self.discount_amount)
        self.amount_spin.setPrefix("$")
        self.amount_spin.setDecimals(2)
        self.amount_spin.setMinimumHeight(35)
        layout.addRow("Cart Discount Amount:", self.amount_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        apply_btn = QPushButton("Apply")
        apply_btn.setMinimumHeight(35)
        apply_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        apply_btn.clicked.connect(self.accept)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(35)
        cancel_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
    
    def get_discounts(self):
        return self.percent_spin.value(), self.amount_spin.value()

class EnhancedCartWidget(QWidget):
    """Enhanced cart widget that supports both regular sales and table orders."""
    
    # Signals
    order_saved = pyqtSignal(object)  # Emitted when an order is saved
    
    def __init__(self, sale_controller: SaleController, user):
        super().__init__()
        self.sale_controller = sale_controller
        self.user = user
        self.cart_items: Dict[int, QWidget] = {}
        
        # Order memory for loaded orders
        self.loaded_order = None
        self.loaded_customer_name = ""
        self.loaded_notes = ""
        
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Cart header
        self.cart_header = QLabel("Shopping Cart")
        self.cart_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; padding: 5px;")
        layout.addWidget(self.cart_header)
        
        # Cart items scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMinimumHeight(300)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollArea {
                border: 1px solid #e0e0e0;
                border-radius: 8px;
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
        
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        self.cart_layout.setSpacing(8)
        self.cart_layout.setContentsMargins(5, 5, 5, 5)
        scroll.setWidget(self.cart_container)
        layout.addWidget(scroll, stretch=1)
        
        # Totals section
        totals_widget = QWidget()
        totals_widget.setStyleSheet("background-color: #f8f9fa; border-radius: 8px; padding: 10px; border: 1px solid #e0e0e0;")
        totals_layout = QVBoxLayout(totals_widget)
        totals_layout.setSpacing(8)
        
        # Subtotal
        subtotal_layout = QHBoxLayout()
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        self.subtotal_amount = QLabel("$0.00")
        self.subtotal_amount.setStyleSheet("font-size: 14px; font-weight: bold; color: #2c3e50;")
        subtotal_layout.addWidget(subtotal_label)
        subtotal_layout.addStretch()
        subtotal_layout.addWidget(self.subtotal_amount)
        totals_layout.addLayout(subtotal_layout)
        
        # Discount
        discount_layout = QHBoxLayout()
        discount_label = QLabel("Discount:")
        discount_label.setStyleSheet("font-size: 14px; color: #e74c3c;")
        self.discount_amount = QLabel("$0.00")
        self.discount_amount.setStyleSheet("font-size: 14px; color: #e74c3c;")
        discount_layout.addWidget(discount_label)
        discount_layout.addStretch()
        discount_layout.addWidget(self.discount_amount)
        totals_layout.addLayout(discount_layout)
        
        # Tax
        tax_layout = QHBoxLayout()
        tax_label = QLabel("Tax:")
        tax_label.setStyleSheet("font-size: 14px; color: #3498db;")
        self.tax_amount = QLabel("$0.00")
        self.tax_amount.setStyleSheet("font-size: 14px; color: #3498db;")
        tax_layout.addWidget(tax_label)
        tax_layout.addStretch()
        tax_layout.addWidget(self.tax_amount)
        totals_layout.addLayout(tax_layout)
        
        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("background-color: #bdc3c7; margin: 5px 0;")
        totals_layout.addWidget(separator)
        
        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("Total:")
        total_label.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        self.total_amount = QLabel("$0.00")
        self.total_amount.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50;")
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_amount)
        totals_layout.addLayout(total_layout)
        
        layout.addWidget(totals_widget)
        
        # Action buttons - make them more responsive
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)
        
        # Top row buttons
        top_btn_layout = QHBoxLayout()
        top_btn_layout.setSpacing(8)
        
        # Discount button
        discount_btn = QPushButton("Cart Discount")
        discount_btn.clicked.connect(self.apply_cart_discount)
        discount_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 13px;
            font-weight: bold;
            min-height: 40px;
        """)
        
        clear_btn = QPushButton("Clear Cart")
        clear_btn.clicked.connect(self.clear_cart)
        
        # Style based on user role - show admin requirement for cashiers
        if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
            clear_btn.setStyleSheet("""
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border: 2px solid #f39c12;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                min-height: 40px;
            """)
            clear_btn.setToolTip("Clear cart (Admin authentication required)")
        else:
            clear_btn.setStyleSheet("""
                background-color: #e74c3c;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 5px;
                font-size: 13px;
                font-weight: bold;
                min-height: 40px;
            """)
            clear_btn.setToolTip("Clear cart")
        
        top_btn_layout.addWidget(discount_btn)
        top_btn_layout.addWidget(clear_btn)
        btn_layout.addLayout(top_btn_layout)
        
        # Bottom row buttons
        bottom_btn_layout = QHBoxLayout()
        bottom_btn_layout.setSpacing(8)
        
        # Save Order button
        self.create_order_btn = QPushButton("Save Order")
        self.create_order_btn.clicked.connect(self.create_order)
        self.create_order_btn.setStyleSheet("""
            background-color: #9b59b6;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            min-height: 45px;
        """)
        
        self.checkout_btn = QPushButton("Checkout")
        self.checkout_btn.clicked.connect(self.checkout)
        self.checkout_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
            font-weight: bold;
            min-height: 45px;
        """)
        
        bottom_btn_layout.addWidget(self.create_order_btn)
        bottom_btn_layout.addWidget(self.checkout_btn)
        btn_layout.addLayout(bottom_btn_layout)
        
        layout.addLayout(btn_layout)
        

    
    def add_item(self, product) -> None:
        """Add a product to the cart."""
        if self.sale_controller.add_to_cart(product, 1):
            if product.id not in self.cart_items:
                self.create_item_widget(product)
            else:
                self.update_item_widget(product.id)
            self.update_totals()
    
    def create_item_widget(self, product) -> None:
        """Create a widget for a cart item."""
        if product.id in self.cart_items:
            return
        
        item_widget = QWidget()
        item_widget.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 8px;
                padding: 8px;
            }
            QWidget:hover {
                border-color: #b39ddb;
                background-color: #f8f9fa;
            }
        """)
        
        item_layout = QHBoxLayout(item_widget)
        item_layout.setContentsMargins(8, 8, 8, 8)
        item_layout.setSpacing(10)
        
        # Product info (left side)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(4)
        
        name_label = QLabel(product.name)
        name_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #2c3e50;")
        name_label.setWordWrap(True)
        info_layout.addWidget(name_label)
        
        price_label = QLabel(f"${product.price:.2f} each")
        price_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        info_layout.addWidget(price_label)
        
        item_layout.addLayout(info_layout, stretch=2)
        
        # Quantity controls (center)
        qty_layout = QVBoxLayout()
        qty_layout.setSpacing(4)
        
        qty_label = QLabel("Qty:")
        qty_label.setStyleSheet("font-size: 11px; color: #666;")
        qty_layout.addWidget(qty_label)
        
        qty_controls = QHBoxLayout()
        qty_controls.setSpacing(4)
        
        minus_btn = QPushButton("-")
        minus_btn.setFixedSize(28, 28)
        minus_btn.clicked.connect(lambda: self.update_quantity(product.id, -1))
        minus_btn.setStyleSheet("""
            background-color: #e74c3c; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            font-weight: bold;
            font-size: 14px;
        """)
        
        qty_label = QLabel("1")
        qty_label.setStyleSheet("""
            font-weight: bold; 
            min-width: 35px; 
            text-align: center; 
            font-size: 13px;
            padding: 4px;
            background-color: #f8f9fa;
            border-radius: 4px;
        """)
        
        plus_btn = QPushButton("+")
        plus_btn.setFixedSize(28, 28)
        plus_btn.clicked.connect(lambda: self.update_quantity(product.id, 1))
        plus_btn.setStyleSheet("""
            background-color: #27ae60; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            font-weight: bold;
            font-size: 14px;
        """)
        
        qty_controls.addWidget(minus_btn)
        qty_controls.addWidget(qty_label)
        qty_controls.addWidget(plus_btn)
        qty_layout.addLayout(qty_controls)
        
        item_layout.addLayout(qty_layout)
        
        # Total and actions (right side)
        total_layout = QVBoxLayout()
        total_layout.setSpacing(4)
        
        item_total_label = QLabel(f"${product.price:.2f}")
        item_total_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        total_layout.addWidget(item_total_label)
        
        action_layout = QHBoxLayout()
        action_layout.setSpacing(4)
        
        discount_btn = QPushButton("Discount")
        discount_btn.setFixedSize(65, 28)
        discount_btn.clicked.connect(lambda: self.apply_item_discount(product.id))
        discount_btn.setStyleSheet("""
            background-color: #f39c12; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            font-size: 10px;
            font-weight: bold;
        """)
        
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(28, 28)
        remove_btn.clicked.connect(lambda: self.remove_item(product.id))
        
        # Style based on user role - show admin requirement for cashiers
        if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
            remove_btn.setStyleSheet("""
                background-color: #e74c3c; 
                color: white; 
                border: 2px solid #f39c12; 
                border-radius: 4px; 
                font-weight: bold;
                font-size: 16px;
            """)
            remove_btn.setToolTip("Remove item (Admin authentication required)")
        else:
            remove_btn.setStyleSheet("""
                background-color: #e74c3c; 
                color: white; 
                border: none; 
                border-radius: 4px; 
                font-weight: bold;
                font-size: 16px;
            """)
            remove_btn.setToolTip("Remove item")
        
        action_layout.addWidget(discount_btn)
        action_layout.addWidget(remove_btn)
        total_layout.addLayout(action_layout)
        
        item_layout.addLayout(total_layout)
        
        # Store the labels as attributes of the item widget for later access
        item_widget.qty_label = qty_label
        item_widget.item_total_label = item_total_label
        
        self.cart_items[product.id] = item_widget
        self.cart_layout.addWidget(item_widget)
    
    def update_item_display(self, product_id: int) -> None:
        """Update the display of a cart item."""
        if product_id not in self.sale_controller.cart:
            return
        
        item = self.sale_controller.cart[product_id]
        widget = self.cart_items.get(product_id)
        
        if widget and hasattr(widget, 'qty_label'):
            widget.qty_label.setText(str(item.quantity))
        
        if widget and hasattr(widget, 'item_total_label'):
            if item.discount_total > 0:
                widget.item_total_label.setText(f"${item.total:.2f}")
                widget.item_total_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
            else:
                widget.item_total_label.setText(f"${item.total:.2f}")
                widget.item_total_label.setStyleSheet("")
    
    def update_item_widget(self, product_id: int) -> None:
        """Update the display of a cart item."""
        self.update_item_display(product_id)
    
    def remove_item(self, product_id: int) -> None:
        """Remove an item from the cart."""
        # Check if current user is cashier and requires admin authentication
        if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
            # Show admin authentication dialog
            from ui.components.admin_auth_dialog import AdminAuthDialog
            auth_dialog = AdminAuthDialog(self, "remove items from cart")
            
            if auth_dialog.exec_() != QDialog.Accepted:
                return  # User cancelled or authentication failed
        
        # Proceed with item removal
        if product_id in self.cart_items:
            widget = self.cart_items[product_id]
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
            del self.cart_items[product_id]
            self.sale_controller.remove_from_cart(product_id)
            self.update_totals()
    
    def update_quantity(self, product_id: int, change: int) -> None:
        """Update the quantity of an item in the cart."""
        if product_id in self.sale_controller.cart:
            item = self.sale_controller.cart[product_id]
            new_qty = item.quantity + change
            
            # If trying to reduce quantity to 0 (remove item), check permissions
            if new_qty <= 0:
                # Check if current user is cashier and requires admin authentication
                if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
                    # Show admin authentication dialog
                    from ui.components.admin_auth_dialog import AdminAuthDialog
                    auth_dialog = AdminAuthDialog(self, "remove items from cart")
                    
                    if auth_dialog.exec_() != QDialog.Accepted:
                        return  # User cancelled or authentication failed
                
                # If admin authenticated or user is not cashier, remove the item
                self.remove_item(product_id)
                return
            
            # Normal quantity update
            if self.sale_controller.update_quantity(product_id, new_qty):
                self.update_item_widget(product_id)
                self.update_totals()
    
    def apply_item_discount(self, product_id: int) -> None:
        """Apply discount to a specific cart item."""
        # Check if current user is cashier and requires admin authentication
        if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
            # Show admin authentication dialog
            from ui.components.admin_auth_dialog import AdminAuthDialog
            auth_dialog = AdminAuthDialog(self, "apply discount to items")
            
            if auth_dialog.exec_() != QDialog.Accepted:
                return  # User cancelled or authentication failed
        
        if product_id in self.sale_controller.cart:
            item = self.sale_controller.cart[product_id]
            dialog = DiscountDialog(
                self, 
                item.product.name, 
                item.discount_percentage, 
                item.discount_amount
            )
            if dialog.exec_() == QDialog.Accepted:
                percent, amount = dialog.get_discounts()
                self.sale_controller.apply_item_discount(product_id, percent, amount)
                self.update_item_display(product_id)
                self.update_totals()
    
    def apply_cart_discount(self) -> None:
        """Apply discount to the entire cart."""
        # Check if current user is cashier and requires admin authentication
        if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
            # Show admin authentication dialog
            from ui.components.admin_auth_dialog import AdminAuthDialog
            auth_dialog = AdminAuthDialog(self, "apply cart discount")
            
            if auth_dialog.exec_() != QDialog.Accepted:
                return  # User cancelled or authentication failed
        
        dialog = CartDiscountDialog(
            self,
            self.sale_controller.cart_discount_percentage,
            self.sale_controller.cart_discount_amount
        )
        if dialog.exec_() == QDialog.Accepted:
            percent, amount = dialog.get_discounts()
            self.sale_controller.apply_cart_discount(percent, amount)
            self.update_totals()
    
    def update_totals(self) -> None:
        """Update the displayed totals including discounts and tax."""
        subtotal = self.sale_controller.get_cart_subtotal()
        discount_total = self.sale_controller.get_cart_discount_total()
        tax_total = self.sale_controller.get_cart_tax_total()
        total_with_tax = self.sale_controller.get_cart_total_with_tax()
        
        self.subtotal_amount.setText(f"${subtotal:.2f}")
        self.discount_amount.setText(f"${discount_total:.2f}")
        self.tax_amount.setText(f"${tax_total:.2f}")
        self.total_amount.setText(f"${total_with_tax:.2f}")
        
        # Update button states
        self.update_button_states()
    
    def update_button_states(self) -> None:
        """Update the state of action buttons based on cart contents."""
        has_items = bool(self.sale_controller.cart)
        self.create_order_btn.setEnabled(has_items)
        self.checkout_btn.setEnabled(has_items)
    
    def clear_cart(self) -> None:
        """Clear all items from the cart."""
        # Check if current user is cashier and requires admin authentication
        if hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
            # Show admin authentication dialog
            from ui.components.admin_auth_dialog import AdminAuthDialog
            auth_dialog = AdminAuthDialog(self, "clear the cart")
            
            if auth_dialog.exec_() != QDialog.Accepted:
                return  # User cancelled or authentication failed
        
        # Proceed with clearing cart
        self.sale_controller.clear_cart()
        for widget in self.cart_items.values():
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
        self.cart_items.clear()
        
        # Clear order memory
        self.loaded_order = None
        self.loaded_customer_name = ""
        self.loaded_notes = ""
        
        # Reset cart header
        self.update_cart_header()
        
        self.update_totals()
    
    def clear_cart_after_save(self) -> None:
        """Clear cart after saving order (no admin authentication required)."""
        self.sale_controller.clear_cart()
        for widget in self.cart_items.values():
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
        self.cart_items.clear()
        
        # Clear order memory
        self.loaded_order = None
        self.loaded_customer_name = ""
        self.loaded_notes = ""
        
        # Reset cart header
        self.update_cart_header()
        
        self.update_totals()
    
    def refresh_order_management(self) -> None:
        """Refresh the order management widget to show new orders."""
        try:
            # Find the main window to access the order management widget
            parent = self.parent()
            while parent and not hasattr(parent, 'order_management_widget'):
                parent = parent.parent()
            
            if parent and hasattr(parent, 'order_management_widget'):
                order_widget = parent.order_management_widget
                if hasattr(order_widget, 'refresh_orders'):
                    order_widget.refresh_orders()
                    logger.info("Order management widget refreshed after sale completion")
                else:
                    logger.warning("Order management widget does not have refresh_orders method")
            else:
                logger.warning("Could not find order management widget to refresh")
        except Exception as e:
            logger.error(f"Error refreshing order management widget: {str(e)}")
    
    def create_order(self) -> None:
        """Save a new order from cart items or checkout completed orders."""
        if not self.sale_controller.cart:
            QMessageBox.warning(self, "Empty Cart", "Cart is empty. Please add items before saving an order.")
            return
        
        # Check if we're updating an existing order
        if self.loaded_order:
            # If it's a completed order, process checkout
            if self.loaded_order.status.value == "completed":
                self.checkout()
            else:
                # For active orders, ask user what they want to do
                from PyQt5.QtWidgets import QMessageBox
                reply = QMessageBox.question(
                    self, 
                    "Active Order Action", 
                    f"Order {self.loaded_order.order_number} is currently active.\n\n"
                    f"What would you like to do?\n\n"
                    f"• Update Order: Modify the order items and details\n"
                    f"• Checkout Order: Complete the sale and mark order as completed",
                    QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                    QMessageBox.Yes
                )
                
                if reply == QMessageBox.Yes:
                    # Update existing active order
                    self.update_existing_order()
                elif reply == QMessageBox.No:
                    # Checkout the active order
                    self.checkout_active_order()
                # If Cancel, do nothing
        else:
            # Create new order
            self.create_new_order()
    
    def update_existing_order(self) -> None:
        """Update an existing order with current cart items."""
        try:
            from controllers.order_controller import OrderController
            order_controller = OrderController()
            
            # Get current cart items
            items = []
            for product_id, cart_item in self.sale_controller.cart.items():
                items.append({
                    'product_id': product_id,
                    'quantity': cart_item.quantity,
                    'price': cart_item.price,
                    'notes': None
                })
            
            # Clear existing items from the order
            from models.order import order_products
            order_controller.session.execute(
                order_products.delete().where(order_products.c.order_id == self.loaded_order.id)
            )
            
            # Add new items to the order
            if order_controller.add_items_to_order(self.loaded_order, items):
                # Update customer name and notes if changed
                customer_name = self.loaded_customer_name.strip()
                notes = self.loaded_notes.strip()
                
                if customer_name != (self.loaded_order.customer_name or ""):
                    order_controller.update_order_customer_name(self.loaded_order, customer_name)
                
                if notes != (self.loaded_order.notes or ""):
                    order_controller.update_order_notes(self.loaded_order, notes)
                
                # Refresh the session
                order_controller.refresh_session()
                
                # Store order reference before clearing cart
                updated_order = self.loaded_order
                
                QMessageBox.information(self, "Success", f"Order {updated_order.order_number} updated successfully!")
                self.clear_cart_after_save()
                self.order_saved.emit(updated_order)
            else:
                QMessageBox.warning(self, "Error", "Failed to update order.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to update order: {str(e)}")
            print(f"Order update error: {e}")
    
    def create_new_order(self) -> None:
        """Create a new order from cart items."""
        if not self.user:
            QMessageBox.warning(self, "Error", "No user available. Please log in again.")
            return
            
        # Make sure sale controller has the user set
        self.sale_controller.current_user = self.user
            
        # Show new order dialog with loaded order information
        from ui.components.new_order_dialog import NewOrderDialog
        dialog = NewOrderDialog(
            self.user, 
            self.sale_controller, 
            self,
            customer_name=self.loaded_customer_name,
            notes=self.loaded_notes
        )
        if dialog.exec_() == QDialog.Accepted and dialog.order:
            # Store order reference before clearing cart
            new_order = dialog.order
            
            # Note: Success message is already shown by the NewOrderDialog, so we don't show it again here
            # Clear cart after saving order (without admin auth for order saving)
            self.clear_cart_after_save()
            # Emit signal to refresh order management
            self.order_saved.emit(new_order)
    
    def checkout(self) -> None:
        """Process the checkout."""
        if not self.sale_controller.cart:
            QMessageBox.warning(self, "Empty Cart", "Cart is empty.")
            return
        
        # Complete sale directly without payment dialog
        try:
            if self.sale_controller.complete_sale(self.user):
                QMessageBox.information(self, "Success", "Sale completed successfully!")
                self.clear_cart_after_save()
                
                # Refresh order management widget to show new completed order
                self.refresh_order_management()
            else:
                QMessageBox.warning(self, "Error", "Failed to complete sale. Please try again.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during checkout: {str(e)}")
    
    def load_order(self, order) -> None:
        """Load an order into the cart."""
        # Store order information for memory
        self.loaded_order = order
        self.loaded_customer_name = order.customer_name or ""
        self.loaded_notes = order.notes or ""
        
        # Load order items into cart
        self.sale_controller.load_order_to_cart(order)
        
        # Update cart header to show loaded order info
        self.update_cart_header()
        
        # Refresh cart display
        self.refresh_cart_display()
        
        # Show confirmation with appropriate message based on order status
        if order.status.value == "completed":
            QMessageBox.information(
                self, 
                "Order Loaded", 
                f"Completed order {order.order_number} loaded into cart!\n\n"
                f"Customer: {self.loaded_customer_name or 'No name'}\n"
                f"Total: ${order.total_amount:.2f}\n\n"
                f"Click 'Checkout' to process the sale."
            )
        else:
            QMessageBox.information(
                self, 
                "Order Loaded", 
                f"Active order {order.order_number} loaded into cart!\n\n"
                f"Customer: {self.loaded_customer_name or 'No name'}\n"
                f"Status: {order.get_status_display()}\n\n"
                f"Click 'Checkout' to:\n"
                f"• Update the order (modify items/details)\n"
                f"• Complete the sale (process payment)"
            )
    
    def update_cart_header(self) -> None:
        """Update the cart header to show loaded order information."""
        if self.loaded_order and self.loaded_customer_name:
            status_text = " (Completed)" if self.loaded_order.status.value == "completed" else " (Active)"
            self.cart_header.setText(f"📋 Order {self.loaded_order.order_number} - {self.loaded_customer_name}{status_text}")
            
            if self.loaded_order.status.value == "completed":
                self.cart_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #f39c12; padding: 5px;")
                # For completed orders, show "Checkout" to process the sale
                self.create_order_btn.setText("Checkout")
                self.create_order_btn.setStyleSheet("""
                    background-color: #27ae60;
                    color: white;
                    padding: 12px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    min-height: 45px;
                """)
            else:
                self.cart_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db; padding: 5px;")
                # For active orders, show "Checkout" to allow both update and checkout options
                self.create_order_btn.setText("Checkout")
                self.create_order_btn.setStyleSheet("""
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    min-height: 45px;
                """)
        elif self.loaded_order:
            status_text = " (Completed)" if self.loaded_order.status.value == "completed" else " (Active)"
            self.cart_header.setText(f"📋 Order {self.loaded_order.order_number} - No Name{status_text}")
            
            if self.loaded_order.status.value == "completed":
                self.cart_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #f39c12; padding: 5px;")
                # For completed orders, show "Checkout" to process the sale
                self.create_order_btn.setText("Checkout")
                self.create_order_btn.setStyleSheet("""
                    background-color: #27ae60;
                    color: white;
                    padding: 12px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    min-height: 45px;
                """)
            else:
                self.cart_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #3498db; padding: 5px;")
                # For active orders, show "Checkout" to allow both update and checkout options
                self.create_order_btn.setText("Checkout")
                self.create_order_btn.setStyleSheet("""
                    background-color: #3498db;
                    color: white;
                    padding: 12px;
                    border: none;
                    border-radius: 5px;
                    font-size: 14px;
                    font-weight: bold;
                    min-height: 45px;
                """)
        else:
            self.cart_header.setText("Shopping Cart")
            self.cart_header.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; padding: 5px;")
            # Reset button text to default
            self.create_order_btn.setText("Save Order")
            self.create_order_btn.setStyleSheet("""
                background-color: #9b59b6;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                min-height: 45px;
            """)
    
    def refresh_cart_display(self) -> None:
        """Refresh the cart display after loading items."""
        # Clear existing cart items
        for widget in self.cart_items.values():
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
        self.cart_items.clear()
        
        # Recreate cart items
        for product_id, cart_item in self.sale_controller.cart.items():
            self.create_item_widget(cart_item.product)
        
        # Update totals
        self.update_totals()
    
    def is_from_loaded_order(self) -> bool:
        """Check if the current cart is from a loaded order."""
        return self.loaded_order is not None
    
    def get_loaded_order_info(self) -> dict:
        """Get information about the loaded order."""
        return {
            'order': self.loaded_order,
            'customer_name': self.loaded_customer_name,
            'notes': self.loaded_notes
        } 

    def checkout_active_order(self) -> None:
        """Checkout an active order by completing it and processing the sale."""
        try:
            if not self.loaded_order:
                QMessageBox.warning(self, "Error", "No order loaded to checkout.")
                return
            
            # Confirm checkout action
            reply = QMessageBox.question(
                self,
                "Confirm Checkout",
                f"Are you sure you want to checkout order {self.loaded_order.order_number}?\n\n"
                f"This will:\n"
                f"• Complete the sale\n"
                f"• Mark the order as completed\n"
                f"• Process payment\n\n"
                f"Customer: {self.loaded_customer_name or 'No name'}\n"
                f"Total: ${self.sale_controller.get_cart_total_with_tax():.2f}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.Yes
            )
            
            if reply == QMessageBox.Yes:
                # First complete the order
                from controllers.order_controller import OrderController
                order_controller = OrderController()
                
                if order_controller.complete_order(self.loaded_order):
                    # Then process the sale
                    if self.sale_controller.complete_sale(self.user):
                        QMessageBox.information(
                            self, 
                            "Success", 
                            f"Order {self.loaded_order.order_number} checked out successfully!\n\n"
                            f"Sale completed and order marked as completed."
                        )
                        self.clear_cart_after_save()
                        
                        # Refresh order management widget to show updated order
                        self.refresh_order_management()
                    else:
                        QMessageBox.warning(self, "Error", "Failed to complete sale. Please try again.")
                else:
                    QMessageBox.warning(self, "Error", "Failed to complete order. Please try again.")
                    
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during checkout: {str(e)}")
            print(f"Checkout error: {e}") 