"""
Cart widget component for the POS interface.
"""
from typing import Dict
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton,
                           QScrollArea, QFrame, QHBoxLayout, QLineEdit, 
                           QDialog, QFormLayout, QDoubleSpinBox, QMessageBox)
from PyQt5.QtCore import Qt
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
        
        # Percentage discount
        self.percent_spin = QDoubleSpinBox()
        self.percent_spin.setRange(0.0, 100.0)
        self.percent_spin.setValue(self.discount_percentage)
        self.percent_spin.setSuffix("%")
        layout.addRow("Discount Percentage:", self.percent_spin)
        
        # Fixed amount discount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.0, 9999.99)
        self.amount_spin.setValue(self.discount_amount)
        self.amount_spin.setPrefix("$")
        self.amount_spin.setDecimals(2)
        layout.addRow("Discount Amount:", self.amount_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
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
        
        # Percentage discount
        self.percent_spin = QDoubleSpinBox()
        self.percent_spin.setRange(0.0, 100.0)
        self.percent_spin.setValue(self.discount_percentage)
        self.percent_spin.setSuffix("%")
        layout.addRow("Cart Discount Percentage:", self.percent_spin)
        
        # Fixed amount discount
        self.amount_spin = QDoubleSpinBox()
        self.amount_spin.setRange(0.0, 9999.99)
        self.amount_spin.setValue(self.discount_amount)
        self.amount_spin.setPrefix("$")
        self.amount_spin.setDecimals(2)
        layout.addRow("Cart Discount Amount:", self.amount_spin)
        
        # Buttons
        btn_layout = QHBoxLayout()
        apply_btn = QPushButton("Apply")
        apply_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(apply_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
    
    def get_discounts(self):
        return self.percent_spin.value(), self.amount_spin.value()

class CartWidget(QWidget):
    """Widget for displaying and managing the shopping cart."""
    
    def __init__(self, sale_controller: SaleController, user=None):
        """Initialize the cart widget."""
        super().__init__()
        self.sale_controller = sale_controller
        self.user = user
        self.cart_items: Dict[int, QWidget] = {}
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Cart header
        header = QLabel("Shopping Cart")
        header.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(header)
        
        # Cart items scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        scroll.setWidget(self.cart_container)
        layout.addWidget(scroll)
        
        # Totals section
        totals_widget = QWidget()
        totals_layout = QVBoxLayout(totals_widget)
        
        # Subtotal
        subtotal_layout = QHBoxLayout()
        subtotal_label = QLabel("Subtotal:")
        subtotal_label.setStyleSheet("font-size: 14px;")
        self.subtotal_amount = QLabel("$0.00")
        self.subtotal_amount.setStyleSheet("font-size: 14px;")
        subtotal_layout.addWidget(subtotal_label)
        subtotal_layout.addWidget(self.subtotal_amount)
        totals_layout.addLayout(subtotal_layout)
        
        # Discount
        discount_layout = QHBoxLayout()
        discount_label = QLabel("Discount:")
        discount_label.setStyleSheet("font-size: 14px; color: #e74c3c;")
        self.discount_amount = QLabel("$0.00")
        self.discount_amount.setStyleSheet("font-size: 14px; color: #e74c3c;")
        discount_layout.addWidget(discount_label)
        discount_layout.addWidget(self.discount_amount)
        totals_layout.addLayout(discount_layout)
        
        # Tax
        tax_layout = QHBoxLayout()
        tax_label = QLabel("Tax:")
        tax_label.setStyleSheet("font-size: 14px; color: #3498db;")
        self.tax_amount = QLabel("$0.00")
        self.tax_amount.setStyleSheet("font-size: 14px; color: #3498db;")
        tax_layout.addWidget(tax_label)
        tax_layout.addWidget(self.tax_amount)
        totals_layout.addLayout(tax_layout)
        
        # Total
        total_layout = QHBoxLayout()
        total_label = QLabel("Total:")
        total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        self.total_amount = QLabel("$0.00")
        self.total_amount.setStyleSheet("font-size: 14px; font-weight: bold;")
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_amount)
        totals_layout.addLayout(total_layout)
        
        layout.addWidget(totals_widget)
        
        # Action buttons
        btn_layout = QHBoxLayout()
        
        # Discount button
        discount_btn = QPushButton("Cart Discount")
        discount_btn.clicked.connect(self.apply_cart_discount)
        discount_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            padding: 8px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        """)
        
        clear_btn = QPushButton("Clear Cart")
        clear_btn.clicked.connect(self.clear_cart)
        clear_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 8px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        """)
        
        checkout_btn = QPushButton("Checkout")
        checkout_btn.clicked.connect(self.checkout)
        checkout_btn.setStyleSheet("""
            background-color: #2ecc71;
            color: white;
            padding: 8px;
            border: none;
            border-radius: 5px;
            font-size: 14px;
        """)
        
        btn_layout.addWidget(discount_btn)
        btn_layout.addWidget(clear_btn)
        btn_layout.addWidget(checkout_btn)
        layout.addLayout(btn_layout)
        
    def add_item(self, product) -> None:
        """
        Add an item to the cart.
        
        Args:
            product: The product to add to the cart
        """
        if self.sale_controller.add_to_cart(product, 1):
            if product.id not in self.cart_items:
                self.create_item_widget(product)
            else:
                self.update_item_widget(product.id)
            self.update_totals()
    
    def create_item_widget(self, product) -> None:
        """
        Create a widget for a cart item.
        
        Args:
            product: The product to create a widget for
        """
        item_widget = QWidget()
        layout = QHBoxLayout(item_widget)
        
        # Product info
        info_layout = QVBoxLayout()
        name_label = QLabel(f"{product.name}")
        name_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        price_label = QLabel(f"${product.price:.2f} each")
        price_label.setStyleSheet("font-size: 14px; color: #666;")
        info_layout.addWidget(name_label)
        info_layout.addWidget(price_label)
        layout.addLayout(info_layout)
        
        # Quantity controls
        qty_layout = QHBoxLayout()
        dec_btn = QPushButton("-")
        dec_btn.setFixedSize(24, 24)
        dec_btn.setStyleSheet("font-size: 14px;")
        dec_btn.clicked.connect(lambda: self.update_quantity(product.id, -1))
        
        qty_label = QLabel("1")
        qty_label.setAlignment(Qt.AlignCenter)
        qty_label.setFixedWidth(30)
        qty_label.setStyleSheet("font-size: 14px;")
        
        inc_btn = QPushButton("+")
        inc_btn.setFixedSize(24, 24)
        inc_btn.setStyleSheet("font-size: 14px;")
        inc_btn.clicked.connect(lambda: self.update_quantity(product.id, 1))
        
        qty_layout.addWidget(dec_btn)
        qty_layout.addWidget(qty_label)
        qty_layout.addWidget(inc_btn)
        layout.addLayout(qty_layout)
        
        # Item total
        item_total_label = QLabel("$0.00")
        item_total_label.setAlignment(Qt.AlignRight)
        item_total_label.setFixedWidth(60)
        item_total_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(item_total_label)
        
        # Discount button
        discount_btn = QPushButton("$")
        discount_btn.setFixedSize(24, 24)
        discount_btn.setToolTip("Apply discount")
        discount_btn.clicked.connect(lambda: self.apply_item_discount(product.id))
        discount_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 14px;
        """)
        layout.addWidget(discount_btn)
        
        # Remove button
        remove_btn = QPushButton("×")
        remove_btn.setFixedSize(24, 24)
        remove_btn.clicked.connect(lambda: self.remove_item(product.id))
        remove_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 3px;
            font-size: 14px;
        """)
        layout.addWidget(remove_btn)
        
        # Store references to labels for easy updating
        item_widget.qty_label = qty_label
        item_widget.item_total_label = item_total_label
        
        self.cart_items[product.id] = item_widget
        self.cart_layout.addWidget(item_widget)
        self.update_item_display(product.id)
    
    def update_item_display(self, product_id: int) -> None:
        """Update the display of a cart item including discounts."""
        if product_id in self.cart_items and product_id in self.sale_controller.cart:
            item = self.sale_controller.cart[product_id]
            widget = self.cart_items[product_id]
            
            # Update quantity label
            if hasattr(widget, 'qty_label'):
                widget.qty_label.setText(str(item.quantity))
            
            # Update total label
            if hasattr(widget, 'item_total_label'):
                if item.discount_total > 0:
                    widget.item_total_label.setText(f"${item.total:.2f}")
                    widget.item_total_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                else:
                    widget.item_total_label.setText(f"${item.total:.2f}")
                    widget.item_total_label.setStyleSheet("")
    
    def update_item_widget(self, product_id: int) -> None:
        """
        Update the display of a cart item.
        
        Args:
            product_id: ID of the product to update
        """
        self.update_item_display(product_id)
    
    def remove_item(self, product_id: int) -> None:
        """
        Remove an item from the cart.
        
        Args:
            product_id: ID of the product to remove
        """
        if product_id in self.cart_items:
            widget = self.cart_items[product_id]
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
            del self.cart_items[product_id]
            self.sale_controller.remove_from_cart(product_id)
            self.update_totals()
    
    def update_quantity(self, product_id: int, change: int) -> None:
        """
        Update the quantity of an item in the cart.
        
        Args:
            product_id: ID of the product to update
            change: Amount to change the quantity by
        """
        if product_id in self.sale_controller.cart:
            item = self.sale_controller.cart[product_id]
            new_qty = item.quantity + change
            
            # Validate quantity
            if new_qty <= 0:
                # Remove item if quantity would be 0 or negative
                self.remove_item(product_id)
                return
            
            # Update quantity if valid
            if self.sale_controller.update_quantity(product_id, new_qty):
                self.update_item_widget(product_id)
                self.update_totals()
    
    def apply_item_discount(self, product_id: int) -> None:
        """Apply discount to a specific cart item."""
        # Check if current user is cashier and requires admin authentication
        if hasattr(self, 'user') and hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
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
        if hasattr(self, 'user') and hasattr(self.user, 'role') and getattr(self.user.role, 'value', None) == 'cashier':
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
    
    def clear_cart(self) -> None:
        """Clear all items from the cart."""
        self.sale_controller.clear_cart()
        for widget in self.cart_items.values():
            self.cart_layout.removeWidget(widget)
            widget.deleteLater()
        self.cart_items.clear()
        self.update_totals()
    
    def checkout(self) -> None:
        """Process the checkout."""
        if not self.sale_controller.cart:
            QMessageBox.warning(self, "Empty Cart", "Cart is empty.")
            return
        
        # Complete sale directly without payment dialog
        try:
            # Note: This requires a user object, but CartWidget doesn't have one
            # For now, we'll just show a message that checkout is not implemented
            QMessageBox.information(self, "Checkout", "Checkout functionality requires user authentication. Please use the enhanced cart widget.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred during checkout: {str(e)}")
