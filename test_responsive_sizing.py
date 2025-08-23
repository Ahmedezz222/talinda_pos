#!/usr/bin/env python3
"""
Test script for responsive sizing functionality
==============================================

This script tests the responsive UI utilities to ensure they work correctly
across different screen resolutions and DPI settings.
"""

import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QTextEdit
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.responsive_ui import ResponsiveUI, ResponsiveLayout, ResponsiveBreakpoints


class ResponsiveTestWindow(QMainWindow):
    """Test window to demonstrate responsive sizing."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Responsive Sizing Test")
        self.init_ui()
        
    def init_ui(self):
        """Initialize the test UI."""
        # Use responsive window sizing
        window_size = ResponsiveUI.get_responsive_window_size()
        self.setMinimumSize(window_size.width(), window_size.height())
        self.resize(window_size.width(), window_size.height())
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(ResponsiveLayout.get_spacing_for_screen())
        layout.setContentsMargins(
            ResponsiveLayout.get_margin_for_screen(),
            ResponsiveLayout.get_margin_for_screen(),
            ResponsiveLayout.get_margin_for_screen(),
            ResponsiveLayout.get_margin_for_screen()
        )
        
        # Screen info display
        self.create_screen_info_display(layout)
        
        # Responsive elements test
        self.create_responsive_elements_test(layout)
        
        # Apply responsive styling
        self.apply_responsive_styling()
        
    def create_screen_info_display(self, layout):
        """Create screen information display."""
        # Screen info label
        screen_info = self.get_screen_info_text()
        info_label = QLabel(screen_info)
        info_label.setWordWrap(True)
        info_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 15px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        layout.addWidget(info_label)
        
    def create_responsive_elements_test(self, layout):
        """Create test elements with responsive sizing."""
        # Responsive button
        button_size = ResponsiveUI.get_responsive_button_size()
        test_button = QPushButton(f"Responsive Button ({button_size.width()}x{button_size.height()})")
        test_button.setFixedSize(button_size.width(), button_size.height())
        test_button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)
        layout.addWidget(test_button)
        
        # Responsive card
        card_size = ResponsiveUI.get_responsive_card_size()
        card_label = QLabel(f"Responsive Card ({card_size.width()}x{card_size.height()})")
        card_label.setFixedSize(card_size.width(), card_size.height())
        card_label.setAlignment(Qt.AlignCenter)
        card_label.setStyleSheet("""
            QLabel {
                background-color: #e9ecef;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                font-weight: bold;
                color: #495057;
            }
        """)
        layout.addWidget(card_label)
        
        # Responsive font test
        font_size = ResponsiveUI.get_responsive_font_size(16)
        font_label = QLabel(f"Responsive Font Size: {font_size}pt")
        font_label.setFont(QFont("Arial", font_size))
        font_label.setStyleSheet("color: #28a745; font-weight: bold;")
        layout.addWidget(font_label)
        
        # Responsive dialog size test
        dialog_size = ResponsiveUI.get_responsive_dialog_size('standard')
        dialog_label = QLabel(f"Standard Dialog Size: {dialog_size.width()}x{dialog_size.height()}")
        dialog_label.setStyleSheet("color: #dc3545; font-weight: bold;")
        layout.addWidget(dialog_label)
        
        # Responsive sidebar width test
        sidebar_width = ResponsiveUI.get_responsive_sidebar_width()
        sidebar_label = QLabel(f"Sidebar Width: {sidebar_width}px")
        sidebar_label.setStyleSheet("color: #6f42c1; font-weight: bold;")
        layout.addWidget(sidebar_label)
        
        # Add flexible spacer
        layout.addStretch()
        
    def get_screen_info_text(self) -> str:
        """Get formatted screen information text."""
        screen_width, screen_height, scaling_factor = ResponsiveUI.get_screen_info()
        screen_category = ResponsiveUI.get_screen_category()
        
        info = f"""
Screen Information:
==================
Screen Resolution: {screen_width}x{screen_height}
DPI Scaling Factor: {scaling_factor:.2f}
Screen Category: {screen_category}

Responsive Sizes:
================
Window Size: {ResponsiveUI.get_responsive_window_size().width()}x{ResponsiveUI.get_responsive_window_size().height()}
Button Size: {ResponsiveUI.get_responsive_button_size().width()}x{ResponsiveUI.get_responsive_button_size().height()}
Card Size: {ResponsiveUI.get_responsive_card_size().width()}x{ResponsiveUI.get_responsive_card_size().height()}
Sidebar Width: {ResponsiveUI.get_responsive_sidebar_width()}px
Font Size (16pt base): {ResponsiveUI.get_responsive_font_size(16)}pt

Layout Spacing:
==============
Margin: {ResponsiveLayout.get_margin_for_screen()}px
Spacing: {ResponsiveLayout.get_spacing_for_screen()}px
Padding: {ResponsiveLayout.get_padding_for_screen()}px

Grid Columns: {ResponsiveBreakpoints.get_columns_for_screen()}
        """
        return info.strip()
        
    def apply_responsive_styling(self):
        """Apply responsive styling to the window."""
        base_stylesheet = """
            QMainWindow {
                background-color: #f8f9fa;
            }
            QLabel {
                font-size: 14px;
                margin: 5px;
            }
            QPushButton {
                font-size: 14px;
                padding: 8px 16px;
            }
        """
        
        responsive_stylesheet = ResponsiveUI.apply_responsive_stylesheet(self, base_stylesheet)
        self.setStyleSheet(responsive_stylesheet)


def main():
    """Main function to run the responsive sizing test."""
    app = QApplication(sys.argv)
    
    # Create and show the test window
    test_window = ResponsiveTestWindow()
    test_window.show()
    
    print("Responsive Sizing Test Window opened.")
    print("This window demonstrates responsive sizing across different screen resolutions.")
    print("Resize the window to see how elements adapt to different sizes.")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 