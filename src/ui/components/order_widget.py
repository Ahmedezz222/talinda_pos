"""
Order widget component for displaying and managing orders.
"""
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QScrollArea, QFrame, QDialog,
                           QLineEdit, QTextEdit, QMessageBox, QComboBox,
                           QTableWidget, QTableWidgetItem, QHeaderView,
                           QTabWidget, QSplitter, QGroupBox, QGridLayout)
from PyQt5.QtCore import Qt, pyqtSignal, QTimer
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication
from datetime import datetime
from controllers.order_controller import OrderController
from models.order import OrderStatus
from models.user import User

class OrderCard(QFrame):
    """Widget for displaying an individual order."""
    
    # Signals
    order_completed = pyqtSignal(object)  # Emitted when order is completed
    order_cancelled = pyqtSignal(object)  # Emitted when order is cancelled
    order_edited = pyqtSignal(object)     # Emitted when order is edited
    order_clicked = pyqtSignal(object)    # Emitted when order card is clicked
    
    def __init__(self, order, user: User, parent=None):
        super().__init__(parent)
        self.order = order
        self.user = user
        self.order_controller = OrderController()
        self.init_ui()
        
    def init_ui(self):
        """Initialize the user interface."""
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('''
            OrderCard {
                background-color: #ffffff;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 15px;
                margin: 5px;
                min-width: 320px;
                max-width: 380px;
                min-height: 200px;
            }
            OrderCard:hover {
                border-color: #3498db;
                background-color: #f8f9fa;
            }
        ''')
        
        # Enable mouse tracking for hover effects
        self.setMouseTracking(True)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        
        # Header with status only
        header_layout = QHBoxLayout()
        
        header_layout.addStretch()
        
        # Status badge
        status_label = QLabel(self.order.get_status_display())
        status_label.setStyleSheet(self._get_status_style())
        status_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(status_label)
        
        layout.addLayout(header_layout)
        
        # Customer name
        if self.order.customer_name:
            customer_label = QLabel(f"Customer: {self.order.customer_name}")
            customer_label.setStyleSheet("font-weight: bold; color: #34495e; margin: 5px 0; font-size: 13px;")
            layout.addWidget(customer_label)
        
        # Order items
        items_label = QLabel("Items:")
        items_label.setStyleSheet("font-weight: bold; margin-top: 10px; font-size: 13px;")
        layout.addWidget(items_label)
        
        items_text = ""
        order_items = self.order.get_order_items()
        for item in order_items:
            items_text += f"• {item['product'].name} x{item['quantity']} - ${item['price']:.2f}\n"
            if item.get('notes'):
                items_text += f"  Note: {item['notes']}\n"
        
        if items_text:
            items_display = QLabel(items_text)
            items_display.setStyleSheet("color: #555; font-size: 12px; margin-left: 10px;")
            items_display.setWordWrap(True)
            layout.addWidget(items_display)
        
        # Total amount
        total_label = QLabel(f"Total: ${self.order.total_amount:.2f}")
        total_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 15px; margin-top: 10px;")
        layout.addWidget(total_label)
        
        # Time created
        time_label = QLabel(f"Created: {self.order.created_at.strftime('%H:%M:%S')}")
        time_label.setStyleSheet("color: #7f8c8d; font-size: 11px;")
        layout.addWidget(time_label)
        
        # Notes if any
        if self.order.notes:
            notes_label = QLabel(f"Notes: {self.order.notes}")
            notes_label.setStyleSheet("color: #e67e22; font-style: italic; font-size: 11px; margin-top: 5px;")
            notes_label.setWordWrap(True)
            layout.addWidget(notes_label)
        
        # Action buttons (only for active orders)
        if self.order.status == OrderStatus.ACTIVE:
            btn_layout = QHBoxLayout()
            btn_layout.setSpacing(8)
            
            edit_btn = QPushButton("Edit")
            edit_btn.setStyleSheet("""
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
                min-height: 30px;
            """)
            edit_btn.clicked.connect(self.edit_order)
            btn_layout.addWidget(edit_btn)
            
            complete_btn = QPushButton("Complete")
            complete_btn.setStyleSheet("""
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
                min-height: 30px;
            """)
            complete_btn.clicked.connect(self.complete_order)
            btn_layout.addWidget(complete_btn)
            
            cancel_btn = QPushButton("Cancel")
            cancel_btn.setStyleSheet("""
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 12px;
                font-weight: bold;
                min-height: 30px;
            """)
            cancel_btn.clicked.connect(self.cancel_order)
            btn_layout.addWidget(cancel_btn)
            
            layout.addLayout(btn_layout)
    
    def _get_status_style(self):
        """Get CSS style for status badge."""
        status_styles = {
            OrderStatus.ACTIVE: "background-color: #3498db; color: white; padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;",
            OrderStatus.COMPLETED: "background-color: #27ae60; color: white; padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;",
            OrderStatus.CANCELLED: "background-color: #e74c3c; color: white; padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;",
            OrderStatus.PENDING: "background-color: #f39c12; color: white; padding: 3px 8px; border-radius: 10px; font-size: 10px; font-weight: bold;"
        }
        return status_styles.get(self.order.status, "")
    
    def edit_order(self):
        """Edit the order."""
        dialog = OrderEditDialog(self.order, self.user, self)
        if dialog.exec_() == QDialog.Accepted:
            self.order_edited.emit(self.order)
    
    def complete_order(self):
        """Complete the order."""
        reply = QMessageBox.question(
            self, 
            "Complete Order", 
            f"Are you sure you want to complete order #{self.order.order_number}?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            if self.order_controller.complete_order(self.order):
                self.order_completed.emit(self.order)
                QMessageBox.information(self, "Success", "Order completed successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to complete order.")
    
    def cancel_order(self):
        """Cancel the order."""
        dialog = OrderCancelDialog(self.order, self.user, self)
        if dialog.exec_() == QDialog.Accepted:
            if self.order_controller.cancel_order(self.order, self.user, dialog.reason):
                self.order_cancelled.emit(self.order)
                QMessageBox.information(self, "Success", "Order cancelled successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to cancel order.")
    
    def mousePressEvent(self, event):
        """Handle mouse click events."""
        if event.button() == Qt.LeftButton:
            # Only emit signal for active orders
            if self.order.status == OrderStatus.ACTIVE:
                self.order_clicked.emit(self.order)
        super().mousePressEvent(event)


class OrderEditDialog(QDialog):
    """Dialog for editing order details."""
    
    def __init__(self, order, user: User, parent=None):
        super().__init__(parent)
        self.order = order
        self.user = user
        self.order_controller = OrderController()
        self.setWindowTitle("Edit Order")
        self.setFixedSize(400, 300)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Customer name
        layout.addWidget(QLabel("Customer Name:"))
        self.customer_name_input = QLineEdit(self.order.customer_name or "")
        layout.addWidget(self.customer_name_input)
        
        # Notes
        layout.addWidget(QLabel("Notes:"))
        self.notes_input = QTextEdit()
        self.notes_input.setPlainText(self.order.notes or "")
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.save_changes)
        save_btn.setStyleSheet("background-color: #27ae60; color: white; padding: 8px 16px; border-radius: 5px;")
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px 16px; border-radius: 5px;")
        
        btn_layout.addWidget(save_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def save_changes(self):
        """Save the changes to the order."""
        customer_name = self.customer_name_input.text().strip()
        notes = self.notes_input.toPlainText().strip()
        
        success = True
        if customer_name != (self.order.customer_name or ""):
            success &= self.order_controller.update_order_customer_name(self.order, customer_name)
        
        if notes != (self.order.notes or ""):
            success &= self.order_controller.update_order_notes(self.order, notes)
        
        if success:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Failed to save changes.")


class OrderCancelDialog(QDialog):
    """Dialog for cancelling an order."""
    
    def __init__(self, order, user: User, parent=None):
        super().__init__(parent)
        self.order = order
        self.user = user
        self.reason = ""
        self.setWindowTitle("Cancel Order")
        self.setFixedSize(400, 200)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Are you sure you want to cancel this order?"))
        
        # Reason for cancellation
        layout.addWidget(QLabel("Reason for cancellation (optional):"))
        self.reason_input = QTextEdit()
        self.reason_input.setMaximumHeight(80)
        layout.addWidget(self.reason_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        confirm_btn = QPushButton("Confirm Cancel")
        confirm_btn.clicked.connect(self.confirm_cancel)
        confirm_btn.setStyleSheet("background-color: #e74c3c; color: white; padding: 8px 16px; border-radius: 5px;")
        
        cancel_btn = QPushButton("Keep Order")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("background-color: #95a5a6; color: white; padding: 8px 16px; border-radius: 5px;")
        
        btn_layout.addWidget(confirm_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
    
    def confirm_cancel(self):
        """Confirm the cancellation."""
        self.reason = self.reason_input.toPlainText().strip()
        self.accept()


class OrderManagementWidget(QWidget):
    """Main widget for managing orders with tabs for different statuses."""
    
    # Signals
    order_updated = pyqtSignal()  # Emitted when any order is updated
    
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user
        self.order_controller = OrderController()
        self.order_cards = {}  # Store order cards by order ID
        self.init_ui()
        self.refresh_orders()
        
        # Auto-refresh timer
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_orders)
        self.refresh_timer.start(30000)  # Refresh every 30 seconds
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Header
        header_layout = QHBoxLayout()
        title_label = QLabel("Order Management")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        header_layout.addWidget(title_label)
        
        header_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_orders)
        refresh_btn.setStyleSheet("""
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: bold;
        """)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        # Tab widget for different order statuses
        self.tab_widget = QTabWidget()
        
        # Active orders tab
        self.active_tab = self.create_orders_tab("Active Orders")
        self.tab_widget.addTab(self.active_tab, "Active Orders")
        
        # Completed orders tab
        self.completed_tab = self.create_orders_tab("Completed Orders")
        self.tab_widget.addTab(self.completed_tab, "Completed Orders")
        
        # Cancelled orders tab
        self.cancelled_tab = self.create_orders_tab("Cancelled Orders")
        self.tab_widget.addTab(self.cancelled_tab, "Cancelled Orders")
        
        layout.addWidget(self.tab_widget)
    
    def create_orders_tab(self, title):
        """Create a tab for displaying orders of a specific status."""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Scroll area for order cards
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Container for order cards with grid layout
        orders_container = QWidget()
        orders_layout = QGridLayout(orders_container)
        orders_layout.setSpacing(15)
        orders_layout.setContentsMargins(10, 10, 10, 10)
        
        scroll.setWidget(orders_container)
        layout.addWidget(scroll)
        
        # Store reference to the container for later use
        tab.orders_container = orders_container
        tab.orders_layout = orders_layout
        tab.title = title  # Store title for reference
        
        return tab
    
    def refresh_orders(self):
        """Refresh all orders."""
        # Clear existing order cards
        for card in self.order_cards.values():
            card.setParent(None)
            card.deleteLater()
        self.order_cards.clear()
        
        # Get orders by status
        active_orders = self.order_controller.get_active_orders()
        completed_orders = self.order_controller.get_completed_orders()
        cancelled_orders = self.order_controller.get_cancelled_orders()
        
        # Add order cards to appropriate tabs
        self.add_order_cards_to_tab(self.active_tab, active_orders)
        self.add_order_cards_to_tab(self.completed_tab, completed_orders)
        self.add_order_cards_to_tab(self.cancelled_tab, cancelled_orders)
    
    def add_order_cards_to_tab(self, tab, orders):
        """Add order cards to a specific tab using responsive grid layout."""
        # Clear existing widgets in the tab
        while tab.orders_layout.count():
            item = tab.orders_layout.takeAt(0)
            if item.widget():
                item.widget().setParent(None)
        
        if not orders:
            # Show "No orders" message
            title = getattr(tab, 'title', 'orders').lower()
            no_orders_label = QLabel(f"No {title} found")
            no_orders_label.setAlignment(Qt.AlignCenter)
            no_orders_label.setStyleSheet("font-size: 16px; color: #666; padding: 40px; background-color: #f8f9fa; border-radius: 10px;")
            tab.orders_layout.addWidget(no_orders_label, 0, 0, 1, 3)  # Span multiple columns
            return
        
        # Calculate responsive grid columns
        available_width = self.width() - 50  # Account for margins
        card_width = 350  # Approximate card width
        max_cols = max(1, min(4, int(available_width / card_width)))  # Limit to 4 columns max
        
        row = 0
        col = 0
        
        # Add new order cards
        for order in orders:
            card = OrderCard(order, self.user)
            card.order_completed.connect(self.on_order_completed)
            card.order_cancelled.connect(self.on_order_cancelled)
            card.order_edited.connect(self.on_order_edited)
            card.order_clicked.connect(self.on_order_clicked)
            
            tab.orders_layout.addWidget(card, row, col)
            self.order_cards[order.id] = card
            
            col += 1
            if col >= max_cols:
                col = 0
                row += 1
        
        # Add stretch to fill remaining space
        tab.orders_layout.setRowStretch(row + 1, 1)
        for i in range(max_cols):
            tab.orders_layout.setColumnStretch(i, 1)
    
    def on_order_completed(self, order):
        """Handle order completion."""
        self.refresh_orders()
        self.order_updated.emit()
    
    def on_order_cancelled(self, order):
        """Handle order cancellation."""
        self.refresh_orders()
        self.order_updated.emit()
    
    def on_order_edited(self, order):
        """Handle order editing."""
        self.refresh_orders()
        self.order_updated.emit()
    
    def on_order_clicked(self, order):
        """Handle order click - load order into cart."""
        # Find the main window to access the cart
        parent = self.parent()
        while parent and not hasattr(parent, 'pos_widget'):
            parent = parent.parent()
        
        if parent and hasattr(parent, 'pos_widget'):
            cart_widget = parent.pos_widget.cart_widget
            if hasattr(cart_widget, 'load_order'):
                cart_widget.load_order(order)
                # Switch to POS tab
                parent.sidebar.setCurrentRow(0)
    
    def __del__(self):
        """Clean up timer."""
        try:
            if hasattr(self, 'refresh_timer') and self.refresh_timer:
                self.refresh_timer.stop()
        except:
            pass  # Ignore errors during cleanup 