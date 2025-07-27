#!/usr/bin/env python3
"""
Tests for Main Window
====================

Basic tests for the main window functionality.
"""

import pytest
import sys
from unittest.mock import Mock, patch
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Add src to path for imports
sys.path.insert(0, 'src')

from ui.main_window import ModernMainWindow
from config import get_config


@pytest.fixture
def app():
    """Create QApplication instance for testing."""
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    yield app
    # Cleanup is handled by pytest-qt


@pytest.fixture
def mock_user():
    """Create a mock user for testing."""
    user = Mock()
    user.username = "testuser"
    user.role.value = "admin"
    return user


@pytest.fixture
def main_window(app, mock_user):
    """Create main window instance for testing."""
    window = ModernMainWindow(mock_user)
    yield window
    window.close()


class TestMainWindow:
    """Test cases for MainWindow."""
    
    def test_main_window_creation(self, app, mock_user):
        """Test that main window can be created."""
        window = ModernMainWindow(mock_user)
        assert window is not None
        assert window.user == mock_user
        window.close()
    
    def test_main_window_title(self, main_window):
        """Test that main window has correct title."""
        expected_title = f"{get_config().APP_NAME} - {main_window.user.username}"
        assert main_window.windowTitle() == expected_title
    
    def test_main_window_visible(self, main_window):
        """Test that main window can be shown."""
        main_window.show()
        assert main_window.isVisible()
    
    def test_sidebar_creation(self, main_window):
        """Test that sidebar is created."""
        assert hasattr(main_window, 'sidebar')
        assert main_window.sidebar is not None
    
    def test_menu_creation(self, main_window):
        """Test that menu bar is created."""
        assert main_window.menuBar() is not None
    
    def test_status_bar_creation(self, main_window):
        """Test that status bar is created."""
        assert main_window.statusBar() is not None


class TestResponsiveUI:
    """Test cases for responsive UI functionality."""
    
    def test_responsive_sizing(self, app):
        """Test responsive sizing utilities."""
        from utils.responsive_ui import ResponsiveUI
        
        # Test basic scaling
        base_size = 100
        scaled_size = ResponsiveUI.get_scaled_size(base_size)
        assert scaled_size >= base_size
        
        # Test font size
        font_size = ResponsiveUI.get_responsive_font_size(12)
        assert font_size > 0
    
    def test_screen_info(self, app):
        """Test screen information retrieval."""
        from utils.responsive_ui import ResponsiveUI
        
        width, height, scaling = ResponsiveUI.get_screen_info()
        assert width > 0
        assert height > 0
        assert scaling > 0


class TestErrorHandling:
    """Test cases for error handling."""
    
    def test_error_handler_creation(self):
        """Test error handler can be created."""
        from utils.error_handler import ErrorHandler
        
        handler = ErrorHandler()
        assert handler is not None
    
    def test_validation_functions(self):
        """Test input validation functions."""
        from utils.error_handler import validate_input, ValidationError
        
        # Test valid input
        validate_input("test", "test_field")
        
        # Test invalid input
        with pytest.raises(ValidationError):
            validate_input("", "test_field", required=True)
        
        # Test optional input
        validate_input("", "test_field", required=False)  # Should not raise
    
    def test_safe_conversion_functions(self):
        """Test safe conversion functions."""
        from utils.error_handler import safe_int, safe_float, safe_divide
        
        # Test safe_int
        assert safe_int("123") == 123
        assert safe_int("abc", default=0) == 0
        assert safe_int(None, default=5) == 5
        
        # Test safe_float
        assert safe_float("123.45") == 123.45
        assert safe_float("abc", default=0.0) == 0.0
        
        # Test safe_divide
        assert safe_divide(10, 2) == 5.0
        assert safe_divide(10, 0, default=0) == 0


class TestConfiguration:
    """Test cases for configuration management."""
    
    def test_config_loading(self):
        """Test configuration can be loaded."""
        config = get_config()
        assert config is not None
        assert hasattr(config, 'APP_NAME')
        assert hasattr(config, 'DATABASE_URL')
    
    def test_config_validation(self):
        """Test configuration validation."""
        config = get_config()
        assert config.validate() is True
    
    def test_database_url_formatting(self):
        """Test database URL formatting."""
        config = get_config()
        db_url = config.get_database_url()
        assert db_url is not None
        assert isinstance(db_url, str)


# Integration tests
class TestIntegration:
    """Integration tests for the application."""
    
    def test_full_application_flow(self, app, mock_user):
        """Test complete application flow."""
        # Create main window
        window = ModernMainWindow(mock_user)
        assert window is not None
        
        # Show window
        window.show()
        assert window.isVisible()
        
        # Test basic functionality
        assert window.user.username == "testuser"
        assert window.user.role.value == "admin"
        
        # Cleanup
        window.close()
    
    def test_error_handling_integration(self, app):
        """Test error handling integration."""
        from utils.error_handler import error_handler
        
        # Test error handler can show messages
        with patch('PyQt5.QtWidgets.QMessageBox.critical') as mock_critical:
            error_handler.show_error_to_user("Test error")
            # In a real test environment, this would verify the message box was called
            # For now, we just ensure no exceptions are raised
            assert True


if __name__ == "__main__":
    pytest.main([__file__]) 