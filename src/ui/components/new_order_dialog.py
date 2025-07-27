"""
Dialog for creating new orders with customer names and cart items.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QTextEdit, QMessageBox,
                           QScrollArea, QFrame, QWidget, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont
from controllers.order_controller import OrderController
from controllers.sale_controller import SaleController
from models.user import User

class NewOrderDialog(QDialog):
    """Dialog for creating a new order."""
    
    # Signals
    order_created = pyqtSignal(object)  # Emitted when order is created
    
    def __init__(self, user: User, sale_controller: SaleController, parent=None):
        super().__init__(parent)
        self.user = user
        self.sale_controller = sale_controller
        self.order_controller = OrderController()
        self.order = None
        self.setWindowTitle("Create New Order")
        self.setFixedSize(500, 600)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header_label = QLabel("Save New Order")
        header_label.setFont(QFont("Arial", 16, QFont.Bold))
        header_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Customer name input
        layout.addWidget(QLabel("Customer Name (optional):"))
        self.customer_name_input = QLineEdit()
        self.customer_name_input.setPlaceholderText("Enter customer name...")
        self.customer_name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.customer_name_input)
        
        # Notes input
        layout.addWidget(QLabel("Notes (optional):"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText("Enter any special instructions or notes...")
        self.notes_input.setMaximumHeight(80)
        self.notes_input.setStyleSheet("""
            QTextEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 12px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.notes_input)
        
        # Cart items display
        layout.addWidget(QLabel("Cart Items:"))
        
        # Scroll area for cart items
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setMaximumHeight(200)
        
        self.cart_container = QWidget()
        self.cart_layout = QVBoxLayout(self.cart_container)
        scroll.setWidget(self.cart_container)
        layout.addWidget(scroll)
        
        # Display cart items
        self.display_cart_items()
        
        # Total amount
        total_layout = QHBoxLayout()
        total_label = QLabel("Total Amount:")
        total_label.setFont(QFont("Arial", 14, QFont.Bold))
        total_label.setStyleSheet("color: #2c3e50;")
        
        self.total_amount_label = QLabel(f"${self.sale_controller.get_cart_total():.2f}")
        self.total_amount_label.setFont(QFont("Arial", 14, QFont.Bold))
        self.total_amount_label.setStyleSheet("color: #27ae60;")
        
        total_layout.addWidget(total_label)
        total_layout.addStretch()
        total_layout.addWidget(self.total_amount_label)
        layout.addLayout(total_layout)
        
        # Warning if cart is empty
        if not self.sale_controller.cart:
            warning_label = QLabel("⚠️ Cart is empty. Please add items before creating an order.")
            warning_label.setStyleSheet("color: #e74c3c; font-weight: bold; padding: 10px; background-color: #fdf2f2; border-radius: 5px;")
            warning_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(warning_label)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            background-color: #95a5a6;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
        """)
        
        create_btn = QPushButton("Save Order")
        create_btn.clicked.connect(self.create_order)
        create_btn.setEnabled(bool(self.sale_controller.cart))
        create_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            font-size: 14px;
            font-weight: bold;
        """)
        self.create_button = create_btn
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(create_btn)
        layout.addLayout(btn_layout)
    
    def display_cart_items(self):
        """Display cart items in the dialog."""
        # Clear existing items
        while self.cart_layout.count():
            item = self.cart_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        if not self.sale_controller.cart:
            no_items_label = QLabel("No items in cart")
            no_items_label.setStyleSheet("color: #7f8c8d; font-style: italic; padding: 20px;")
            no_items_label.setAlignment(Qt.AlignCenter)
            self.cart_layout.addWidget(no_items_label)
            return
        
        # Display each cart item
        for product_id, cart_item in self.sale_controller.cart.items():
            item_widget = self.create_cart_item_widget(cart_item)
            self.cart_layout.addWidget(item_widget)
        
        # Add stretch to push items to top
        self.cart_layout.addStretch()
    
    def create_cart_item_widget(self, cart_item):
        """Create a widget for displaying a cart item."""
        item_frame = QFrame()
        item_frame.setFrameStyle(QFrame.StyledPanel)
        item_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }
        """)
        
        layout = QHBoxLayout(item_frame)
        
        # Product info
        info_layout = QVBoxLayout()
        
        name_label = QLabel(cart_item.product.name)
        name_label.setFont(QFont("Arial", 12, QFont.Bold))
        name_label.setStyleSheet("color: #2c3e50;")
        info_layout.addWidget(name_label)
        
        price_label = QLabel(f"${cart_item.price:.2f} each")
        price_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        info_layout.addWidget(price_label)
        
        layout.addLayout(info_layout)
        layout.addStretch()
        
        # Quantity and total
        qty_layout = QVBoxLayout()
        
        qty_label = QLabel(f"Qty: {cart_item.quantity}")
        qty_label.setStyleSheet("color: #34495e; font-weight: bold;")
        qty_layout.addWidget(qty_label)
        
        total_label = QLabel(f"${cart_item.total:.2f}")
        total_label.setStyleSheet("color: #27ae60; font-weight: bold; font-size: 12px;")
        qty_layout.addWidget(total_label)
        
        layout.addLayout(qty_layout)
        
        return item_frame
    
    def create_order(self):
        """Save the order."""
        if not self.sale_controller.cart:
            QMessageBox.warning(self, "Empty Cart", "Please add items to the cart before saving an order.")
            return
        
        customer_name = self.customer_name_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        try:
            # Create the order
            self.order = self.order_controller.create_order(
                user=self.user,
                customer_name=customer_name if customer_name else None,
                notes=notes if notes else None
            )
            
            # Add cart items to the order
            items = []
            for product_id, cart_item in self.sale_controller.cart.items():
                items.append({
                    'product_id': product_id,
                    'quantity': cart_item.quantity,
                    'price': cart_item.price,
                    'notes': None  # Could add item-specific notes here
                })
            
            if self.order_controller.add_items_to_order(self.order, items):
                # Refresh the session to ensure the order is properly saved
                self.order_controller.refresh_session()
                QMessageBox.information(self, "Success", f"Order {self.order.order_number} saved successfully!")
                self.order_created.emit(self.order)
                self.accept()
            else:
                QMessageBox.warning(self, "Error", "Failed to add items to order.")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create order: {str(e)}")
            print(f"Order creation error: {e}")


class OrderNameTagDialog(QDialog):
    """Simple dialog for adding a name tag to an order."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.customer_name = ""
        self.setWindowTitle("Add Name Tag")
        self.setFixedSize(300, 150)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Enter customer name for the order:"))
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Customer name...")
        self.name_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        layout.addWidget(self.name_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            background-color: #95a5a6;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
        """)
        
        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        ok_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
        """)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)
    
    def accept(self):
        """Accept the dialog and save the customer name."""
        self.customer_name = self.name_input.text().strip()
        super().accept() 