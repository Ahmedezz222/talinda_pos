from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout
from PyQt5.QtCore import Qt
from controllers.sale_controller import SaleController
from controllers.auth_controller import AuthController

class SalesReportWindow(QDialog):
    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Sales Report')
        self.setMinimumSize(700, 500)
        self.user = user
        self.sale_controller = SaleController()
        self.auth_controller = AuthController()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        title = QLabel('Sales Report')
        title.setStyleSheet('font-size: 22px; font-weight: bold; color: #273c75; margin-bottom: 10px;')
        layout.addWidget(title)

        # Opening amount
        opening_amount = self.get_opening_amount()
        layout.addWidget(QLabel(f'Opening Amount: {opening_amount:.2f}'))

        # Sales table
        sales = self.get_sales_summary()
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(['Product', 'Quantity Sold', 'Total'])
        table.setAlternatingRowColors(True)
        table.setStyleSheet('QTableWidget { alternate-background-color: #f0f6ff; }')
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setRowCount(len(sales))
        for row, sale in enumerate(sales):
            table.setItem(row, 0, QTableWidgetItem(sale['product']))
            table.setItem(row, 1, QTableWidgetItem(str(sale['quantity'])))
            table.setItem(row, 2, QTableWidgetItem(f"{sale['total']:.2f}"))
        layout.addWidget(table)

        # Closing amount
        closing_amount = self.get_closing_amount()
        if closing_amount is not None:
            layout.addWidget(QLabel(f'Closing Amount: {closing_amount:.2f}'))
        else:
            layout.addWidget(QLabel('Closing Amount: (not closed yet)'))

        btn_layout = QHBoxLayout()
        close_btn = QPushButton('Close')
        close_btn.clicked.connect(self.close)
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)

    def get_opening_amount(self):
        # This should fetch the opening amount for the current shift/user
        shift = self.auth_controller.get_open_shift(self.user)
        return getattr(shift, 'opening_amount', 0.0) if shift else 0.0

    def get_closing_amount(self):
        # This should fetch the closing amount for the current shift/user
        shift = self.auth_controller.get_open_shift(self.user)
        return getattr(shift, 'closing_amount', None) if shift else None

    def get_sales_summary(self):
        # This should fetch sales for the current shift/user and summarize by product
        sales = self.sale_controller.get_sales_for_shift(self.user)
        summary = {}
        for sale in sales:
            for item in sale.items:
                key = item.product.name
                if key not in summary:
                    summary[key] = {'product': key, 'quantity': 0, 'total': 0.0}
                summary[key]['quantity'] += item.quantity
                summary[key]['total'] += item.quantity * item.price
        return list(summary.values()) 