"""
Admin Authentication Dialog for restricted operations.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QLineEdit, QFrame, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from controllers.auth_controller import AuthController
from models.user import UserRole

class AdminAuthDialog(QDialog):
    """Dialog for admin authentication before restricted operations."""
    
    def __init__(self, parent=None, operation="this operation"):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.operation = operation
        self.admin_user = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Admin Authentication Required")
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setModal(True)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Header section
        self.create_header(layout)
        
        # Form section
        self.create_form(layout)
        
        # Footer section
        self.create_footer(layout)
        
        # Apply styling
        self.setStyleSheet(self.get_stylesheet())
    
    def create_header(self, layout):
        """Create the header section."""
        # Icon and title
        header_layout = QHBoxLayout()
        
        # Security icon
        icon_label = QLabel("🔒")
        icon_label.setStyleSheet("font-size: 48px;")
        icon_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(icon_label)
        
        # Title and description
        title_layout = QVBoxLayout()
        
        title_label = QLabel("Admin Authentication")
        title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 5px;
        """)
        
        desc_label = QLabel(f"Admin password required to {self.operation}")
        desc_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        desc_label.setWordWrap(True)
        
        title_layout.addWidget(title_label)
        title_layout.addWidget(desc_label)
        header_layout.addLayout(title_layout)
        
        layout.addLayout(header_layout)
    
    def create_form(self, layout):
        """Create the authentication form."""
        # Username field
        username_layout = QVBoxLayout()
        username_label = QLabel("Admin Username:")
        username_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter admin username")
        self.username_input.setFixedHeight(40)
        self.username_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password field
        password_layout = QVBoxLayout()
        password_label = QLabel("Admin Password:")
        password_label.setStyleSheet("font-weight: bold; color: #2c3e50; font-size: 14px;")
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter admin password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFixedHeight(40)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Add enter key handling for better UX
        self.username_input.returnPressed.connect(lambda: self.password_input.setFocus())
        self.password_input.returnPressed.connect(self.authenticate)
    
    def create_footer(self, layout):
        """Create the footer section with buttons."""
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(10)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setFixedHeight(40)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        # Authenticate button
        auth_btn = QPushButton("Authenticate")
        auth_btn.setFixedHeight(40)
        auth_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        auth_btn.clicked.connect(self.authenticate)
        
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(auth_btn)
        layout.addLayout(btn_layout)
    
    def authenticate(self):
        """Authenticate the admin user."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, "Missing Information", "Please enter both username and password.")
            return
        
        try:
            # Attempt to authenticate
            if self.auth_controller.login(username, password):
                user = self.auth_controller.get_current_user()
                
                # Check if user is admin
                if hasattr(user, 'role') and getattr(user.role, 'value', None) == 'admin':
                    self.admin_user = user
                    QMessageBox.information(self, "Authentication Successful", 
                                          f"Welcome, {user.username}! You can now {self.operation}.")
                    self.accept()
                else:
                    QMessageBox.warning(self, "Access Denied", 
                                      "Only administrators can perform this operation.")
                    self.password_input.clear()
            else:
                QMessageBox.warning(self, "Authentication Failed", 
                                  "Invalid username or password.")
                self.password_input.clear()
                
        except Exception as e:
            QMessageBox.critical(self, "Authentication Error", 
                               f"An error occurred during authentication: {str(e)}")
    
    def get_stylesheet(self) -> str:
        """Get the stylesheet for the dialog."""
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
        """
    
    def get_admin_user(self):
        """Get the authenticated admin user."""
        return self.admin_user 