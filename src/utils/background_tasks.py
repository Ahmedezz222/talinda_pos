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
from utils.localization import get_current_local_time

logger = logging.getLogger(__name__)

class BackgroundTaskManager(QObject):
    """Manager for background tasks like auto-closing orders and cleanup."""
    
    # Signals
    orders_auto_closed = pyqtSignal(int)  # Number of orders closed
    orders_cleaned_up = pyqtSignal(int)   # Number of orders cleaned up
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
        
        # Message cooldown tracking
        self.last_orders_closed_time = None
        self.last_orders_cleaned_time = None
        self.last_error_time = None
        self.message_cooldown = 300  # 5 minutes cooldown between messages
        
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
            cutoff_time = get_current_local_time() - timedelta(hours=24)
            
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
                
                # Check cooldown before emitting signal
                now = get_current_local_time()
                if (self.last_orders_closed_time is None or 
                    (now - self.last_orders_closed_time).total_seconds() > self.message_cooldown):
                    self.last_orders_closed_time = now
                    self.orders_auto_closed.emit(closed_count)
            
            # Also clean up old completed/cancelled orders
            self.cleanup_old_completed_orders()
            
        except Exception as e:
            logger.error(f"Error in check_and_close_old_orders: {e}")
            self._handle_task_error(f"Error checking old orders: {str(e)}")
    
    def cleanup_old_completed_orders(self):
        """
        Clean up completed and cancelled orders older than 24 hours.
        This method runs in the background and doesn't block the UI.
        """
        try:
            logger.debug("Checking for old completed/cancelled orders to clean up...")
            
            # Use the order controller to clean up old orders
            cleaned_count = self.order_controller.cleanup_old_completed_orders(hours_old=24)
            
            if cleaned_count > 0:
                logger.info(f"Cleaned up {cleaned_count} old completed/cancelled orders")
                
                # Check cooldown before emitting signal
                now = get_current_local_time()
                if (self.last_orders_cleaned_time is None or 
                    (now - self.last_orders_cleaned_time).total_seconds() > self.message_cooldown):
                    self.last_orders_cleaned_time = now
                    self.orders_cleaned_up.emit(cleaned_count)
            
        except Exception as e:
            logger.error(f"Error in cleanup_old_completed_orders: {e}")
            self._handle_task_error(f"Error cleaning up old orders: {str(e)}")
    
    def _handle_task_error(self, error_msg: str):
        """Handle task errors with cooldown."""
        logger.error(error_msg)
        
        # Check cooldown before emitting error signal
        current_time = get_current_local_time()
        if (self.last_error_time is None or 
            (current_time - self.last_error_time).total_seconds() > self.message_cooldown):
            self.last_error_time = current_time
            self.task_error.emit(error_msg)
        else:
            logger.debug("Skipping task_error signal due to cooldown")
    
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