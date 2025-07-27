from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from controllers.product_controller import ProductController

class ShowProductsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('All Products')
        self.setMinimumSize(900, 500)
        self.product_controller = ProductController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel('All Products')
        title.setStyleSheet('font-size: 22px; font-weight: bold; color: #273c75; margin-bottom: 10px;')
        layout.addWidget(title)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['Name', 'Description', 'Price', 'Category', 'Stock', 'Barcode', 'Image Path'])
        self.table.setAlternatingRowColors(True)
        self.table.setStyleSheet('QTableWidget { alternate-background-color: #f0f6ff; }')
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.load_products()
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def load_products(self):
        products = self.product_controller.get_products(None)
        self.table.setRowCount(0)
        for product in products:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(product.name))
            self.table.setItem(row, 1, QTableWidgetItem(product.description or ''))
            self.table.setItem(row, 2, QTableWidgetItem(str(product.price)))
            cat_name = product.category.name if product.category else 'No Category'
            self.table.setItem(row, 3, QTableWidgetItem(cat_name))
            self.table.setItem(row, 4, QTableWidgetItem(str(product.stock)))
            self.table.setItem(row, 5, QTableWidgetItem(product.barcode or ''))
            self.table.setItem(row, 6, QTableWidgetItem(product.image_path or ''))