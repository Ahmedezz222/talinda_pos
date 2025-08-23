#!/usr/bin/env python3
"""
Comprehensive Arabic Support Test
================================

Test script to verify complete Arabic language support including RTL layout,
font rendering, and UI components in Talinda POS.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir / 'src'))

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox
from PyQt5.QtCore import Qt
from utils.localization import tr, set_language, is_rtl, apply_arabic_to_widget
from utils.arabic_support import ArabicSupport, is_arabic_text, get_arabic_text_alignment


def test_rtl_layout():
    """Test RTL layout functionality."""
    print("Testing RTL Layout Support")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Test 1: Switch to Arabic and check RTL
    set_language('ar')
    assert is_rtl(), "Arabic should be RTL"
    
    # Test 2: Check layout direction
    layout_direction = QApplication.instance().layoutDirection()
    assert layout_direction == Qt.RightToLeft, "Layout direction should be RightToLeft for Arabic"
    
    print("✓ RTL layout test passed")
    print()


def test_arabic_font_rendering():
    """Test Arabic font rendering functionality."""
    print("Testing Arabic Font Rendering")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Test Arabic font setup
    arabic_font = ArabicSupport.setup_arabic_fonts()
    assert arabic_font is not None, "Arabic font should be available"
    print(f"Arabic font: {arabic_font}")
    
    # Test Arabic stylesheet
    arabic_stylesheet = ArabicSupport.apply_arabic_stylesheet()
    assert arabic_stylesheet is not None, "Arabic stylesheet should be available"
    assert len(arabic_stylesheet) > 0, "Arabic stylesheet should not be empty"
    
    print("✓ Arabic font rendering test passed")
    print()


def test_arabic_ui_components():
    """Test Arabic UI components functionality."""
    print("Testing Arabic UI Components")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    set_language('ar')
    
    # Test various UI components with Arabic text
    test_components = [
        ('QLabel', QLabel("نص عربي تجريبي")),
        ('QPushButton', QPushButton("زر عربي")),
        ('QLineEdit', QLineEdit("إدخال نص عربي")),
        ('QTextEdit', QTextEdit("نص طويل عربي للاختبار")),
        ('QComboBox', QComboBox()),
    ]
    
    for component_type, component in test_components:
        # Apply Arabic support
        result = apply_arabic_to_widget(component, component.text() if hasattr(component, 'text') else "")
        
        # Check if Arabic support was applied
        if is_arabic_text(component.text() if hasattr(component, 'text') else ""):
            assert result, f"Arabic support should be applied to {component_type}"
            print(f"✓ {component_type}: Arabic support applied successfully")
        else:
            print(f"ℹ {component_type}: No Arabic text detected")
    
    print("✓ Arabic UI components test passed")
    print()


def test_arabic_text_alignment():
    """Test Arabic text alignment functionality."""
    print("Testing Arabic Text Alignment")
    print("=" * 50)
    
    # Test cases for text alignment
    test_cases = [
        ("نص عربي", Qt.AlignRight | Qt.AlignVCenter, "Arabic text should align right"),
        ("English text", Qt.AlignLeft | Qt.AlignVCenter, "English text should align left"),
        ("Mixed نص English", Qt.AlignRight | Qt.AlignVCenter, "Mixed text with Arabic should align right"),
        ("123", Qt.AlignLeft | Qt.AlignVCenter, "Numbers should align left"),
        ("", Qt.AlignLeft | Qt.AlignVCenter, "Empty string should align left"),
    ]
    
    for text, expected_alignment, description in test_cases:
        actual_alignment = get_arabic_text_alignment(text)
        assert actual_alignment == expected_alignment, f"{description}: got {actual_alignment}, expected {expected_alignment}"
        print(f"✓ {description}: '{text}' -> {actual_alignment}")
    
    print("✓ Arabic text alignment test passed")
    print()


def test_complete_arabic_workflow():
    """Test complete Arabic language workflow."""
    print("Testing Complete Arabic Workflow")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Test complete workflow: English -> Arabic -> English
    print("1. Starting in English...")
    set_language('en')
    assert not is_rtl(), "Should not be RTL in English"
    print(f"   Language: en, RTL: {is_rtl()}")
    print(f"   Translation: {tr('common.language', 'Language')}")
    
    print("2. Switching to Arabic...")
    set_language('ar')
    assert is_rtl(), "Should be RTL in Arabic"
    print(f"   Language: ar, RTL: {is_rtl()}")
    print(f"   Translation: {tr('common.language', 'Language')}")
    
    # Test Arabic translations
    arabic_tests = [
        ('login.title', 'مرحباً بعودتك'),
        ('pos.title', 'نقطة البيع'),
        ('common.apply', 'تطبيق'),
        ('common.close', 'إغلاق'),
    ]
    
    for key, expected in arabic_tests:
        result = tr(key)
        assert result == expected, f"Arabic translation mismatch for {key}"
        print(f"   ✓ {key}: {result}")
    
    print("3. Switching back to English...")
    set_language('en')
    assert not is_rtl(), "Should not be RTL after switching back to English"
    print(f"   Language: en, RTL: {is_rtl()}")
    print(f"   Translation: {tr('common.language', 'Language')}")
    
    print("✓ Complete Arabic workflow test passed")
    print()


if __name__ == "__main__":
    try:
        print("Starting Comprehensive Arabic Support Tests")
        print("=" * 60)
        
        test_rtl_layout()
        test_arabic_font_rendering()
        test_arabic_text_alignment()
        test_arabic_ui_components()
        test_complete_arabic_workflow()
        
        print("🎉 All comprehensive Arabic support tests completed successfully!")
        print()
        print("Summary:")
        print("- RTL layout support: ✅ Working")
        print("- Arabic font rendering: ✅ Working") 
        print("- Arabic text alignment: ✅ Working")
        print("- Arabic UI components: ✅ Working")
        print("- Complete workflow: ✅ Working")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
