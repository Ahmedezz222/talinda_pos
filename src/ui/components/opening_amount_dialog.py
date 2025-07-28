from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QFrame, QGroupBox, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from datetime import datetime

class OpeningAmountDialog(QDialog):
    def __init__(self, parent=None, existing_shift=None):
        super().__init__(parent)
        self.setWindowTitle('Shift Management')
        self.existing_shift = existing_shift
        self.amount = None
        self.action = None  # 'open_new' or 'close_existing'
        
        # Adjust size based on whether there's an existing shift
        if existing_shift:
            self.setFixedSize(600, 550)  # Further increased size for better content display
        else:
            self.setFixedSize(450, 320)  # Increased size for better proportions
            
        # Center the dialog on screen
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.setModal(True)
        
        self.init_ui()

    def init_ui(self):
        if self.existing_shift:
            # Use scroll area for existing shift mode to ensure all content is visible
            self.create_scrollable_ui()
        else:
            # Simple layout for new shift mode
            layout = QVBoxLayout(self)
            layout.setSpacing(20)
            layout.setContentsMargins(30, 30, 30, 30)
            self.create_new_shift_ui(layout)

    def create_scrollable_ui(self):
        """Create a scrollable UI for existing shift mode."""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: #f0f0f0;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: #c0c0c0;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #a0a0a0;
            }
        """)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Add content to the scrollable area
        self.create_existing_shift_ui(content_layout)
        
        # Set the content widget
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def create_existing_shift_ui(self, layout):
        """Create UI when there's an existing open shift."""
        # Warning header
        warning_label = QLabel("⚠️ You already have an open shift!")
        warning_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
            color: #e74c3c;
            margin-bottom: 15px;
            padding: 15px;
            background-color: #fdf2f2;
            border-radius: 10px;
            border: 2px solid #f5b7b1;
        """)
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setWordWrap(True)
        layout.addWidget(warning_label)
        
        # Existing shift info
        shift_info_group = QGroupBox("📊 Current Shift Information")
        shift_info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #3498db;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 20px;
                background-color: #f8f9fa;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: #3498db;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        shift_layout = QVBoxLayout(shift_info_group)
        shift_layout.setSpacing(15)
        shift_layout.setContentsMargins(25, 25, 25, 25)
        
        # Format the open time
        open_time = self.existing_shift.open_time
        if isinstance(open_time, str):
            open_time_str = open_time
        else:
            open_time_str = open_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Create individual labels for better control
        amount_label = QLabel(f"💰 Opening Amount: ${self.existing_shift.opening_amount:.2f}")
        amount_label.setStyleSheet("""
            font-size: 16px;
            color: #27ae60;
            font-weight: bold;
            padding: 8px;
            background-color: #e8f5e8;
            border-radius: 8px;
            border: 1px solid #27ae60;
        """)
        
        time_label = QLabel(f"🕒 Open Time: {open_time_str}")
        time_label.setStyleSheet("""
            font-size: 14px;
            color: #2c3e50;
            padding: 8px;
            background-color: #ecf0f1;
            border-radius: 8px;
            border: 1px solid #bdc3c7;
        """)
        
        status_label = QLabel(f"📋 Status: {self.existing_shift.status.value.title()}")
        status_label.setStyleSheet("""
            font-size: 14px;
            color: #3498db;
            padding: 8px;
            background-color: #ebf3fd;
            border-radius: 8px;
            border: 1px solid #3498db;
        """)
        
        shift_layout.addWidget(amount_label)
        shift_layout.addWidget(time_label)
        shift_layout.addWidget(status_label)
        
        layout.addWidget(shift_info_group)
        
        # Options group
        options_group = QGroupBox("🎯 Choose an Option")
        options_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #e67e22;
                border-radius: 12px;
                margin-top: 20px;
                padding-top: 20px;
                background-color: #fef9e7;
                font-size: 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 20px;
                padding: 0 10px 0 10px;
                color: #e67e22;
                font-size: 16px;
                font-weight: bold;
            }
        """)
        
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(20)
        options_layout.setContentsMargins(25, 25, 25, 25)
        
        # Option 1: Close existing shift
        close_btn = QPushButton("🔒 Close Current Shift")
        close_btn.setFixedHeight(55)  # Increased button height for better usability
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
                transform: scale(1.02);
            }
        """)
        close_btn.clicked.connect(self.close_existing_shift)
        
        # Add description for close button
        close_desc = QLabel("Close your current shift and return to login. You'll need to enter your password.")
        close_desc.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
            padding: 5px 0;
            margin-bottom: 10px;
        """)
        close_desc.setWordWrap(True)
        
        options_layout.addWidget(close_desc)
        options_layout.addWidget(close_btn)
        
        # Option 2: Open new shift (replace current)
        new_shift_btn = QPushButton("🔄 Open New Shift (Replace Current)")
        new_shift_btn.setFixedHeight(55)  # Increased button height for better usability
        new_shift_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
                transform: scale(1.02);
            }
        """)
        new_shift_btn.clicked.connect(self.open_new_shift)
        
        # Add description for new shift button
        new_shift_desc = QLabel("Replace your current shift with a new one. The current shift will be automatically closed.")
        new_shift_desc.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
            padding: 5px 0;
            margin-bottom: 10px;
        """)
        new_shift_desc.setWordWrap(True)
        
        options_layout.addWidget(new_shift_desc)
        options_layout.addWidget(new_shift_btn)
        
        layout.addWidget(options_group)
        
        # Cancel button
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setFixedHeight(50)  # Increased button height
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

    def create_new_shift_ui(self, layout):
        """Create UI for opening a new shift."""
        # Header
        header_label = QLabel("🆕 Open New Shift")
        header_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            padding: 15px;
            background-color: #ecf0f1;
            border-radius: 10px;
            border: 2px solid #bdc3c7;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Amount input
        amount_label = QLabel("💰 Enter opening cash amount:")
        amount_label.setStyleSheet("""
            font-size: 16px; 
            color: #34495e; 
            margin-bottom: 10px;
            font-weight: bold;
        """)
        layout.addWidget(amount_label)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('e.g. 1000.00')
        self.amount_input.setFixedHeight(55)  # Increased input field height
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 10px;
                padding: 15px 20px;
                font-size: 16px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        """)
        layout.addWidget(self.amount_input)
        
        # Add some spacing
        layout.addSpacing(25)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(20)  # Space between buttons
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setFixedSize(140, 50)  # Fixed button size
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("✅ Open Shift")
        ok_btn.setFixedSize(140, 50)  # Fixed button size
        ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 10px;
                padding: 12px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        ok_btn.clicked.connect(self.handle_open_new_shift)
        
        btn_layout.addStretch()  # Add stretch to center buttons
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()  # Add stretch to center buttons
        layout.addLayout(btn_layout)

    def close_existing_shift(self):
        """Handle closing the existing shift."""
        self.action = 'close_existing'
        self.accept()

    def open_new_shift(self):
        """Handle opening a new shift (replacing current)."""
        self.action = 'open_new'
        self.accept()

    def handle_open_new_shift(self):
        """Handle opening a new shift with amount input."""
        try:
            value = float(self.amount_input.text())
            if value < 0:
                raise ValueError
            self.amount = value
            self.action = 'open_new'
            self.accept()
        except ValueError:
            QMessageBox.warning(self, 'Invalid Amount', 'Please enter a valid positive number.') 

    def get_action(self):
        """Get the selected action."""
        return self.action

    def get_amount(self):
        """Get the entered amount."""
        return self.amount 