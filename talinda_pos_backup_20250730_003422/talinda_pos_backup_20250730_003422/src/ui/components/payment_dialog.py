"""
Payment dialog for processing transactions.
"""
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                           QPushButton, QLineEdit, QFrame, QWidget)
from PyQt5.QtCore import Qt
from controllers.sale_controller import SaleController

class PaymentDialog(QDialog):
    """Dialog for processing payments."""
    
    def __init__(self, sale_controller: SaleController, parent=None):
        """Initialize the payment dialog."""
        super().__init__(parent)
        self.sale_controller = sale_controller
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle('Payment')
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout(self)
        
        # Total amount
        total_widget = QWidget()
        total_layout = QHBoxLayout(total_widget)
        
        total_label = QLabel("Total Amount:")
        total_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        self.total_amount = QLabel(f"${self.sale_controller.get_cart_total_with_tax():.2f}")
        self.total_amount.setStyleSheet("font-size: 18px; font-weight: bold;")
        
        total_layout.addWidget(total_label)
        total_layout.addWidget(self.total_amount)
        layout.addWidget(total_widget)
        
        # Payment amount input
        amount_widget = QWidget()
        amount_layout = QHBoxLayout(amount_widget)
        
        amount_label = QLabel("Payment:")
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Enter payment amount")
        self.amount_input.textChanged.connect(self.validate_payment)
        
        amount_layout.addWidget(amount_label)
        amount_layout.addWidget(self.amount_input)
        layout.addWidget(amount_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        confirm_btn = QPushButton("Confirm Payment")
        confirm_btn.clicked.connect(self.accept)
        confirm_btn.setEnabled(False)
        self.confirm_button = confirm_btn
        
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(confirm_btn)
        layout.addLayout(button_layout)
    
    def validate_payment(self):
        """Validate the payment amount."""
        try:
            payment = float(self.amount_input.text() or 0)
            total = self.sale_controller.get_cart_total_with_tax()
            self.confirm_button.setEnabled(payment >= total)
        except ValueError:
            self.confirm_button.setEnabled(False)
