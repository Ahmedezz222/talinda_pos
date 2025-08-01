from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, 
    QMessageBox, QFrame, QGroupBox, QScrollArea, QWidget
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QBrush
from datetime import datetime

class OpeningAmountDialog(QDialog):
    def __init__(self, parent=None, existing_shift=None):
        super().__init__(parent)
        self.setWindowTitle('Shift Management')
        self.existing_shift = existing_shift
        self.amount = None
        self.action = None  # 'open_new' or 'close_existing'
        
        # Optimized sizes for better proportions
        if existing_shift:
            self.setFixedSize(700, 600)  # Increased for better content display
        else:
            self.setFixedSize(500, 380)  # Better proportions for new shift
            
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
            layout.setSpacing(25)
            layout.setContentsMargins(35, 35, 35, 35)
            self.create_new_shift_ui(layout)

    def create_scrollable_ui(self):
        """Create a scrollable UI for existing shift mode."""
        # Main layout with better margins
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Create scroll area with improved styling
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
                background-color: #f5f5f5;
                width: 14px;
                border-radius: 7px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0c0c0, stop:1 #a0a0a0);
                border-radius: 7px;
                min-height: 30px;
                margin: 2px;
            }
            QScrollBar::handle:vertical:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a0a0a0, stop:1 #808080);
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        
        # Create content widget
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(25)
        content_layout.setContentsMargins(25, 25, 25, 25)
        
        # Add content to the scrollable area
        self.create_existing_shift_ui(content_layout)
        
        # Set the content widget
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

    def create_existing_shift_ui(self, layout):
        """Create UI when there's an existing open shift."""
        # Warning header with gradient background
        warning_label = QLabel("⚠️ You already have an open shift!")
        warning_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            color: #d63031;
            margin-bottom: 20px;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #ffeaa7, stop:1 #fab1a0);
            border-radius: 15px;
            border: 3px solid #e17055;
        """)
        warning_label.setAlignment(Qt.AlignCenter)
        warning_label.setWordWrap(True)
        layout.addWidget(warning_label)
        
        # Existing shift info with gradient
        shift_info_group = QGroupBox("📊 Current Shift Information")
        shift_info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #74b9ff;
                border-radius: 15px;
                margin-top: 20px;
                padding-top: 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f8f9fa, stop:1 #e3f2fd);
                font-size: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 25px;
                padding: 0 15px 0 15px;
                color: #0984e3;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        shift_layout = QVBoxLayout(shift_info_group)
        shift_layout.setSpacing(18)
        shift_layout.setContentsMargins(30, 30, 30, 30)
        
        # Format the open time
        open_time = self.existing_shift.open_time
        if isinstance(open_time, str):
            open_time_str = open_time
        else:
            open_time_str = open_time.strftime("%Y-%m-%d %I:%M:%S %p")
        
        # Create individual labels with gradients
        amount_label = QLabel(f"💰 Opening Amount: ${self.existing_shift.opening_amount:.2f}")
        amount_label.setStyleSheet("""
            font-size: 18px;
            color: #00b894;
            font-weight: bold;
            padding: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e8f5e8, stop:1 #d4edda);
            border-radius: 12px;
            border: 2px solid #00b894;
        """)
        
        time_label = QLabel(f"🕒 Open Time: {open_time_str}")
        time_label.setStyleSheet("""
            font-size: 16px;
            color: #2d3436;
            padding: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            border-radius: 12px;
            border: 2px solid #6c757d;
        """)
        
        status_label = QLabel(f"📋 Status: {self.existing_shift.status.value.title()}")
        status_label.setStyleSheet("""
            font-size: 16px;
            color: #0984e3;
            padding: 12px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #e3f2fd, stop:1 #bbdefb);
            border-radius: 12px;
            border: 2px solid #0984e3;
        """)
        
        shift_layout.addWidget(amount_label)
        shift_layout.addWidget(time_label)
        shift_layout.addWidget(status_label)
        
        layout.addWidget(shift_info_group)
        
        # Options group with gradient
        options_group = QGroupBox("🎯 Choose an Option")
        options_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 3px solid #fdcb6e;
                border-radius: 15px;
                margin-top: 25px;
                padding-top: 25px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #fff8e1, stop:1 #ffecb3);
                font-size: 18px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 25px;
                padding: 0 15px 0 15px;
                color: #e17055;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        
        options_layout = QVBoxLayout(options_group)
        options_layout.setSpacing(25)
        options_layout.setContentsMargins(30, 30, 30, 30)
        
        # Option 1: Close existing shift with gradient button
        close_btn = QPushButton("🔒 Close Current Shift")
        close_btn.setFixedHeight(60)
        close_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #e74c3c, stop:1 #c0392b);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #c0392b, stop:1 #a93226);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #a93226, stop:1 #922b21);
            }
        """)
        close_btn.clicked.connect(self.close_existing_shift)
        
        # Add description for close button
        close_desc = QLabel("Close your current shift and return to login. You'll need to enter your password.")
        close_desc.setStyleSheet("""
            font-size: 14px;
            color: #636e72;
            padding: 8px 0;
            margin-bottom: 15px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
            padding: 10px;
        """)
        close_desc.setWordWrap(True)
        
        options_layout.addWidget(close_desc)
        options_layout.addWidget(close_btn)
        
        # Option 2: Open new shift with gradient button
        new_shift_btn = QPushButton("🔄 Open New Shift (Replace Current)")
        new_shift_btn.setFixedHeight(60)
        new_shift_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498db, stop:1 #2980b9);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 18px;
                font-size: 18px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980b9, stop:1 #21618c);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #21618c, stop:1 #1b4f72);
            }
        """)
        new_shift_btn.clicked.connect(self.open_new_shift)
        
        # Add description for new shift button
        new_shift_desc = QLabel("Replace your current shift with a new one. The current shift will be automatically closed.")
        new_shift_desc.setStyleSheet("""
            font-size: 14px;
            color: #636e72;
            padding: 8px 0;
            margin-bottom: 15px;
            background-color: rgba(255, 255, 255, 0.7);
            border-radius: 8px;
            padding: 10px;
        """)
        new_shift_desc.setWordWrap(True)
        
        options_layout.addWidget(new_shift_desc)
        options_layout.addWidget(new_shift_btn)
        
        layout.addWidget(options_group)
        
        # Cancel button with gradient
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setFixedHeight(55)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c7b7d, stop:1 #5a6c7d);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

    def create_new_shift_ui(self, layout):
        """Create UI for opening a new shift."""
        # Header with gradient
        header_label = QLabel("🆕 Open New Shift")
        header_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2d3436;
            margin-bottom: 25px;
            padding: 20px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #f8f9fa, stop:1 #e9ecef);
            border-radius: 15px;
            border: 3px solid #6c757d;
        """)
        header_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(header_label)
        
        # Amount input
        amount_label = QLabel("💰 Enter opening cash amount:")
        amount_label.setStyleSheet("""
            font-size: 18px; 
            color: #2d3436; 
            margin-bottom: 15px;
            font-weight: bold;
        """)
        layout.addWidget(amount_label)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('e.g. 1000.00')
        self.amount_input.setFixedHeight(60)
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border: 3px solid #bdc3c7;
                border-radius: 12px;
                padding: 18px 25px;
                font-size: 18px;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #f8f9fa);
            }
            QLineEdit:focus {
                border-color: #3498db;
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #ffffff, stop:1 #e3f2fd);
            }
        """)
        layout.addWidget(self.amount_input)
        
        # Add some spacing
        layout.addSpacing(30)
        
        # Buttons with gradients
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(25)
        
        cancel_btn = QPushButton("❌ Cancel")
        cancel_btn.setFixedSize(160, 55)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #95a5a6, stop:1 #7f8c8d);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7f8c8d, stop:1 #6c7b7d);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6c7b7d, stop:1 #5a6c7d);
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        
        ok_btn = QPushButton("✅ Open Shift")
        ok_btn.setFixedSize(160, 55)
        ok_btn.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00b894, stop:1 #00a085);
                color: white;
                border: none;
                border-radius: 12px;
                padding: 15px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #00a085, stop:1 #008f7a);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #008f7a, stop:1 #007f6b);
            }
        """)
        ok_btn.clicked.connect(self.handle_open_new_shift)
        
        btn_layout.addStretch()
        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(ok_btn)
        btn_layout.addStretch()
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