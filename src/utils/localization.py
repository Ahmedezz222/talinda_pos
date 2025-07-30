#!/usr/bin/env python3
"""
Localization Module for Talinda POS System
==========================================

This module provides Arabic language support and localization functionality
for the Talinda POS application.

Author: Talinda POS Team
Version: 1.0.0
License: MIT
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from PyQt5.QtCore import QTranslator, QLocale, QCoreApplication, Qt
from PyQt5.QtWidgets import QApplication


class LocalizationManager:
    """Manages application localization and translations."""
    
    def __init__(self):
        self.current_language = 'en'
        self.translations = {}
        self.translator = QTranslator()
        self.load_translations()
    
    def load_translations(self):
        """Load all translation files."""
        translations_dir = Path(__file__).parent.parent / 'resources' / 'translations'
        translations_dir.mkdir(exist_ok=True)
        
        # Load English translations (default)
        self.translations['en'] = self._get_english_translations()
        
        # Load Arabic translations
        arabic_file = translations_dir / 'ar.json'
        if arabic_file.exists():
            try:
                with open(arabic_file, 'r', encoding='utf-8') as f:
                    self.translations['ar'] = json.load(f)
            except Exception as e:
                print(f"Error loading Arabic translations: {e}")
                self.translations['ar'] = self._get_arabic_translations()
        else:
            # Create Arabic translations file
            self.translations['ar'] = self._get_arabic_translations()
            self._save_translations('ar', self.translations['ar'])
    
    def _save_translations(self, language: str, translations: Dict[str, Any]):
        """Save translations to file."""
        translations_dir = Path(__file__).parent.parent / 'resources' / 'translations'
        translations_dir.mkdir(exist_ok=True)
        
        file_path = translations_dir / f'{language}.json'
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(translations, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving translations: {e}")
    
    def _get_english_translations(self) -> Dict[str, Any]:
        """Get English translations."""
        return {
            "app_name": "Talinda POS",
            "login": {
                "title": "Welcome Back",
                "subtitle": "Please sign in to continue",
                "username": "Username",
                "password": "Password",
                "show_password": "Show Password",
                "sign_in": "Sign In",
                "signing_in": "Signing In...",
                "error": "Login Error",
                "invalid_credentials": "Invalid username or password.",
                "error_occurred": "An error occurred during login. Please try again.",
                "username_required": "Username is required",
                "password_required": "Password is required",
                "both_required": "Please enter both username and password.",
                "remember_me": "Remember Me",
                "forgot_password": "Forgot Password?",
                "create_account": "Create Account",
                "login_successful": "Login successful",
                "logout": "Logout",
                "logout_successful": "Logout successful",
                "session_expired": "Session expired. Please login again.",
                "account_locked": "Account locked. Please contact administrator.",
                "too_many_attempts": "Too many login attempts. Please try again later."
            },
            "main_window": {
                "title": "Talinda POS System",
                "file_menu": "File",
                "edit_menu": "Edit",
                "view_menu": "View",
                "help_menu": "Help",
                "exit": "Exit",
                "about": "About",
                "settings": "Settings",
                "admin_panel": "Admin Panel"
            },
            "pos": {
                "title": "Point of Sale",
                "new_sale": "New Sale",
                "add_to_cart": "Add to Cart",
                "remove_from_cart": "Remove",
                "clear_cart": "Clear Cart",
                "checkout": "Checkout",
                "total": "Total",
                "subtotal": "Subtotal",
                "tax": "Tax",
                "discount": "Discount",
                "grand_total": "Grand Total",
                "payment_method": "Payment Method",
                "cash": "Cash",
                "card": "Card",
                "change": "Change",
                "complete_sale": "Complete Sale",
                "cancel_sale": "Cancel Sale",
                "print_receipt": "Print Receipt",
                "no_items": "No items in cart",
                "item_added": "Item added to cart",
                "item_removed": "Item removed from cart",
                "cart_cleared": "Cart cleared",
                "sale_completed": "Sale completed successfully",
                "sale_cancelled": "Sale cancelled",
                "insufficient_funds": "Insufficient funds",
                "invalid_amount": "Invalid amount",
                "search_products": "Search Products",
                "categories": "Categories",
                "all_categories": "All Categories",
                "cart": "Cart",
                "quantity": "Quantity",
                "price": "Price",
                "amount": "Amount",
                "payment": "Payment",
                "receipt": "Receipt"
            },
            "products": {
                "title": "Products",
                "add_product": "Add Product",
                "edit_product": "Edit Product",
                "delete_product": "Delete Product",
                "product_name": "Product Name",
                "product_code": "Product Code",
                "price": "Price",
                "category": "Category",
                "stock": "Stock",
                "description": "Description",
                "save": "Save",
                "cancel": "Cancel",
                "delete": "Delete",
                "confirm_delete": "Are you sure you want to delete this product?",
                "product_saved": "Product saved successfully",
                "product_deleted": "Product deleted successfully",
                "error_saving": "Error saving product",
                "error_deleting": "Error deleting product"
            },
            "orders": {
                "title": "Orders",
                "order_id": "Order ID",
                "date": "Date",
                "time": "Time",
                "status": "Status",
                "total": "Total",
                "actions": "Actions",
                "view": "View",
                "edit": "Edit",
                "delete": "Delete",
                "complete": "Complete",
                "cancel": "Cancel",
                "pending": "Pending",
                "completed": "Completed",
                "cancelled": "Cancelled",
                "no_orders": "No orders found"
            },
            "reports": {
                "title": "Reports",
                "sales_report": "Sales Report",
                "daily_report": "Daily Report",
                "weekly_report": "Weekly Report",
                "monthly_report": "Monthly Report",
                "custom_report": "Custom Report",
                "shift_reports": "Shift Reports",
                "start_date": "Start Date",
                "end_date": "End Date",
                "generate": "Generate",
                "export": "Export",
                "print": "Print",
                "total_sales": "Total Sales",
                "total_orders": "Total Orders",
                "average_order": "Average Order",
                "top_products": "Top Products",
                "sales_by_category": "Sales by Category",
                "date": "Date",
                "time": "Time",
                "cashier": "Cashier",
                "items_sold": "Items Sold",
                "revenue": "Revenue",
                "profit": "Profit",
                "cost": "Cost",
                "margin": "Margin",
                "percentage": "Percentage",
                "summary": "Summary",
                "details": "Details",
                "filter": "Filter",
                "search": "Search",
                "refresh": "Refresh",
                "loading": "Loading...",
                "no_data": "No data available",
                "export_to_excel": "Export to Excel",
                "export_to_pdf": "Export to PDF"
            },
            "shifts": {
                "title": "Shift Management",
                "open_shift": "Open Shift",
                "close_shift": "Close Shift",
                "opening_amount": "Opening Amount",
                "closing_amount": "Closing Amount",
                "shift_summary": "Shift Summary",
                "cashier": "Cashier",
                "start_time": "Start Time",
                "end_time": "End Time",
                "duration": "Duration",
                "total_sales": "Total Sales",
                "total_orders": "Total Orders",
                "shift_opened": "Shift opened successfully",
                "shift_closed": "Shift closed successfully",
                "enter_password": "Enter your password to close shift",
                "invalid_password": "Invalid password",
                "shift_already_open": "There's already an open shift",
                "no_open_shift": "No open shift found",
                "current_shift": "Current Shift",
                "shift_history": "Shift History",
                "shift_details": "Shift Details",
                "shift_status": "Shift Status",
                "open": "Open",
                "closed": "Closed",
                "pending": "Pending",
                "cash_drawer": "Cash Drawer",
                "expected_amount": "Expected Amount",
                "actual_amount": "Actual Amount",
                "difference": "Difference",
                "notes": "Notes",
                "comments": "Comments",
                "authorized_by": "Authorized By",
                "authorization_time": "Authorization Time"
            },
            "common": {
                "yes": "Yes",
                "no": "No",
                "ok": "OK",
                "cancel": "Cancel",
                "close": "Close",
                "save": "Save",
                "delete": "Delete",
                "edit": "Edit",
                "add": "Add",
                "search": "Search",
                "filter": "Filter",
                "refresh": "Refresh",
                "loading": "Loading...",
                "error": "Error",
                "success": "Success",
                "warning": "Warning",
                "info": "Information",
                "confirm": "Confirm",
                "back": "Back",
                "next": "Next",
                "previous": "Previous",
                "finish": "Finish",
                "retry": "Retry",
                "ignore": "Ignore",
                "abort": "Abort",
                "continue": "Continue",
                "language": "Language",
                "apply": "Apply",
                "language_info": "Language changes will take effect immediately",
                "language_settings": "Language Settings",
                "tools": "Tools",
                "logged_in_as": "Logged in as: {username}"
            },
            "admin": {
                "user_management": "User Management",
                "system_info": "System Information",
                "add_user": "Add User",
                "edit_user": "Edit User",
                "delete_user": "Delete User",
                "username": "Username",
                "role": "Role",
                "password": "Password",
                "confirm_password": "Confirm Password",
                "email": "Email",
                "phone": "Phone",
                "status": "Status",
                "active": "Active",
                "inactive": "Inactive",
                "created_date": "Created Date",
                "last_login": "Last Login",
                "actions": "Actions",
                "view": "View",
                "edit": "Edit",
                "delete": "Delete",
                "save": "Save",
                "cancel": "Cancel",
                "close": "Close",
                "confirm": "Confirm",
                "yes": "Yes",
                "no": "No"
            },
            "messages": {
                "operation_successful": "Operation completed successfully",
                "operation_failed": "Operation failed",
                "data_saved": "Data saved successfully",
                "data_deleted": "Data deleted successfully",
                "connection_error": "Connection error",
                "database_error": "Database error",
                "file_error": "File error",
                "permission_error": "Permission denied",
                "validation_error": "Validation error",
                "timeout_error": "Request timeout",
                "network_error": "Network error",
                "server_error": "Server error",
                "unknown_error": "An unknown error occurred"
            }
        }
    
    def _get_arabic_translations(self) -> Dict[str, Any]:
        """Get Arabic translations."""
        return {
            "app_name": "نظام نقاط البيع تاليندا",
            "login": {
                "title": "مرحباً بعودتك",
                "subtitle": "يرجى تسجيل الدخول للمتابعة",
                "username": "اسم المستخدم",
                "password": "كلمة المرور",
                "show_password": "إظهار كلمة المرور",
                "sign_in": "تسجيل الدخول",
                "signing_in": "جاري تسجيل الدخول...",
                "error": "خطأ في تسجيل الدخول",
                "invalid_credentials": "اسم المستخدم أو كلمة المرور غير صحيحة.",
                "error_occurred": "حدث خطأ أثناء تسجيل الدخول. يرجى المحاولة مرة أخرى.",
                "username_required": "اسم المستخدم مطلوب",
                "password_required": "كلمة المرور مطلوبة",
                "both_required": "يرجى إدخال اسم المستخدم وكلمة المرور.",
                "remember_me": "تذكرني",
                "forgot_password": "نسيت كلمة المرور؟",
                "create_account": "إنشاء حساب",
                "login_successful": "تم تسجيل الدخول بنجاح",
                "logout": "تسجيل الخروج",
                "logout_successful": "تم تسجيل الخروج بنجاح",
                "session_expired": "انتهت صلاحية الجلسة. يرجى تسجيل الدخول مرة أخرى.",
                "account_locked": "الحساب مقفل. يرجى الاتصال بالمدير.",
                "too_many_attempts": "محاولات تسجيل دخول كثيرة جداً. يرجى المحاولة لاحقاً."
            },
            "main_window": {
                "title": "نظام نقاط البيع تاليندا",
                "file_menu": "ملف",
                "edit_menu": "تحرير",
                "view_menu": "عرض",
                "help_menu": "مساعدة",
                "exit": "خروج",
                "about": "حول",
                "settings": "الإعدادات",
                "admin_panel": "لوحة الإدارة"
            },
            "pos": {
                "title": "نقطة البيع",
                "new_sale": "بيع جديد",
                "add_to_cart": "إضافة إلى السلة",
                "remove_from_cart": "إزالة",
                "clear_cart": "تفريغ السلة",
                "checkout": "إتمام الشراء",
                "total": "المجموع",
                "subtotal": "المجموع الفرعي",
                "tax": "الضريبة",
                "discount": "الخصم",
                "grand_total": "المجموع الكلي",
                "payment_method": "طريقة الدفع",
                "cash": "نقداً",
                "card": "بطاقة",
                "change": "المتبقي",
                "complete_sale": "إتمام البيع",
                "cancel_sale": "إلغاء البيع",
                "print_receipt": "طباعة الإيصال",
                "no_items": "لا توجد منتجات في السلة",
                "item_added": "تم إضافة المنتج إلى السلة",
                "item_removed": "تم إزالة المنتج من السلة",
                "cart_cleared": "تم تفريغ السلة",
                "sale_completed": "تم إتمام البيع بنجاح",
                "sale_cancelled": "تم إلغاء البيع",
                "insufficient_funds": "أموال غير كافية",
                "invalid_amount": "مبلغ غير صحيح",
                "search_products": "البحث عن المنتجات",
                "categories": "الفئات",
                "all_categories": "جميع الفئات",
                "cart": "السلة",
                "quantity": "الكمية",
                "price": "السعر",
                "amount": "المبلغ",
                "payment": "الدفع",
                "receipt": "الإيصال"
            },
            "products": {
                "title": "المنتجات",
                "add_product": "إضافة منتج",
                "edit_product": "تعديل المنتج",
                "delete_product": "حذف المنتج",
                "product_name": "اسم المنتج",
                "product_code": "رمز المنتج",
                "price": "السعر",
                "category": "الفئة",
                "stock": "المخزون",
                "description": "الوصف",
                "save": "حفظ",
                "cancel": "إلغاء",
                "delete": "حذف",
                "confirm_delete": "هل أنت متأكد من حذف هذا المنتج؟",
                "product_saved": "تم حفظ المنتج بنجاح",
                "product_deleted": "تم حذف المنتج بنجاح",
                "error_saving": "خطأ في حفظ المنتج",
                "error_deleting": "خطأ في حذف المنتج"
            },
            "orders": {
                "title": "الطلبات",
                "order_id": "رقم الطلب",
                "date": "التاريخ",
                "time": "الوقت",
                "status": "الحالة",
                "total": "المجموع",
                "actions": "الإجراءات",
                "view": "عرض",
                "edit": "تعديل",
                "delete": "حذف",
                "complete": "إتمام",
                "cancel": "إلغاء",
                "pending": "قيد الانتظار",
                "completed": "مكتمل",
                "cancelled": "ملغي",
                "no_orders": "لا توجد طلبات"
            },
            "reports": {
                "title": "التقارير",
                "sales_report": "تقرير المبيعات",
                "daily_report": "التقرير اليومي",
                "weekly_report": "التقرير الأسبوعي",
                "monthly_report": "التقرير الشهري",
                "custom_report": "تقرير مخصص",
                "shift_reports": "تقارير المناوبات",
                "start_date": "تاريخ البداية",
                "end_date": "تاريخ النهاية",
                "generate": "إنشاء",
                "export": "تصدير",
                "print": "طباعة",
                "total_sales": "إجمالي المبيعات",
                "total_orders": "إجمالي الطلبات",
                "average_order": "متوسط الطلب",
                "top_products": "أفضل المنتجات",
                "sales_by_category": "المبيعات حسب الفئة",
                "date": "التاريخ",
                "time": "الوقت",
                "cashier": "الكاشير",
                "items_sold": "المنتجات المباعة",
                "revenue": "الإيرادات",
                "profit": "الربح",
                "cost": "التكلفة",
                "margin": "الهامش",
                "percentage": "النسبة المئوية",
                "summary": "الملخص",
                "details": "التفاصيل",
                "filter": "تصفية",
                "search": "بحث",
                "refresh": "تحديث",
                "loading": "جاري التحميل...",
                "no_data": "لا توجد بيانات متاحة",
                "export_to_excel": "تصدير إلى Excel",
                "export_to_pdf": "تصدير إلى PDF"
            },
            "shifts": {
                "title": "إدارة المناوبات",
                "open_shift": "فتح مناوبة",
                "close_shift": "إغلاق مناوبة",
                "opening_amount": "مبلغ الافتتاح",
                "closing_amount": "مبلغ الإغلاق",
                "shift_summary": "ملخص المناوبة",
                "cashier": "الكاشير",
                "start_time": "وقت البداية",
                "end_time": "وقت النهاية",
                "duration": "المدة",
                "total_sales": "إجمالي المبيعات",
                "total_orders": "إجمالي الطلبات",
                "shift_opened": "تم فتح المناوبة بنجاح",
                "shift_closed": "تم إغلاق المناوبة بنجاح",
                "enter_password": "أدخل كلمة المرور لإغلاق المناوبة",
                "invalid_password": "كلمة المرور غير صحيحة",
                "shift_already_open": "هناك مناوبة مفتوحة بالفعل",
                "no_open_shift": "لا توجد مناوبة مفتوحة",
                "current_shift": "المناوبة الحالية",
                "shift_history": "تاريخ المناوبات",
                "shift_details": "تفاصيل المناوبة",
                "shift_status": "حالة المناوبة",
                "open": "مفتوحة",
                "closed": "مغلقة",
                "pending": "قيد الانتظار",
                "cash_drawer": "الصندوق النقدي",
                "expected_amount": "المبلغ المتوقع",
                "actual_amount": "المبلغ الفعلي",
                "difference": "الفرق",
                "notes": "ملاحظات",
                "comments": "تعليقات",
                "authorized_by": "مصرح به من",
                "authorization_time": "وقت التصريح"
            },
            "common": {
                "yes": "نعم",
                "no": "لا",
                "ok": "موافق",
                "cancel": "إلغاء",
                "close": "إغلاق",
                "save": "حفظ",
                "delete": "حذف",
                "edit": "تعديل",
                "add": "إضافة",
                "search": "بحث",
                "filter": "تصفية",
                "refresh": "تحديث",
                "loading": "جاري التحميل...",
                "error": "خطأ",
                "success": "نجح",
                "warning": "تحذير",
                "info": "معلومات",
                "confirm": "تأكيد",
                "back": "رجوع",
                "next": "التالي",
                "previous": "السابق",
                "finish": "إنهاء",
                "retry": "إعادة المحاولة",
                "ignore": "تجاهل",
                "abort": "إلغاء",
                "continue": "متابعة",
                "language": "اللغة",
                "apply": "تطبيق",
                "language_info": "ستؤثر تغييرات اللغة فوراً",
                "language_settings": "إعدادات اللغة",
                "tools": "الأدوات",
                "logged_in_as": "تم تسجيل الدخول كـ: {username}"
            },
            "admin": {
                "user_management": "إدارة المستخدمين",
                "system_info": "معلومات النظام",
                "add_user": "إضافة مستخدم",
                "edit_user": "تعديل المستخدم",
                "delete_user": "حذف المستخدم",
                "username": "اسم المستخدم",
                "role": "الدور",
                "password": "كلمة المرور",
                "confirm_password": "تأكيد كلمة المرور",
                "email": "البريد الإلكتروني",
                "phone": "الهاتف",
                "status": "الحالة",
                "active": "نشط",
                "inactive": "غير نشط",
                "created_date": "تاريخ الإنشاء",
                "last_login": "آخر تسجيل دخول",
                "actions": "الإجراءات",
                "view": "عرض",
                "edit": "تعديل",
                "delete": "حذف",
                "save": "حفظ",
                "cancel": "إلغاء",
                "close": "إغلاق",
                "confirm": "تأكيد",
                "yes": "نعم",
                "no": "لا"
            },
            "messages": {
                "operation_successful": "تم إتمام العملية بنجاح",
                "operation_failed": "فشلت العملية",
                "data_saved": "تم حفظ البيانات بنجاح",
                "data_deleted": "تم حذف البيانات بنجاح",
                "connection_error": "خطأ في الاتصال",
                "database_error": "خطأ في قاعدة البيانات",
                "file_error": "خطأ في الملف",
                "permission_error": "تم رفض الإذن",
                "validation_error": "خطأ في التحقق",
                "timeout_error": "انتهت مهلة الطلب",
                "network_error": "خطأ في الشبكة",
                "server_error": "خطأ في الخادم",
                "unknown_error": "حدث خطأ غير معروف"
            }
        }
    
    def set_language(self, language: str):
        """Set the current language."""
        if language not in self.translations:
            language = 'en'  # Default to English
        
        self.current_language = language
        
        # Set Qt locale for RTL support
        if language == 'ar':
            QApplication.setLayoutDirection(Qt.RightToLeft)
            locale = QLocale(QLocale.Arabic, QLocale.SaudiArabia)
        else:
            QApplication.setLayoutDirection(Qt.LeftToRight)
            locale = QLocale(QLocale.English, QLocale.UnitedStates)
        
        QLocale.setDefault(locale)
        
        # Load Qt translator if available
        if self.translator.load(f"qt_{language}", QLocale.system().uiLanguages()[0]):
            QCoreApplication.installTranslator(self.translator)
    
    def get_text(self, key: str, default: str = None) -> str:
        """Get translated text by key."""
        try:
            keys = key.split('.')
            value = self.translations[self.current_language]
            
            for k in keys:
                value = value[k]
            
            return value
        except (KeyError, TypeError):
            # Fallback to English
            try:
                keys = key.split('.')
                value = self.translations['en']
                
                for k in keys:
                    value = value[k]
                
                return value
            except (KeyError, TypeError):
                return default or key
    
    def get_current_language(self) -> str:
        """Get current language code."""
        return self.current_language
    
    def get_available_languages(self) -> list:
        """Get list of available languages."""
        return list(self.translations.keys())
    
    def is_rtl(self) -> bool:
        """Check if current language is RTL (Right-to-Left)."""
        return self.current_language == 'ar'


# Global instance
localization_manager = LocalizationManager()


def tr(key: str, default: str = None) -> str:
    """Convenience function to get translated text."""
    return localization_manager.get_text(key, default)


def set_language(language: str):
    """Convenience function to set language."""
    localization_manager.set_language(language)


def is_rtl() -> bool:
    """Convenience function to check if current language is RTL."""
    return localization_manager.is_rtl() 


def format_time_12hour(dt):
    """
    Format datetime object to 12-hour format with AM/PM.
    
    Args:
        dt: datetime object
        
    Returns:
        str: Time formatted as "hh:mm:ss AM/PM" or "hh:mm AM/PM"
    """
    if dt is None:
        return "N/A"
    
    # Format as 12-hour with AM/PM
    return dt.strftime("%I:%M:%S %p")

def format_time_12hour_short(dt):
    """
    Format datetime object to 12-hour format with AM/PM (short version without seconds).
    
    Args:
        dt: datetime object
        
    Returns:
        str: Time formatted as "hh:mm AM/PM"
    """
    if dt is None:
        return "N/A"
    
    # Format as 12-hour with AM/PM (no seconds)
    return dt.strftime("%I:%M %p")

def format_datetime_12hour(dt):
    """
    Format datetime object to include date and 12-hour time with AM/PM.
    
    Args:
        dt: datetime object
        
    Returns:
        str: DateTime formatted as "YYYY-MM-DD hh:mm:ss AM/PM"
    """
    if dt is None:
        return "N/A"
    
    # Format as date with 12-hour time
    return dt.strftime("%Y-%m-%d %I:%M:%S %p") 