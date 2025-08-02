#!/usr/bin/env python3
"""
Show Users and Their Shifts
==========================

A simple script to display all users and their shift information.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from database.database_manager import DatabaseManager
from database.db_config import get_fresh_session
from models.user import User, Shift, ShiftStatus
from datetime import datetime

def show_users_and_shifts():
    """Display all users and their shifts."""
    print("👥 Users and Their Shifts Report")
    print("=" * 60)
    
    try:
        session = get_fresh_session()
        
        # Get all users
        users = session.query(User).all()
        
        if not users:
            print("❌ No users found in the database.")
            return
        
        print(f"📊 Found {len(users)} users in the system\n")
        
        for user in users:
            print(f"👤 User: {user.username}")
            print(f"   📝 Full Name: {user.full_name or 'Not specified'}")
            print(f"   🔑 Role: {user.role.value.title()}")
            print(f"   ✅ Status: {'Active' if user.active else 'Inactive'}")
            
            # Get shifts for this user
            user_shifts = session.query(Shift).filter_by(user_id=user.id).order_by(Shift.open_time.desc()).all()
            
            if user_shifts:
                print(f"   📋 Total Shifts: {len(user_shifts)}")
                print("   ┌─" + "─" * 50 + "─┐")
                
                for i, shift in enumerate(user_shifts, 1):
                    status_icon = "🟢" if shift.status == ShiftStatus.OPEN else "🔴"
                    status_text = "OPEN" if shift.status == ShiftStatus.OPEN else "CLOSED"
                    
                    print(f"   │ {i:2d}. Shift #{shift.id:3d} - {status_icon} {status_text}")
                    print(f"   │     📅 Opened: {shift.open_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    print(f"   │     💰 Opening Amount: ${shift.opening_amount:.2f}")
                    
                    if shift.close_time:
                        duration = shift.close_time - shift.open_time
                        hours = int(duration.total_seconds() // 3600)
                        minutes = int((duration.total_seconds() % 3600) // 60)
                        print(f"   │     🕐 Closed: {shift.close_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"   │     ⏱️  Duration: {hours}h {minutes}m")
                    else:
                        print(f"   │     🕐 Closed: Still Open")
                        print(f"   │     ⏱️  Duration: Ongoing")
                    
                    if i < len(user_shifts):
                        print("   │")
                
                print("   └─" + "─" * 50 + "─┘")
            else:
                print("   📋 Total Shifts: 0 (No shifts found)")
            
            print()  # Empty line between users
        
        # Summary statistics
        print("📈 Summary Statistics")
        print("=" * 60)
        
        total_shifts = session.query(Shift).count()
        open_shifts = session.query(Shift).filter_by(status=ShiftStatus.OPEN).count()
        closed_shifts = session.query(Shift).filter_by(status=ShiftStatus.CLOSED).count()
        
        print(f"📊 Total Shifts: {total_shifts}")
        print(f"🟢 Open Shifts: {open_shifts}")
        print(f"🔴 Closed Shifts: {closed_shifts}")
        
        if total_shifts > 0:
            # Find most active user
            user_shift_counts = {}
            for user in users:
                shift_count = session.query(Shift).filter_by(user_id=user.id).count()
                user_shift_counts[user.username] = shift_count
            
            most_active_user = max(user_shift_counts.items(), key=lambda x: x[1])
            print(f"👑 Most Active User: {most_active_user[0]} ({most_active_user[1]} shifts)")
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

def show_current_open_shifts():
    """Show currently open shifts."""
    print("\n🟢 Currently Open Shifts")
    print("=" * 60)
    
    try:
        session = get_fresh_session()
        
        open_shifts = session.query(Shift).filter_by(status=ShiftStatus.OPEN).all()
        
        if not open_shifts:
            print("✅ No open shifts found.")
            return
        
        print(f"📊 Found {len(open_shifts)} open shift(s)\n")
        
        for shift in open_shifts:
            user = session.query(User).filter_by(id=shift.user_id).first()
            username = user.username if user else "Unknown User"
            
            print(f"🟢 Shift #{shift.id}")
            print(f"   👤 User: {username}")
            print(f"   📅 Opened: {shift.open_time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"   💰 Opening Amount: ${shift.opening_amount:.2f}")
            print(f"   ⏱️  Duration: Ongoing")
            print()
        
        session.close()
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    print("🚀 Starting Users and Shifts Report")
    print("=" * 60)
    
    show_users_and_shifts()
    show_current_open_shifts()
    
    print("\n✅ Report completed!") 