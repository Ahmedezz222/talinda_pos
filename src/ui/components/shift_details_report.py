#!/usr/bin/env python3
"""
Shift Details Report Window
==========================

A comprehensive report window that displays detailed information about a specific shift
including sales breakdown, product sales, and order details.

Author: Talinda POS Team
Version: 1.0.0
"""

import sys
import os
from typing import Optional, Dict, Any
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.parent.parent.absolute()
sys.path.insert(0, str(current_dir))

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QWidget, QGridLayout, QTableWidget, QTableWidgetItem, QGroupBox,
    QFrame, QSplitter, QTextEdit, QComboBox, QMessageBox, QHeaderView,
    QSizePolicy, QSpacerItem, QTabWidget
)
from PyQt5.QtGui import (
    QFont, QPalette, QColor, QPixmap, QIcon, QPainter, QBrush,
    QLinearGradient
)
from PyQt5.QtCore import (
    Qt, QTimer, QSize, QRect, QPropertyAnimation, QEasingCurve
)

from controllers.shift_controller import ShiftController
from database.database_manager import DatabaseManager
from utils.localization import tr


class ShiftDetailsReportDialog(QDialog):
    """Dialog for displaying comprehensive shift details report."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shift_controller = ShiftController()
        self.db_manager = DatabaseManager()
        self.current_shift_id = None
        self.shift_data = None
        
        self.init_ui()
        self.setup_connections()
        self.load_shifts()
    
    def init_ui(self):
        """Initialize the user interface."""
        self.setWindowTitle("Shift Details Report")
        self.setMinimumSize(1600, 1000)
        self.setModal(True)
        
        # Set window icon and style
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QGroupBox {
                font-weight: bold;
                font-size: 16px;
                color: #2c3e50;
                border: 3px solid #dee2e6;
                border-radius: 12px;
                margin-top: 15px;
                padding-top: 15px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 10px 0 10px;
                background-color: white;
            }
            QTableWidget {
                background-color: white;
                border: 2px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #f8f9fa;
                selection-background-color: #e3f2fd;
                selection-color: #1976d2;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #f8f9fa;
                font-size: 14px;
            }
            QTableWidget::item:selected {
                background-color: #e3f2fd;
                color: #1976d2;
                font-weight: bold;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                padding: 12px;
                border: none;
                border-bottom: 3px solid #007bff;
                font-weight: bold;
                color: #495057;
                font-size: 14px;
            }
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-height: 20px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #0056b3, stop:1 #004085);
                transform: translateY(-1px);
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #004085, stop:1 #002752);
            }
            QComboBox {
                padding: 12px;
                border: 3px solid #dee2e6;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QComboBox:focus {
                border-color: #007bff;
                border-width: 3px;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #6c757d;
                margin-right: 10px;
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QTabWidget::pane {
                border: 3px solid #dee2e6;
                border-radius: 12px;
                background-color: white;
                margin-top: 5px;
            }
            QTabWidget::tab-bar {
                alignment: center;
                background-color: transparent;
            }
            QTabBar::tab {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                color: #6c757d;
                padding: 15px 25px;
                margin-right: 5px;
                border-top-left-radius: 12px;
                border-top-right-radius: 12px;
                font-weight: bold;
                font-size: 15px;
                min-width: 140px;
                min-height: 20px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #007bff, stop:1 #0056b3);
                color: white;
                border-bottom: 3px solid #007bff;
            }
            QTabBar::tab:hover:!selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9ecef, stop:1 #dee2e6);
                color: #495057;
            }
        """)
        
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(25, 25, 25, 25)
        
        # Header section
        header_widget = self.create_header_section()
        main_layout.addWidget(header_widget)
        
        # Shift selection section
        selection_widget = self.create_selection_section()
        main_layout.addWidget(selection_widget)
        
        # Create tabbed content area
        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabWidget::pane {
                border: 3px solid #dee2e6;
                border-radius: 12px;
                background-color: white;
                padding: 25px;
            }
        """)
        
        # Create tabs
        self.create_overview_tab()
        self.create_sales_tab()
        self.create_products_tab()
        self.create_orders_tab()
        
        main_layout.addWidget(self.tab_widget)
        
        # Buttons section
        buttons_widget = self.create_buttons_section()
        main_layout.addWidget(buttons_widget)
    
    def create_header_section(self) -> QWidget:
        """Create the header section with title and description."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Title with gradient background
        title_frame = QFrame()
        title_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #007bff, stop:1 #0056b3);
                border-radius: 15px;
                padding: 20px;
            }
        """)
        title_layout = QVBoxLayout(title_frame)
        
        # Title
        title_label = QLabel("📊 Shift Details Report")
        title_label.setStyleSheet("""
            QLabel {
                font-size: 32px;
                font-weight: bold;
                color: white;
                padding: 10px 0;
            }
        """)
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        
        # Description
        desc_label = QLabel("Comprehensive report showing shift performance, sales breakdown, and order details")
        desc_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                color: #e3f2fd;
                padding: 5px 0;
            }
        """)
        desc_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(desc_label)
        
        layout.addWidget(title_frame)
        return widget
    
    def create_selection_section(self) -> QWidget:
        """Create the shift selection section."""
        widget = QGroupBox("🎯 Select Shift")
        layout = QHBoxLayout(widget)
        layout.setSpacing(20)
        
        # Shift selection combo box
        self.shift_combo = QComboBox()
        self.shift_combo.setMinimumWidth(500)
        self.shift_combo.setStyleSheet("""
            QComboBox {
                font-size: 14px;
                padding: 15px;
                min-height: 25px;
            }
        """)
        layout.addWidget(QLabel("📋 Shift:"))
        layout.addWidget(self.shift_combo)
        
        # Load button
        self.load_button = QPushButton("🔄 Load Report")
        self.load_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #28a745, stop:1 #218838);
                min-width: 160px;
                padding: 15px 25px;
                min-height: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #218838, stop:1 #1e7e34);
            }
        """)
        layout.addWidget(self.load_button)
        
        layout.addStretch()
        return widget
    
    def create_overview_tab(self):
        """Create the overview tab."""
        overview_widget = QWidget()
        layout = QVBoxLayout(overview_widget)
        layout.setSpacing(25)
        
        # Shift overview section
        overview_group = QGroupBox("📋 Shift Overview")
        overview_layout = QGridLayout(overview_group)
        overview_layout.setSpacing(20)
        
        # Create labels for shift details
        self.shift_id_label = QLabel("Shift ID: -")
        self.user_label = QLabel("User: -")
        self.open_time_label = QLabel("Open Time: -")
        self.close_time_label = QLabel("Close Time: -")
        self.duration_label = QLabel("Duration: -")
        self.opening_amount_label = QLabel("Opening Amount: -")
        self.status_label = QLabel("Status: -")
        
        # Style the labels
        for label in [self.shift_id_label, self.user_label, self.open_time_label,
                     self.close_time_label, self.duration_label, self.opening_amount_label,
                     self.status_label]:
            label.setStyleSheet("""
                QLabel {
                    font-size: 16px;
                    padding: 15px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 #f8f9fa, stop:1 #e9ecef);
                    border: 2px solid #dee2e6;
                    border-radius: 8px;
                    min-width: 280px;
                    font-weight: bold;
                    color: #2c3e50;
                }
            """)
        
        # Add labels to grid
        overview_layout.addWidget(QLabel("🆔 Shift ID:"), 0, 0)
        overview_layout.addWidget(self.shift_id_label, 0, 1)
        overview_layout.addWidget(QLabel("👤 User:"), 0, 2)
        overview_layout.addWidget(self.user_label, 0, 3)
        
        overview_layout.addWidget(QLabel("🕐 Open Time:"), 1, 0)
        overview_layout.addWidget(self.open_time_label, 1, 1)
        overview_layout.addWidget(QLabel("🕐 Close Time:"), 1, 2)
        overview_layout.addWidget(self.close_time_label, 1, 3)
        
        overview_layout.addWidget(QLabel("⏱️ Duration:"), 2, 0)
        overview_layout.addWidget(self.duration_label, 2, 1)
        overview_layout.addWidget(QLabel("💰 Opening Amount:"), 2, 2)
        overview_layout.addWidget(self.opening_amount_label, 2, 3)
        
        overview_layout.addWidget(QLabel("📊 Status:"), 3, 0)
        overview_layout.addWidget(self.status_label, 3, 1)
        
        layout.addWidget(overview_group)
        layout.addStretch()
        
        self.tab_widget.addTab(overview_widget, "📋 Overview")
    
    def create_sales_tab(self):
        """Create the sales tab."""
        sales_widget = QWidget()
        layout = QVBoxLayout(sales_widget)
        layout.setSpacing(25)
        
        # Sales by payment method section
        payment_group = QGroupBox("💳 Sales by Payment Method")
        payment_layout = QVBoxLayout(payment_group)
        
        # Create table
        self.payment_table = QTableWidget()
        self.payment_table.setColumnCount(2)
        self.payment_table.setHorizontalHeaderLabels(["Payment Method", "Total Amount"])
        self.payment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.payment_table.setAlternatingRowColors(True)
        self.payment_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                min-height: 250px;
            }
        """)
        
        payment_layout.addWidget(self.payment_table)
        layout.addWidget(payment_group)
        layout.addStretch()
        
        self.tab_widget.addTab(sales_widget, "💳 Sales")
    
    def create_products_tab(self):
        """Create the products tab."""
        products_widget = QWidget()
        layout = QVBoxLayout(products_widget)
        layout.setSpacing(25)
        
        # Product sales section
        products_group = QGroupBox("📦 Product Sales Details")
        products_layout = QVBoxLayout(products_group)
        
        # Create table
        self.products_table = QTableWidget()
        self.products_table.setColumnCount(4)
        self.products_table.setHorizontalHeaderLabels([
            "Product Name", "Quantity", "Unit Price", "Total Amount"
        ])
        self.products_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.products_table.setAlternatingRowColors(True)
        self.products_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                min-height: 350px;
            }
        """)
        
        products_layout.addWidget(self.products_table)
        layout.addWidget(products_group)
        layout.addStretch()
        
        self.tab_widget.addTab(products_widget, "📦 Products")
    
    def create_orders_tab(self):
        """Create the orders tab."""
        orders_widget = QWidget()
        layout = QVBoxLayout(orders_widget)
        layout.setSpacing(25)
        
        # Orders section
        orders_group = QGroupBox("📋 Orders")
        orders_layout = QVBoxLayout(orders_group)
        
        # Create table
        self.orders_table = QTableWidget()
        self.orders_table.setColumnCount(6)
        self.orders_table.setHorizontalHeaderLabels([
            "Order #", "Customer", "Status", "Created", "Total Amount", "Subtotal"
        ])
        self.orders_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.orders_table.setAlternatingRowColors(True)
        self.orders_table.setStyleSheet("""
            QTableWidget {
                font-size: 14px;
                min-height: 350px;
            }
        """)
        
        orders_layout.addWidget(self.orders_table)
        layout.addWidget(orders_group)
        layout.addStretch()
        
        self.tab_widget.addTab(orders_widget, "📋 Orders")
    
    def create_buttons_section(self) -> QWidget:
        """Create the buttons section."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(15)
        
        # Print button
        self.print_button = QPushButton("🖨️ Print Report")
        self.print_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #17a2b8, stop:1 #138496);
                min-width: 180px;
                padding: 15px 25px;
                min-height: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #138496, stop:1 #117a8b);
            }
        """)
        
        # Export button
        self.export_button = QPushButton("📄 Export to Excel")
        self.export_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #6f42c1, stop:1 #5a32a3);
                min-width: 180px;
                padding: 15px 25px;
                min-height: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #5a32a3, stop:1 #4c2b8a);
            }
        """)
        
        # Close button
        self.close_button = QPushButton("❌ Close")
        self.close_button.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dc3545, stop:1 #c82333);
                min-width: 140px;
                padding: 15px 25px;
                min-height: 25px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #c82333, stop:1 #bd2130);
            }
        """)
        
        layout.addStretch()
        layout.addWidget(self.print_button)
        layout.addWidget(self.export_button)
        layout.addWidget(self.close_button)
        
        return widget
    
    def setup_connections(self):
        """Setup signal connections."""
        self.load_button.clicked.connect(self.load_shift_report)
        self.print_button.clicked.connect(self.print_report)
        self.export_button.clicked.connect(self.export_report)
        self.close_button.clicked.connect(self.close)
    
    def load_shifts(self):
        """Load available shifts into the combo box."""
        try:
            shifts = self.db_manager.get_all_shifts()
            self.shift_combo.clear()
            
            for shift in shifts:
                shift_text = f"Shift #{shift['shift_id']} - {shift['username']} - {shift['open_time'].strftime('%Y-%m-%d %H:%M')}"
                self.shift_combo.addItem(shift_text, shift['shift_id'])
            
            if shifts:
                self.shift_combo.setCurrentIndex(0)
                self.load_shift_report()
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load shifts: {str(e)}")
    
    def load_shift_report(self):
        """Load the selected shift report."""
        try:
            shift_id = self.shift_combo.currentData()
            if not shift_id:
                return
            
            # Get shift details report
            report = self.shift_controller.get_shift_details_report(shift_id)
            if not report:
                QMessageBox.warning(self, "Error", "Failed to load shift report")
                return
            
            self.shift_data = report
            self.current_shift_id = shift_id
            
            # Update UI with report data
            self.update_overview_section(report['shift_details'])
            self.update_payment_section(report['sales_by_payment'])
            self.update_products_section(report['product_sales'])
            self.update_orders_section(report['orders'])
            
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load shift report: {str(e)}")
    
    def update_overview_section(self, shift_details: Dict[str, Any]):
        """Update the overview section with shift details."""
        self.shift_id_label.setText(f"Shift ID: {shift_details['shift_id']}")
        self.user_label.setText(f"User: {shift_details['username']}")
        self.open_time_label.setText(f"Open Time: {shift_details['open_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        if shift_details['close_time']:
            self.close_time_label.setText(f"Close Time: {shift_details['close_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            if shift_details['duration']:
                hours = int(shift_details['duration'].total_seconds() // 3600)
                minutes = int((shift_details['duration'].total_seconds() % 3600) // 60)
                self.duration_label.setText(f"Duration: {hours}h {minutes}m")
            else:
                self.duration_label.setText("Duration: -")
        else:
            self.close_time_label.setText("Close Time: -")
            self.duration_label.setText("Duration: -")
        
        self.opening_amount_label.setText(f"Opening Amount: ${shift_details['opening_amount']:.2f}")
        self.status_label.setText(f"Status: {shift_details['status'].title()}")
    
    def update_payment_section(self, sales_by_payment: list):
        """Update the payment section with sales data."""
        self.payment_table.setRowCount(len(sales_by_payment))
        
        for row, item in enumerate(sales_by_payment):
            # Payment method
            method_item = QTableWidgetItem(item['payment_method'])
            method_item.setTextAlignment(Qt.AlignCenter)
            self.payment_table.setItem(row, 0, method_item)
            
            # Total amount
            amount_item = QTableWidgetItem(f"${item['total_amount']:.2f}")
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.payment_table.setItem(row, 1, amount_item)
    
    def update_products_section(self, product_sales: list):
        """Update the products section with sales data."""
        self.products_table.setRowCount(len(product_sales))
        
        for row, item in enumerate(product_sales):
            # Product name
            name_item = QTableWidgetItem(item['product_name'])
            self.products_table.setItem(row, 0, name_item)
            
            # Quantity
            qty_item = QTableWidgetItem(str(item['quantity']))
            qty_item.setTextAlignment(Qt.AlignCenter)
            self.products_table.setItem(row, 1, qty_item)
            
            # Unit price
            price_item = QTableWidgetItem(f"${item['unit_price']:.2f}")
            price_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 2, price_item)
            
            # Total amount
            total_item = QTableWidgetItem(f"${item['total_amount']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.products_table.setItem(row, 3, total_item)
    
    def update_orders_section(self, orders: list):
        """Update the orders section with order data."""
        self.orders_table.setRowCount(len(orders))
        
        for row, order in enumerate(orders):
            # Order number
            order_num_item = QTableWidgetItem(order['order_number'])
            self.orders_table.setItem(row, 0, order_num_item)
            
            # Customer name
            customer_item = QTableWidgetItem(order['customer_name'])
            self.orders_table.setItem(row, 1, customer_item)
            
            # Status
            status_item = QTableWidgetItem(order['status'].title())
            status_item.setTextAlignment(Qt.AlignCenter)
            self.orders_table.setItem(row, 2, status_item)
            
            # Created time
            created_item = QTableWidgetItem(order['created_at'].strftime('%Y-%m-%d %H:%M'))
            created_item.setTextAlignment(Qt.AlignCenter)
            self.orders_table.setItem(row, 3, created_item)
            
            # Total amount
            total_item = QTableWidgetItem(f"${order['total_amount']:.2f}")
            total_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.orders_table.setItem(row, 4, total_item)
            
            # Subtotal
            subtotal_item = QTableWidgetItem(f"${order['subtotal']:.2f}")
            subtotal_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.orders_table.setItem(row, 5, subtotal_item)
    
    def print_report(self):
        """Print the current report."""
        QMessageBox.information(self, "Print", "Print functionality will be implemented in a future update.")
    
    def export_report(self):
        """Export the report to Excel."""
        QMessageBox.information(self, "Export", "Export functionality will be implemented in a future update.") 