"""
Time utilities for Talinda POS application.
Provides functions for time synchronization and validation.
"""

import time
import logging
from datetime import datetime
from typing import Optional, Tuple
from PyQt5.QtCore import QDateTime, QTimer

logger = logging.getLogger(__name__)

def get_system_time() -> QDateTime:
    """
    Get the current system time with validation.
    
    Returns:
        QDateTime: Current system time
    """
    try:
        current_time = QDateTime.currentDateTime()
        
        if not current_time.isValid():
            logger.warning("Invalid system time detected, attempting to fix...")
            # Try to get time from Python's datetime as fallback
            python_time = datetime.now()
            current_time = QDateTime.fromString(
                python_time.strftime("%Y-%m-%d %H:%M:%S"), 
                "yyyy-MM-dd hh:mm:ss"
            )
            
            if not current_time.isValid():
                logger.error("Failed to get valid system time")
                return QDateTime()
        
        return current_time
        
    except Exception as e:
        logger.error(f"Error getting system time: {e}")
        return QDateTime()

def format_time_12hour(dt: QDateTime) -> str:
    """
    Format QDateTime to 12-hour format with AM/PM.
    
    Args:
        dt: QDateTime object
        
    Returns:
        str: Formatted time string
    """
    if not dt.isValid():
        return "--:--:-- --"
    
    return dt.toString("hh:mm:ss AP")

def format_datetime_12hour(dt: QDateTime) -> str:
    """
    Format QDateTime to include date and 12-hour time.
    
    Args:
        dt: QDateTime object
        
    Returns:
        str: Formatted datetime string
    """
    if not dt.isValid():
        return "Invalid Date/Time"
    
    return dt.toString("yyyy-MM-dd hh:mm:ss AP")

def validate_system_time() -> Tuple[bool, str]:
    """
    Validate that the system time is reasonable.
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        current_time = get_system_time()
        
        if not current_time.isValid():
            return False, "System time is invalid"
        
        # Check if time is in reasonable range (not too far in past or future)
        current_year = current_time.date().year()
        if current_year < 2020 or current_year > 2030:
            return False, f"System year {current_year} is outside reasonable range"
        
        return True, "System time is valid"
        
    except Exception as e:
        return False, f"Error validating system time: {e}"

def sync_time_display(timer: QTimer, update_callback) -> bool:
    """
    Synchronize time display with system time.
    
    Args:
        timer: QTimer object
        update_callback: Function to call for time updates
        
    Returns:
        bool: True if synchronization successful
    """
    try:
        # Stop existing timer
        if timer.isActive():
            timer.stop()
        
        # Validate system time first
        is_valid, error_msg = validate_system_time()
        if not is_valid:
            logger.warning(f"System time validation failed: {error_msg}")
            # Continue anyway, but log the warning
        
        # Set up precise timer
        timer.setTimerType(QTimer.PreciseTimer)
        timer.timeout.connect(update_callback)
        timer.start(1000)  # Update every second
        
        # Initial update
        update_callback()
        
        logger.info("Time display synchronized successfully")
        return True
        
    except Exception as e:
        logger.error(f"Failed to synchronize time display: {e}")
        return False

def get_time_difference(time1: QDateTime, time2: QDateTime) -> int:
    """
    Get the difference in seconds between two QDateTime objects.
    
    Args:
        time1: First QDateTime
        time2: Second QDateTime
        
    Returns:
        int: Difference in seconds (positive if time2 > time1)
    """
    if not time1.isValid() or not time2.isValid():
        return 0
    
    return time1.secsTo(time2) 