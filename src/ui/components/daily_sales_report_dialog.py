"""
Dialog for displaying daily sales reports.
"""
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QTableWidget, QTableWidgetItem, QTabWidget, QWidget,
    QGroupBox, QGridLayout, QScrollArea, QFrame, QSplitter,
    QHeaderView, QTextEdit, QDateEdit, QCalendarWidget
)
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QFont, QColor, QPalette
from datetime import date, datetime
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class DailySalesReportDialog(QDialog):
    def __init__(self, parent=None, report_data: Optional[Dict[str, Any]] = None):
        super().__init__(parent)
        self.setWindowTitle('Daily Sales Report')
        self.setMinimumSize(1000, 700)  # Increased size for new tab
        self.report_data = report_data or {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        
        # Date selector
        date_label = QLabel("Report Date:")
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.dateChanged.connect(self.on_date_changed)
        
        header_layout.addWidget(date_label)
        header_layout.addWidget(self.date_edit)
        header_layout.addStretch()
        
        # Refresh button
        self.refresh_btn = QPushButton("Refresh Report")
        self.refresh_btn.clicked.connect(self.refresh_report)
        header_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Create tab widget for different sections
        self.tab_widget = QTabWidget()
        
        # Summary tab
        self.summary_tab = self.create_summary_tab()
        self.tab_widget.addTab(self.summary_tab, "Summary")
        
        # Product Details tab (NEW)
        self.product_details_tab = self.create_product_details_tab()
        self.tab_widget.addTab(self.product_details_tab, "Product Details")
        
        # Sale Details tab (NEW)
        self.sale_details_tab = self.create_sale_details_tab()
        self.tab_widget.addTab(self.sale_details_tab, "Sale Details")
        
        # Sales by Hour tab
        self.hourly_tab = self.create_hourly_tab()
        self.tab_widget.addTab(self.hourly_tab, "Sales by Hour")
        
        # Orders by Hour tab
        self.orders_hourly_tab = self.create_orders_hourly_tab()
        self.tab_widget.addTab(self.orders_hourly_tab, "Orders by Hour")
        
        # Combined Hourly tab
        self.combined_hourly_tab = self.create_combined_hourly_tab()
        self.tab_widget.addTab(self.combined_hourly_tab, "Combined Hourly")
        
        # Shifts tab
        self.shifts_tab = self.create_shifts_tab()
        self.tab_widget.addTab(self.shifts_tab, "Shifts")
        
        layout.addWidget(self.tab_widget)
        
        # Close button
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.close_btn = QPushButton("Close")
        self.close_btn.clicked.connect(self.accept)
        button_layout.addWidget(self.close_btn)
        
        layout.addLayout(button_layout)
        
        # Load initial data
        self.load_report_data()

    def create_summary_tab(self) -> QWidget:
        """Create the summary tab with key metrics."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Key metrics group
        metrics_group = QGroupBox("Daily Summary")
        metrics_layout = QGridLayout(metrics_group)
        
        # Create metric labels
        self.total_sales_label = QLabel("0")
        self.total_orders_label = QLabel("0")
        self.total_transactions_label = QLabel("0")
        self.total_amount_label = QLabel("$0.00")
        self.average_transaction_label = QLabel("$0.00")
        
        # Style the metric labels
        metric_font = QFont()
        metric_font.setPointSize(18)
        metric_font.setBold(True)
        
        self.total_sales_label.setFont(metric_font)
        self.total_orders_label.setFont(metric_font)
        self.total_transactions_label.setFont(metric_font)
        self.total_amount_label.setFont(metric_font)
        self.average_transaction_label.setFont(metric_font)
        
        # Add to layout
        metrics_layout.addWidget(QLabel("Total Sales:"), 0, 0)
        metrics_layout.addWidget(self.total_sales_label, 0, 1)
        
        metrics_layout.addWidget(QLabel("Total Orders:"), 1, 0)
        metrics_layout.addWidget(self.total_orders_label, 1, 1)
        
        metrics_layout.addWidget(QLabel("Total Transactions:"), 2, 0)
        metrics_layout.addWidget(self.total_transactions_label, 2, 1)
        
        metrics_layout.addWidget(QLabel("Total Amount:"), 3, 0)
        metrics_layout.addWidget(self.total_amount_label, 3, 1)
        
        metrics_layout.addWidget(QLabel("Average Transaction:"), 4, 0)
        metrics_layout.addWidget(self.average_transaction_label, 4, 1)
        
        layout.addWidget(metrics_group)
        
        # Order status breakdown
        order_status_group = QGroupBox("Order Status Breakdown")
        order_status_layout = QGridLayout(order_status_group)
        
        self.active_orders_label = QLabel("0")
        self.completed_orders_label = QLabel("0")
        self.cancelled_orders_label = QLabel("0")
        
        # Style the order status labels
        status_font = QFont()
        status_font.setPointSize(14)
        status_font.setBold(True)
        
        self.active_orders_label.setFont(status_font)
        self.completed_orders_label.setFont(status_font)
        self.cancelled_orders_label.setFont(status_font)
        
        # Color code the status labels
        self.active_orders_label.setStyleSheet("color: #3498db;")
        self.completed_orders_label.setStyleSheet("color: #27ae60;")
        self.cancelled_orders_label.setStyleSheet("color: #e74c3c;")
        
        order_status_layout.addWidget(QLabel("Active Orders:"), 0, 0)
        order_status_layout.addWidget(self.active_orders_label, 0, 1)
        
        order_status_layout.addWidget(QLabel("Completed Orders:"), 1, 0)
        order_status_layout.addWidget(self.completed_orders_label, 1, 1)
        
        order_status_layout.addWidget(QLabel("Cancelled Orders:"), 2, 0)
        order_status_layout.addWidget(self.cancelled_orders_label, 2, 1)
        
        layout.addWidget(order_status_group)
        
        # Report date
        date_group = QGroupBox("Report Information")
        date_layout = QGridLayout(date_group)
        
        self.report_date_label = QLabel("")
        date_layout.addWidget(QLabel("Report Date:"), 0, 0)
        date_layout.addWidget(self.report_date_label, 0, 1)
        
        layout.addWidget(date_group)
        
        # Product Summary group (NEW)
        product_summary_group = QGroupBox("Product Summary")
        product_summary_layout = QGridLayout(product_summary_group)
        
        # Create product summary labels
        self.total_products_sold_summary_label = QLabel("0")
        self.total_quantity_sold_summary_label = QLabel("0")
        self.top_product_summary_label = QLabel("None")
        
        # Style the product summary labels
        product_summary_font = QFont()
        product_summary_font.setPointSize(14)
        product_summary_font.setBold(True)
        
        self.total_products_sold_summary_label.setFont(product_summary_font)
        self.total_quantity_sold_summary_label.setFont(product_summary_font)
        self.top_product_summary_label.setFont(product_summary_font)
        
        # Color code the product summary labels
        self.total_products_sold_summary_label.setStyleSheet("color: #27ae60;")
        self.total_quantity_sold_summary_label.setStyleSheet("color: #3498db;")
        self.top_product_summary_label.setStyleSheet("color: #e67e22;")
        
        product_summary_layout.addWidget(QLabel("Total Products Sold:"), 0, 0)
        product_summary_layout.addWidget(self.total_products_sold_summary_label, 0, 1)
        
        product_summary_layout.addWidget(QLabel("Total Quantity Sold:"), 1, 0)
        product_summary_layout.addWidget(self.total_quantity_sold_summary_label, 1, 1)
        
        product_summary_layout.addWidget(QLabel("Top Selling Product:"), 2, 0)
        product_summary_layout.addWidget(self.top_product_summary_label, 2, 1)
        
        layout.addWidget(product_summary_group)
        
        layout.addStretch()
        return widget

    def create_product_details_tab(self) -> QWidget:
        """Create the product details tab showing quantity and product information."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Product sales summary group
        summary_group = QGroupBox("Product Sales Summary")
        summary_layout = QGridLayout(summary_group)
        
        # Create summary labels
        self.total_products_sold_label = QLabel("0")
        self.total_quantity_sold_label = QLabel("0")
        self.top_product_label = QLabel("None")
        self.top_product_quantity_label = QLabel("0")
        
        # Style the summary labels
        summary_font = QFont()
        summary_font.setPointSize(14)
        summary_font.setBold(True)
        
        self.total_products_sold_label.setFont(summary_font)
        self.total_quantity_sold_label.setFont(summary_font)
        self.top_product_label.setFont(summary_font)
        self.top_product_quantity_label.setFont(summary_font)
        
        # Color code the labels
        self.total_products_sold_label.setStyleSheet("color: #27ae60;")
        self.total_quantity_sold_label.setStyleSheet("color: #3498db;")
        self.top_product_label.setStyleSheet("color: #e67e22;")
        self.top_product_quantity_label.setStyleSheet("color: #e67e22;")
        
        # Add to layout
        summary_layout.addWidget(QLabel("Total Products Sold:"), 0, 0)
        summary_layout.addWidget(self.total_products_sold_label, 0, 1)
        
        summary_layout.addWidget(QLabel("Total Quantity Sold:"), 1, 0)
        summary_layout.addWidget(self.total_quantity_sold_label, 1, 1)
        
        summary_layout.addWidget(QLabel("Top Selling Product:"), 2, 0)
        summary_layout.addWidget(self.top_product_label, 2, 1)
        
        summary_layout.addWidget(QLabel("Top Product Quantity:"), 3, 0)
        summary_layout.addWidget(self.top_product_quantity_label, 3, 1)
        
        layout.addWidget(summary_group)
        
        # Product details table
        self.product_details_table = QTableWidget()
        self.product_details_table.setColumnCount(7)
        self.product_details_table.setHorizontalHeaderLabels([
            "Product Name", "Category", "Quantity Sold", "Unit Price", "Total Amount", "Sales Count", "Avg per Sale"
        ])
        
        # Set table properties
        header = self.product_details_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Style the table
        self.product_details_table.setAlternatingRowColors(True)
        self.product_details_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #1976d2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.product_details_table)
        
        return widget

    def create_sale_details_tab(self) -> QWidget:
        """Create the sale details tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Sale details table
        self.sale_details_table = QTableWidget()
        self.sale_details_table.setColumnCount(8)
        self.sale_details_table.setHorizontalHeaderLabels([
            "Sale ID", "Date", "Time", "Cashier", "Product", "Quantity", "Unit Price", "Total Amount"
        ])
        
        # Set table properties
        header = self.sale_details_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        # Style the table
        self.sale_details_table.setAlternatingRowColors(True)
        self.sale_details_table.setStyleSheet("""
            QTableWidget {
                gridline-color: #e0e0e0;
                background-color: white;
                alternate-background-color: #f8f9fa;
            }
            QHeaderView::section {
                background-color: #1976d2;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        """)
        
        layout.addWidget(self.sale_details_table)
        return widget

    def create_hourly_tab(self) -> QWidget:
        """Create the hourly sales tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Hourly sales table
        self.hourly_table = QTableWidget()
        self.hourly_table.setColumnCount(4)
        self.hourly_table.setHorizontalHeaderLabels([
            "Hour", "Sales Count", "Total Amount", "Average"
        ])
        
        # Set table properties
        header = self.hourly_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.hourly_table)
        return widget

    def create_orders_hourly_tab(self) -> QWidget:
        """Create the hourly orders tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Hourly orders table
        self.orders_hourly_table = QTableWidget()
        self.orders_hourly_table.setColumnCount(4)
        self.orders_hourly_table.setHorizontalHeaderLabels([
            "Hour", "Orders Count", "Total Amount", "Average"
        ])
        
        # Set table properties
        header = self.orders_hourly_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.orders_hourly_table)
        return widget

    def create_combined_hourly_tab(self) -> QWidget:
        """Create the combined hourly tab showing both sales and orders."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Combined hourly table
        self.combined_hourly_table = QTableWidget()
        self.combined_hourly_table.setColumnCount(7)
        self.combined_hourly_table.setHorizontalHeaderLabels([
            "Hour", "Sales Count", "Sales Amount", "Orders Count", "Orders Amount", "Total Count", "Total Amount"
        ])
        
        # Set table properties
        header = self.combined_hourly_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.combined_hourly_table)
        return widget

    def create_shifts_tab(self) -> QWidget:
        """Create the shifts tab."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Shifts table
        self.shifts_table = QTableWidget()
        self.shifts_table.setColumnCount(6)
        self.shifts_table.setHorizontalHeaderLabels([
            "Cashier", "Opening Amount", "Open Time", 
            "Close Time", "Duration", "Status"
        ])
        
        # Set table properties
        header = self.shifts_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        
        layout.addWidget(self.shifts_table)
        return widget

    def load_report_data(self):
        """Load and display the report data."""
        try:
            # Update summary
            total_sales = self.report_data.get('total_sales', 0)
            total_orders = self.report_data.get('total_orders', 0)
            total_transactions = self.report_data.get('total_transactions', 0)
            total_amount = self.report_data.get('total_amount', 0.0)
            average_transaction = self.report_data.get('average_transaction', 0.0)
            report_date = self.report_data.get('date', date.today().isoformat())
            
            # Order status breakdown
            order_status_breakdown = self.report_data.get('order_status_breakdown', {})
            active_orders = order_status_breakdown.get('active', 0)
            completed_orders = order_status_breakdown.get('completed', 0)
            cancelled_orders = order_status_breakdown.get('cancelled', 0)
            
            self.total_sales_label.setText(str(total_sales))
            self.total_orders_label.setText(str(total_orders))
            self.total_transactions_label.setText(str(total_transactions))
            self.total_amount_label.setText(f"${total_amount:.2f}")
            self.average_transaction_label.setText(f"${average_transaction:.2f}")
            self.report_date_label.setText(report_date)
            
            # Update order status breakdown
            self.active_orders_label.setText(str(active_orders))
            self.completed_orders_label.setText(str(completed_orders))
            self.cancelled_orders_label.setText(str(cancelled_orders))
            
            # Update product summary
            product_sales_summary = self.report_data.get('product_sales_summary', {})
            self.total_products_sold_summary_label.setText(str(product_sales_summary.get('total_products_sold', 0)))
            self.total_quantity_sold_summary_label.setText(str(product_sales_summary.get('total_quantity_sold', 0)))
            self.top_product_summary_label.setText(product_sales_summary.get('top_product_name', 'None'))
            
            # Update product details
            self.update_product_details_summary()
            self.update_product_details_table()

            # Update sale details
            self.update_sale_details_table()

            # Update tables
            self.update_hourly_table()
            self.update_orders_hourly_table()
            self.update_combined_hourly_table()
            self.update_shifts_table()
            
        except Exception as e:
            logger.error(f"Error loading report data: {e}")

    def update_product_details_summary(self):
        """Update the product sales summary labels."""
        product_sales_summary = self.report_data.get('product_sales_summary', {})
        self.total_products_sold_label.setText(str(product_sales_summary.get('total_products_sold', 0)))
        self.total_quantity_sold_label.setText(str(product_sales_summary.get('total_quantity_sold', 0)))
        self.top_product_label.setText(product_sales_summary.get('top_product_name', 'None'))
        self.top_product_quantity_label.setText(str(product_sales_summary.get('top_product_quantity', 0)))

    def update_product_details_table(self):
        """Update the product details table."""
        product_details = self.report_data.get('product_details', [])
        
        # Clear existing data
        self.product_details_table.setRowCount(0)
        
        for item in product_details:
            row = self.product_details_table.rowCount()
            self.product_details_table.insertRow(row)
            
            # Product Name
            name_item = QTableWidgetItem(item.get('product_name', 'N/A'))
            self.product_details_table.setItem(row, 0, name_item)
            
            # Category
            category_item = QTableWidgetItem(item.get('category', 'N/A'))
            self.product_details_table.setItem(row, 1, category_item)
            
            # Quantity Sold
            quantity_item = QTableWidgetItem(str(item.get('quantity_sold', 0)))
            self.product_details_table.setItem(row, 2, quantity_item)
            
            # Unit Price
            unit_price_item = QTableWidgetItem(f"${item.get('unit_price', 0):.2f}")
            self.product_details_table.setItem(row, 3, unit_price_item)
            
            # Total Amount
            total_amount_item = QTableWidgetItem(f"${item.get('total_amount', 0):.2f}")
            self.product_details_table.setItem(row, 4, total_amount_item)
            
            # Sales Count
            sales_count_item = QTableWidgetItem(str(item.get('sales_count', 0)))
            self.product_details_table.setItem(row, 5, sales_count_item)
            
            # Average per Sale
            avg_item = QTableWidgetItem(f"${item.get('average_per_sale', 0):.2f}")
            self.product_details_table.setItem(row, 6, avg_item)
            
            # Color code rows
            if item.get('quantity_sold', 0) > 0:
                for col in range(7):
                    item = self.product_details_table.item(row, col)
                    if item:
                        item.setBackground(QColor(240, 248, 255))  # Light blue

    def update_sale_details_table(self):
        """Update the sale details table."""
        sale_details = self.report_data.get('sale_details', [])
        
        # Clear existing data
        self.sale_details_table.setRowCount(0)
        
        for item in sale_details:
            row = self.sale_details_table.rowCount()
            self.sale_details_table.insertRow(row)
            
            # Sale ID
            sale_id_item = QTableWidgetItem(str(item.get('sale_id', 'N/A')))
            self.sale_details_table.setItem(row, 0, sale_id_item)
            
            # Date
            date_item = QTableWidgetItem(item.get('date', 'N/A'))
            self.sale_details_table.setItem(row, 1, date_item)
            
            # Time
            time_item = QTableWidgetItem(item.get('time', 'N/A'))
            self.sale_details_table.setItem(row, 2, time_item)
            
            # Cashier
            cashier_item = QTableWidgetItem(item.get('cashier', 'N/A'))
            self.sale_details_table.setItem(row, 3, cashier_item)
            
            # Product
            product_item = QTableWidgetItem(item.get('product_name', 'N/A'))
            self.sale_details_table.setItem(row, 4, product_item)
            
            # Quantity
            quantity_item = QTableWidgetItem(str(item.get('quantity', 0)))
            self.sale_details_table.setItem(row, 5, quantity_item)
            
            # Unit Price
            unit_price_item = QTableWidgetItem(f"${item.get('unit_price', 0):.2f}")
            self.sale_details_table.setItem(row, 6, unit_price_item)
            
            # Total Amount
            total_amount_item = QTableWidgetItem(f"${item.get('total_amount', 0):.2f}")
            self.sale_details_table.setItem(row, 7, total_amount_item)
            
            # Color code rows
            if item.get('quantity', 0) > 0:
                for col in range(8):
                    item = self.sale_details_table.item(row, col)
                    if item:
                        item.setBackground(QColor(240, 248, 255))  # Light blue

    def update_hourly_table(self):
        """Update the hourly sales table."""
        hourly_sales = self.report_data.get('hourly_sales', {})
        
        # Clear existing data
        self.hourly_table.setRowCount(0)
        
        # Add data for each hour (0-23)
        for hour in range(24):
            hour_data = hourly_sales.get(hour, {'count': 0, 'amount': 0.0})
            
            row = self.hourly_table.rowCount()
            self.hourly_table.insertRow(row)
            
            # Hour
            hour_item = QTableWidgetItem(f"{hour:02d}:00")
            self.hourly_table.setItem(row, 0, hour_item)
            
            # Sales count
            count_item = QTableWidgetItem(str(hour_data['count']))
            self.hourly_table.setItem(row, 1, count_item)
            
            # Total amount
            amount_item = QTableWidgetItem(f"${hour_data['amount']:.2f}")
            self.hourly_table.setItem(row, 2, amount_item)
            
            # Average
            avg = hour_data['amount'] / hour_data['count'] if hour_data['count'] > 0 else 0
            avg_item = QTableWidgetItem(f"${avg:.2f}")
            self.hourly_table.setItem(row, 3, avg_item)
            
            # Color code rows with sales
            if hour_data['count'] > 0:
                for col in range(4):
                    item = self.hourly_table.item(row, col)
                    if item:
                        item.setBackground(QColor(240, 248, 255))  # Light blue

    def update_orders_hourly_table(self):
        """Update the hourly orders table."""
        hourly_orders = self.report_data.get('hourly_orders', {})
        
        # Clear existing data
        self.orders_hourly_table.setRowCount(0)
        
        # Add data for each hour (0-23)
        for hour in range(24):
            hour_data = hourly_orders.get(hour, {'count': 0, 'amount': 0.0})
            
            row = self.orders_hourly_table.rowCount()
            self.orders_hourly_table.insertRow(row)
            
            # Hour
            hour_item = QTableWidgetItem(f"{hour:02d}:00")
            self.orders_hourly_table.setItem(row, 0, hour_item)
            
            # Orders count
            count_item = QTableWidgetItem(str(hour_data['count']))
            self.orders_hourly_table.setItem(row, 1, count_item)
            
            # Total amount
            amount_item = QTableWidgetItem(f"${hour_data['amount']:.2f}")
            self.orders_hourly_table.setItem(row, 2, amount_item)
            
            # Average
            avg = hour_data['amount'] / hour_data['count'] if hour_data['count'] > 0 else 0
            avg_item = QTableWidgetItem(f"${avg:.2f}")
            self.orders_hourly_table.setItem(row, 3, avg_item)
            
            # Color code rows with orders
            if hour_data['count'] > 0:
                for col in range(4):
                    item = self.orders_hourly_table.item(row, col)
                    if item:
                        item.setBackground(QColor(255, 248, 220))  # Light yellow

    def update_combined_hourly_table(self):
        """Update the combined hourly table showing both sales and orders."""
        hourly_combined = self.report_data.get('hourly_combined', {})
        
        # Clear existing data
        self.combined_hourly_table.setRowCount(0)
        
        # Add data for each hour (0-23)
        for hour in range(24):
            hour_data = hourly_combined.get(hour, {
                'sales_count': 0, 'sales_amount': 0.0,
                'orders_count': 0, 'orders_amount': 0.0,
                'total_count': 0, 'total_amount': 0.0
            })
            
            row = self.combined_hourly_table.rowCount()
            self.combined_hourly_table.insertRow(row)
            
            # Hour
            hour_item = QTableWidgetItem(f"{hour:02d}:00")
            self.combined_hourly_table.setItem(row, 0, hour_item)
            
            # Sales count
            sales_count_item = QTableWidgetItem(str(hour_data['sales_count']))
            self.combined_hourly_table.setItem(row, 1, sales_count_item)
            
            # Sales amount
            sales_amount_item = QTableWidgetItem(f"${hour_data['sales_amount']:.2f}")
            self.combined_hourly_table.setItem(row, 2, sales_amount_item)
            
            # Orders count
            orders_count_item = QTableWidgetItem(str(hour_data['orders_count']))
            self.combined_hourly_table.setItem(row, 3, orders_count_item)
            
            # Orders amount
            orders_amount_item = QTableWidgetItem(f"${hour_data['orders_amount']:.2f}")
            self.combined_hourly_table.setItem(row, 4, orders_amount_item)
            
            # Total count
            total_count_item = QTableWidgetItem(str(hour_data['total_count']))
            self.combined_hourly_table.setItem(row, 5, total_count_item)
            
            # Total amount
            total_amount_item = QTableWidgetItem(f"${hour_data['total_amount']:.2f}")
            self.combined_hourly_table.setItem(row, 6, total_amount_item)
            
            # Color code rows with activity
            if hour_data['total_count'] > 0:
                for col in range(7):
                    item = self.combined_hourly_table.item(row, col)
                    if item:
                        if hour_data['sales_count'] > 0 and hour_data['orders_count'] > 0:
                            item.setBackground(QColor(220, 255, 220))  # Light green (both)
                        elif hour_data['sales_count'] > 0:
                            item.setBackground(QColor(240, 248, 255))  # Light blue (sales only)
                        elif hour_data['orders_count'] > 0:
                            item.setBackground(QColor(255, 248, 220))  # Light yellow (orders only)

    def update_shifts_table(self):
        """Update the shifts table."""
        shifts = self.report_data.get('shifts', [])
        
        # Clear existing data
        self.shifts_table.setRowCount(0)
        
        for shift in shifts:
            row = self.shifts_table.rowCount()
            self.shifts_table.insertRow(row)
            
            # Cashier
            cashier_item = QTableWidgetItem(shift.get('user', 'Unknown'))
            self.shifts_table.setItem(row, 0, cashier_item)
            
            # Opening amount
            opening_item = QTableWidgetItem(f"${shift.get('opening_amount', 0):.2f}")
            self.shifts_table.setItem(row, 1, opening_item)
            
            # Open time
            open_time = shift.get('open_time')
            open_time_str = open_time.strftime("%H:%M:%S") if open_time else "N/A"
            open_item = QTableWidgetItem(open_time_str)
            self.shifts_table.setItem(row, 2, open_item)
            
            # Close time
            close_time = shift.get('close_time')
            close_time_str = close_time.strftime("%H:%M:%S") if close_time else "N/A"
            close_item = QTableWidgetItem(close_time_str)
            self.shifts_table.setItem(row, 3, close_item)
            
            # Duration
            duration_item = QTableWidgetItem(shift.get('duration', 'N/A'))
            self.shifts_table.setItem(row, 4, duration_item)
            
            # Status
            status_item = QTableWidgetItem(shift.get('status', 'Unknown'))
            self.shifts_table.setItem(row, 5, status_item)
            
            # Color code based on status
            status = shift.get('status', '')
            if status == 'closed':
                for col in range(6):
                    item = self.shifts_table.item(row, col)
                    if item:
                        item.setBackground(QColor(240, 255, 240))  # Light green
            elif status == 'open':
                for col in range(6):
                    item = self.shifts_table.item(row, col)
                    if item:
                        item.setBackground(QColor(255, 248, 220))  # Light yellow

    def on_date_changed(self, qdate):
        """Handle date change."""
        # This would typically trigger a new report generation
        # For now, we'll just update the display
        pass

    def refresh_report(self):
        """Refresh the report data."""
        # This would typically fetch new data from the controller
        # For now, we'll just reload the current data
        self.load_report_data()

    def set_report_data(self, report_data: Dict[str, Any]):
        """Set new report data and refresh display."""
        self.report_data = report_data
        self.load_report_data() 