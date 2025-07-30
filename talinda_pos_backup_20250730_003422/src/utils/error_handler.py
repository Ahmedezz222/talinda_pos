#!/usr/bin/env python3
"""
Error Handling Utilities for Talinda POS
========================================

Comprehensive error handling with user-friendly messages and logging.
"""

import logging
import traceback
import functools
from typing import Optional, Callable, Any
from PyQt5.QtWidgets import QMessageBox, QApplication
from PyQt5.QtCore import QObject, pyqtSignal


class ErrorHandler(QObject):
    """Centralized error handling for the application."""
    
    error_occurred = pyqtSignal(str, str)  # title, message
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
    
    def handle_exception(self, func: Callable) -> Callable:
        """Decorator to handle exceptions in functions."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error(func.__name__, e)
                self.show_error_to_user(str(e))
                return None
        return wrapper
    
    def handle_qt_exception(self, func: Callable) -> Callable:
        """Decorator to handle exceptions in Qt methods."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                self.log_error(func.__name__, e)
                self.show_error_to_user(str(e))
                return None
        return wrapper
    
    def log_error(self, function_name: str, exception: Exception):
        """Log error with detailed information."""
        error_msg = f"Error in {function_name}: {str(exception)}"
        self.logger.error(error_msg)
        self.logger.debug(f"Traceback: {traceback.format_exc()}")
    
    def show_error_to_user(self, message: str, title: str = "Error"):
        """Show error message to user."""
        try:
            # Try to show message box if QApplication exists
            app = QApplication.instance()
            if app:
                QMessageBox.critical(None, title, message)
            else:
                print(f"ERROR - {title}: {message}")
        except Exception as e:
            # Fallback to console output
            print(f"ERROR - {title}: {message}")
            print(f"Failed to show error dialog: {e}")
    
    def show_warning_to_user(self, message: str, title: str = "Warning"):
        """Show warning message to user."""
        try:
            app = QApplication.instance()
            if app:
                QMessageBox.warning(None, title, message)
            else:
                print(f"WARNING - {title}: {message}")
        except Exception as e:
            print(f"WARNING - {title}: {message}")
            print(f"Failed to show warning dialog: {e}")
    
    def show_info_to_user(self, message: str, title: str = "Information"):
        """Show information message to user."""
        try:
            app = QApplication.instance()
            if app:
                QMessageBox.information(None, title, message)
            else:
                print(f"INFO - {title}: {message}")
        except Exception as e:
            print(f"INFO - {title}: {message}")
            print(f"Failed to show info dialog: {e}")


class DatabaseErrorHandler:
    """Specialized error handler for database operations."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.error_handler = ErrorHandler()
    
    def handle_database_error(self, func: Callable) -> Callable:
        """Decorator to handle database-specific errors."""
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_msg = self.get_user_friendly_error(e)
                self.logger.error(f"Database error in {func.__name__}: {str(e)}")
                self.error_handler.show_error_to_user(error_msg, "Database Error")
                return None
        return wrapper
    
    def get_user_friendly_error(self, exception: Exception) -> str:
        """Convert technical database errors to user-friendly messages."""
        error_str = str(exception).lower()
        
        if "no such table" in error_str:
            return "Database table not found. Please contact support."
        elif "foreign key constraint" in error_str:
            return "Cannot delete this item as it is being used elsewhere."
        elif "unique constraint" in error_str:
            return "This item already exists. Please use a different name."
        elif "not null constraint" in error_str:
            return "Required information is missing. Please fill all required fields."
        elif "connection" in error_str:
            return "Database connection failed. Please check your connection and try again."
        else:
            return "A database error occurred. Please try again or contact support."


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class BusinessLogicError(Exception):
    """Custom exception for business logic errors."""
    pass


def validate_input(value: Any, field_name: str, required: bool = True) -> None:
    """Validate input values."""
    if required and (value is None or value == ""):
        raise ValidationError(f"{field_name} is required.")
    
    if isinstance(value, str) and len(value.strip()) == 0:
        raise ValidationError(f"{field_name} cannot be empty.")
    
    if isinstance(value, (int, float)) and value < 0:
        raise ValidationError(f"{field_name} must be positive.")


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safely divide two numbers, returning default on division by zero."""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ValueError):
        return default


def safe_int(value: Any, default: int = 0) -> int:
    """Safely convert value to integer."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default


def safe_float(value: Any, default: float = 0.0) -> float:
    """Safely convert value to float."""
    try:
        return float(value) if value is not None else default
    except (ValueError, TypeError):
        return default


# Global error handler instance
error_handler = ErrorHandler()
db_error_handler = DatabaseErrorHandler()


# Convenience decorators
def handle_errors(func: Callable) -> Callable:
    """Convenience decorator for general error handling."""
    return error_handler.handle_exception(func)


def handle_qt_errors(func: Callable) -> Callable:
    """Convenience decorator for Qt error handling."""
    return error_handler.handle_qt_exception(func)


def handle_db_errors(func: Callable) -> Callable:
    """Convenience decorator for database error handling."""
    return db_error_handler.handle_database_error(func) 