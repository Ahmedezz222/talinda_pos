"""
Simple Sale Report Dialog - Simplified version for basic sales reporting.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QGroupBox, QGridLayout,
    QDateEdit, QHeaderView
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor
from datetime import date, datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class SimpleSaleReportDialog(QDialog):
    def __init__(self, parent=None, report_data: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.setWindowTitle('Simple Sale Report')
        self.setMinimumSize(800, 600)
        self.report_data = report_data or {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Header with date selector
        header_layout = QHBoxLayout()
        
        date_label = QLabel("Report Date:")
        date_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        self.date_edit.setStyleSheet("""
            QDateEdit {
                padding: 8px;
                border: 2px solid #3498db;
                border-radius: 5px;
                font-size: 14px;
            }
        """)
        
        header_layout.addWidget(date_label)
        header_layout.addWidget(self.date_edit)
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("🔄 Refresh")
        self.refresh_btn.clicked.connect(self.refresh_report)
        self.refresh_btn.setStyleSheet("""
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
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Summary section
        summary_group = self.create_summary_section()
        layout.addWidget(summary_group)
        
        # Sales table
        sales_group = self.create_sales_table_section()
        layout.addWidget(sales_group)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                padding: 10px 30px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Load initial data
        self.generate_report_for_date(self.date_edit.date().toPyDate())

    def create_summary_section(self) -> QGroupBox:
        """Create the summary section with key metrics."""
        group = QGroupBox("Daily Summary")
        group.setStyleSheet("""
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
        
        layout = QGridLayout(group)
        layout.setSpacing(15)
        
        # Create metric labels with styling
        self.total_sales_label = self.create_metric_label("0")
        self.total_amount_label = self.create_metric_label("$0.00")
        self.average_sale_label = self.create_metric_label("$0.00")
        
        # Add metrics to layout
        layout.addWidget(QLabel("Total Sales:"), 0, 0)
        layout.addWidget(self.total_sales_label, 0, 1)
        
        layout.addWidget(QLabel("Total Amount:"), 1, 0)
        layout.addWidget(self.total_amount_label, 1, 1)
        
        layout.addWidget(QLabel("Average Sale:"), 2, 0)
        layout.addWidget(self.average_sale_label, 2, 1)
        
        return group

    def create_metric_label(self, text: str) -> QLabel:
        """Create a styled metric label."""
        label = QLabel(text)
        label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            padding: 10px;
            background-color: #ecf0f1;
            border-radius: 5px;
            border: 1px solid #bdc3c7;
        """)
        return label

    def create_sales_table_section(self) -> QGroupBox:
        """Create the sales table section."""
        group = QGroupBox("Sales Details")
        group.setStyleSheet("""
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
        
        layout = QVBoxLayout(group)
        
        # Create sales table
        self.sales_table = QTableWidget()
        self.sales_table.setColumnCount(6)
        self.sales_table.setHorizontalHeaderLabels([
            "Time", "Cashier", "Products", "Quantity", "Total Amount", "Notes"
        ])
        
        # Set table properties
        header = self.sales_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Style the table
        self.sales_table.setAlternatingRowColors(True)
        self.sales_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #bdc3c7;
                background-color: white;
                alternate-background-color: #f8f9fa;
                border: 1px solid #bdc3c7;
                border-radius: 5px;
            }
            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 10px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #ecf0f1;
            }
        """)
        
        layout.addWidget(self.sales_table)
        
        return group

    def load_report_data(self):
        """Load and display the report data."""
        try:
            # Update summary metrics
            total_sales = self.report_data.get('total_sales', 0)
            total_amount = self.report_data.get('total_amount', 0.0)
            average_sale = self.report_data.get('average_transaction', 0.0)
            
            self.total_sales_label.setText(str(total_sales))
            self.total_amount_label.setText(f"${total_amount:.2f}")
            self.average_sale_label.setText(f"${average_sale:.2f}")
            
            # Update sales table
            self.update_sales_table()
            
        except Exception as e:
            logger.error(f"Error loading report data: {e}")

    def update_sales_table(self):
        """Update the sales table with data."""
        sale_details = self.report_data.get('sale_details', [])
        
        # Clear existing data
        self.sales_table.setRowCount(0)
        
        for item in sale_details:
            row = self.sales_table.rowCount()
            self.sales_table.insertRow(row)
            
            # Time
            time_str = item.get('time', 'N/A')
            time_item = QTableWidgetItem(time_str)
            self.sales_table.setItem(row, 0, time_item)
            
            # Cashier
            cashier_item = QTableWidgetItem(item.get('cashier', 'N/A'))
            self.sales_table.setItem(row, 1, cashier_item)
            
            # Products (simplified - just show product name)
            product_item = QTableWidgetItem(item.get('product_name', 'N/A'))
            self.sales_table.setItem(row, 2, product_item)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(item.get('quantity', 0)))
            self.sales_table.setItem(row, 3, quantity_item)
            
            # Total Amount
            total_amount_item = QTableWidgetItem(f"${item.get('total_amount', 0):.2f}")
            self.sales_table.setItem(row, 4, total_amount_item)
            
            # Notes (simplified)
            notes = item.get('item_notes', '') or item.get('order_notes', '')
            notes_item = QTableWidgetItem(notes[:50] + "..." if len(notes) > 50 else notes)
            self.sales_table.setItem(row, 5, notes_item)
            
            # Color code rows based on transaction type
            if item.get('transaction_type') == 'Completed Order':
                for col in range(6):
                    item = self.sales_table.item(row, col)
                    if item:
                        item.setBackground(QColor(255, 248, 220))  # Light yellow for orders
            else:
                for col in range(6):
                    item = self.sales_table.item(row, col)
                    if item:
                        item.setBackground(QColor(240, 248, 255))  # Light blue for sales

    def on_date_changed(self, qdate):
        """Handle date change."""
        try:
            selected_date = qdate.toPyDate()
            self.generate_report_for_date(selected_date)
        except Exception as e:
            logger.error(f"Error handling date change: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Failed to load report for selected date: {str(e)}")

    def refresh_report(self):
        """Refresh the report data."""
        try:
            selected_date = self.date_edit.date().toPyDate()
            self.generate_report_for_date(selected_date)
        except Exception as e:
            logger.error(f"Error refreshing report: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Failed to refresh report: {str(e)}")

    def generate_report_for_date(self, report_date):
        """Generate report data for a specific date."""
        try:
            # Show loading state
            self.refresh_btn.setEnabled(False)
            self.refresh_btn.setText("⏳ Loading...")
            self.date_edit.setEnabled(False)
            
            # Process events to update UI
            from PyQt5.QtCore import QCoreApplication
            QCoreApplication.processEvents()
            
            # Import the shift controller
            from controllers.shift_controller import ShiftController
            
            # Create shift controller instance
            shift_controller = ShiftController()
            
            # Get report data for the selected date
            new_report_data = shift_controller.get_daily_sales_report(report_date)
            
            # Update the report data and refresh display
            self.set_report_data(new_report_data)
            
            logger.info(f"Simple report generated successfully for date: {report_date}")
            
        except Exception as e:
            logger.error(f"Error generating simple report for date {report_date}: {e}")
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.warning(self, "Error", f"Failed to load report: {str(e)}")
        finally:
            # Restore UI state
            self.refresh_btn.setEnabled(True)
            self.refresh_btn.setText("🔄 Refresh")
            self.date_edit.setEnabled(True)

    def set_report_data(self, report_data: Dict[str, Any]):
        """Set new report data and refresh display."""
        self.report_data = report_data
        self.load_report_data() 