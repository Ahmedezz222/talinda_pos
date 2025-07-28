from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, QMessageBox, QHeaderView, QWidget
from PyQt5.QtCore import Qt
from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController

class ShowProductsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('All Products')
        self.setMinimumSize(1000, 600)
        self.product_controller = ProductController()
        self.sale_controller = SaleController()
        self.products = []  # Store products for reference
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel('All Products')
        title.setStyleSheet('font-size: 22px; font-weight: bold; color: #273c75; margin-bottom: 10px;')
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(7)  # Removed stock column
        self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Price', 'Category', 'Barcode', 'Image Path', 'Actions'])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet('QTableWidget { alternate-background-color: #f0f6ff; }')
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set column widths
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Name column stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Description
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Price
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Barcode
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Image Path
        header.setSectionResizeMode(6, QHeaderView.Fixed)  # Actions column fixed width
        self.table.setColumnWidth(6, 100)  # Set actions column width
        
        self.load_products()
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.load_products)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """)
        
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)
        
        btn_layout.addWidget(refresh_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def load_products(self):
        self.products = self.product_controller.get_products(None)
        self.table.setRowCount(0)
        
        for product in self.products:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Add product data
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.description or ''))
            self.table.setItem(row, 2, QTableWidgetItem(f"${product.price:.2f}"))
            cat_name = product.category.name if product.category else 'No Category'
            self.table.setItem(row, 3, QTableWidgetItem(cat_name))
            self.table.setItem(row, 4, QTableWidgetItem(product.barcode or ''))
            self.table.setItem(row, 5, QTableWidgetItem(product.image_path or ''))
            
            # Create actions widget
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)
            
            # Check if product has sales
            sales_info = self.product_controller.get_product_sales_info(product.id)
            has_sales = sales_info['sales_count'] > 0
            
            # Add View Sales button if product has sales
            if has_sales:
                view_sales_btn = QPushButton('View Sales')
                view_sales_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #3498db;
                        color: white;
                        border: none;
                        padding: 4px 6px;
                        border-radius: 3px;
                        font-size: 10px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #2980b9;
                    }
                """)
                view_sales_btn.clicked.connect(lambda checked, pid=product.id, pname=product.name: self.view_product_sales(pid, pname))
                actions_layout.addWidget(view_sales_btn)
            
            # Add delete button
            delete_btn = QPushButton('Delete')
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #c0392b;
                }
                QPushButton:pressed {
                    background-color: #a93226;
                }
            """)
            delete_btn.clicked.connect(lambda checked, pid=product.id, pname=product.name: self.delete_product(pid, pname))
            actions_layout.addWidget(delete_btn)
            
            # If product has sales, disable delete button and show warning
            if has_sales:
                delete_btn.setEnabled(False)
                delete_btn.setToolTip(f"Cannot delete - used in {sales_info['sales_count']} sales")
                delete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #95a5a6;
                        color: white;
                        border: none;
                        padding: 4px 8px;
                        border-radius: 3px;
                        font-size: 11px;
                        font-weight: bold;
                    }
                """)
            
            actions_layout.addStretch()
            self.table.setCellWidget(row, 6, actions_widget)

    def delete_product(self, product_id: int, product_name: str):
        """Delete a product with confirmation dialog."""
        reply = QMessageBox.question(
            self, 
            'Confirm Deletion',
            f'Are you sure you want to delete the product "{product_name}"?\n\nThis action cannot be undone.',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                if self.product_controller.delete_product(product_id):
                    QMessageBox.information(
                        self,
                        'Success',
                        f'Product "{product_name}" has been deleted successfully.'
                    )
                    self.load_products()  # Refresh the table
                else:
                    QMessageBox.critical(
                        self,
                        'Error',
                        f'Failed to delete product "{product_name}". Please try again.'
                    )
            except ValueError as e:
                # Show detailed error message with sales information
                error_msg = str(e)
                
                # Get additional sales information if available
                try:
                    sales_info = self.product_controller.get_product_sales_info(product_id)
                    if sales_info['sales_count'] > 0:
                        error_msg += f"\n\nSales Details:\n"
                        error_msg += f"• Total sales containing this product: {sales_info['sales_count']}\n"
                        error_msg += f"• First few sales:\n"
                        for i, sale in enumerate(sales_info['sales_details'][:3]):  # Show first 3 sales
                            error_msg += f"  - Sale #{sale['sale_id']} (${sale['total_amount']:.2f}) - {sale['timestamp'].strftime('%Y-%m-%d %H:%M')}\n"
                        if sales_info['sales_count'] > 3:
                            error_msg += f"  ... and {sales_info['sales_count'] - 3} more sales\n"
                except Exception as sales_error:
                    # If we can't get sales info, just continue with the original error
                    pass
                
                QMessageBox.warning(
                    self,
                    'Cannot Delete Product',
                    error_msg
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error',
                    f'An unexpected error occurred while deleting "{product_name}":\n{str(e)}'
                )

    def view_product_sales(self, product_id: int, product_name: str):
        """Show sales information for a specific product."""
        try:
            sales_info = self.product_controller.get_product_sales_info(product_id)
            
            if sales_info['sales_count'] == 0:
                QMessageBox.information(
                    self,
                    'Sales Information',
                    f'Product "{product_name}" has no sales records.'
                )
                return
            
            # Create detailed sales information message
            msg = f"Sales Information for '{product_name}'\n\n"
            msg += f"Total sales containing this product: {sales_info['sales_count']}\n\n"
            msg += "Sales Details:\n"
            
            for i, sale in enumerate(sales_info['sales_details'][:10]):  # Show first 10 sales
                msg += f"{i+1}. Sale #{sale['sale_id']}\n"
                msg += f"   Date: {sale['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}\n"
                msg += f"   Quantity: {sale['quantity']}\n"
                msg += f"   Price at sale: ${sale['price_at_sale']:.2f}\n"
                msg += f"   Total sale amount: ${sale['total_amount']:.2f}\n\n"
            
            if sales_info['sales_count'] > 10:
                msg += f"... and {sales_info['sales_count'] - 10} more sales\n\n"
            
            msg += "Note: To delete this product, you must first delete all sales containing it using the product deletion interface."
            
            # Ask user if they want to delete all sales for this product
            reply = QMessageBox.question(
                self,
                'Product Sales Information',
                msg + "\n\nWould you like to delete all sales containing this product?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                self.delete_sales_for_product(product_id, product_name, sales_info)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Failed to retrieve sales information for "{product_name}":\n{str(e)}'
            )

    def delete_sales_for_product(self, product_id: int, product_name: str, sales_info: dict):
        """Delete all sales containing a specific product."""
        try:
            # Confirm deletion of all sales
            reply = QMessageBox.question(
                self,
                'Confirm Sales Deletion',
                f'Are you sure you want to delete ALL {sales_info["sales_count"]} sales containing "{product_name}"?\n\n'
                f'This will:\n'
                f'• Delete {sales_info["sales_count"]} sales records\n'
                f'• Restore stock for all products in those sales\n'
                f'• Allow you to delete the product afterward\n\n'
                f'This action cannot be undone!',
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            
            if reply == QMessageBox.Yes:
                # Delete each sale
                deleted_count = 0
                for sale in sales_info['sales_details']:
                    if self.sale_controller.delete_sale(sale['sale_id']):
                        deleted_count += 1
                    else:
                        QMessageBox.warning(
                            self,
                            'Partial Deletion',
                            f'Failed to delete some sales. {deleted_count} sales were deleted successfully.'
                        )
                        break
                
                if deleted_count == sales_info['sales_count']:
                    QMessageBox.information(
                        self,
                        'Success',
                        f'Successfully deleted all {deleted_count} sales containing "{product_name}".\n\n'
                        f'You can now delete the product if needed.'
                    )
                    # Refresh the products table
                    self.load_products()
                else:
                    QMessageBox.warning(
                        self,
                        'Partial Success',
                        f'Deleted {deleted_count} out of {sales_info["sales_count"]} sales.\n\n'
                        f'Some sales could not be deleted. Please try again.'
                    )
                    
        except Exception as e:
            QMessageBox.critical(
                self,
                'Error',
                f'Failed to delete sales for "{product_name}":\n{str(e)}'
            )