from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout, QMessageBox, QHeaderView, QWidget, QLineEdit, QTextEdit, QDoubleSpinBox, QComboBox, QFormLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from controllers.product_controller import ProductController

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
        self.products = []  # Store products for reference
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel('📦 Product Management')
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #2c3e50; 
            margin-bottom: 15px;
            padding: 10px;
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #3498db, stop:1 #2980b9);
            border-radius: 8px;
            color: white;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        # Products table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Product Name', 'Description', 'Price', 'Category', 'Barcode', 'Image Path', 'Actions'])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet("""
            QTableWidget { 
                alternate-background-color: #f8f9fa; 
                background-color: white;
                gridline-color: #dee2e6;
                border: 1px solid #dee2e6;
                border-radius: 8px;
            }
            QHeaderView::section {
                background-color: #495057;
                color: white;
                padding: 8px;
                border: none;
                font-weight: bold;
                font-size: 12px;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            QTableWidget::item:selected {
                background-color: #007bff;
                color: white;
            }
        """)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        
        # Set column widths for better display
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)  # Product Name - stretches
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)  # Description
        header.setSectionResizeMode(2, QHeaderView.Fixed)  # Price - fixed width
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(4, QHeaderView.Fixed)  # Barcode - fixed width
        header.setSectionResizeMode(5, QHeaderView.Fixed)  # Image Path - fixed width
        header.setSectionResizeMode(6, QHeaderView.Fixed)  # Actions - fixed width
        
        # Set specific column widths
        self.table.setColumnWidth(2, 80)   # Price
        self.table.setColumnWidth(4, 120)  # Barcode
        self.table.setColumnWidth(5, 150)  # Image Path
        self.table.setColumnWidth(6, 180)  # Actions
        
        self.load_products()
        layout.addWidget(self.table)

        # Bottom buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        refresh_btn = QPushButton('🔄 Refresh Products')
        refresh_btn.clicked.connect(self.load_products)
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
        """)
        
        close_btn = QPushButton('❌ Close')
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 14px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
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
            
            # Add product data with better formatting
            name_item = QTableWidgetItem(product.name)
            name_item.setFont(QFont("Arial", 11, QFont.Bold))
            self.table.setItem(row, 0, name_item)
            
            desc_item = QTableWidgetItem(product.description or 'No description')
            desc_item.setFont(QFont("Arial", 10))
            self.table.setItem(row, 1, desc_item)
            
            price_item = QTableWidgetItem(f"${product.price:.2f}")
            price_item.setFont(QFont("Arial", 10, QFont.Bold))
            price_item.setForeground(QColor("#27ae60"))
            self.table.setItem(row, 2, price_item)
            
            cat_name = product.category.name if product.category else 'No Category'
            cat_item = QTableWidgetItem(cat_name)
            cat_item.setFont(QFont("Arial", 10))
            self.table.setItem(row, 3, cat_item)
            
            barcode_item = QTableWidgetItem(product.barcode or 'No barcode')
            barcode_item.setFont(QFont("Arial", 9))
            barcode_item.setForeground(QColor("#7f8c8d"))
            self.table.setItem(row, 4, barcode_item)
            
            image_item = QTableWidgetItem(product.image_path or 'No image')
            image_item.setFont(QFont("Arial", 9))
            image_item.setForeground(QColor("#7f8c8d"))
            self.table.setItem(row, 5, image_item)
            
            # Create actions widget
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(2, 2, 2, 2)
            actions_layout.setSpacing(4)
            
            # Add Edit button
            edit_btn = QPushButton('✏️ Edit')
            edit_btn.setStyleSheet("""
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                    min-width: 60px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
                QPushButton:pressed {
                    background-color: #21618c;
                }
            """)
            edit_btn.clicked.connect(lambda checked, p=product: self.edit_product(p))
            actions_layout.addWidget(edit_btn)
            
            # Add delete button
            delete_btn = QPushButton('🗑️ Delete')
            delete_btn.setStyleSheet("""
                QPushButton {
                    background-color: #e74c3c;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 5px;
                    font-size: 12px;
                    font-weight: bold;
                    min-width: 70px;
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
                QMessageBox.warning(
                    self,
                    'Cannot Delete Product',
                    str(e)
                )
            except Exception as e:
                QMessageBox.critical(
                    self,
                    'Error',
                    f'An unexpected error occurred while deleting "{product_name}":\n{str(e)}'
                )

    # Sales information methods removed as requested