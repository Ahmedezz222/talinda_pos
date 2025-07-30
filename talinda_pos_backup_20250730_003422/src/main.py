#!/usr/bin/env python3
"""
Talinda POS System - Main Entry Point
=====================================

A comprehensive Point of Sale system built with PyQt5 and SQLAlchemy.
This module serves as the main entry point for the application.

Author: Talinda POS Team
Version: 2.0.0
License: MIT
"""

import sys
import os
import logging
import traceback
from pathlib import Path
from typing import Optional, Tuple
import datetime

# Add the src directory to Python path for imports
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

# Third-party imports
from PyQt5.QtWidgets import (
    QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox, QHBoxLayout, QCheckBox, 
    QSpacerItem, QSizePolicy, QFrame, QProgressBar
)
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QPropertyAnimation, QEasingCurve

# Local imports
from controllers.auth_controller import AuthController
from ui.main_window import MainWindow
from ui.components.opening_amount_dialog import OpeningAmountDialog
from models.user import Shift, ShiftStatus
from init_database import init_database
from utils.background_tasks import BackgroundTaskManager
from utils.daily_reset_task import DailyResetTask
from database.db_config import safe_commit
from utils.localization import tr, set_language, is_rtl


# Import configuration
from config import get_config

# Get configuration instance
config = get_config()

class ApplicationConfig:
    """Configuration class for the application."""
    
    APP_NAME = config.APP_NAME
    APP_VERSION = config.APP_VERSION
    APP_AUTHOR = config.APP_AUTHOR
    
    # Window settings
    LOGIN_WINDOW_SIZE = (400, 500)
    LOGIN_WINDOW_TITLE = f"{APP_NAME} - Login"
    
    # File paths
    CSS_FILE = config.CSS_FILE
    LOGO_FILE = config.LOGO_FILE
    
    # Styling
    PRIMARY_COLOR = config.PRIMARY_COLOR
    SECONDARY_COLOR = config.SECONDARY_COLOR
    SUCCESS_COLOR = config.SUCCESS_COLOR
    ERROR_COLOR = config.ERROR_COLOR
    WARNING_COLOR = config.WARNING_COLOR


class LoggingConfig:
    """Configuration for application logging."""
    
    @staticmethod
    def setup_logging():
        """Setup application logging configuration."""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=config.get_log_level(),
            format=config.LOG_FORMAT,
            handlers=[
                logging.FileHandler(log_dir / Path(config.LOG_FILE).name),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        # Set specific loggers
        logging.getLogger('PyQt5').setLevel(logging.WARNING)
        logging.getLogger('sqlalchemy').setLevel(logging.WARNING)


class SplashScreen(QDialog):
    """Splash screen shown during application startup."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle(ApplicationConfig.APP_NAME)
        self.setFixedSize(400, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the splash screen UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Main frame
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 15px;
                border: 2px solid #e0e0e0;
            }
        """)
        
        frame_layout = QVBoxLayout(frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(30, 30, 30, 30)
        
        # Logo/Title
        title_label = QLabel(ApplicationConfig.APP_NAME)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"""
            font-size: 24px;
            font-weight: bold;
            color: {ApplicationConfig.PRIMARY_COLOR};
            margin-bottom: 10px;
        """)
        frame_layout.addWidget(title_label)
        
        # Version
        version_label = QLabel(f"Version {ApplicationConfig.APP_VERSION}")
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setStyleSheet("color: #666; font-size: 12px;")
        frame_layout.addWidget(version_label)
        
        # Loading message
        self.loading_label = QLabel("Initializing application...")
        self.loading_label.setAlignment(Qt.AlignCenter)
        self.loading_label.setStyleSheet("color: #333; font-size: 14px;")
        frame_layout.addWidget(self.loading_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #1976d2;
                border-radius: 4px;
            }
        """)
        self.progress_bar.setRange(0, 100)
        frame_layout.addWidget(self.progress_bar)
        
        layout.addWidget(frame)
    
    def update_progress(self, value: int, message: str = ""):
        """Update progress bar and loading message."""
        self.progress_bar.setValue(value)
        if message:
            self.loading_label.setText(message)
        QApplication.processEvents()


class ModernLoginDialog(QDialog):
    """Modern login dialog with improved UI and functionality."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.auth_controller = AuthController()
        self.user = None
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the login dialog UI."""
        self.setWindowTitle(ApplicationConfig.LOGIN_WINDOW_TITLE)
        self.setFixedSize(*ApplicationConfig.LOGIN_WINDOW_SIZE)
        self.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(40, 30, 40, 30)
        
        # Header section
        self.create_header(layout)
        
        # Form section
        self.create_form(layout)
        
        # Footer section
        self.create_footer(layout)
        
        # Apply styling
        self.setStyleSheet(self.get_stylesheet())
        
        # Set initial focus to username field
        self.username_input.setFocus()
        
        # Initialize step indicator
        self.update_step_indicator(1)
        
        # Enable keyboard shortcuts
        self.setup_keyboard_shortcuts()
    
    def create_header(self, layout):
        """Create the header section with logo and title."""
        # Logo
        logo_label = QLabel()
        logo_path = current_dir / ApplicationConfig.LOGO_FILE
        
        if logo_path.exists():
            pixmap = QPixmap(str(logo_path))
            if not pixmap.isNull():
                logo_label.setPixmap(pixmap.scaledToHeight(60, Qt.SmoothTransformation))
        else:
            logo_label.setText("🛒")
            logo_label.setStyleSheet("font-size: 48px;")
        
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Title
        title_label = QLabel(tr("login.title", "Welcome Back"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin: 10px 0;
        """)
        layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel(tr("login.subtitle", "Please sign in to continue"))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout.addWidget(subtitle_label)
    
    def create_form(self, layout):
        """Create the login form section."""
        # Username field
        self.username_input = self.create_input_field(tr("login.username", "Username"), "👤")
        layout.addWidget(self.username_input)
        
        # Password field
        self.password_input = self.create_input_field(tr("login.password", "Password"), "🔒", is_password=True)
        layout.addWidget(self.password_input)
        
        # Show password checkbox
        show_pw_layout = QHBoxLayout()
        self.show_password_cb = QCheckBox(tr("login.show_password", "Show Password"))
        self.show_password_cb.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        show_pw_layout.addWidget(self.show_password_cb)
        show_pw_layout.addStretch()
        layout.addLayout(show_pw_layout)
        
        # Login button
        self.login_btn = QPushButton(tr("login.sign_in", "Sign In"))
        self.login_btn.setFixedHeight(45)
        self.login_btn.setCursor(Qt.PointingHandCursor)
        self.login_btn.setToolTip("Click to login or press Enter in password field")
        layout.addWidget(self.login_btn)
        
        # Add step indicator
        self.create_step_indicator(layout)
    
    def create_step_indicator(self, layout):
        """Create a visual step indicator for the login process."""
        step_layout = QHBoxLayout()
        step_layout.setSpacing(10)
        
        # Step 1: Username
        self.step1_label = QLabel(f"1. {tr('login.username', 'Username')}")
        self.step1_label.setStyleSheet("""
            QLabel {
                color: #1976d2;
                font-weight: bold;
                font-size: 12px;
                padding: 5px 10px;
                background-color: #e3f2fd;
                border-radius: 15px;
                border: 1px solid #1976d2;
            }
        """)
        
        # Step 2: Password
        self.step2_label = QLabel(f"2. {tr('login.password', 'Password')}")
        self.step2_label.setStyleSheet("""
            QLabel {
                color: #9e9e9e;
                font-size: 12px;
                padding: 5px 10px;
                background-color: #f5f5f5;
                border-radius: 15px;
                border: 1px solid #e0e0e0;
            }
        """)
        
        step_layout.addWidget(self.step1_label)
        step_layout.addWidget(self.step2_label)
        step_layout.addStretch()
        
        layout.addLayout(step_layout)
    
    def update_step_indicator(self, current_step):
        """Update the step indicator to show current progress."""
        if current_step == 1:
            # Username step active
            self.step1_label.setStyleSheet("""
                QLabel {
                    color: #1976d2;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #e3f2fd;
                    border-radius: 15px;
                    border: 1px solid #1976d2;
                }
            """)
            self.step2_label.setStyleSheet("""
                QLabel {
                    color: #9e9e9e;
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #f5f5f5;
                    border-radius: 15px;
                    border: 1px solid #e0e0e0;
                }
            """)
        elif current_step == 2:
            # Password step active
            self.step1_label.setStyleSheet("""
                QLabel {
                    color: #4caf50;
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #e8f5e8;
                    border-radius: 15px;
                    border: 1px solid #4caf50;
                }
            """)
            self.step2_label.setStyleSheet("""
                QLabel {
                    color: #1976d2;
                    font-weight: bold;
                    font-size: 12px;
                    padding: 5px 10px;
                    background-color: #e3f2fd;
                    border-radius: 15px;
                    border: 1px solid #1976d2;
                }
            """)
    
    def create_input_field(self, placeholder: str, icon: str, is_password: bool = False) -> QLineEdit:
        """Create a styled input field with enhanced keyboard navigation."""
        input_field = QLineEdit()
        input_field.setPlaceholderText(f"{icon} {placeholder}")
        input_field.setFixedHeight(45)
        input_field.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 14px;
                background-color: white;
                transition: border-color 0.2s ease;
            }
            QLineEdit:focus {
                border-color: #1976d2;
                background-color: #f8f9fa;
                box-shadow: 0 0 0 2px rgba(25, 118, 210, 0.2);
            }
            QLineEdit:disabled {
                background-color: #f5f5f5;
                color: #999;
            }
        """)
        
        # Set input method hints for better mobile/tablet support
        if is_password:
            input_field.setEchoMode(QLineEdit.Password)
            input_field.setInputMethodHints(Qt.ImhHiddenText)
        else:
            input_field.setInputMethodHints(Qt.ImhPreferUppercase)
        
        # Add tooltip with keyboard shortcuts
        if is_password:
            input_field.setToolTip("Enter your password\nPress Enter to login")
        else:
            input_field.setToolTip("Enter your username\nPress Enter to continue")
        
        return input_field
    
    def create_footer(self, layout):
        """Create the footer section."""
        footer_label = QLabel(f"© 2024 {ApplicationConfig.APP_AUTHOR}")
        footer_label.setAlignment(Qt.AlignCenter)
        footer_label.setStyleSheet("color: #95a5a6; font-size: 11px; margin-top: 20px;")
        layout.addWidget(footer_label)
    
    def setup_connections(self):
        """Setup signal connections."""
        self.show_password_cb.toggled.connect(self.toggle_password_visibility)
        self.login_btn.clicked.connect(self.handle_login)
        
        # Enhanced Enter key handling for better navigation flow
        self.username_input.returnPressed.connect(self.on_username_enter)
        self.password_input.returnPressed.connect(self.on_password_enter)
        
        # Connect focus signals for step indicator
        self.username_input.textChanged.connect(lambda: self.on_username_changed())
        self.password_input.textChanged.connect(lambda: self.on_password_changed())
        
        # Set tab order for better keyboard navigation
        self.setTabOrder(self.username_input, self.password_input)
        self.setTabOrder(self.password_input, self.show_password_cb)
        self.setTabOrder(self.show_password_cb, self.login_btn)
    
    def on_username_changed(self):
        """Handle username field text changes."""
        username = self.username_input.text().strip()
        if username:
            self.update_step_indicator(2)  # Move to password step
        else:
            self.update_step_indicator(1)  # Stay on username step
    
    def on_password_changed(self):
        """Handle password field text changes."""
        password = self.password_input.text()
        username = self.username_input.text().strip()
        
        if username and password:
            # Both fields have content, ready for login
            self.login_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4caf50;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3d8b40;
                }
            """)
        else:
            # Reset button style
            self.login_btn.setStyleSheet("""
                QPushButton {
                    background-color: #1976d2;
                    color: white;
                    border: none;
                    border-radius: 8px;
                    font-size: 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #1565c0;
                }
                QPushButton:pressed {
                    background-color: #0d47a1;
                }
            """)
    
    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for better user experience."""
        from PyQt5.QtWidgets import QShortcut
        from PyQt5.QtGui import QKeySequence
        
        # Ctrl+L to focus login button
        login_shortcut = QShortcut(QKeySequence("Ctrl+L"), self)
        login_shortcut.activated.connect(self.handle_login)
        
        # Ctrl+U to focus username field
        username_shortcut = QShortcut(QKeySequence("Ctrl+U"), self)
        username_shortcut.activated.connect(lambda: self.username_input.setFocus())
        
        # Ctrl+P to focus password field
        password_shortcut = QShortcut(QKeySequence("Ctrl+P"), self)
        password_shortcut.activated.connect(lambda: self.password_input.setFocus())
        
        # Escape to clear fields
        escape_shortcut = QShortcut(QKeySequence("Escape"), self)
        escape_shortcut.activated.connect(self.clear_fields)
    
    def clear_fields(self):
        """Clear all input fields."""
        self.username_input.clear()
        self.password_input.clear()
        self.username_input.setFocus()
    
    def on_username_enter(self):
        """Handle Enter key press in username field."""
        username = self.username_input.text().strip()
        if username:
            # If username is entered, move to password field
            self.password_input.setFocus()
            self.password_input.selectAll()  # Select all text for easy replacement
            self.update_step_indicator(2)  # Update to password step
        else:
            # If username is empty, show subtle error and keep focus
            self.show_field_error(self.username_input, "Username is required")
            self.username_input.setFocus()
            self.update_step_indicator(1)  # Stay on username step
    
    def on_password_enter(self):
        """Handle Enter key press in password field."""
        password = self.password_input.text()
        username = self.username_input.text().strip()
        
        if not username:
            # If username is empty, move back to username field
            self.show_field_error(self.username_input, "Username is required")
            self.username_input.setFocus()
            self.username_input.selectAll()
            self.update_step_indicator(1)  # Back to username step
        elif not password:
            # If password is empty, show subtle error and keep focus
            self.show_field_error(self.password_input, "Password is required")
            self.password_input.setFocus()
            self.update_step_indicator(2)  # Stay on password step
        else:
            # Both fields have content, attempt login
            self.handle_login()
    
    def show_field_error(self, field, message):
        """Show a subtle error message for a specific field."""
        # Temporarily change border color to indicate error
        original_style = field.styleSheet()
        error_style = original_style.replace("#e0e0e0", "#e74c3c").replace("#1976d2", "#e74c3c")
        field.setStyleSheet(error_style)
        
        # Set tooltip with error message
        field.setToolTip(f"Error: {message}")
        
        # Reset after 3 seconds
        QTimer.singleShot(3000, lambda: self.reset_field_style(field, original_style))
    
    def reset_field_style(self, field, original_style):
        """Reset field style to original and clear error tooltip."""
        field.setStyleSheet(original_style)
        if field == self.username_input:
            field.setToolTip("Enter your username\nPress Enter to continue")
        elif field == self.password_input:
            field.setToolTip("Enter your password\nPress Enter to login")
    
    def toggle_password_visibility(self, checked: bool):
        """Toggle password field visibility."""
        self.password_input.setEchoMode(QLineEdit.Normal if checked else QLineEdit.Password)
    
    def handle_login(self):
        """Handle login attempt."""
        username = self.username_input.text().strip()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("Please enter both username and password.")
            return
        
        # Disable login button during authentication
        self.login_btn.setEnabled(False)
        self.login_btn.setText(tr("login.signing_in", "Signing In..."))
        QApplication.processEvents()
        
        try:
            if self.auth_controller.login(username, password):
                self.user = self.auth_controller.get_current_user()
                logging.info(f"Successful login for user: {username}")
                self.accept()
            else:
                self.show_error(tr("login.invalid_credentials", "Invalid username or password."))
                logging.warning(f"Failed login attempt for user: {username}")
        except Exception as e:
            logging.error(f"Login error: {str(e)}")
            self.show_error(tr("login.error_occurred", "An error occurred during login. Please try again."))
        finally:
            self.login_btn.setEnabled(True)
            self.login_btn.setText(tr("login.sign_in", "Sign In"))
    
    def show_error(self, message: str):
        """Show error message to user."""
        QMessageBox.warning(self, tr("login.error", "Login Error"), message)
    
    def get_stylesheet(self) -> str:
        """Get the stylesheet for the login dialog."""
        return """
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
            }
            QPushButton#loginBtn {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton#loginBtn:hover {
                background-color: #1565c0;
            }
            QPushButton#loginBtn:pressed {
                background-color: #0d47a1;
            }
            QPushButton#loginBtn:disabled {
                background-color: #bdbdbd;
            }
        """


class ApplicationManager:
    """Manages the application lifecycle and initialization."""
    
    def __init__(self):
        self.app = None
        self.splash_screen = None
        self.login_dialog = None
        self.main_window = None
        self.background_task_manager = None
        self.daily_reset_task = None
        self.logger = logging.getLogger(__name__)
        
        # Message deduplication tracking
        self.last_messages = {}
        self.message_cooldown = 5  # seconds between same messages
        self.last_message_time = {}
    
    def show_message_once(self, message_type: str, title: str, message: str, parent=None):
        """
        Show a message only once within a cooldown period to prevent duplicates.
        
        Args:
            message_type: Type of message ('info', 'warning', 'error', 'critical')
            title: Message title
            message: Message content
            parent: Parent widget for the message box
        """
        import time
        current_time = time.time()
        message_key = f"{message_type}_{title}_{message}"
        
        # Check if this message was shown recently
        if message_key in self.last_message_time:
            time_since_last = current_time - self.last_message_time[message_key]
            if time_since_last < self.message_cooldown:
                self.logger.debug(f"Skipping duplicate message: {title} - {message}")
                return
        
        # Update the last shown time
        self.last_message_time[message_key] = current_time
        
        # Show the message
        try:
            if message_type == 'info':
                QMessageBox.information(parent, title, message)
            elif message_type == 'warning':
                QMessageBox.warning(parent, title, message)
            elif message_type == 'error':
                QMessageBox.critical(parent, title, message)
            elif message_type == 'question':
                return QMessageBox.question(parent, title, message)
        except Exception as e:
            self.logger.error(f"Error showing message: {e}")
            # Fallback to print if QMessageBox fails
            print(f"{title}: {message}")
    
    def initialize_application(self) -> bool:
        """Initialize the application and its components."""
        try:
            # Setup logging
            LoggingConfig.setup_logging()
            self.logger.info("Starting Talinda POS application")
            
            # Create QApplication
            self.app = QApplication(sys.argv)
            self.app.setApplicationName(ApplicationConfig.APP_NAME)
            self.app.setApplicationVersion(ApplicationConfig.APP_VERSION)
            
            # Show splash screen
            self.splash_screen = SplashScreen()
            self.splash_screen.show()
            self.splash_screen.update_progress(10, "Initializing application...")
            
            # Initialize localization system
            self.splash_screen.update_progress(20, "Initializing localization...")
            set_language('en')  # Default to English, can be changed later
            
            # Initialize database
            self.splash_screen.update_progress(30, "Initializing database...")
            init_database()
            
            # Load stylesheet
            self.splash_screen.update_progress(60, "Loading styles...")
            self.load_stylesheet()
            
            # Initialize background task manager
            self.splash_screen.update_progress(80, "Initializing background tasks...")
            self.background_task_manager = BackgroundTaskManager(check_interval_minutes=60)
            
            # Initialize daily reset task
            self.daily_reset_task = DailyResetTask()
            self.daily_reset_task.reset_triggered.connect(self.on_daily_reset)
            self.daily_reset_task.start()
            
            # Complete initialization
            self.splash_screen.update_progress(100, "Ready!")
            QTimer.singleShot(1000, self.splash_screen.close)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Application initialization failed: {str(e)}")
            self.show_message_once('error', "Initialization Error", 
                                 f"Failed to initialize application:\n{str(e)}")
            return False
    
    def load_stylesheet(self):
        """Load and apply the application stylesheet."""
        try:
            css_path = current_dir / ApplicationConfig.CSS_FILE
            if css_path.exists():
                with open(css_path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                self.app.setStyleSheet(stylesheet)
                self.logger.info("Stylesheet loaded successfully")
            else:
                self.logger.warning(f"Stylesheet not found at {css_path}")
        except Exception as e:
            self.logger.error(f"Error loading stylesheet: {str(e)}")
    
    def run_authentication(self) -> Optional[Tuple]:
        """Run the authentication process."""
        try:
            self.login_dialog = ModernLoginDialog()
            if self.login_dialog.exec_() == QDialog.Accepted and self.login_dialog.user:
                user = self.login_dialog.user
                opening_amount = None
                
                # Handle cashier-specific flow
                if hasattr(user, 'role') and getattr(user.role, 'value', None) == 'cashier':
                    opening_amount = self.handle_cashier_flow(user)
                    if opening_amount is None:
                        return None
                
                return user, opening_amount
            return None
            
        except Exception as e:
            self.logger.error(f"Authentication error: {str(e)}")
            self.show_message_once("error", "Authentication Error", 
                                 f"Authentication failed:\n{str(e)}")
            return None
    
    def handle_cashier_flow(self, user) -> Optional[float]:
        """Handle cashier-specific opening amount flow with existing shift management."""
        try:
            # Check if there's already an open shift
            from controllers.shift_controller import ShiftController
            shift_controller = ShiftController()
            
            any_open_shift = shift_controller.get_any_open_shift()
            if any_open_shift and any_open_shift.user_id != user.id:
                self.show_message_once(
                    "error", 
                    "Shift Already Open", 
                    f"There's already an open shift by {any_open_shift.user.username}. "
                    "Please close that shift before opening a new one."
                )
                return None
            
            # Check if this user already has an open shift
            current_shift = shift_controller.get_current_shift(user)
            
            # Show the enhanced opening amount dialog
            opening_dialog = OpeningAmountDialog(existing_shift=current_shift)
            if opening_dialog.exec_() == QDialog.Accepted:
                action = opening_dialog.get_action()
                
                if action == 'close_existing':
                    # Close the existing shift
                    if current_shift:
                        # Show password authentication for closing
                        from ui.components.shift_close_auth_dialog import ShiftCloseAuthDialog
                        auth_dialog = ShiftCloseAuthDialog(user.username)
                        if auth_dialog.exec_() == QDialog.Accepted and auth_dialog.is_authenticated():
                            password = auth_dialog.get_password()
                            closed_shift = shift_controller.close_shift_with_auth(user, password)
                            if closed_shift:
                                # Show shift summary
                                shift_summary = shift_controller.get_shift_summary(closed_shift)
                                summary_message = f"""
Shift Closed Successfully!

Cashier: {shift_summary.get('user', 'Unknown')}
Opening Amount: ${shift_summary.get('opening_amount', 0):.2f}
Total Sales: {shift_summary.get('total_sales', 0)}
Total Amount: ${shift_summary.get('total_amount', 0):.2f}
                                """
                                self.show_message_once(
                                    "info",
                                    "Shift Closed",
                                    summary_message
                                )
                                # Return to login (user will need to log in again)
                                return None
                            else:
                                self.show_message_once("error", "Error", "Failed to close shift. Please try again.")
                                return None
                        else:
                            # User cancelled authentication
                            return None
                    else:
                        self.show_message_once("error", "Error", "No shift found to close.")
                        return None
                
                elif action == 'open_new':
                    # Open a new shift (this will replace the current one if it exists)
                    amount = opening_dialog.get_amount()
                    if amount is not None:
                        # If there's an existing shift, close it first
                        if current_shift:
                            # Close existing shift without authentication (since user chose to replace)
                            current_shift.status = ShiftStatus.CLOSED
                            current_shift.close_time = datetime.datetime.utcnow()
                            # Use the new opening amount as closing amount for simplicity
                            current_shift.closing_amount = amount
                            safe_commit(shift_controller.session)
                            self.logger.info(f"Closed existing shift for user {user.username}")
                        
                        # Open new shift
                        shift = shift_controller.open_shift(user, amount)
                        if shift:
                            return amount
                        else:
                            self.show_message_once("error", "Error", "Failed to open shift. Please try again.")
                            return None
                    else:
                        self.show_message_once("error", "Error", "Please enter a valid opening amount.")
                        return None
            
            return None
            
        except Exception as e:
            self.logger.error(f"Cashier flow error: {str(e)}")
            self.show_message_once("error", "Error", f"Failed to handle shift management:\n{str(e)}")
            return None
    
    def create_main_window(self, user, opening_amount: Optional[float]):
        """Create and configure the main window."""
        try:
            self.main_window = MainWindow(user, opening_amount)
            
            # Handle cashier closing flow
            if hasattr(user, 'role') and getattr(user.role, 'value', None) == 'cashier':
                self.setup_cashier_closing(user)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Main window creation error: {str(e)}")
            self.show_message_once("error", "Error", f"Failed to create main window:\n{str(e)}")
            return False
    
    def setup_cashier_closing(self, user):
        """Setup cashier closing flow with password authentication."""
        def on_close_event(event):
            try:
                # Use the new shift controller
                from controllers.shift_controller import ShiftController
                from PyQt5.QtWidgets import QMessageBox
                from ui.components.shift_close_auth_dialog import ShiftCloseAuthDialog
                
                shift_controller = ShiftController()
                current_shift = shift_controller.get_current_shift(user)
                
                if not current_shift:
                    self.logger.warning(f"No open shift found for user {user.username}")
                    # Show a simple message and close
                    self.show_message_once(
                        "info",
                        "No Active Shift",
                        f"No active shift found for {user.username}. Closing application.",
                        self.main_window
                    )
                    event.accept()
                    self.app.quit()
                    return
                
                # Show password authentication dialog
                auth_dialog = ShiftCloseAuthDialog(user.username, self.main_window)
                if auth_dialog.exec_() == QDialog.Accepted and auth_dialog.is_authenticated():
                    password = auth_dialog.get_password()
                    
                    # Close the shift with password authentication
                    closed_shift = shift_controller.close_shift_with_auth(user, password)
                    if closed_shift:
                        # Show shift summary
                        shift_summary = shift_controller.get_shift_summary(closed_shift)
                        summary_message = f"""
Shift Closed Successfully!

Cashier: {shift_summary.get('user', 'Unknown')}
Opening Amount: ${shift_summary.get('opening_amount', 0):.2f}
Total Sales: {shift_summary.get('total_sales', 0)}
Total Amount: ${shift_summary.get('total_amount', 0):.2f}
                        """
                        self.show_message_once(
                            "info",
                            "Shift Closed",
                            summary_message
                        )
                        
                        # Stop background task manager
                        if self.background_task_manager:
                            self.background_task_manager.stop()
                            self.logger.info("Background task manager stopped")
                        
                        # Close the application
                        event.accept()
                        self.app.quit()
                    else:
                        self.show_message_once(
                            "warning",
                            "Authentication Failed",
                            "Invalid password. Please try again.",
                            self.main_window
                        )
                        # Don't close the application, let the user try again
                        event.ignore()
                else:
                    # User cancelled the authentication dialog
                    self.logger.info(f"User {user.username} cancelled shift close authentication")
                    event.ignore()
                    
            except Exception as e:
                self.logger.error(f"Closing dialog error: {str(e)}")
                self.show_message_once(
                    "error",
                    "Error",
                    f"An error occurred while closing the shift:\n{str(e)}",
                    self.main_window
                )
                event.ignore()
        
        self.main_window.closeEvent = on_close_event
    
    def show_error_dialog(self, title: str, message: str):
        """Show error dialog to user."""
        if self.app:
            self.show_message_once("error", title, message)
        else:
            print(f"ERROR - {title}: {message}")
    
    def setup_background_task_handlers(self):
        """Setup handlers for background task events."""
        if self.background_task_manager:
            # Connect signals to handlers
            self.background_task_manager.orders_auto_closed.connect(self.on_orders_auto_closed)
            self.background_task_manager.orders_cleaned_up.connect(self.on_orders_cleaned_up)
            self.background_task_manager.task_error.connect(self.on_background_task_error)
    
    def on_orders_auto_closed(self, count: int):
        """Handle orders auto-closed event."""
        self.logger.info(f"Background task auto-closed {count} orders")
        # Only show notification if count > 0 and not too frequently
        if count > 0 and self.main_window:
            try:
                self.show_message_once(
                    "info",
                    "Orders Auto-Closed",
                    f"{count} orders older than 24 hours have been automatically completed.",
                    self.main_window
                )
            except Exception as e:
                self.logger.error(f"Error showing auto-close notification: {e}")
    
    def on_orders_cleaned_up(self, count: int):
        """Handle orders cleaned up event."""
        self.logger.info(f"Background task cleaned up {count} old orders")
        # Only show notification if count > 0 and not too frequently
        if count > 0 and self.main_window:
            try:
                self.show_message_once(
                    "info",
                    "Orders Cleaned Up",
                    f"{count} old completed/cancelled orders have been removed from the system.",
                    self.main_window
                )
            except Exception as e:
                self.logger.error(f"Error showing cleanup notification: {e}")
    
    def on_background_task_error(self, error_message: str):
        """Handle background task error."""
        self.logger.error(f"Background task error: {error_message}")
        # Only show error notification to user if main window exists
        if self.main_window:
            try:
                self.show_message_once(
                    "warning",
                    "Background Task Error",
                    f"An error occurred in background tasks:\n{error_message}",
                    self.main_window
                )
            except Exception as e:
                self.logger.error(f"Error showing background task error notification: {e}")
    
    def on_daily_reset(self):
        """Handle daily reset event."""
        try:
            from controllers.shift_controller import ShiftController
            shift_controller = ShiftController()
            shift_controller.reset_daily_sales()
            
            self.logger.info("Daily sales reset completed")
            
            # Only show notification if main window exists
            if self.main_window:
                self.show_message_once(
                    "info",
                    "Daily Reset",
                    "Daily sales data has been reset for the new day.",
                    self.main_window
                )
                
        except Exception as e:
            self.logger.error(f"Error during daily reset: {e}")
            if self.main_window:
                self.show_message_once(
                    "warning",
                    "Daily Reset Error",
                    f"Error during daily reset: {str(e)}",
                    self.main_window
                )
    
    def cleanup(self):
        """Clean up resources before application exit."""
        try:
            if self.background_task_manager:
                self.background_task_manager.stop()
                self.logger.info("Background task manager cleaned up")
            
            if self.daily_reset_task:
                self.daily_reset_task.stop()
                self.logger.info("Daily reset task cleaned up")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def run(self) -> int:
        """Run the complete application."""
        try:
            # Initialize application
            if not self.initialize_application():
                return 1
            
            # Run authentication
            auth_result = self.run_authentication()
            if auth_result is None:
                return 0
            
            user, opening_amount = auth_result
            
            # Create main window
            if not self.create_main_window(user, opening_amount):
                return 1
            
            # Setup background task handlers
            self.setup_background_task_handlers()
            
            # Start background task manager
            if self.background_task_manager:
                self.background_task_manager.start()
                self.logger.info("Background task manager started")
            
            # Show main window and run application
            self.main_window.show()
            self.logger.info("Application started successfully")
            
            # Run the application and cleanup on exit
            try:
                return self.app.exec_()
            finally:
                self.cleanup()
            
        except Exception as e:
            self.logger.error(f"Application runtime error: {str(e)}")
            self.show_message_once("error", "Runtime Error", 
                                 f"An unexpected error occurred:\n{str(e)}")
            return 1


def main():
    """Main entry point for the Talinda POS application."""
    try:
        app_manager = ApplicationManager()
        return app_manager.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 0
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
