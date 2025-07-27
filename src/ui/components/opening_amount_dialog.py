from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox

class OpeningAmountDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Enter Opening Amount')
        self.setFixedSize(300, 150)
        self.amount = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel('Enter opening cash amount:'))
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('e.g. 1000.00')
        layout.addWidget(self.amount_input)
        self.ok_btn = QPushButton('OK')
        self.ok_btn.clicked.connect(self.handle_ok)
        layout.addWidget(self.ok_btn)

    def handle_ok(self):
        try:
            value = float(self.amount_input.text())
            if value < 0:
                raise ValueError
            self.amount = value
            self.accept()
        except ValueError:
            QMessageBox.warning(self, 'Invalid Amount', 'Please enter a valid positive number.') 