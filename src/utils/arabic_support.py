#!/usr/bin/env python3
"""
Arabic Language Support Utilities
================================

This module provides comprehensive Arabic language support for the Talinda POS application,
including proper font configuration, RTL layout handling, and text rendering fixes.

Author: Talinda POS Team
Version: 1.0.0
License: MIT
"""

import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QFont, QFontDatabase


class ArabicSupport:
    """Handles Arabic language support and RTL layout."""
    
    # Arabic font families that work well with Arabic text
    ARABIC_FONTS = [
        'Segoe UI',
        'Tahoma',
        'Arial',
        'Microsoft Sans Serif',
        'Noto Sans Arabic',
        'Amiri',
        'Scheherazade',
        'Lateef',
        'KacstOne',
        'Droid Arabic Naskh',
        'Droid Arabic Kufi'
    ]
    
    @staticmethod
    def setup_arabic_fonts():
        """Setup Arabic fonts for the application."""
        try:
            # Get available fonts
            font_db = QFontDatabase()
            available_fonts = font_db.families()
            
            # Find the best Arabic font
            arabic_font = None
            for font_name in ArabicSupport.ARABIC_FONTS:
                if font_name in available_fonts:
                    arabic_font = font_name
                    break
            
            # If no Arabic font found, use system default
            if not arabic_font:
                arabic_font = QApplication.font().family()
            
            # Set application font
            app_font = QFont(arabic_font, 9)
            QApplication.setFont(app_font)
            
            return arabic_font
            
        except Exception as e:
            print(f"Error setting up Arabic fonts: {e}")
            return None
    
    @staticmethod
    def setup_rtl_layout():
        """Setup RTL (Right-to-Left) layout for Arabic."""
        try:
            # Set application layout direction to RTL
            QApplication.setLayoutDirection(Qt.RightToLeft)
            
            # Set Arabic locale
            locale = QLocale(QLocale.Arabic, QLocale.SaudiArabia)
            QLocale.setDefault(locale)
            
            return True
            
        except Exception as e:
            print(f"Error setting up RTL layout: {e}")
            return False
    
    @staticmethod
    def setup_ltr_layout():
        """Setup LTR (Left-to-Right) layout for English."""
        try:
            # Set application layout direction to LTR
            QApplication.setLayoutDirection(Qt.LeftToRight)
            
            # Set English locale
            locale = QLocale(QLocale.English, QLocale.UnitedStates)
            QLocale.setDefault(locale)
            
            return True
            
        except Exception as e:
            print(f"Error setting up LTR layout: {e}")
            return False
    
    @staticmethod
    def apply_arabic_stylesheet():
        """Apply Arabic-specific stylesheet for better RTL support."""
        arabic_stylesheet = """
        /* Arabic-specific styles */
        QWidget {
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
        }
        
        /* RTL-specific adjustments */
        QMainWindow[layoutDirection="1"] QMenuBar::item {
            padding-right: 8px;
            padding-left: 8px;
        }
        
        QMainWindow[layoutDirection="1"] QToolBar {
            spacing: 8px;
        }
        
        QMainWindow[layoutDirection="1"] QPushButton {
            text-align: center;
        }
        
        QMainWindow[layoutDirection="1"] QLabel {
            text-align: right;
        }
        
        QMainWindow[layoutDirection="1"] QLineEdit {
            text-align: right;
        }
        
        QMainWindow[layoutDirection="1"] QTextEdit {
            text-align: right;
        }
        
        QMainWindow[layoutDirection="1"] QComboBox {
            text-align: right;
        }
        
        QMainWindow[layoutDirection="1"] QTableWidget {
            text-align: right;
        }
        
        QMainWindow[layoutDirection="1"] QHeaderView::section {
            text-align: right;
        }
        
        /* Arabic text specific */
        QLabel[arabic="true"] {
            text-align: right;
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
        }
        
        QLineEdit[arabic="true"] {
            text-align: right;
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
        }
        
        QTextEdit[arabic="true"] {
            text-align: right;
            font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
        }
        """
        
        return arabic_stylesheet
    
    @staticmethod
    def is_arabic_text(text):
        """Check if text contains Arabic characters."""
        if not text:
            return False
        
        # Arabic Unicode ranges
        arabic_ranges = [
            (0x0600, 0x06FF),   # Arabic
            (0x0750, 0x077F),   # Arabic Supplement
            (0x08A0, 0x08FF),   # Arabic Extended-A
            (0xFB50, 0xFDFF),   # Arabic Presentation Forms-A
            (0xFE70, 0xFEFF),   # Arabic Presentation Forms-B
        ]
        
        for char in text:
            char_code = ord(char)
            for start, end in arabic_ranges:
                if start <= char_code <= end:
                    return True
        
        return False
    
    @staticmethod
    def get_text_alignment(text):
        """Get appropriate text alignment based on text content."""
        if ArabicSupport.is_arabic_text(text):
            return Qt.AlignRight | Qt.AlignVCenter
        else:
            return Qt.AlignLeft | Qt.AlignVCenter
    
    @staticmethod
    def setup_widget_for_arabic(widget, text=None):
        """Setup a widget for proper Arabic text display."""
        try:
            if text and ArabicSupport.is_arabic_text(text):
                # Set Arabic-specific properties
                widget.setProperty("arabic", True)
                widget.setStyleSheet("""
                    QWidget[arabic="true"] {
                        text-align: right;
                        font-family: 'Segoe UI', 'Tahoma', 'Arial', sans-serif;
                    }
                """)
                
                # Set text alignment
                if hasattr(widget, 'setAlignment'):
                    widget.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
                
                # Set text direction
                if hasattr(widget, 'setTextDirection'):
                    widget.setTextDirection(Qt.RightToLeft)
            
            return True
            
        except Exception as e:
            print(f"Error setting up widget for Arabic: {e}")
            return False


def setup_arabic_support():
    """Initialize Arabic language support."""
    try:
        # Setup Arabic fonts
        font = ArabicSupport.setup_arabic_fonts()
        
        # Apply Arabic stylesheet
        arabic_stylesheet = ArabicSupport.apply_arabic_stylesheet()
        
        return {
            'font': font,
            'stylesheet': arabic_stylesheet,
            'success': True
        }
        
    except Exception as e:
        print(f"Error setting up Arabic support: {e}")
        return {
            'font': None,
            'stylesheet': '',
            'success': False,
            'error': str(e)
        }


def apply_arabic_to_widget(widget, text=None):
    """Apply Arabic support to a specific widget."""
    return ArabicSupport.setup_widget_for_arabic(widget, text)


def is_arabic_text(text):
    """Check if text contains Arabic characters."""
    return ArabicSupport.is_arabic_text(text)


def get_arabic_text_alignment(text):
    """Get appropriate text alignment for Arabic text."""
    return ArabicSupport.get_text_alignment(text) 