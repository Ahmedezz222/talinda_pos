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
        
        # Add tooltip for completed orders
        if self.order.status == OrderStatus.COMPLETED:
            self.setToolTip("Click to load this completed order into cart for checkout")
        
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
        
        # Get a session to access product categories
        from database.db_config import get_fresh_session
        session = get_fresh_session()
        
        try:
            for item in order_items:
                product = item['product']
                item_total = item['price'] * item['quantity']
                tax_rate = 0.0
                
                # Get product with category from session to avoid lazy loading issues
                try:
                    from models.product import Product
                    session_product = session.query(Product).filter_by(id=product.id).first()
                    if session_product and hasattr(session_product, 'category') and session_product.category:
                        tax_rate = getattr(session_product.category, 'tax_rate', 0.0)
                except Exception as e:
                    # If we can't get the category, just use 0 tax rate
                    tax_rate = 0.0
                
                items_text += f"• {product.name} x{item['quantity']} - ${item['price']:.2f}\n"
                items_text += f"  Subtotal: ${item_total:.2f}"
                if tax_rate > 0:
                    item_tax = item_total * (tax_rate / 100.0)
                    items_text += f" (Tax: {tax_rate}% = ${item_tax:.2f})"
                items_text += "\n"
                
                if item.get('notes'):
                    items_text += f"  Note: {item['notes']}\n"
        finally:
            session.close()
        
        if items_text:
            items_display = QLabel(items_text)
            items_display.setStyleSheet("color: #555; font-size: 12px; margin-left: 10px;")
            items_display.setWordWrap(True)
            layout.addWidget(items_display)
        
        # Order totals breakdown
        totals_layout = QVBoxLayout()
        totals_layout.setSpacing(2)
        
        # Subtotal
        subtotal_label = QLabel(f"Subtotal: ${self.order.subtotal:.2f}")
        subtotal_label.setStyleSheet("color: #555; font-size: 12px;")
        totals_layout.addWidget(subtotal_label)
        
        # Tax amount
        if self.order.tax_amount > 0:
            tax_label = QLabel(f"Tax: ${self.order.tax_amount:.2f}")
            tax_label.setStyleSheet("color: #e67e22; font-size: 12px;")
            totals_layout.addWidget(tax_label)
        
        # Discount amount
        if self.order.discount_amount > 0:
            discount_label = QLabel(f"Discount: -${self.order.discount_amount:.2f}")
            discount_label.setStyleSheet("color: #e74c3c; font-size: 12px;")
            totals_layout.addWidget(discount_label)
        
        # Total amount
        total_label = QLabel(f"Total: ${self.order.total_amount:.2f}")
        total_label.setStyleSheet("font-weight: bold; color: #27ae60; font-size: 15px; margin-top: 5px;")
        totals_layout.addWidget(total_label)
        
        layout.addLayout(totals_layout)
        
        # Time created
        time_label = QLabel(f"Created: {self.order.created_at.strftime('%I:%M:%S %p')}")
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
        elif self.order.status == OrderStatus.COMPLETED:
            # Add a note for completed orders that they can be clicked to load into cart
            note_label = QLabel("💡 Click to load into cart for checkout")
            note_label.setStyleSheet("""
                color: #f39c12;
                font-style: italic;
                font-size: 11px;
                margin-top: 5px;
                text-align: center;
            """)
            layout.addWidget(note_label)
    
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
            # Allow clicking on active and completed orders to load into cart
            if self.order.status in [OrderStatus.ACTIVE, OrderStatus.COMPLETED]:
                self.order_clicked.emit(self.order)
        try:
            super().mousePressEvent(event)
        except RuntimeError:
            # Widget has been deleted, ignore
            pass


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


class OrderResetDialog(QDialog):
    """Dialog for resetting the order manager."""
    
    def __init__(self, user: User, parent=None):
        super().__init__(parent)
        self.user = user
        self.reset_type = "all"
        self.setWindowTitle("Reset Order Manager")
        self.setFixedSize(450, 350)
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout(self)
        
        # Warning message
        warning_label = QLabel("⚠️ WARNING: This action cannot be undone!")
        warning_label.setStyleSheet("""
            color: #e74c3c;
            font-weight: bold;
            font-size: 14px;
            padding: 10px;
            background-color: #fdf2f2;
            border: 1px solid #e74c3c;
            border-radius: 5px;
        """)
        layout.addWidget(warning_label)
        
        # Sales report info
        sales_report_info = QLabel("📊 Note: Orders will be archived instead of deleted to preserve sales report data.")
        sales_report_info.setStyleSheet("""
            color: #27ae60;
            font-weight: bold;
            font-size: 12px;
            padding: 8px;
            background-color: #e8f5e8;
            border: 1px solid #27ae60;
            border-radius: 5px;
            margin: 5px 0;
        """)
        layout.addWidget(sales_report_info)
        
        # Description
        desc_label = QLabel("Select what you want to reset in the order manager:")
        desc_label.setStyleSheet("font-size: 12px; color: #666; margin: 10px 0;")
        layout.addWidget(desc_label)
        
        # Reset options
        from PyQt5.QtWidgets import QRadioButton, QButtonGroup
        
        self.radio_group = QButtonGroup()
        
        # All orders option
        all_radio = QRadioButton("Archive All Orders (Active, Completed, Cancelled, Old)")
        all_radio.setChecked(True)
        all_radio.setStyleSheet("font-weight: bold; color: #e74c3c;")
        self.radio_group.addButton(all_radio, 0)
        layout.addWidget(all_radio)
        
        # Active orders option
        active_radio = QRadioButton("Archive Active Orders Only")
        active_radio.setStyleSheet("color: #3498db;")
        self.radio_group.addButton(active_radio, 1)
        layout.addWidget(active_radio)
        
        # Completed orders option
        completed_radio = QRadioButton("Archive Completed Orders Only")
        completed_radio.setStyleSheet("color: #27ae60;")
        self.radio_group.addButton(completed_radio, 2)
        layout.addWidget(completed_radio)
        
        # Cancelled orders option
        cancelled_radio = QRadioButton("Archive Cancelled Orders Only")
        cancelled_radio.setStyleSheet("color: #f39c12;")
        self.radio_group.addButton(cancelled_radio, 3)
        layout.addWidget(cancelled_radio)
        
        # Old orders option
        old_radio = QRadioButton("Clean Up Old Orders (Older than 24 hours)")
        old_radio.setStyleSheet("color: #9b59b6;")
        self.radio_group.addButton(old_radio, 4)
        layout.addWidget(old_radio)
        
        # Connect radio buttons
        self.radio_group.buttonClicked.connect(self.on_radio_changed)
        
        # Current stats
        stats_group = QGroupBox("Current Order Statistics")
        stats_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #ddd;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
            }
        """)
        stats_layout = QVBoxLayout(stats_group)
        
        self.stats_label = QLabel("Loading statistics...")
        self.stats_label.setStyleSheet("font-size: 11px; color: #666;")
        stats_layout.addWidget(self.stats_label)
        
        layout.addWidget(stats_group)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset Orders")
        reset_btn.clicked.connect(self.confirm_reset)
        reset_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: bold;
        """)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet("""
            background-color: #95a5a6;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
        """)
        
        btn_layout.addWidget(reset_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addLayout(btn_layout)
        
        # Load current stats
        self.load_stats()
    
    def on_radio_changed(self, button):
        """Handle radio button selection change."""
        button_id = self.radio_group.id(button)
        reset_types = ["all", "active", "completed", "cancelled", "old"]
        self.reset_type = reset_types[button_id]
    
    def load_stats(self):
        """Load and display current order statistics."""
        try:
            from controllers.order_controller import OrderController
            order_controller = OrderController()
            stats = order_controller.get_order_manager_stats()
            
            stats_text = f"""
            Active Orders: {stats['active_orders']}
            Completed Orders: {stats['completed_orders']}
            Cancelled Orders: {stats['cancelled_orders']}
            Today's Orders: {stats['today_orders']}
            Total Orders: {stats['total_orders']}
            """
            
            self.stats_label.setText(stats_text)
        except Exception as e:
            self.stats_label.setText("Error loading statistics")
    
    def confirm_reset(self):
        """Confirm the reset operation."""
        # Show confirmation dialog
        reset_types = {
            "all": "ALL ORDERS (Active, Completed, Cancelled, and Old)",
            "active": "ACTIVE ORDERS ONLY",
            "completed": "COMPLETED ORDERS ONLY", 
            "cancelled": "CANCELLED ORDERS ONLY",
            "old": "OLD ORDERS (Older than 24 hours)"
        }
        
        reset_type_name = reset_types.get(self.reset_type, self.reset_type.upper())
        
        reply = QMessageBox.question(
            self,
            "Confirm Reset",
            f"Are you absolutely sure you want to archive {reset_type_name}?\n\n"
            "Orders will be archived (not deleted) to preserve sales report data.\n"
            "This action cannot be undone!",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.accept()
        else:
            self.reject()


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
        
        # Today's order count
        self.today_count_label = QLabel("Today: 0")
        self.today_count_label.setStyleSheet("""
            color: #27ae60;
            font-weight: bold;
            font-size: 14px;
            padding: 5px 10px;
            background-color: #e8f5e8;
            border-radius: 5px;
        """)
        header_layout.addWidget(self.today_count_label)
        
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
        

        
        # Reset button - only show for admin users
        if self.user.role.value == "admin":
            reset_btn = QPushButton("Reset")
            reset_btn.clicked.connect(self.show_reset_dialog)
            reset_btn.setStyleSheet("""
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-weight: bold;
            """)
            header_layout.addWidget(reset_btn)
        
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
        
        # Update today's order count
        self.update_today_count()
        
        # Emit signal that orders were updated
        self.order_updated.emit()
    
    def update_today_count(self):
        """Update the today's order count display."""
        try:
            today_count = self.order_controller.get_today_order_count()
            self.today_count_label.setText(f"Today: {today_count}")
        except Exception as e:
            logger.error(f"Error updating today's order count: {e}")
            self.today_count_label.setText("Today: ?")
    
    def force_refresh(self):
        """Force a complete refresh of the order list."""
        self.refresh_orders()
    
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
                if hasattr(parent, 'sidebar'):
                    parent.sidebar.setCurrentRow(0)
                QMessageBox.information(self, "Order Loaded", f"Order {order.order_number} loaded into cart!")
            else:
                QMessageBox.warning(self, "Error", "Cart widget does not support loading orders.")
        else:
            QMessageBox.warning(self, "Error", "Could not find cart widget.")
    


    def show_reset_dialog(self):
        """Show the order reset dialog."""
        dialog = OrderResetDialog(self.user, self)
        if dialog.exec_() == QDialog.Accepted:
            reset_type = dialog.reset_type
            
            # Perform the reset
            results = self.order_controller.reset_order_manager(reset_type, self.user)
            
            if results["success"]:
                # Show success message with details
                total_archived = (results["active_archived"] + results["completed_archived"] + 
                                results["cancelled_archived"])
                
                message = f"Order manager reset completed successfully!\n\n"
                message += f"Orders archived:\n"
                message += f"• Active: {results['active_archived']}\n"
                message += f"• Completed: {results['completed_archived']}\n"
                message += f"• Cancelled: {results['cancelled_archived']}\n"
                message += f"• Old orders cleared: {results['old_cleared']}\n"
                message += f"• Total archived: {total_archived}"
                message += f"\n\n📊 Note: Order data is preserved for sales reports!"
                
                if results["errors"]:
                    message += f"\n\nWarnings: {len(results['errors'])} errors occurred during reset."
                
                QMessageBox.information(self, "Reset Complete", message)
            else:
                # Show error message
                error_message = "Failed to reset order manager:\n\n"
                for error in results["errors"]:
                    error_message += f"• {error}\n"
                
                QMessageBox.critical(self, "Reset Failed", error_message)
            
            # Refresh the order display
            self.refresh_orders()
            self.order_updated.emit()
    
    def __del__(self):
        """Clean up timer."""
        try:
            if hasattr(self, 'refresh_timer') and self.refresh_timer:
                self.refresh_timer.stop()
        except:
            pass  # Ignore errors during cleanup 