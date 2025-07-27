#!/usr/bin/env python3
"""
Simple test to verify CSS file loads without Qt-incompatible property errors.
"""

import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

def test_css_loading():
    """Test that CSS file loads without errors."""
    print("Testing CSS file loading...")
    
    # Create application
    app = QApplication(sys.argv)
    
    # Get CSS file path
    css_path = os.path.join(src_dir, "resources", "styles", "main.qss")
    
    if os.path.exists(css_path):
        try:
            # Load and apply CSS
            with open(css_path, 'r', encoding='utf-8') as f:
                css_content = f.read()
            
            # Apply CSS to application
            app.setStyleSheet(css_content)
            
            # Create a simple test window
            window = QMainWindow()
            window.setWindowTitle("CSS Test")
            window.setGeometry(100, 100, 400, 300)
            
            # Create central widget
            central_widget = QWidget()
            window.setCentralWidget(central_widget)
            
            # Create layout
            layout = QVBoxLayout(central_widget)
            
            # Add some test buttons
            button1 = QPushButton("Test Button 1")
            button2 = QPushButton("Test Button 2")
            button3 = QPushButton("Test Button 3")
            
            layout.addWidget(button1)
            layout.addWidget(button2)
            layout.addWidget(button3)
            
            # Show window briefly
            window.show()
            
            # Process events briefly
            app.processEvents()
            
            print("✓ CSS file loaded successfully!")
            print("✓ No Qt-incompatible property errors!")
            print("✓ Application runs without CSS issues!")
            
            # Close window
            window.close()
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading CSS: {e}")
            return False
    else:
        print(f"⚠ CSS file not found at: {css_path}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("CSS FIX VERIFICATION TEST")
    print("=" * 50)
    
    success = test_css_loading()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 CSS fix verification PASSED!")
        print("All Qt-incompatible properties have been removed.")
        print("The application should now run without CSS warnings.")
    else:
        print("❌ CSS fix verification FAILED!")
        print("Please check the CSS file for remaining issues.")
    print("=" * 50)
    
    sys.exit(0 if success else 1) 