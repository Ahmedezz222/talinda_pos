"""
Background task for daily sales reset at midnight.
"""
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, time, timedelta
from utils.localization import get_current_local_time
import logging
import time as time_module

logger = logging.getLogger(__name__)

class DailyResetTask(QThread):
    """Background task that resets daily sales data and closes shifts at midnight."""
    
    reset_triggered = pyqtSignal()  # Signal emitted when reset is triggered
    shift_closing_triggered = pyqtSignal(int)  # Signal emitted when shifts are closed (with count)
    
    def __init__(self):
        super().__init__()
        self.running = False
        self.last_reset_time = None
        self.reset_cooldown = 300  # 5 minutes cooldown between resets
        
    def run(self):
        """Run the daily reset task."""
        self.running = True
        logger.info("Daily reset task started")
        
        while self.running:
            try:
                # Calculate time until next midnight
                now = get_current_local_time()
                tomorrow = now.date() + timedelta(days=1)
                midnight = datetime.combine(tomorrow, time.min)
                seconds_until_midnight = (midnight - now).total_seconds()
                
                # Sleep until midnight (checking every minute)
                sleep_interval = min(60, seconds_until_midnight)  # Sleep for 1 minute or until midnight
                
                if sleep_interval > 0:
                    # Sleep in smaller intervals to allow for stopping
                    for _ in range(int(sleep_interval)):
                        if not self.running:
                            return
                        time_module.sleep(1)
                
                # Check if it's midnight
                now = get_current_local_time()
                if now.hour == 0 and now.minute == 0:
                    # Check cooldown to prevent multiple triggers
                    if (self.last_reset_time is None or 
                        (now - self.last_reset_time).total_seconds() > self.reset_cooldown):
                        
                        logger.info("Midnight reached - triggering daily sales reset and shift closing")
                        self.last_reset_time = now
                        self.reset_triggered.emit()
                        
                        # Also trigger shift closing notification if enabled
                        try:
                            from config import config
                            if config.AUTO_CLOSE_SHIFTS_AT_MIDNIGHT:
                                from controllers.shift_controller import ShiftController
                                shift_controller = ShiftController()
                                closed_count = shift_controller.close_all_open_shifts()
                                if config.SHIFT_CLOSE_NOTIFICATION_ENABLED:
                                    self.shift_closing_triggered.emit(closed_count)
                                logger.info(f"Automatically closed {closed_count} shifts at midnight")
                            else:
                                logger.info("Automatic shift closing is disabled in configuration")
                                self.shift_closing_triggered.emit(0)
                        except Exception as e:
                            logger.error(f"Error in automatic shift closing: {e}")
                            self.shift_closing_triggered.emit(0)
                        
                        # Sleep for 2 minutes to avoid multiple triggers
                        for _ in range(120):
                            if not self.running:
                                return
                            time_module.sleep(1)
                    else:
                        logger.debug("Daily reset skipped due to cooldown")
                        # Sleep for 1 minute before next check
                        for _ in range(60):
                            if not self.running:
                                return
                            time_module.sleep(1)
                else:
                    # Sleep for 1 minute before next check
                    for _ in range(60):
                        if not self.running:
                            return
                        time_module.sleep(1)
                        
            except Exception as e:
                logger.error(f"Error in daily reset task: {e}")
                # Sleep for 1 minute before retrying
                for _ in range(60):
                    if not self.running:
                        return
                    time_module.sleep(1)
            
    def stop(self):
        """Stop the daily reset task."""
        self.running = False
        logger.info("Daily reset task stopped") 