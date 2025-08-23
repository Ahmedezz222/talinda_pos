#!/usr/bin/env python3
"""
Language Switching Test
=======================

Test script to verify Arabic language switching functionality in Talinda POS.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir / 'src'))

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from utils.localization import LocalizationManager, tr, set_language, is_rtl


def test_language_switching():
    """Test language switching functionality."""
    print("Testing Language Switching Functionality")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Use the global localization manager instance
    from utils.localization import localization_manager
    
    # Test 1: Default language should be English
    print("Test 1: Default Language")
    print(f"Current language: {localization_manager.get_current_language()}")
    print(f"Is RTL: {localization_manager.is_rtl()}")
    print(f"Translation test: {tr('common.language', 'Language')}")
    assert localization_manager.get_current_language() == 'en', "Default language should be English"
    assert not localization_manager.is_rtl(), "English should not be RTL"
    print("✓ Default language test passed")
    print()
    
    # Test 2: Switch to Arabic
    print("Test 2: Switch to Arabic")
    set_language('ar')
    print(f"Current language: {localization_manager.get_current_language()}")
    print(f"Is RTL: {localization_manager.is_rtl()}")
    print(f"Translation test: {tr('common.language', 'Language')}")
    assert localization_manager.get_current_language() == 'ar', "Language should be Arabic"
    assert localization_manager.is_rtl(), "Arabic should be RTL"
    print("✓ Arabic language test passed")
    print()
    
    # Test 3: Test Arabic translations
    print("Test 3: Arabic Translations")
    arabic_translations = [
        ('common.language', 'اللغة'),
        ('common.apply', 'تطبيق'),
        ('pos.title', 'نقطة البيع'),
        ('login.title', 'مرحباً بعودتك')
    ]
    
    for key, expected in arabic_translations:
        result = tr(key)
        print(f"{key}: {result}")
        assert result == expected, f"Translation mismatch for {key}: got {result}, expected {expected}"
    
    print("✓ Arabic translations test passed")
    print()
    
    # Test 4: Switch back to English
    print("Test 4: Switch back to English")
    set_language('en')
    print(f"Current language: {localization_manager.get_current_language()}")
    print(f"Is RTL: {localization_manager.is_rtl()}")
    print(f"Translation test: {tr('common.language', 'Language')}")
    assert localization_manager.get_current_language() == 'en', "Language should be English"
    assert not localization_manager.is_rtl(), "English should not be RTL"
    print("✓ Switch back to English test passed")
    print()
    
    # Test 5: Test English translations
    print("Test 5: English Translations")
    english_translations = [
        ('common.language', 'Language'),
        ('common.apply', 'Apply'),
        ('pos.title', 'Point of Sale'),
        ('login.title', 'Welcome Back')
    ]
    
    for key, expected in english_translations:
        result = tr(key)
        print(f"{key}: {result}")
        assert result == expected, f"Translation mismatch for {key}: got {result}, expected {expected}"
    
    print("✓ English translations test passed")
    print()
    
    print("All language switching tests passed! ✅")
    return True


def test_arabic_text_detection():
    """Test Arabic text detection functionality."""
    print("Testing Arabic Text Detection")
    print("=" * 50)
    
    from utils.arabic_support import is_arabic_text
    
    # Test cases
    test_cases = [
        ("مرحبا", True, "Basic Arabic text"),
        ("Hello", False, "English text"),
        ("123", False, "Numbers"),
        ("مرحبا Hello", True, "Mixed text with Arabic"),
        ("", False, "Empty string"),
        ("مرحبا 123", True, "Arabic with numbers"),
        ("!@#$%", False, "Special characters"),
        ("قهوة عربية", True, "Arabic product name"),
        ("مشروبات", True, "Arabic category name"),
    ]
    
    for text, expected, description in test_cases:
        result = is_arabic_text(text)
        print(f"{description}: '{text}' -> Arabic: {result}")
        assert result == expected, f"Arabic detection failed for '{text}': got {result}, expected {expected}"
    
    print("✓ Arabic text detection tests passed")
    print()


if __name__ == "__main__":
    try:
        print("Starting Language Switching Tests")
        print("=" * 50)
        
        test_arabic_text_detection()
        test_language_switching()
        
        print("All tests completed successfully! 🎉")
        
    except Exception as e:
        print(f"Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
