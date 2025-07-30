"""
Time Zone Settings Dialog for Talinda POS.
Allows admin users to configure time zone caching settings.
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QCheckBox, QComboBox, QGroupBox, QFormLayout, QSpinBox,
    QMessageBox, QTextEdit, QTabWidget, QWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont
import json
import os
import logging
from datetime import datetime
import time
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TimeZoneSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Time Zone Settings')
        self.setMinimumSize(600, 500)
        self.settings_file = "timezone_settings.json"
        self.settings = self.load_settings()
        self.init_ui()
        self.load_current_settings()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("🕐 Time Zone Settings")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        """)
        layout.addWidget(title)
        
        # Description
        description = QLabel("Configure time zone caching and synchronization settings for the application.")
        description.setStyleSheet("""
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 20px;
            text-align: center;
        """)
        layout.addWidget(description)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                color: #2c3e50;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #bdc3c7;
            }
        """)
        
        # General Settings Tab
        self.general_tab = self.create_general_tab()
        self.tab_widget.addTab(self.general_tab, "⚙️ General Settings")
        
        # Time Zone Cache Tab
        self.cache_tab = self.create_cache_tab()
        self.tab_widget.addTab(self.cache_tab, "💾 Cache Settings")
        
        # System Info Tab
        self.info_tab = self.create_info_tab()
        self.tab_widget.addTab(self.info_tab, "ℹ️ System Info")
        
        layout.addWidget(self.tab_widget)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        # Reset button
        self.reset_btn = QPushButton("🔄 Reset to Defaults")
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.reset_btn.clicked.connect(self.reset_to_defaults)
        button_layout.addWidget(self.reset_btn)
        
        # Save button
        self.save_btn = QPushButton("💾 Save Settings")
        self.save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        """)
        self.save_btn.clicked.connect(self.save_settings)
        button_layout.addWidget(self.save_btn)
        
        # Close button
        self.close_btn = QPushButton("❌ Close")
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)

    def create_general_tab(self) -> QWidget:
        """Create the general settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Time Zone Settings Group
        timezone_group = QGroupBox("🌍 Time Zone Configuration")
        timezone_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #3498db;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        timezone_layout = QFormLayout(timezone_group)
        timezone_layout.setSpacing(15)
        
        # Enable time zone caching
        self.enable_cache_checkbox = QCheckBox("Enable Time Zone Caching")
        self.enable_cache_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #2c3e50;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        timezone_layout.addRow("", self.enable_cache_checkbox)
        
        # Auto-detect time zone
        self.auto_detect_checkbox = QCheckBox("Auto-detect System Time Zone")
        self.auto_detect_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #2c3e50;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
            }
        """)
        timezone_layout.addRow("", self.auto_detect_checkbox)
        
        # Manual time zone selection
        self.timezone_combo = QComboBox()
        self.timezone_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                min-width: 200px;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
            }
        """)
        
        # Add common time zones
        timezones = [
            "UTC",
            "America/New_York",
            "America/Chicago", 
            "America/Denver",
            "America/Los_Angeles",
            "Europe/London",
            "Europe/Paris",
            "Asia/Tokyo",
            "Asia/Dubai",
            "Asia/Kolkata"
        ]
        
        for tz in timezones:
            self.timezone_combo.addItem(tz)
        
        timezone_layout.addRow("Manual Time Zone:", self.timezone_combo)
        
        layout.addWidget(timezone_group)
        
        # Time Display Settings Group
        display_group = QGroupBox("🕐 Time Display Settings")
        display_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #e67e22;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        display_layout = QFormLayout(display_group)
        display_layout.setSpacing(15)
        
        # 12/24 hour format
        self.hour_format_combo = QComboBox()
        self.hour_format_combo.addItems(["12-hour (AM/PM)", "24-hour"])
        self.hour_format_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                min-width: 150px;
            }
        """)
        display_layout.addRow("Time Format:", self.hour_format_combo)
        
        # Show seconds
        self.show_seconds_checkbox = QCheckBox("Show Seconds in Time Display")
        self.show_seconds_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        display_layout.addRow("", self.show_seconds_checkbox)
        
        layout.addWidget(display_group)
        layout.addStretch()
        
        return widget

    def create_cache_tab(self) -> QWidget:
        """Create the cache settings tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Cache Settings Group
        cache_group = QGroupBox("💾 Cache Configuration")
        cache_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #9b59b6;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        cache_layout = QFormLayout(cache_group)
        cache_layout.setSpacing(15)
        
        # Cache duration
        self.cache_duration_spin = QSpinBox()
        self.cache_duration_spin.setRange(1, 24)
        self.cache_duration_spin.setSuffix(" hours")
        self.cache_duration_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        cache_layout.addRow("Cache Duration:", self.cache_duration_spin)
        
        # Auto-refresh cache
        self.auto_refresh_checkbox = QCheckBox("Auto-refresh Cache")
        self.auto_refresh_checkbox.setStyleSheet("""
            QCheckBox {
                font-size: 14px;
                color: #2c3e50;
            }
        """)
        cache_layout.addRow("", self.auto_refresh_checkbox)
        
        # Refresh interval
        self.refresh_interval_spin = QSpinBox()
        self.refresh_interval_spin.setRange(1, 60)
        self.refresh_interval_spin.setSuffix(" minutes")
        self.refresh_interval_spin.setStyleSheet("""
            QSpinBox {
                padding: 8px;
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                font-size: 14px;
                min-width: 100px;
            }
        """)
        cache_layout.addRow("Refresh Interval:", self.refresh_interval_spin)
        
        layout.addWidget(cache_group)
        
        # Cache Actions Group
        actions_group = QGroupBox("🔧 Cache Actions")
        actions_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #e74c3c;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        actions_layout = QVBoxLayout(actions_group)
        actions_layout.setSpacing(10)
        
        # Clear cache button
        self.clear_cache_btn = QPushButton("🗑️ Clear Time Zone Cache")
        self.clear_cache_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        self.clear_cache_btn.clicked.connect(self.clear_cache)
        actions_layout.addWidget(self.clear_cache_btn)
        
        # Refresh cache button
        self.refresh_cache_btn = QPushButton("🔄 Refresh Cache Now")
        self.refresh_cache_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        self.refresh_cache_btn.clicked.connect(self.refresh_cache)
        actions_layout.addWidget(self.refresh_cache_btn)
        
        layout.addWidget(actions_group)
        layout.addStretch()
        
        return widget

    def create_info_tab(self) -> QWidget:
        """Create the system info tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Current System Info Group
        info_group = QGroupBox("ℹ️ Current System Information")
        info_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #27ae60;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        info_layout = QFormLayout(info_group)
        info_layout.setSpacing(15)
        
        # Current time
        self.current_time_label = QLabel()
        self.current_time_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        info_layout.addRow("Current Time:", self.current_time_label)
        
        # System timezone
        self.system_timezone_label = QLabel()
        self.system_timezone_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        info_layout.addRow("System Timezone:", self.system_timezone_label)
        
        # Cache status
        self.cache_status_label = QLabel()
        self.cache_status_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        info_layout.addRow("Cache Status:", self.cache_status_label)
        
        # Last cache update
        self.last_cache_label = QLabel()
        self.last_cache_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        info_layout.addRow("Last Cache Update:", self.last_cache_label)
        
        layout.addWidget(info_group)
        
        # Cache Log Group
        log_group = QGroupBox("📋 Cache Log")
        log_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                border: 2px solid #f39c12;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
        """)
        
        log_layout = QVBoxLayout(log_group)
        
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(150)
        self.log_text.setStyleSheet("""
            QTextEdit {
                border: 1px solid #bdc3c7;
                border-radius: 5px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
            }
        """)
        log_layout.addWidget(self.log_text)
        
        layout.addWidget(log_group)
        layout.addStretch()
        
        # Update timer for real-time info
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self.update_system_info)
        self.update_timer.start(1000)  # Update every second
        
        return widget

    def load_settings(self) -> Dict[str, Any]:
        """Load settings from file."""
        default_settings = {
            "enable_cache": True,
            "auto_detect": True,
            "manual_timezone": "UTC",
            "hour_format": "12-hour (AM/PM)",
            "show_seconds": True,
            "cache_duration": 6,
            "auto_refresh": True,
            "refresh_interval": 15,
            "last_cache_update": None,
            "cache_log": []
        }
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r') as f:
                    settings = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    for key, value in default_settings.items():
                        if key not in settings:
                            settings[key] = value
                    return settings
        except Exception as e:
            logger.error(f"Error loading timezone settings: {e}")
        
        return default_settings

    def save_settings(self):
        """Save settings to file."""
        try:
            # Update settings from UI
            self.settings["enable_cache"] = self.enable_cache_checkbox.isChecked()
            self.settings["auto_detect"] = self.auto_detect_checkbox.isChecked()
            self.settings["manual_timezone"] = self.timezone_combo.currentText()
            self.settings["hour_format"] = self.hour_format_combo.currentText()
            self.settings["show_seconds"] = self.show_seconds_checkbox.isChecked()
            self.settings["cache_duration"] = self.cache_duration_spin.value()
            self.settings["auto_refresh"] = self.auto_refresh_checkbox.isChecked()
            self.settings["refresh_interval"] = self.refresh_interval_spin.value()
            
            # Save to file
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=2)
            
            # Add to log
            self.add_log_entry("Settings saved successfully")
            
            QMessageBox.information(self, "Success", "Time zone settings saved successfully!")
            
        except Exception as e:
            logger.error(f"Error saving timezone settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")

    def load_current_settings(self):
        """Load current settings into UI."""
        self.enable_cache_checkbox.setChecked(self.settings.get("enable_cache", True))
        self.auto_detect_checkbox.setChecked(self.settings.get("auto_detect", True))
        
        # Set timezone combo
        manual_tz = self.settings.get("manual_timezone", "UTC")
        index = self.timezone_combo.findText(manual_tz)
        if index >= 0:
            self.timezone_combo.setCurrentIndex(index)
        
        # Set hour format
        hour_format = self.settings.get("hour_format", "12-hour (AM/PM)")
        index = self.hour_format_combo.findText(hour_format)
        if index >= 0:
            self.hour_format_combo.setCurrentIndex(index)
        
        self.show_seconds_checkbox.setChecked(self.settings.get("show_seconds", True))
        self.cache_duration_spin.setValue(self.settings.get("cache_duration", 6))
        self.auto_refresh_checkbox.setChecked(self.settings.get("auto_refresh", True))
        self.refresh_interval_spin.setValue(self.settings.get("refresh_interval", 15))

    def update_system_info(self):
        """Update system information display."""
        try:
            # Current time
            current_time = datetime.now().strftime("%I:%M:%S %p")
            self.current_time_label.setText(current_time)
            
            # System timezone
            try:
                import time
                system_tz = time.tzname[time.daylight]
                self.system_timezone_label.setText(system_tz)
            except:
                self.system_timezone_label.setText("Unknown")
            
            # Cache status
            if self.settings.get("enable_cache", True):
                self.cache_status_label.setText("🟢 Enabled")
                self.cache_status_label.setStyleSheet("font-weight: bold; color: #27ae60;")
            else:
                self.cache_status_label.setText("🔴 Disabled")
                self.cache_status_label.setStyleSheet("font-weight: bold; color: #e74c3c;")
            
            # Last cache update
            last_update = self.settings.get("last_cache_update")
            if last_update:
                self.last_cache_label.setText(last_update)
            else:
                self.last_cache_label.setText("Never")
                
        except Exception as e:
            logger.error(f"Error updating system info: {e}")

    def clear_cache(self):
        """Clear the time zone cache."""
        try:
            reply = QMessageBox.question(
                self, "Clear Cache", 
                "Are you sure you want to clear the time zone cache?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.settings["last_cache_update"] = None
                self.settings["cache_log"] = []
                self.add_log_entry("Cache cleared by admin")
                QMessageBox.information(self, "Success", "Time zone cache cleared successfully!")
                
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            QMessageBox.critical(self, "Error", f"Failed to clear cache: {str(e)}")

    def refresh_cache(self):
        """Refresh the time zone cache."""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            self.settings["last_cache_update"] = current_time
            self.add_log_entry(f"Cache refreshed at {current_time}")
            QMessageBox.information(self, "Success", "Time zone cache refreshed successfully!")
            
        except Exception as e:
            logger.error(f"Error refreshing cache: {e}")
            QMessageBox.critical(self, "Error", f"Failed to refresh cache: {str(e)}")

    def reset_to_defaults(self):
        """Reset settings to defaults."""
        try:
            reply = QMessageBox.question(
                self, "Reset Settings", 
                "Are you sure you want to reset all time zone settings to defaults?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.settings = {
                    "enable_cache": True,
                    "auto_detect": True,
                    "manual_timezone": "UTC",
                    "hour_format": "12-hour (AM/PM)",
                    "show_seconds": True,
                    "cache_duration": 6,
                    "auto_refresh": True,
                    "refresh_interval": 15,
                    "last_cache_update": None,
                    "cache_log": []
                }
                
                self.load_current_settings()
                self.add_log_entry("Settings reset to defaults")
                QMessageBox.information(self, "Success", "Settings reset to defaults successfully!")
                
        except Exception as e:
            logger.error(f"Error resetting settings: {e}")
            QMessageBox.critical(self, "Error", f"Failed to reset settings: {str(e)}")

    def add_log_entry(self, message: str):
        """Add entry to cache log."""
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
            log_entry = f"[{timestamp}] {message}"
            
            if "cache_log" not in self.settings:
                self.settings["cache_log"] = []
            
            self.settings["cache_log"].append(log_entry)
            
            # Keep only last 50 entries
            if len(self.settings["cache_log"]) > 50:
                self.settings["cache_log"] = self.settings["cache_log"][-50:]
            
            # Update log display
            self.log_text.setPlainText("\n".join(self.settings["cache_log"]))
            
        except Exception as e:
            logger.error(f"Error adding log entry: {e}")

    def closeEvent(self, event):
        """Handle close event."""
        if self.update_timer.isActive():
            self.update_timer.stop()
        event.accept() 