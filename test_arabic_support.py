#!/usr/bin/env python3
"""
Test Arabic Language Support
===========================

This script tests the Arabic language support functionality in the Talinda POS application.

Author: Talinda POS Team
Version: 1.0.0
License: MIT
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from utils.localization import tr, set_language, is_rtl, apply_arabic_to_widget, is_arabic_text
from utils.arabic_support import ArabicSupport, setup_arabic_support


class ArabicTestWindow(QMainWindow):
    """Test window for Arabic language support."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Arabic Language Support Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create layout
        layout = QVBoxLayout(central_widget)
        
        # Test labels
        self.create_test_labels(layout)
        
        # Test input fields
        self.create_test_inputs(layout)
        
        # Test buttons
        self.create_test_buttons(layout)
        
        # Language switch button
        self.language_btn = QPushButton("Switch to Arabic")
        self.language_btn.clicked.connect(self.switch_language)
        layout.addWidget(self.language_btn)
        
        self.current_language = 'en'
    
    def create_test_labels(self, layout):
        """Create test labels with different text."""
        # English text
        en_label = QLabel("This is English text")
        layout.addWidget(en_label)
        
        # Arabic text
        ar_label = QLabel("هذا نص عربي")
        apply_arabic_to_widget(ar_label, "هذا نص عربي")
        layout.addWidget(ar_label)
        
        # Mixed text
        mixed_label = QLabel("English and العربية mixed")
        apply_arabic_to_widget(mixed_label, "English and العربية mixed")
        layout.addWidget(mixed_label)
    
    def create_test_inputs(self, layout):
        """Create test input fields."""
        # English input
        en_input = QLineEdit()
        en_input.setPlaceholderText("Enter English text...")
        layout.addWidget(en_input)
        
        # Arabic input
        ar_input = QLineEdit()
        ar_input.setPlaceholderText("أدخل نص عربي...")
        apply_arabic_to_widget(ar_input, "أدخل نص عربي...")
        layout.addWidget(ar_input)
        
        # Text edit
        text_edit = QTextEdit()
        text_edit.setPlaceholderText("Enter text here...\nأدخل النص هنا...")
        apply_arabic_to_widget(text_edit, "Enter text here...\nأدخل النص هنا...")
        layout.addWidget(text_edit)
    
    def create_test_buttons(self, layout):
        """Create test buttons."""
        # English button
        en_btn = QPushButton("English Button")
        layout.addWidget(en_btn)
        
        # Arabic button
        ar_btn = QPushButton("زر عربي")
        apply_arabic_to_widget(ar_btn, "زر عربي")
        layout.addWidget(ar_btn)
    
    def switch_language(self):
        """Switch between English and Arabic."""
        if self.current_language == 'en':
            set_language('ar')
            self.current_language = 'ar'
            self.language_btn.setText("Switch to English")
            self.setWindowTitle("اختبار دعم اللغة العربية")
        else:
            set_language('en')
            self.current_language = 'en'
            self.language_btn.setText("Switch to Arabic")
            self.setWindowTitle("Arabic Language Support Test")


def test_arabic_detection():
    """Test Arabic text detection."""
    print("Testing Arabic text detection...")
    
    test_texts = [
        "Hello World",
        "مرحبا بالعالم",
        "Hello العربية",
        "123456",
        "أهلاً وسهلاً",
        "Mixed text with العربية",
        "",
        None
    ]
    
    for text in test_texts:
        is_arabic = is_arabic_text(text)
        print(f"Text: '{text}' -> Arabic: {is_arabic}")


def test_arabic_support():
    """Test Arabic support setup."""
    print("\nTesting Arabic support setup...")
    
    # Create a temporary QApplication for font testing
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    result = setup_arabic_support()
    print(f"Arabic support setup result: {result}")


def test_translations():
    """Test Arabic translations."""
    print("\nTesting Arabic translations...")
    
    # Create QApplication if needed
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Test English
    set_language('en')
    print(f"English - App Name: {tr('app_name')}")
    print(f"English - Login Title: {tr('login.title')}")
    
    # Test Arabic
    set_language('ar')
    print(f"Arabic - App Name: {tr('app_name')}")
    print(f"Arabic - Login Title: {tr('login.title')}")
    print(f"Arabic - Username: {tr('login.username')}")
    print(f"Arabic - Password: {tr('login.password')}")


def main():
    """Main test function."""
    print("Arabic Language Support Test")
    print("=" * 40)
    
    # Test Arabic detection
    test_arabic_detection()
    
    # Test Arabic support setup
    test_arabic_support()
    
    # Test translations
    test_translations()
    
    # Create GUI test
    print("\nStarting GUI test...")
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Setup Arabic support
    setup_arabic_support()
    
    # Create test window
    window = ArabicTestWindow()
    window.show()
    
    print("GUI test window opened. You can:")
    print("1. See how Arabic text is displayed")
    print("2. Click 'Switch to Arabic' to test RTL layout")
    print("3. Enter text in the input fields")
    print("4. Close the window to exit")
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main() 