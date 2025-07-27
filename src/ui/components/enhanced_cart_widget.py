"""
Enhanced cart widget that supports both regular POS sales and table orders.
"""
import sys
import os

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


class DiscountDialog(QDialog):
    """Dialog for applying discounts to cart items."""
    
    def __init__(self, parent=None, item_name="", current_discount_percent=0.0, current_discount_amount=0.0):
        super().__init__(parent)
        self.setWindowTitle(f"Apply Discount - {item_name}")
        self.setFixedSize(300, 200)
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
        self.setFixedSize(300, 200)
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
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Cart header
        header = QLabel("Shopping Cart")
        header.setStyleSheet("font-size: 16px; font-weight: bold; color: #2c3e50; padding: 5px;")
        layout.addWidget(header)
        
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
        else:
            QMessageBox.warning(self, "Stock Error", f"Insufficient stock for {product.name}")
    
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
        
        self.qty_label = QLabel("1")
        self.qty_label.setStyleSheet("""
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
        qty_controls.addWidget(self.qty_label)
        qty_controls.addWidget(plus_btn)
        qty_layout.addLayout(qty_controls)
        
        item_layout.addLayout(qty_layout)
        
        # Total and actions (right side)
        total_layout = QVBoxLayout()
        total_layout.setSpacing(4)
        
        self.item_total_label = QLabel(f"${product.price:.2f}")
        self.item_total_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        total_layout.addWidget(self.item_total_label)
        
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
        remove_btn.setStyleSheet("""
            background-color: #e74c3c; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            font-weight: bold;
            font-size: 16px;
        """)
        
        action_layout.addWidget(discount_btn)
        action_layout.addWidget(remove_btn)
        total_layout.addLayout(action_layout)
        
        item_layout.addLayout(total_layout)
        
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
            if new_qty > 0 and self.sale_controller.update_quantity(product_id, new_qty):
                self.update_item_widget(product_id)
                self.update_totals()
    
    def apply_item_discount(self, product_id: int) -> None:
        """Apply discount to a specific cart item."""
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
    
    def clear_cart(self) -> None:
        """Clear all items from the cart."""
        self.sale_controller.clear_cart()
        for widget in self.cart_items.values():
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
        self.cart_items.clear()
        self.update_totals()
    
    def create_order(self) -> None:
        """Save a new order from cart items."""
        if not self.sale_controller.cart:
            QMessageBox.warning(self, "Empty Cart", "Cart is empty. Please add items before saving an order.")
            return
        
        # Show new order dialog
        from ui.components.new_order_dialog import NewOrderDialog
        dialog = NewOrderDialog(self.user, self.sale_controller, self)
        if dialog.exec_() == QDialog.Accepted and dialog.order:
            QMessageBox.information(self, "Success", "Order saved successfully!")
            # Clear cart after saving order
            self.clear_cart()
            # Emit signal to refresh order management
            if hasattr(self, 'order_saved'):
                self.order_saved.emit(dialog.order)
    
    def checkout(self) -> None:
        """Process the checkout."""
        if not self.sale_controller.cart:
            QMessageBox.warning(self, "Empty Cart", "Cart is empty.")
            return
        
        # Show payment dialog and complete sale
        from ui.components.payment_dialog import PaymentDialog
        dialog = PaymentDialog(self.sale_controller, self)
        if dialog.exec_() == QDialog.Accepted:
            if self.sale_controller.complete_sale(self.user):
                QMessageBox.information(self, "Success", "Sale completed successfully!")
                self.clear_cart()
            else:
                QMessageBox.warning(self, "Error", "Failed to complete sale.")
    
    def load_order(self, order) -> None:
        """Load an order into the cart."""
        # Load order items into cart
        self.sale_controller.load_order_to_cart(order)
        
        # Refresh cart display
        self.refresh_cart_display()
        
        # Show confirmation
        QMessageBox.information(self, "Order Loaded", "Order loaded into cart!")
    
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