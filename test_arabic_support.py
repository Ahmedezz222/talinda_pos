#!/usr/bin/env python3
"""Test Arabic text logging and display support."""

import os
import sys
import logging
from pathlib import Path

# Add src directory to Python path for imports
src_dir = Path(__file__).parent / 'src'
if src_dir not in sys.path:
    sys.path.insert(0, str(src_dir))

from config import get_config
from main import LoggingConfig

def test_arabic_logging():
    """Test logging Arabic text."""
    # Initialize logging with UTF-8 support
    LoggingConfig.setup_logging()
    logger = logging.getLogger(__name__)
    
    # Test Arabic text
    arabic_text = "مرحبا بكم في نظام نقاط البيع"  # "Welcome to POS system" in Arabic
    arabic_product = "قهوة عربية"  # "Arabic coffee" in Arabic
    arabic_category = "مشروبات"  # "Beverages" in Arabic
    
    # Log Arabic text
    logger.info(f"Testing Arabic text: {arabic_text}")
    logger.info(f"Product name: {arabic_product}")
    logger.info(f"Category name: {arabic_category}")
    
    # Verify log file encoding
    log_file = Path("logs/talinda_pos.log")
    if log_file.exists():
        with open(log_file, 'r', encoding='utf-8') as f:
            last_lines = f.readlines()[-3:]  # Get last 3 lines
            
        print("\nVerifying last 3 log lines:")
        for line in last_lines:
            print(line.strip())
    else:
        print("Log file not found!")

if __name__ == "__main__":
    test_arabic_logging()
