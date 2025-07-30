from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, QMessageBox, QHeaderView, QWidget, QLineEdit, QTextEdit, QDoubleSpinBox, QComboBox, QFormLayout
from PyQt5.QtCore import Qt
from controllers.product_controller import ProductController
from controllers.sale_controller import SaleController

class ProductEditDialog(QDialog):
    """Dialog for editing product details."""
    
    def __init__(self, product, parent=None):
        super().__init__(parent)
        self.product = product
        self.product_controller = ProductController()
        self.setWindowTitle(f"Edit Product - {product.name}")
        self.setFixedSize(600, 500)  # Increased size for better usability
        self.setMinimumSize(500, 400)  # Set minimum size
        self.init_ui()
        self.load_product_data()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)  # Increased margins
        
        # Title
        title = QLabel(f"Edit Product: {self.product.name}")
        title.setStyleSheet("font-size: 20px; font-weight: bold; color: #2c3e50; margin-bottom: 20px;")
        layout.addWidget(title)
        
        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(20)  # Increased spacing between form elements
        form_layout.setLabelAlignment(Qt.AlignRight)
        
        # Style for form labels
        label_style = """
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #2c3e50;
                padding: 8px 0px;
            }
        """
        
        # Product name
        name_label = QLabel("Product Name:")
        name_label.setStyleSheet(label_style)
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter product name")
        self.name_input.setMinimumHeight(40)  # Increased height
        self.name_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(name_label, self.name_input)
        
        # Description
        desc_label = QLabel("Description:")
        desc_label.setStyleSheet(label_style)
        self.description_input = QTextEdit()
        self.description_input.setMaximumHeight(100)  # Increased height
        self.description_input.setPlaceholderText("Enter product description")
        self.description_input.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(desc_label, self.description_input)
        
        # Price
        price_label = QLabel("Price:")
        price_label.setStyleSheet(label_style)
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0.01, 9999.99)
        self.price_input.setDecimals(2)
        self.price_input.setPrefix("$")
        self.price_input.setMinimumHeight(40)  # Increased height
        self.price_input.setStyleSheet("""
            QDoubleSpinBox {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QDoubleSpinBox:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(price_label, self.price_input)
        
        # Category
        cat_label = QLabel("Category:")
        cat_label.setStyleSheet(label_style)
        self.category_combo = QComboBox()
        self.category_combo.setMinimumHeight(40)  # Increased height
        self.category_combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QComboBox:focus {
                border-color: #3498db;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 10px;
            }
        """)
        self.load_categories()
        form_layout.addRow(cat_label, self.category_combo)
        
        # Barcode
        barcode_label = QLabel("Barcode:")
        barcode_label.setStyleSheet(label_style)
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText("Enter barcode (optional)")
        self.barcode_input.setMinimumHeight(40)  # Increased height
        self.barcode_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(barcode_label, self.barcode_input)
        
        # Image path
        image_label = QLabel("Image Path:")
        image_label.setStyleSheet(label_style)
        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("Enter image path (optional)")
        self.image_path_input.setMinimumHeight(40)  # Increased height
        self.image_path_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #3498db;
            }
        """)
        form_layout.addRow(image_label, self.image_path_input)
        
        layout.addLayout(form_layout)
        
        # Add some spacing before buttons
        layout.addSpacing(20)
        
        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)  # Increased spacing between buttons
        
        save_btn = QPushButton("Save Changes")
        save_btn.setMinimumHeight(45)  # Increased button height
        save_btn.clicked.connect(self.save_changes)
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.setMinimumHeight(45)  # Increased button height
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
            QPushButton:pressed {
                background-color: #6c7b7d;
            }
        """)
        
        btn_layout.addStretch()  # Add stretch to center buttons
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        btn_layout.addStretch()  # Add stretch to center buttons
        
        layout.addLayout(btn_layout)
    
    def load_categories(self):
        """Load categories into the combo box."""
        try:
            categories = self.product_controller.get_categories()
            for category in categories:
                self.category_combo.addItem(category.name, category.id)
        except Exception as e:
            print(f"Error loading categories: {e}")
    
    def load_product_data(self):
        """Load current product data into the form."""
        self.name_input.setText(self.product.name)
        self.description_input.setPlainText(self.product.description or "")
        self.price_input.setValue(self.product.price)
        
        # Set category
        if self.product.category:
            index = self.category_combo.findText(self.product.category.name)
            if index >= 0:
                self.category_combo.setCurrentIndex(index)
        
        self.barcode_input.setText(self.product.barcode or "")
        self.image_path_input.setText(self.product.image_path or "")
    
    def save_changes(self):
        """Save the changes to the product."""
        try:
            # Get form data
            name = self.name_input.text().strip()
            description = self.description_input.toPlainText().strip()
            price = self.price_input.value()
            category_id = self.category_combo.currentData()
            barcode = self.barcode_input.text().strip()
            image_path = self.image_path_input.text().strip()
            
            # Validate required fields
            if not name:
                QMessageBox.warning(self, "Validation Error", "Product name is required!")
                return
            
            if price <= 0:
                QMessageBox.warning(self, "Validation Error", "Price must be greater than 0!")
                return
            
            # Update product
            success = self.product_controller.update_product(
                self.product.id,
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                barcode=barcode if barcode else None,
                image_path=image_path if image_path else None
            )
            
            if success:
                QMessageBox.information(self, "Success", "Product updated successfully!")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update product!")
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")

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
        self.table.setColumnWidth(6, 150)  # Set actions column width
        
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
            
            # Add Edit button
            edit_btn = QPushButton('Edit')
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #f39c12;
                    color: white;
                    border: none;
                    padding: 4px 8px;
                    border-radius: 3px;
                    font-size: 11px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #e67e22;
                }
            """)
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            actions_layout.addWidget(edit_btn)
            
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

    def edit_product(self, product):
        """Open the edit dialog for a product."""
        dialog = ProductEditDialog(product, self)
        if dialog.exec_() == QDialog.Accepted:
            # Refresh the table to show updated data
            self.load_products()

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