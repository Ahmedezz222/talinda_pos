import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, current_dir)

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog, QMessageBox, QInputDialog, QTabWidget, QListWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal
from controllers.product_controller import ProductController

class AddProductPage(QWidget):
    product_added = pyqtSignal(dict)  # Emitted when a product is added
    cancelled = pyqtSignal()  # Emitted when the form is cancelled/reset
    category_added = pyqtSignal(dict)  # Emitted when a new category is added

    def __init__(self, categories=None, parent=None):
        super().__init__(parent)
        self.product_controller = ProductController()
        self.categories = categories or self._fetch_categories()
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

        # Add/remove category controls
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
        remove_btn = QPushButton('Remove Category')
        remove_btn.clicked.connect(self.remove_category_from_tab)
        controls_layout.addWidget(remove_btn)
        layout.addLayout(controls_layout)

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