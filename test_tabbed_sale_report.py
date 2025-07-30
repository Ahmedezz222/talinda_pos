#!/usr/bin/env python3
"""
Test script for the Tabbed Simple Sale Report Dialog.
"""
import sys
import os
from datetime import date, timedelta
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import QDate
from ui.components.simple_sale_report_dialog import SimpleSaleReportDialog
from controllers.shift_controller import ShiftController
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TabbedSaleReportTest(QMainWindow):
    """Test window for the Tabbed Simple Sale Report Dialog."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tabbed Sale Report Test")
        self.setGeometry(100, 100, 400, 300)
        self.shift_controller = ShiftController()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the test UI."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)
        
        # Title
        title = QLabel("Tabbed Sale Report Test")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "This test demonstrates the new tabbed simple sale report dialog. "
            "Click any button below to open the tabbed sale report for different dates."
        )
        description.setStyleSheet("""
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 30px;
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Test buttons
        self.create_test_button(layout, "Today's Report", date.today())
        self.create_test_button(layout, "Yesterday's Report", date.today() - timedelta(days=1))
        self.create_test_button(layout, "Last Week's Report", date.today() - timedelta(days=7))
        
        # Status label
        self.status_label = QLabel("Ready to test tabbed sale reports")
        self.status_label.setStyleSheet("""
            font-size: 12px;
            color: #95a5a6;
            font-style: italic;
            margin-top: 20px;
        """)
        layout.addWidget(self.status_label)
    
    def create_test_button(self, layout, label, target_date):
        """Create a test button for a specific date."""
        button = QPushButton(f"📊 {label} ({target_date.strftime('%Y-%m-%d')})")
        button.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #7d3c98;
            }
        """)
        button.clicked.connect(lambda: self.test_tabbed_report(target_date))
        layout.addWidget(button)
    
    def test_tabbed_report(self, target_date):
        """Test the tabbed sale report for a specific date."""
        try:
            self.status_label.setText(f"Testing tabbed report for {target_date.strftime('%Y-%m-%d')}...")
            
            # Generate report data for the target date
            report_data = self.shift_controller.get_daily_sales_report(target_date)
            
            # Create and show the tabbed simple sale report dialog
            dialog = SimpleSaleReportDialog(report_data=report_data)
            
            # Set the dialog's date to match the target date
            dialog.date_edit.setDate(QDate(target_date.year, target_date.month, target_date.day))
            
            # Show the dialog
            dialog.exec_()
            
            self.status_label.setText(f"Tabbed report test completed for {target_date.strftime('%Y-%m-%d')}")
            logger.info(f"Tabbed sale report test completed successfully for {target_date}")
            
        except Exception as e:
            logger.error(f"Error testing tabbed report for {target_date}: {e}")
            self.status_label.setText(f"Error testing report: {str(e)}")

def main():
    """Main function to run the tabbed sale report test."""
    print("🚀 Starting Tabbed Sale Report Test")
    print("=" * 50)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create and show the test window
        test_window = TabbedSaleReportTest()
        test_window.show()
        
        print("✅ Tabbed sale report test window opened successfully!")
        print("📋 Test Instructions:")
        print("   1. Click any test button to open the tabbed sale report")
        print("   2. Verify the new tabbed interface with 3 tabs:")
        print("      - 📊 Summary Tab: Key metrics")
        print("      - 👥 Cashier Shifts Tab: Shift details")
        print("      - 🛒 Sales Details Tab: Transaction details")
        print("   3. Test switching between tabs")
        print("   4. Test the date picker functionality")
        print("   5. Test the refresh button")
        print("\n🎯 The tabbed sale report should be well-organized and easy to navigate!")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 