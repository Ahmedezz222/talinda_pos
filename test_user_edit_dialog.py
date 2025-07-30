#!/usr/bin/env python3
"""
Test User Edit Dialog Script
============================

This script tests the user edit dialog to ensure it works correctly.
"""

import sys
from pathlib import Path

# Add src directory to path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication
from database.db_config import Session
from models.user import User
from ui.components.user_edit_dialog import UserEditDialog

def test_user_edit_dialog():
    """Test the user edit dialog."""
    app = QApplication(sys.argv)
    
    # Get the admin user
    session = Session()
    admin_user = session.query(User).filter_by(username='admin').first()
    
    if admin_user:
        print("Testing User Edit Dialog...")
        print(f"Admin user found: {admin_user.username}")
        
        # Test edit dialog
        dialog = UserEditDialog(user=admin_user)
        result = dialog.exec_()
        
        if result == UserEditDialog.Accepted:
            print("✅ User edit dialog accepted")
        else:
            print("❌ User edit dialog cancelled")
    else:
        print("❌ Admin user not found!")
    
    session.close()
    app.quit()

if __name__ == "__main__":
    test_user_edit_dialog() 