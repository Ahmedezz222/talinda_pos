"""
Background task for daily sales reset at midnight.
"""
from PyQt5.QtCore import QThread, pyqtSignal
from datetime import datetime, time, timedelta
import logging
import time as time_module

logger = logging.getLogger(__name__)

class DailyResetTask(QThread):
    """Background task that resets daily sales data at midnight."""
    
    reset_triggered = pyqtSignal()  # Signal emitted when reset is triggered
    
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
                now = datetime.now()
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
                now = datetime.now()
                if now.hour == 0 and now.minute == 0:
                    # Check cooldown to prevent multiple triggers
                    if (self.last_reset_time is None or 
                        (now - self.last_reset_time).total_seconds() > self.reset_cooldown):
                        
                        logger.info("Midnight reached - triggering daily sales reset")
                        self.last_reset_time = now
                        self.reset_triggered.emit()
                        
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