import sys
import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLineEdit, QPushButton, QLabel, QScrollArea, QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from controllers.pos_controller import POSController
try:
    from ui.components.product_card import ProductCard
except ImportError:
    ProductCard = None  # fallback if not available

class POSView(QWidget):
    def __init__(self, settings=None, database_manager=None, current_user=None, parent=None):
        super().__init__(parent)
        self.settings = settings
        self.database_manager = database_manager
        self.current_user = current_user
        self.pos_controller = POSController(database_manager, current_user, settings)
        self.current_category_id = None  # None = show categories, otherwise show products
        self.init_ui()
        self.reload_categories()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        # Search bar
        search_row = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText('Search...')
        self.search_input.setMinimumHeight(40)
        self.search_input.setStyleSheet('font-size: 18px; border-radius: 10px; padding: 8px 16px;')
        self.search_input.textChanged.connect(self.reload_categories)
        search_row.addWidget(self.search_input)
        main_layout.addLayout(search_row)
        # Category/Product grid
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)
        # Scroll area for grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.grid_widget)
        main_layout.addWidget(scroll, stretch=1)
        self.setLayout(main_layout)
        self.setMinimumSize(900, 600)
        self.resize(1200, 800)

    def reload_categories(self):
        # Remove old widgets from grid
        for i in reversed(range(self.grid_layout.count())):
            widget = self.grid_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        session = self.database_manager.get_session()
        try:
            from models.product import Category, Product
            search_term = self.search_input.text().strip().lower()
            if self.current_category_id is None:
                # Show categories as buttons
                categories = session.query(Category).filter(Category.is_active == True).order_by(Category.name).all()
                if search_term:
                    categories = [cat for cat in categories if search_term in cat.name.lower()]
                for idx, cat in enumerate(categories):
                    cat_btn = QPushButton(cat.name)
                    cat_btn.setFixedSize(170, 90)
                    cat_btn.setStyleSheet('''
                        QPushButton {
                            background: #fff;
                            border-radius: 18px;
                            border: 2px solid #e0e0e0;
                            font-size: 20px;
                            font-weight: bold;
                            color: #6c47ff;
                            margin-bottom: 6px;
            
                        }
                        QPushButton:checked, QPushButton:hover {
                            border: 2.5px solid #6c47ff;
            
                        }
                    ''')
                    cat_btn.clicked.connect(lambda checked, cat_id=cat.id: self.show_category_products(cat_id))
                    row, col = divmod(idx, 4)
                    self.grid_layout.addWidget(cat_btn, row, col)
            else:
                # Show back button
                back_btn = QPushButton('← Back to Categories')
                back_btn.setFixedHeight(48)
                back_btn.setStyleSheet('font-size: 18px; color: #6c47ff; background: #f4f4f4; border-radius: 12px;')
                back_btn.clicked.connect(self.reset_category_grid)
                self.grid_layout.addWidget(back_btn, 0, 0, 1, 4)
                # Show products for selected category
                query = session.query(Product).filter(Product.is_active == True, Product.category_id == self.current_category_id)
                if search_term:
                    query = query.filter(Product.name.ilike(f"%{search_term}%"))
                products = query.order_by(Product.name).all()
                for idx, product in enumerate(products):
                    if ProductCard:
                        prod_card = ProductCard(product)
                        prod_card.product_selected.connect(self.add_to_cart)
                    else:
                        prod_card = self.create_product_card(product)
                    row, col = divmod(idx, 4)
                    self.grid_layout.addWidget(prod_card, row + 1, col)  # +1 for back button
        finally:
            session.close()

    def show_category_products(self, cat_id):
        self.current_category_id = cat_id
        self.reload_categories()

    def reset_category_grid(self):
        self.current_category_id = None
        self.reload_categories()

    def create_product_card(self, product):
        card = QFrame()
        card.setFixedSize(200, 220)
        card.setStyleSheet('''
            QFrame {
                background: white;
                border-radius: 12px;
                border: 1px solid #e0e0e0;
            }
            QFrame:hover {
                border: 2px solid #3498db;
            }
        ''')
        vbox = QVBoxLayout(card)
        vbox.setContentsMargins(10, 10, 10, 10)
        vbox.setSpacing(6)
        name = QLabel(product.name)
        name.setStyleSheet('font-size: 16px; font-weight: bold; color: #222;')
        vbox.addWidget(name, alignment=Qt.AlignCenter)
        price = QLabel(f"EGP {getattr(product, 'selling_price', getattr(product, 'price', 0)):.2f}")
        price.setStyleSheet('font-size: 15px; color: #27ae60; font-weight: bold;')
        vbox.addWidget(price, alignment=Qt.AlignCenter)
        qty = QLabel(f"Qty: {getattr(product, 'quantity', getattr(product, 'stock', 0))}")
        qty.setStyleSheet('font-size: 13px; color: #555;")
        vbox.addWidget(qty, alignment=Qt.AlignCenter)
        add_btn = QPushButton("Add")
        add_btn.setStyleSheet("background-color: #3498db; color: white; border-radius: 6px; font-size: 14px; padding: 4px 12px;")
        add_btn.clicked.connect(lambda _, p=product: self.add_to_cart(p))
        vbox.addWidget(add_btn, alignment=Qt.AlignCenter)
        vbox.addStretch()
        return card

    def add_to_cart(self, product):
        # Implement your add-to-cart logic here
        from PyQt5.QtWidgets import QMessageBox
        if getattr(product, 'quantity', getattr(product, 'stock', 0)) <= 0:
            QMessageBox.warning(self, "Warning", "Product is out of stock!")
            return
        # You can integrate with your cart widget or controller here
        QMessageBox.information(self, "Added", f"Added {product.name} to cart!")

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    from database.database_manager import DatabaseManager
    app = QApplication(sys.argv)
    db_manager = DatabaseManager()
    db_manager.initialize_database()
    window = POSView(database_manager=db_manager)
    window.setWindowTitle("POS View Test")
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec_()) 