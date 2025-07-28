"""
Background task manager for automatic operations.
"""
import logging
import threading
import time
from datetime import datetime, timedelta, timezone
from typing import Optional
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from database.db_config import get_fresh_session
from models.order import Order, OrderStatus
from controllers.order_controller import OrderController

logger = logging.getLogger(__name__)

class BackgroundTaskManager(QObject):
    """Manager for background tasks like auto-closing orders."""
    
    # Signals
    orders_auto_closed = pyqtSignal(int)  # Number of orders closed
    task_error = pyqtSignal(str)  # Error message
    
    def __init__(self, check_interval_minutes: int = 60):
        """
        Initialize the background task manager.
        
        Args:
            check_interval_minutes: How often to check for old orders (default: 60 minutes)
        """
        super().__init__()
        self.check_interval_minutes = check_interval_minutes
        self.timer = QTimer()
        self.timer.timeout.connect(self.check_and_close_old_orders)
        self.order_controller = OrderController()
        self.is_running = False
        
        logger.info(f"Background task manager initialized with {check_interval_minutes} minute interval")
    
    def start(self):
        """Start the background task manager."""
        if not self.is_running:
            self.timer.start(self.check_interval_minutes * 60 * 1000)  # Convert to milliseconds
            self.is_running = True
            logger.info("Background task manager started")
            
            # Run initial check
            self.check_and_close_old_orders()
    
    def stop(self):
        """Stop the background task manager."""
        if self.is_running:
            self.timer.stop()
            self.is_running = False
            logger.info("Background task manager stopped")
    
    def check_and_close_old_orders(self):
        """
        Check for orders older than 24 hours and close them automatically.
        This method runs in the background and doesn't block the UI.
        """
        try:
            logger.debug("Checking for old orders to auto-close...")
            
            # Get a fresh session for this operation
            session = get_fresh_session()
            
            # Calculate the cutoff time (24 hours ago)
            cutoff_time = datetime.now(timezone.utc) - timedelta(hours=24)
            
            # Find active orders older than 24 hours
            old_orders = session.query(Order).filter(
                Order.status == OrderStatus.ACTIVE,
                Order.created_at < cutoff_time
            ).all()
            
            closed_count = 0
            
            for order in old_orders:
                try:
                    # Mark order as completed
                    order.complete_order()
                    closed_count += 1
                    logger.info(f"Auto-closed order {order.order_number} (created: {order.created_at})")
                    
                except Exception as e:
                    logger.error(f"Error auto-closing order {order.order_number}: {e}")
                    continue
            
            # Commit all changes
            session.commit()
            session.close()
            
            if closed_count > 0:
                logger.info(f"Auto-closed {closed_count} orders older than 24 hours")
                self.orders_auto_closed.emit(closed_count)
            else:
                logger.debug("No orders found for auto-closure")
                
        except Exception as e:
            error_msg = f"Error in background order check: {e}"
            logger.error(error_msg)
            self.task_error.emit(error_msg)
    
    def force_check_now(self):
        """Force an immediate check for old orders (for testing or manual trigger)."""
        logger.info("Forcing immediate check for old orders")
        self.check_and_close_old_orders()
    
    def get_status(self) -> dict:
        """
        Get the current status of the background task manager.
        
        Returns:
            dict: Status information
        """
        return {
            'is_running': self.is_running,
            'check_interval_minutes': self.check_interval_minutes,
            'next_check_in': self.timer.remainingTime() / 1000 / 60 if self.is_running else None
        } 