#!/usr/bin/env python3
"""
Language Selector Component
==========================

A component for selecting the application language (English/Arabic).

Author: Talinda POS Team
Version: 1.0.0
License: MIT
"""

from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QLabel, QComboBox, 
    QPushButton, QFrame, QSizePolicy, QDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon

from utils.localization import tr, set_language, is_rtl, apply_arabic_to_widget


class LanguageSelector(QWidget):
    """Language selector widget with Arabic/English support."""
    
    language_changed = pyqtSignal(str)  # Signal emitted when language changes
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_language = 'en'
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        """Initialize the language selector UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Title
        title_label = QLabel(tr("common.language", "Language"))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }
        """)
        # Apply Arabic support if needed
        apply_arabic_to_widget(title_label, tr("common.language", "Language"))
        layout.addWidget(title_label)
        
        # Language selection frame
        selection_frame = QFrame()
        selection_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        frame_layout = QVBoxLayout(selection_frame)
        frame_layout.setSpacing(15)
        
        # Language combo box
        self.language_combo = QComboBox()
        self.language_combo.addItem("🇺🇸 English", "en")
        self.language_combo.addItem("🇸🇦 العربية", "ar")
        self.language_combo.setCurrentText("🇺🇸 English")
        self.language_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #1976d2;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #666;
                margin-right: 10px;
            }
        """)
        frame_layout.addWidget(self.language_combo)
        
        # Apply button
        self.apply_button = QPushButton(tr("common.apply", "Apply"))
        self.apply_button.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
            QPushButton:disabled {
                background-color: #bdbdbd;
            }
        """)
        frame_layout.addWidget(self.apply_button)
        
        layout.addWidget(selection_frame)
        
        # Info text
        info_label = QLabel(tr("common.language_info", "Language changes will take effect immediately"))
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            QLabel {
                color: #6c757d;
                font-size: 12px;
                font-style: italic;
            }
        """)
        # Apply Arabic support if needed
        apply_arabic_to_widget(info_label, tr("common.language_info", "Language changes will take effect immediately"))
        layout.addWidget(info_label)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setMinimumWidth(250)
    
    def setup_connections(self):
        """Setup signal connections."""
        self.apply_button.clicked.connect(self.apply_language_change)
        self.language_combo.currentIndexChanged.connect(self.on_language_selection_changed)
    
    def on_language_selection_changed(self, index):
        """Handle language selection change."""
        language = self.language_combo.itemData(index)
        self.current_language = language
        
        # Update button text based on selected language
        if language == 'ar':
            self.apply_button.setText("تطبيق")
        else:
            self.apply_button.setText("Apply")
    
    def apply_language_change(self):
        """Apply the selected language change."""
        try:
            # Set the new language
            set_language(self.current_language)
            
            # Emit signal for parent components
            self.language_changed.emit(self.current_language)
            
            # Update UI text
            self.update_ui_text()
            
        except Exception as e:
            print(f"Error applying language change: {e}")
    
    def update_ui_text(self):
        """Update UI text after language change."""
        # Update title
        title_label = self.findChild(QLabel)
        if title_label:
            title_label.setText(tr("common.language", "Language"))
        
        # Update info text
        info_labels = self.findChildren(QLabel)
        for label in info_labels:
            if "language_info" in label.text() or "Language changes" in label.text():
                label.setText(tr("common.language_info", "Language changes will take effect immediately"))
                break
    
    def set_current_language(self, language: str):
        """Set the current language in the selector."""
        index = self.language_combo.findData(language)
        if index >= 0:
            self.language_combo.setCurrentIndex(index)
            self.current_language = language
    
    def get_current_language(self) -> str:
        """Get the currently selected language."""
        return self.current_language


class LanguageSelectorDialog(QDialog):
    """Dialog for language selection."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle(tr("common.language_settings", "Language Settings"))
        self.setFixedSize(300, 200)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Add language selector
        self.language_selector = LanguageSelector()
        self.language_selector.language_changed.connect(self.on_language_changed)
        layout.addWidget(self.language_selector)
        
        # Close button
        close_button = QPushButton(tr("common.close", "Close"))
        close_button.clicked.connect(self.close)
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #6c757d;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5a6268;
            }
        """)
        layout.addWidget(close_button)
    
    def on_language_changed(self, language: str):
        """Handle language change."""
        # This can be overridden by parent classes
        pass 