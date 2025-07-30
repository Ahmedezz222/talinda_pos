import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox, QInputDialog, QTabWidget, QListWidget, QGridLayout, QCheckBox, QTextEdit, QGroupBox, QProgressBar
from PyQt5.QtCore import pyqtSignal, QThread, pyqtSignal as Signal
from controllers.product_controller import ProductController
from utils.excel_report_generator import ExcelReportGenerator

class ImportExportWorker(QThread):
    """Worker thread for import/export operations."""
    progress = Signal(str)
    finished = Signal(dict)
    error = Signal(str)
    
    def __init__(self, operation_type, filepath, update_existing=False):
        super().__init__()
        self.operation_type = operation_type
        self.filepath = filepath
        self.update_existing = update_existing
        self.product_controller = ProductController()
    
    def run(self):
        try:
            if self.operation_type == 'export_products':
                self.progress.emit("Exporting products...")
                result = self.product_controller.export_products_to_excel(self.filepath)
                self.finished.emit({'type': 'export_products', 'filepath': result})
                
            elif self.operation_type == 'export_categories':
                self.progress.emit("Exporting categories...")
                result = self.product_controller.export_categories_to_excel(self.filepath)
                self.finished.emit({'type': 'export_categories', 'filepath': result})
                
            elif self.operation_type == 'import_products':
                self.progress.emit("Importing products...")
                result = self.product_controller.import_products_from_excel(self.filepath, self.update_existing)
                self.finished.emit({'type': 'import_products', 'results': result})
                
            elif self.operation_type == 'import_categories':
                self.progress.emit("Importing categories...")
                result = self.product_controller.import_categories_from_excel(self.filepath, self.update_existing)
                self.finished.emit({'type': 'import_categories', 'results': result})
                
        except Exception as e:
            self.error.emit(str(e))

class AddProductPage(QWidget):
    product_added = pyqtSignal(dict)  # Emitted when a product is added
    cancelled = pyqtSignal()  # Emitted when the form is cancelled/reset
    category_added = pyqtSignal(dict)  # Emitted when a new category is added

    def __init__(self, categories=None, parent=None):
        super().__init__(parent)
        self.product_controller = ProductController()
        self.categories = categories or self._fetch_categories()
        self.import_export_worker = None
        self.init_ui()

    def _fetch_categories(self):
        cats = self.product_controller.get_categories()
        return [{'id': cat.id, 'name': cat.name} for cat in cats]

    def init_ui(self):
        self.setObjectName('addProductPage')
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(24)

        title = QLabel('Product Management')
        title.setStyleSheet('font-size: 28px; font-weight: bold; color: #273c75; margin-bottom: 10px;')
        main_layout.addWidget(title)

        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                padding: 20px;
            }
            QTabBar::tab {
                background-color: #ecf0f1;
                padding: 12px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
                color: #2c3e50;
                font-size: 14px;
                min-width: 120px;
            }
            QTabBar::tab:selected {
                background-color: #3498db;
                color: white;
            }
            QTabBar::tab:hover {
                background-color: #bdc3c7;
            }
        """)
        self.tabs.addTab(self._product_tab_ui(), 'Add Product')
        self.tabs.addTab(self._category_tab_ui(), 'Manage Categories')
        self.tabs.addTab(self._import_export_tab_ui(), 'Import/Export')
        main_layout.addWidget(self.tabs)

    def _product_tab_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create a grid layout for better organization
        form_grid = QGridLayout()
        form_grid.setSpacing(15)
        form_grid.setColumnStretch(1, 1)  # Make input fields expand

        # Name
        name_label = QLabel('Name:')
        name_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText('Enter product name')
        self.name_input.setMinimumHeight(40)
        form_grid.addWidget(name_label, 0, 0)
        form_grid.addWidget(self.name_input, 0, 1)

        # Description
        desc_label = QLabel('Description:')
        desc_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText('Enter product description')
        self.desc_input.setMinimumHeight(40)
        form_grid.addWidget(desc_label, 1, 0)
        form_grid.addWidget(self.desc_input, 1, 1)

        # Price
        price_label = QLabel('Price:')
        price_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText('e.g. 99.99')
        self.price_input.setMinimumHeight(40)
        form_grid.addWidget(price_label, 2, 0)
        form_grid.addWidget(self.price_input, 2, 1)

        # Category
        cat_label = QLabel('Category:')
        cat_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.cat_combo = QComboBox()
        self.cat_combo.setMinimumHeight(40)
        self._refresh_category_combo()
        form_grid.addWidget(cat_label, 3, 0)
        form_grid.addWidget(self.cat_combo, 3, 1)



        # Barcode
        barcode_label = QLabel('Barcode:')
        barcode_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        self.barcode_input = QLineEdit()
        self.barcode_input.setPlaceholderText('Scan or enter barcode')
        self.barcode_input.setMinimumHeight(40)
        form_grid.addWidget(barcode_label, 4, 0)
        form_grid.addWidget(self.barcode_input, 4, 1)

        # Image Path
        image_label = QLabel('Image Path:')
        image_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #2c3e50;")
        image_layout = QHBoxLayout()
        self.image_input = QLineEdit()
        self.image_input.setPlaceholderText('Select image file...')
        self.image_input.setMinimumHeight(40)
        image_btn = QPushButton('Browse')
        image_btn.setMinimumHeight(40)
        image_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            padding: 0 20px;
        """)
        image_btn.clicked.connect(self.browse_image)
        image_layout.addWidget(self.image_input)
        image_layout.addWidget(image_btn)
        form_grid.addWidget(image_label, 5, 0)
        form_grid.addLayout(image_layout, 5, 1)

        layout.addLayout(form_grid)

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(15)
        
        submit_btn = QPushButton('Add Product')
        submit_btn.setMinimumHeight(45)
        submit_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        """)
        submit_btn.clicked.connect(self.submit)
        
        reset_btn = QPushButton('Reset Form')
        reset_btn.setMinimumHeight(45)
        reset_btn.setStyleSheet("""
            background-color: #95a5a6;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 16px;
        """)
        reset_btn.clicked.connect(self.reset_form)
        
        btn_layout.addWidget(submit_btn)
        btn_layout.addWidget(reset_btn)
        btn_layout.addStretch()
        
        layout.addLayout(btn_layout)
        layout.addStretch()

        return widget

    def _category_tab_ui(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel('Manage Categories')
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # List of categories
        list_label = QLabel('Existing Categories:')
        list_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #34495e;")
        layout.addWidget(list_label)
        
        self.category_list = QListWidget()
        self.category_list.setMinimumHeight(200)
        self.category_list.setStyleSheet("""
            QListWidget {
                border: 2px solid #bdc3c7;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
            }
            QListWidget::item:selected {
                background-color: #3498db;
                color: white;
            }
        """)
        self._refresh_category_list()
        layout.addWidget(self.category_list)

        # Add/remove/edit category controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(10)
        
        self.new_cat_input = QLineEdit()
        self.new_cat_input.setPlaceholderText('Enter new category name')
        self.new_cat_input.setMinimumHeight(40)
        
        add_btn = QPushButton('Add Category')
        add_btn.setMinimumHeight(40)
        add_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        add_btn.clicked.connect(self.add_category_from_tab)
        
        controls_layout.addWidget(self.new_cat_input)
        controls_layout.addWidget(add_btn)
        
        # Edit and Remove buttons
        edit_btn = QPushButton('Edit Category')
        edit_btn.setMinimumHeight(40)
        edit_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        edit_btn.clicked.connect(self.edit_category_from_tab)
        controls_layout.addWidget(edit_btn)
        
        remove_btn = QPushButton('Remove Category')
        remove_btn.setMinimumHeight(40)
        remove_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 14px;
        """)
        remove_btn.clicked.connect(self.remove_category_from_tab)
        controls_layout.addWidget(remove_btn)
        layout.addLayout(controls_layout)

        return widget

    def _import_export_tab_ui(self):
        """Create the import/export tab UI."""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title
        title_label = QLabel('Import/Export Data')
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50; margin-bottom: 10px;")
        layout.addWidget(title_label)

        # Export Section
        export_group = QGroupBox('Export Data')
        export_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
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
        export_layout = QVBoxLayout(export_group)
        export_layout.setSpacing(15)

        # Export buttons
        export_buttons_layout = QHBoxLayout()
        
        export_products_btn = QPushButton('Export Products')
        export_products_btn.setMinimumHeight(45)
        export_products_btn.setStyleSheet("""
            background-color: #27ae60;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        """)
        export_products_btn.clicked.connect(self.export_products)
        
        export_categories_btn = QPushButton('Export Categories')
        export_categories_btn.setMinimumHeight(45)
        export_categories_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        """)
        export_categories_btn.clicked.connect(self.export_categories)
        
        export_buttons_layout.addWidget(export_products_btn)
        export_buttons_layout.addWidget(export_categories_btn)
        export_buttons_layout.addStretch()
        
        export_layout.addLayout(export_buttons_layout)
        layout.addWidget(export_group)

        # Import Section
        import_group = QGroupBox('Import Data')
        import_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
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
        import_layout = QVBoxLayout(import_group)
        import_layout.setSpacing(15)

        # Import options
        self.update_existing_checkbox = QCheckBox('Update existing items')
        self.update_existing_checkbox.setStyleSheet("font-size: 14px; color: #2c3e50;")
        import_layout.addWidget(self.update_existing_checkbox)

        # Template download section
        template_layout = QHBoxLayout()
        template_label = QLabel('Download Templates:')
        template_label.setStyleSheet("font-size: 14px; color: #2c3e50; font-weight: bold;")
        
        download_products_template_btn = QPushButton('Product Template')
        download_products_template_btn.setMinimumHeight(35)
        download_products_template_btn.setStyleSheet("""
            background-color: #9b59b6;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 12px;
        """)
        download_products_template_btn.clicked.connect(self.download_product_template)
        
        download_categories_template_btn = QPushButton('Category Template')
        download_categories_template_btn.setMinimumHeight(35)
        download_categories_template_btn.setStyleSheet("""
            background-color: #9b59b6;
            color: white;
            border: none;
            border-radius: 6px;
            font-weight: bold;
            font-size: 12px;
        """)
        download_categories_template_btn.clicked.connect(self.download_category_template)
        
        template_layout.addWidget(template_label)
        template_layout.addWidget(download_products_template_btn)
        template_layout.addWidget(download_categories_template_btn)
        template_layout.addStretch()
        
        import_layout.addLayout(template_layout)

        # Import buttons
        import_buttons_layout = QHBoxLayout()
        
        import_products_btn = QPushButton('Import Products')
        import_products_btn.setMinimumHeight(45)
        import_products_btn.setStyleSheet("""
            background-color: #f39c12;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        """)
        import_products_btn.clicked.connect(self.import_products)
        
        import_categories_btn = QPushButton('Import Categories')
        import_categories_btn.setMinimumHeight(45)
        import_categories_btn.setStyleSheet("""
            background-color: #e67e22;
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: bold;
            font-size: 14px;
        """)
        import_categories_btn.clicked.connect(self.import_categories)
        
        import_buttons_layout.addWidget(import_products_btn)
        import_buttons_layout.addWidget(import_categories_btn)
        import_buttons_layout.addStretch()
        
        import_layout.addLayout(import_buttons_layout)
        layout.addWidget(import_group)

        # Progress and Status Section
        status_group = QGroupBox('Status')
        status_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 2px solid #bdc3c7;
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
        status_layout = QVBoxLayout(status_group)
        status_layout.setSpacing(10)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #3498db;
                border-radius: 3px;
            }
        """)
        status_layout.addWidget(self.progress_bar)

        # Status text
        self.status_text = QTextEdit()
        self.status_text.setMaximumHeight(150)
        self.status_text.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                background-color: #f8f9fa;
                font-family: 'Courier New', monospace;
                font-size: 12px;
            }
        """)
        self.status_text.setPlaceholderText("Import/export status will appear here...")
        status_layout.addWidget(self.status_text)

        layout.addWidget(status_group)
        layout.addStretch()

        return widget

    def _refresh_category_combo(self):
        self.cat_combo.clear()
        for cat in self.categories:
            self.cat_combo.addItem(cat['name'], cat['id'])

    def _refresh_category_list(self):
        self.category_list.clear()
        for cat in self.categories:
            self.category_list.addItem(cat['name'])

    def browse_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Select Image', '', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if file_path:
            self.image_input.setText(file_path)

    def add_category_from_tab(self):
        name = self.new_cat_input.text().strip()
        if not name:
            QMessageBox.warning(self, 'Input Error', 'Category name cannot be empty.')
            return
        # Check if already exists
        for cat in self.categories:
            if cat['name'].lower() == name.lower():
                QMessageBox.warning(self, 'Exists', 'Category already exists!')
                return
        try:
            new_cat = self.product_controller.add_category(name)
            cat_dict = {'id': new_cat.id, 'name': new_cat.name}
            self.categories.append(cat_dict)
            self._refresh_category_combo()
            self._refresh_category_list()
            self.new_cat_input.clear()
            self.category_added.emit(cat_dict)
            QMessageBox.information(self, 'Success', 'Category added!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not add category: {e}')

    def edit_category_from_tab(self):
        selected_items = self.category_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select a category to edit.')
            return
        
        selected_name = selected_items[0].text()
        # Find the category dict
        cat = next((c for c in self.categories if c['name'] == selected_name), None)
        if not cat:
            QMessageBox.warning(self, 'Error', 'Selected category not found.')
            return
        
        # Create edit dialog
        new_name, ok = QInputDialog.getText(
            self, 
            'Edit Category', 
            f'Enter new name for category "{selected_name}":',
            text=selected_name
        )
        
        if ok and new_name.strip():
            new_name = new_name.strip()
            
            # Check if new name already exists (excluding current category)
            for existing_cat in self.categories:
                if existing_cat['id'] != cat['id'] and existing_cat['name'].lower() == new_name.lower():
                    QMessageBox.warning(self, 'Exists', 'Category name already exists!')
                    return
            
            try:
                # Update category in database
                updated_cat = self.product_controller.update_category(cat['id'], new_name)
                
                # Update local categories list
                cat['name'] = updated_cat.name
                
                # Refresh UI
                self._refresh_category_combo()
                self._refresh_category_list()
                
                QMessageBox.information(self, 'Success', f'Category "{selected_name}" updated to "{new_name}"!')
            except Exception as e:
                QMessageBox.warning(self, 'Error', f'Could not update category: {e}')
        elif ok and not new_name.strip():
            QMessageBox.warning(self, 'Input Error', 'Category name cannot be empty.')

    def remove_category_from_tab(self):
        selected_items = self.category_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, 'No Selection', 'Please select a category to remove.')
            return
        selected_name = selected_items[0].text()
        # Find the category dict
        cat = next((c for c in self.categories if c['name'] == selected_name), None)
        if not cat:
            QMessageBox.warning(self, 'Error', 'Selected category not found.')
            return
        # Confirm deletion
        reply = QMessageBox.question(self, 'Confirm Delete', f"Are you sure you want to delete the category '{selected_name}'? This cannot be undone.", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return
        # Check if category is in use
        if self.product_controller.get_products(category=type('Cat', (), {'id': cat['id']})):  # Dummy object with id
            QMessageBox.warning(self, 'In Use', 'Cannot delete a category that is assigned to products.')
            return
        try:
            self.product_controller.delete_category(cat['id'])
            self.categories = [c for c in self.categories if c['id'] != cat['id']]
            self._refresh_category_combo()
            self._refresh_category_list()
            QMessageBox.information(self, 'Success', 'Category removed!')
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not remove category: {e}')

    def submit(self):
        name = self.name_input.text().strip()
        description = self.desc_input.text().strip()
        try:
            price = float(self.price_input.text())
        except ValueError:
            QMessageBox.warning(self, 'Input Error', 'Invalid price.')
            return
        category_index = self.cat_combo.currentIndex()
        category_id = self.cat_combo.itemData(category_index)
        barcode = self.barcode_input.text().strip()
        image_path = self.image_input.text().strip()
        if not name or not price or not category_id:
            QMessageBox.warning(self, 'Input Error', 'Name, price, and category are required.')
            return
        product_data = {
            'name': name,
            'description': description,
            'price': price,
            'category_id': category_id,
            'barcode': barcode,
            'image_path': image_path
        }
        try:
            self.product_added.emit(product_data)
            QMessageBox.information(self, 'Success', 'Product added successfully!')
            self.reset_form()
        except ValueError as e:
            if 'barcode' in str(e).lower():
                QMessageBox.warning(self, 'Barcode Error', str(e))
            else:
                QMessageBox.warning(self, 'Error', str(e))
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Could not add product: {e}')

    def reset_form(self):
        self.name_input.clear()
        self.desc_input.clear()
        self.price_input.clear()
        self.barcode_input.clear()
        self.image_input.clear()
        self.cancelled.emit() 

    def download_product_template(self):
        """Download product import template."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Save Product Template',
                'product_import_template.xlsx',
                'Excel Files (*.xlsx);;All Files (*)'
            )
            
            if filepath:
                excel_generator = ExcelReportGenerator()
                result = excel_generator.create_product_import_template(filepath)
                
                if result:
                    self.status_text.append(f"✅ Product template downloaded to: {result}")
                    QMessageBox.information(
                        self,
                        'Template Downloaded',
                        f'Product import template has been saved to:\n{result}\n\n'
                        'You can now fill in your product data and import it back.'
                    )
                else:
                    QMessageBox.warning(self, 'Error', 'Failed to create product template.')
                    
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error downloading template: {str(e)}')

    def download_category_template(self):
        """Download category import template."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Save Category Template',
                'category_import_template.xlsx',
                'Excel Files (*.xlsx);;All Files (*)'
            )
            
            if filepath:
                excel_generator = ExcelReportGenerator()
                result = excel_generator.create_category_import_template(filepath)
                
                if result:
                    self.status_text.append(f"✅ Category template downloaded to: {result}")
                    QMessageBox.information(
                        self,
                        'Template Downloaded',
                        f'Category import template has been saved to:\n{result}\n\n'
                        'You can now fill in your category data and import it back.'
                    )
                else:
                    QMessageBox.warning(self, 'Error', 'Failed to create category template.')
                    
        except Exception as e:
            QMessageBox.warning(self, 'Error', f'Error downloading template: {str(e)}')

    def export_products(self):
        """Export products to Excel file."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Export Products',
                'products_export.xlsx',
                'Excel Files (*.xlsx);;All Files (*)'
            )
            
            if filepath:
                self.progress_bar.setVisible(True)
                self.progress_bar.setRange(0, 0)  # Indeterminate progress
                self.status_text.append("Starting product export...")
                
                self.import_export_worker = ImportExportWorker('export_products', filepath)
                self.import_export_worker.progress.connect(self.update_status)
                self.import_export_worker.finished.connect(self.on_export_finished)
                self.import_export_worker.error.connect(self.on_import_export_error)
                self.import_export_worker.start()
                
        except Exception as e:
            QMessageBox.warning(self, 'Export Error', f'Error starting export: {str(e)}')

    def export_categories(self):
        """Export categories to Excel file."""
        try:
            filepath, _ = QFileDialog.getSaveFileName(
                self,
                'Export Categories',
                'categories_export.xlsx',
                'Excel Files (*.xlsx);;All Files (*)'
            )
            
            if filepath:
                self.progress_bar.setVisible(True)
                self.progress_bar.setRange(0, 0)  # Indeterminate progress
                self.status_text.append("Starting category export...")
                
                self.import_export_worker = ImportExportWorker('export_categories', filepath)
                self.import_export_worker.progress.connect(self.update_status)
                self.import_export_worker.finished.connect(self.on_export_finished)
                self.import_export_worker.error.connect(self.on_import_export_error)
                self.import_export_worker.start()
                
        except Exception as e:
            QMessageBox.warning(self, 'Export Error', f'Error starting export: {str(e)}')

    def import_products(self):
        """Import products from Excel file."""
        try:
            filepath, _ = QFileDialog.getOpenFileName(
                self,
                'Import Products',
                '',
                'Excel Files (*.xlsx);;All Files (*)'
            )
            
            if filepath:
                update_existing = self.update_existing_checkbox.isChecked()
                
                # Confirm import
                msg = f"Import products from '{filepath}'?"
                if update_existing:
                    msg += "\n\nWARNING: This will update existing products with the same name or barcode!"
                
                reply = QMessageBox.question(
                    self,
                    'Confirm Import',
                    msg,
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    self.progress_bar.setVisible(True)
                    self.progress_bar.setRange(0, 0)  # Indeterminate progress
                    self.status_text.append("Starting product import...")
                    
                    self.import_export_worker = ImportExportWorker('import_products', filepath, update_existing)
                    self.import_export_worker.progress.connect(self.update_status)
                    self.import_export_worker.finished.connect(self.on_import_finished)
                    self.import_export_worker.error.connect(self.on_import_export_error)
                    self.import_export_worker.start()
                
        except Exception as e:
            QMessageBox.warning(self, 'Import Error', f'Error starting import: {str(e)}')

    def import_categories(self):
        """Import categories from Excel file."""
        try:
            filepath, _ = QFileDialog.getOpenFileName(
                self,
                'Import Categories',
                '',
                'Excel Files (*.xlsx);;All Files (*)'
            )
            
            if filepath:
                update_existing = self.update_existing_checkbox.isChecked()
                
                # Confirm import
                msg = f"Import categories from '{filepath}'?"
                if update_existing:
                    msg += "\n\nWARNING: This will update existing categories with the same name!"
                
                reply = QMessageBox.question(
                    self,
                    'Confirm Import',
                    msg,
                    QMessageBox.Yes | QMessageBox.No
                )
                
                if reply == QMessageBox.Yes:
                    self.progress_bar.setVisible(True)
                    self.progress_bar.setRange(0, 0)  # Indeterminate progress
                    self.status_text.append("Starting category import...")
                    
                    self.import_export_worker = ImportExportWorker('import_categories', filepath, update_existing)
                    self.import_export_worker.progress.connect(self.update_status)
                    self.import_export_worker.finished.connect(self.on_import_finished)
                    self.import_export_worker.error.connect(self.on_import_export_error)
                    self.import_export_worker.start()
                
        except Exception as e:
            QMessageBox.warning(self, 'Import Error', f'Error starting import: {str(e)}')

    def update_status(self, message):
        """Update status text with progress message."""
        self.status_text.append(message)

    def on_export_finished(self, result):
        """Handle export completion."""
        self.progress_bar.setVisible(False)
        
        if result['type'] == 'export_products':
            self.status_text.append(f"✅ Products exported successfully to: {result['filepath']}")
            QMessageBox.information(self, 'Export Complete', f'Products exported successfully to:\n{result["filepath"]}')
        elif result['type'] == 'export_categories':
            self.status_text.append(f"✅ Categories exported successfully to: {result['filepath']}")
            QMessageBox.information(self, 'Export Complete', f'Categories exported successfully to:\n{result["filepath"]}')

    def on_import_finished(self, result):
        """Handle import completion."""
        self.progress_bar.setVisible(False)
        
        if result['type'] == 'import_products':
            results = result['results']
            self.status_text.append(f"✅ Product import completed:")
            self.status_text.append(f"   - Total rows: {results['total_rows']}")
            self.status_text.append(f"   - Imported: {results['imported']}")
            self.status_text.append(f"   - Updated: {results['updated']}")
            self.status_text.append(f"   - Skipped: {results['skipped']}")
            
            if results['errors']:
                self.status_text.append(f"   - Errors: {len(results['errors'])}")
                for error in results['errors'][:5]:  # Show first 5 errors
                    self.status_text.append(f"     • {error}")
                if len(results['errors']) > 5:
                    self.status_text.append(f"     • ... and {len(results['errors']) - 5} more errors")
            
            # Refresh categories after import
            self.categories = self._fetch_categories()
            self._refresh_category_combo()
            self._refresh_category_list()
            
            QMessageBox.information(
                self,
                'Import Complete',
                f'Product import completed!\n\n'
                f'Imported: {results["imported"]}\n'
                f'Updated: {results["updated"]}\n'
                f'Skipped: {results["skipped"]}\n'
                f'Errors: {len(results["errors"])}'
            )
            
        elif result['type'] == 'import_categories':
            results = result['results']
            self.status_text.append(f"✅ Category import completed:")
            self.status_text.append(f"   - Total rows: {results['total_rows']}")
            self.status_text.append(f"   - Imported: {results['imported']}")
            self.status_text.append(f"   - Updated: {results['updated']}")
            self.status_text.append(f"   - Skipped: {results['skipped']}")
            
            if results['errors']:
                self.status_text.append(f"   - Errors: {len(results['errors'])}")
                for error in results['errors'][:5]:  # Show first 5 errors
                    self.status_text.append(f"     • {error}")
                if len(results['errors']) > 5:
                    self.status_text.append(f"     • ... and {len(results['errors']) - 5} more errors")
            
            # Refresh categories after import
            self.categories = self._fetch_categories()
            self._refresh_category_combo()
            self._refresh_category_list()
            
            QMessageBox.information(
                self,
                'Import Complete',
                f'Category import completed!\n\n'
                f'Imported: {results["imported"]}\n'
                f'Updated: {results["updated"]}\n'
                f'Skipped: {results["skipped"]}\n'
                f'Errors: {len(results["errors"])}'
            )

    def on_import_export_error(self, error_message):
        """Handle import/export errors."""
        self.progress_bar.setVisible(False)
        self.status_text.append(f"❌ Error: {error_message}")
        QMessageBox.warning(self, 'Error', f'Operation failed:\n{error_message}') 