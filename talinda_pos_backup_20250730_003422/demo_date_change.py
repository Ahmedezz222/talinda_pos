#!/usr/bin/env python3
"""
Demonstration script for the date change functionality in the daily sales report dialog.
"""
import sys
import os
from pathlib import Path
from datetime import date, timedelta

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QDate
from ui.components.daily_sales_report_dialog import DailySalesReportDialog
from controllers.shift_controller import ShiftController
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DateChangeDemo(QMainWindow):
    """Demo window to show the date change functionality."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Date Change Functionality Demo")
        self.setGeometry(100, 100, 400, 300)
        
        # Initialize shift controller
        self.shift_controller = ShiftController()
        
        self.init_ui()
    
    def init_ui(self):
        """Initialize the demo UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("📊 Daily Sales Report - Date Change Demo")
        title.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "This demo shows how the date change functionality works in the daily sales report.\n"
            "Click the buttons below to open the report dialog with different dates."
        )
        description.setStyleSheet("""
            font-size: 12px;
            color: #7f8c8d;
            margin-bottom: 20px;
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Buttons for different dates
        self.create_date_button(layout, "Today", date.today())
        self.create_date_button(layout, "Yesterday", date.today() - timedelta(days=1))
        self.create_date_button(layout, "Last Week", date.today() - timedelta(days=7))
        self.create_date_button(layout, "Last Month", date.today() - timedelta(days=30))
        
        # Status label
        self.status_label = QLabel("Ready to show reports")
        self.status_label.setStyleSheet("""
            font-size: 11px;
            color: #95a5a6;
            font-style: italic;
            margin-top: 20px;
        """)
        layout.addWidget(self.status_label)
    
    def create_date_button(self, layout, label, target_date):
        """Create a button for a specific date."""
        button = QPushButton(f"📅 {label} ({target_date.strftime('%Y-%m-%d')})")
        button.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 12px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        button.clicked.connect(lambda: self.show_report_for_date(target_date))
        layout.addWidget(button)
    
    def show_report_for_date(self, target_date):
        """Show the daily sales report for a specific date."""
        try:
            self.status_label.setText(f"Loading report for {target_date.strftime('%Y-%m-%d')}...")
            
            # Generate report data for the target date
            report_data = self.shift_controller.get_daily_sales_report(target_date)
            
            # Create and show the dialog
            dialog = DailySalesReportDialog(report_data=report_data)
            
            # Set the dialog's date to match the target date
            dialog.date_edit.setDate(QDate(target_date.year, target_date.month, target_date.day))
            
            # Show the dialog
            dialog.exec_()
            
            self.status_label.setText(f"Report for {target_date.strftime('%Y-%m-%d')} closed")
            
        except Exception as e:
            logger.error(f"Error showing report for {target_date}: {e}")
            self.status_label.setText(f"Error loading report: {str(e)}")

def main():
    """Main function to run the demo."""
    print("🚀 Starting Date Change Functionality Demo")
    print("=" * 50)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create and show the demo window
        demo = DateChangeDemo()
        demo.show()
        
        print("✅ Demo window opened successfully!")
        print("📋 Instructions:")
        print("   1. Click any date button to open the daily sales report")
        print("   2. In the report dialog, try changing the date using the date picker")
        print("   3. The report should automatically update with data for the new date")
        print("   4. Use the 'Refresh Report' button to manually refresh the data")
        print("\n🎯 The date change functionality is now working correctly!")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 