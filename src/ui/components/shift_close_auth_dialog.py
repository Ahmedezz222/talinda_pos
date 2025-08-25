"""
Shift Close Authentication Dialog
================================

Dialog for cashier password authentication when closing shifts.
This ensures only authorized users can close their shifts.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QFrame, QCheckBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPixmap
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class ShiftCloseAuthDialog(QDialog):
    """Dialog for cashier password authentication when closing shift."""
    
    def __init__(self, cashier_name: str, parent=None):
        super().__init__(parent)
        self.cashier_name = cashier_name
        self.password = None
        self.authenticated = False
        
        self.setWindowTitle("Shift Close Authentication")
        self.setFixedSize(400, 350)  # Increased height from 300 to 350
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setModal(True)
        
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(12)  # Reduced from 15
        layout.setContentsMargins(30, 30, 30, 30)  # Increased from 25
        
        # Header section
        self.create_header(layout)
        
        # Authentication section
        self.create_auth_section(layout)
        
        # Footer section
        self.create_footer(layout)
        
        # Apply styling
        self.setStyleSheet(self.get_stylesheet())
    
    def create_header(self, layout):
        """Create the header section with icon and title."""
        # Icon/Logo
        icon_label = QLabel("🔒")
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet("font-size: 40px; margin: 0; padding: 0;")  # Reduced from 42px
        layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel("Shift Close Authentication")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #2f3640;
            margin: 8px 0;
            padding: 0;
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(f"Cashier: {self.cashier_name}")
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; font-size: 12px; margin: 0; padding: 0;")
        layout.addWidget(subtitle_label)
        
        # Warning message
        warning_label = QLabel("Please enter your password to close your shift.")
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setStyleSheet("color: #e74c3c; font-size: 11px; font-weight: bold; margin: 8px 0; padding: 0;")
        layout.addWidget(warning_label)
    
    def create_auth_section(self, layout):
        """Create the authentication section."""
        # Password field
        self.password_input = self.create_password_field()
        layout.addWidget(self.password_input)
        
        # Show password checkbox
        show_pw_layout = QHBoxLayout()
        show_pw_layout.setSpacing(5)
        show_pw_layout.setContentsMargins(0, 8, 0, 0)  # Added top margin
        self.show_password_cb = QCheckBox("Show Password")
        self.show_password_cb.setStyleSheet("color: #7f8c8d; font-size: 11px; margin: 0; padding: 0;")
        show_pw_layout.addWidget(self.show_password_cb)
        show_pw_layout.addStretch()
        layout.addLayout(show_pw_layout)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)  # Increased from 10
        btn_layout.setContentsMargins(0, 15, 0, 0)  # Increased top margin
        
        # Cancel button
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setFixedHeight(40)  # Increased from 38
        self.cancel_btn.setCursor(Qt.PointingHandCursor)
        self.cancel_btn.setProperty("class", "secondary")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                margin: 0;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        
        # Authenticate button
        self.auth_btn = QPushButton("Close Shift")
        self.auth_btn.setFixedHeight(40)  # Increased from 38
        self.auth_btn.setCursor(Qt.PointingHandCursor)
        self.auth_btn.setProperty("class", "danger")
        self.auth_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                margin: 0;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.auth_btn)
        layout.addLayout(btn_layout)
    
    def create_password_field(self) -> QLineEdit:
        """Create a styled password input field."""
        password_field = QLineEdit()
        password_field.setPlaceholderText("🔒 Enter your password")
        password_field.setEchoMode(QLineEdit.Password)
        password_field.setFixedHeight(42)  # Increased from 40
        password_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdde1;
                border-radius: 6px;
                padding: 10px 15px;
                font-size: 13px;
                background-color: white;
                color: #2f3640;
                margin: 0;
            }
            QLineEdit:focus {
                border-color: #0097e6;
                background-color: #f8f9fa;
            }
        """)
        return password_field
    
    def create_footer(self, layout):
        """Create the footer section."""
        footer_label = QLabel("⚠️ Closing your shift will log you out of the system.")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #e67e22; font-size: 10px; font-weight: bold; margin: 10px 0 0 0; padding: 0;")
        layout.addWidget(footer_label)
    
    def setup_connections(self):
        """Setup signal connections."""
        self.show_password_cb.toggled.connect(self.toggle_password_visibility)
        self.cancel_btn.clicked.connect(self.reject)
        self.auth_btn.clicked.connect(self.handle_authentication)
        self.password_input.returnPressed.connect(self.handle_authentication)
    
    def toggle_password_visibility(self, checked: bool):
        """Toggle password field visibility."""
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
    
    def handle_authentication(self):
        """Handle authentication attempt."""
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "Authentication Error", "Please enter your password.")
            return
        
        # Store the password for verification by the calling code
        self.password = password
        self.authenticated = True
        self.accept()
    
    def get_password(self) -> str:
        """Get the entered password."""
        return self.password or ""
    
    def is_authenticated(self) -> bool:
        """Check if authentication was successful."""
        return self.authenticated
    
    def get_stylesheet(self) -> str:
        """Get the stylesheet for the dialog."""
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f6fa, stop:1 #e9ecef);
            }
            
            QLabel {
                color: #2f3640;
                background-color: transparent;
                margin: 0;
                padding: 0;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            
            QLineEdit {
                border: 2px solid #dcdde1;
                border-radius: 6px;
                padding: 10px 15px;
                background-color: white;
                color: #2f3640;
                font-size: 13px;
                min-height: 35px;
                selection-background-color: #0097e6;
                margin: 0;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            
            QLineEdit:focus {
                border-color: #0097e6;
                background-color: #f8f9fa;
            }
            
            QPushButton {
                background-color: #0097e6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                min-height: 35px;
                margin: 0;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            
            QPushButton:hover {
                background-color: #00a8ff;
            }
            
            QPushButton:disabled {
                background-color: #bdc3c7;
                color: #95a5a6;
            }
            
            QCheckBox {
                color: #2f3640;
                font-size: 13px;
                spacing: 8px;
                margin: 0;
                padding: 0;
                font-family: "Segoe UI", Arial, sans-serif;
            }
            
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #dcdde1;
                border-radius: 3px;
                background-color: white;
                margin: 0;
            }
            
            QCheckBox::indicator:checked {
                background-color: #0097e6;
                border-color: #0097e6;
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }
            
            QCheckBox::indicator:hover {
                border-color: #0097e6;
            }
            
            QVBoxLayout, QHBoxLayout {
                spacing: 0;
                margin: 0;
            }
        """ 