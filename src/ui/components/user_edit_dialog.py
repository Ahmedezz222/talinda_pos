"""
User Edit Dialog for managing user information and passwords.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QComboBox, QCheckBox, QMessageBox, QFormLayout,
    QGroupBox, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
import bcrypt
from models.user import User, UserRole
from database.db_config import Session, safe_commit

class UserEditDialog(QDialog):
    """Dialog for editing user information and changing passwords."""
    
    def __init__(self, user=None, parent=None):
        super().__init__(parent)
        self.user = user
        self.session = Session()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Edit User" if self.user else "Add User")
        self.setFixedSize(450, 550)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(25, 25, 25, 25)
        
        # Title
        title = QLabel("Edit User" if self.user else "Add New User")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # User Information Group
        info_group = QGroupBox("User Information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
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
        
        info_layout = QFormLayout(info_group)
        info_layout.setSpacing(12)
        info_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        info_layout.setLabelAlignment(Qt.AlignRight)
        
        # Username
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        info_layout.addRow("Username:", self.username_input)
        
        # Full Name
        self.fullname_input = QLineEdit()
        self.fullname_input.setPlaceholderText("Enter full name")
        self.fullname_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        info_layout.addRow("Full Name:", self.fullname_input)
        
        # Role
        self.role_combo = QComboBox()
        self.role_combo.addItems([role.value.title() for role in UserRole])
        self.role_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QComboBox:focus {
                border: 2px solid #3498db;
            }
        """)
        info_layout.addRow("Role:", self.role_combo)
        
        # Active Status
        self.active_checkbox = QCheckBox("Active")
        self.active_checkbox.setChecked(True)
        self.active_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        info_layout.addRow("Status:", self.active_checkbox)
        
        layout.addWidget(info_group)
        
        # Password Group
        password_group = QGroupBox("Password")
        password_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
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
        
        password_layout = QFormLayout(password_group)
        password_layout.setSpacing(12)
        password_layout.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        password_layout.setLabelAlignment(Qt.AlignRight)
        
        # New Password
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter new password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        password_layout.addRow("New Password:", self.password_input)
        
        # Confirm Password
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm new password")
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        self.confirm_password_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3498db;
            }
        """)
        password_layout.addRow("Confirm Password:", self.confirm_password_input)
        
        # Add password requirements note
        password_note = QLabel("Note: Password must be at least 6 characters long")
        password_note.setStyleSheet("""
            QLabel {
                color: #7f8c8d;
                font-size: 11px;
                font-style: italic;
                margin-top: 5px;
            }
        """)
        password_note.setAlignment(Qt.AlignCenter)
        password_layout.addRow("", password_note)
        
        layout.addWidget(password_group)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(15)
        button_layout.addStretch(1)
        
        self.save_btn = QPushButton("Save")
        self.save_btn.setShortcut("Ctrl+S")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        self.save_btn.clicked.connect(self.save_user)
        
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setShortcut("Esc")
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.cancel_btn)
        button_layout.addStretch(1)
        
        layout.addLayout(button_layout)
        
        # Add some spacing at the bottom
        layout.addStretch(1)
        
        # Load user data if editing
        if self.user:
            self.load_user_data()
    
    def load_user_data(self):
        """Load existing user data into the form."""
        self.username_input.setText(self.user.username)
        self.fullname_input.setText(self.user.full_name or "")
        self.role_combo.setCurrentText(self.user.role.value.title())
        self.active_checkbox.setChecked(self.user.active == 1)
        
        # Clear password fields for existing users (optional to change)
        self.password_input.clear()
        self.confirm_password_input.clear()
        
        # Disable username editing for existing users
        self.username_input.setEnabled(False)
        self.username_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #bdc3c8;
                border-radius: 4px;
                font-size: 14px;
                background-color: #f8f9fa;
                color: #6c757d;
            }
        """)
        
        # Update password field placeholders for existing users
        self.password_input.setPlaceholderText("Leave blank to keep current password")
        self.confirm_password_input.setPlaceholderText("Leave blank to keep current password")
    
    def validate_inputs(self):
        """Validate form inputs."""
        username = self.username_input.text().strip()
        fullname = self.fullname_input.text().strip()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()
        
        # Username validation
        if not username:
            QMessageBox.warning(self, "Validation Error", "Username is required!")
            self.username_input.setFocus()
            return False
        
        if len(username) < 3:
            QMessageBox.warning(self, "Validation Error", "Username must be at least 3 characters long!")
            self.username_input.setFocus()
            return False
        
        # Full name validation
        if not fullname:
            QMessageBox.warning(self, "Validation Error", "Full name is required!")
            self.fullname_input.setFocus()
            return False
        
        # Check if username already exists (for new users)
        if not self.user:
            existing_user = self.session.query(User).filter_by(username=username).first()
            if existing_user:
                QMessageBox.warning(self, "Validation Error", "Username already exists!")
                self.username_input.setFocus()
                return False
        
        # Password validation
        if password:
            if len(password) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters long!")
                self.password_input.setFocus()
                return False
            
            if password != confirm_password:
                QMessageBox.warning(self, "Validation Error", "Passwords do not match!")
                self.confirm_password_input.setFocus()
                return False
        
        return True
    
    def save_user(self):
        """Save user information."""
        if not self.validate_inputs():
            return
        
        try:
            username = self.username_input.text().strip()
            fullname = self.fullname_input.text().strip()
            role = UserRole(self.role_combo.currentText().lower())
            active = 1 if self.active_checkbox.isChecked() else 0
            password = self.password_input.text()
            
            if self.user:
                # Update existing user
                self.user.full_name = fullname
                self.user.role = role
                self.user.active = active
                
                # Update password if provided
                if password:
                    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                    self.user.password_hash = password_hash
                
                self.session.commit()
                QMessageBox.information(self, "Success", "User updated successfully!")
                
            else:
                # Create new user
                if not password:
                    QMessageBox.warning(self, "Validation Error", "Password is required for new users!")
                    return
                
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                new_user = User(
                    username=username,
                    password_hash=password_hash,
                    role=role,
                    full_name=fullname,
                    active=active
                )
                
                self.session.add(new_user)
                self.session.commit()
                QMessageBox.information(self, "Success", "User created successfully!")
            
            self.accept()
            
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, "Error", f"Failed to save user: {str(e)}")
    
    def closeEvent(self, event):
        """Handle close event."""
        try:
            self.session.close()
        except:
            pass
        super().closeEvent(event) 