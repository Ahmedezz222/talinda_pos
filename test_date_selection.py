#!/usr/bin/env python3
"""
Test script for date selection in shift report
"""

import sys
from pathlib import Path
from datetime import datetime, date

# Add the src directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir / "src"))

from database.database_manager import DatabaseManager

def test_date_selection():
    """Test the date selection functionality."""
    print("Testing date selection in shift report...")
    
    db_manager = DatabaseManager()
    
    # Test getting shifts for today
    today = date.today()
    print(f"\nTesting shifts for today ({today}):")
    shifts_today = db_manager.get_shifts_by_date(today)
    print(f"Found {len(shifts_today)} shifts for today")
    
    for shift in shifts_today:
        print(f"  - Shift #{shift['shift_id']} by {shift['username']} at {shift['open_time'].strftime('%H:%M')}")
    
    # Test getting shifts for yesterday
    yesterday = date.today().replace(day=date.today().day - 1)
    print(f"\nTesting shifts for yesterday ({yesterday}):")
    shifts_yesterday = db_manager.get_shifts_by_date(yesterday)
    print(f"Found {len(shifts_yesterday)} shifts for yesterday")
    
    for shift in shifts_yesterday:
        print(f"  - Shift #{shift['shift_id']} by {shift['username']} at {shift['open_time'].strftime('%H:%M')}")
    
    # Test getting all shifts for comparison
    print(f"\nTesting all shifts:")
    all_shifts = db_manager.get_all_shifts()
    print(f"Found {len(all_shifts)} total shifts")
    
    print("\nDate selection test completed!")

if __name__ == "__main__":
    test_date_selection() 