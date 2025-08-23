#!/usr/bin/env python3
"""
Application Language Switch Test
===============================

Test script to verify language switching works within the actual application.
"""

import sys
import os
import time
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir / 'src'))

from PyQt5.QtWidgets import QApplication
from utils.localization import tr, set_language, is_rtl, localization_manager


def test_application_language_switch():
    """Test language switching within the application context."""
    print("Testing Application Language Switching")
    print("=" * 50)
    
    # Initialize QApplication
    app = QApplication(sys.argv)
    
    # Test 1: Initial state should be English
    print("Test 1: Initial Language State")
    print(f"Current language: {localization_manager.get_current_language()}")
    print(f"Is RTL: {is_rtl()}")
    print(f"Translation test: {tr('common.language', 'Language')}")
    assert localization_manager.get_current_language() == 'en', "Initial language should be English"
    assert not is_rtl(), "Initial language should not be RTL"
    print("✓ Initial language state test passed")
    print()
    
    # Test 2: Switch to Arabic
    print("Test 2: Switch to Arabic")
    set_language('ar')
    print(f"Current language: {localization_manager.get_current_language()}")
    print(f"Is RTL: {is_rtl()}")
    print(f"Translation test: {tr('common.language', 'Language')}")
    assert localization_manager.get_current_language() == 'ar', "Language should be Arabic"
    assert is_rtl(), "Arabic should be RTL"
    print("✓ Arabic language switch test passed")
    print()
    
    # Test 3: Verify Arabic translations work
    print("Test 3: Arabic Translations Verification")
    arabic_tests = [
        ('login.title', 'مرحباً بعودتك'),
        ('pos.title', 'نقطة البيع'),
        ('common.apply', 'تطبيق'),
        ('common.close', 'إغلاق'),
        ('common.save', 'حفظ'),
        ('common.cancel', 'إلغاء'),
        ('products.title', 'المنتجات'),
        ('orders.title', 'الطلبات'),
        ('reports.title', 'التقارير'),
    ]
    
    for key, expected in arabic_tests:
        result = tr(key)
        print(f"  {key}: {result}")
        assert result == expected, f"Arabic translation mismatch for {key}: got {result}, expected {expected}"
    
    print("✓ Arabic translations verification test passed")
    print()
    
    # Test 4: Switch back to English
    print("Test 4: Switch back to English")
    set_language('en')
    print(f"Current language: {localization_manager.get_current_language()}")
    print(f"Is RTL: {is_rtl()}")
    print(f"Translation test: {tr('common.language', 'Language')}")
    assert localization_manager.get_current_language() == 'en', "Language should be English"
    assert not is_rtl(), "English should not be RTL"
    print("✓ Switch back to English test passed")
    print()
    
    # Test 5: Verify English translations work
    print("Test 5: English Translations Verification")
    english_tests = [
        ('login.title', 'Welcome Back'),
        ('pos.title', 'Point of Sale'),
        ('common.apply', 'Apply'),
        ('common.close', 'Close'),
        ('common.save', 'Save'),
        ('common.cancel', 'Cancel'),
        ('products.title', 'Products'),
        ('orders.title', 'Orders'),
        ('reports.title', 'Reports'),
    ]
    
    for key, expected in english_tests:
        result = tr(key)
        print(f"  {key}: {result}")
        assert result == expected, f"English translation mismatch for {key}: got {result}, expected {expected}"
    
    print("✓ English translations verification test passed")
    print()
    
    print("🎉 All application language switching tests completed successfully!")
    return True


if __name__ == "__main__":
    try:
        print("Starting Application Language Switch Tests")
        print("=" * 60)
        
        test_application_language_switch()
        
        print("Summary:")
        print("- Language switching: ✅ Working")
        print("- RTL layout: ✅ Working")
        print("- Arabic translations: ✅ Working")
        print("- English translations: ✅ Working")
        print("- Complete workflow: ✅ Working")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
