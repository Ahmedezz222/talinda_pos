#!/usr/bin/env python3
"""
Test script for Cashier Shift Details in Simple Sale Report.
"""
import sys
import os
from datetime import date, timedelta, datetime
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QTextEdit
from PyQt5.QtCore import QDate
from controllers.shift_controller import ShiftController
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CashierShiftsTest(QMainWindow):
    """Test window for Cashier Shift Details."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cashier Shifts Test")
        self.setGeometry(100, 100, 600, 500)
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
        title = QLabel("Cashier Shift Details Test")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # Description
        description = QLabel(
            "This test demonstrates the cashier shift details functionality. "
            "Click the button below to test the shift data generation."
        )
        description.setStyleSheet("""
            font-size: 14px;
            color: #7f8c8d;
            margin-bottom: 30px;
        """)
        description.setWordWrap(True)
        layout.addWidget(description)
        
        # Test button
        self.test_btn = QPushButton("🧪 Test Cashier Shift Details")
        self.test_btn.clicked.connect(self.test_cashier_shifts)
        self.test_btn.setStyleSheet("""
            QPushButton {
                background-color: #e67e22;
                color: white;
                border: none;
                padding: 15px 25px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d35400;
            }
        """)
        layout.addWidget(self.test_btn)
        
        # Results display
        self.results_display = QTextEdit()
        self.results_display.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bdc3c7;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 12px;
                background-color: #f8f9fa;
            }
        """)
        self.results_display.setPlaceholderText("Test results will appear here...")
        layout.addWidget(self.results_display)
        
        # Status label
        self.status_label = QLabel("Ready to test cashier shift details")
        self.status_label.setStyleSheet("""
            font-size: 12px;
            color: #95a5a6;
            font-style: italic;
            margin-top: 20px;
        """)
        layout.addWidget(self.status_label)
    
    def test_cashier_shifts(self):
        """Test the cashier shift details functionality."""
        try:
            self.status_label.setText("Testing cashier shift details...")
            self.test_btn.setEnabled(False)
            self.test_btn.setText("⏳ Testing...")
            
            # Get report data for today
            today = date.today()
            report_data = self.shift_controller.get_daily_sales_report(today)
            
            # Extract shift information
            shifts = report_data.get('shifts', [])
            
            # Display results
            results = f"Cashier Shift Details Test Results\n"
            results += f"Date: {today.strftime('%Y-%m-%d')}\n"
            results += f"Total Shifts Found: {len(shifts)}\n\n"
            
            if shifts:
                results += "Shift Details:\n"
                results += "-" * 80 + "\n"
                
                for i, shift in enumerate(shifts, 1):
                    results += f"Shift {i}:\n"
                    results += f"  Cashier: {shift.get('user', 'Unknown')}\n"
                    results += f"  Opening Amount: ${shift.get('opening_amount', 0):.2f}\n"
                    results += f"  Open Time: {shift.get('open_time', 'N/A')}\n"
                    results += f"  Close Time: {shift.get('close_time', 'N/A')}\n"
                    results += f"  Duration: {shift.get('duration', 'N/A')}\n"
                    results += f"  Status: {shift.get('status', 'Unknown')}\n"
                    results += f"  Total Sales: ${shift.get('total_sales', 0):.2f}\n"
                    results += f"  Sales Count: {shift.get('sales_count', 0)}\n"
                    results += "-" * 40 + "\n"
            else:
                results += "No shifts found for today.\n"
                results += "This is normal if no shifts have been opened yet.\n"
            
            # Add summary information
            results += f"\nSummary Information:\n"
            results += f"Total Sales: {report_data.get('total_sales', 0)}\n"
            results += f"Total Amount: ${report_data.get('total_amount', 0):.2f}\n"
            results += f"Average Transaction: ${report_data.get('average_transaction', 0):.2f}\n"
            
            self.results_display.setText(results)
            self.status_label.setText("Cashier shift details test completed successfully!")
            logger.info("Cashier shift details test completed successfully")
            
        except Exception as e:
            error_msg = f"Error testing cashier shift details: {str(e)}"
            self.results_display.setText(f"ERROR:\n{error_msg}")
            self.status_label.setText("Error occurred during test")
            logger.error(error_msg)
        finally:
            self.test_btn.setEnabled(True)
            self.test_btn.setText("🧪 Test Cashier Shift Details")

def main():
    """Main function to run the cashier shifts test."""
    print("🚀 Starting Cashier Shift Details Test")
    print("=" * 50)
    
    try:
        # Create QApplication
        app = QApplication(sys.argv)
        
        # Create and show the test window
        test_window = CashierShiftsTest()
        test_window.show()
        
        print("✅ Cashier shift details test window opened successfully!")
        print("📋 Test Instructions:")
        print("   1. Click the 'Test Cashier Shift Details' button")
        print("   2. Review the shift data in the results display")
        print("   3. Verify that shift information includes total sales")
        print("   4. Check that all shift fields are populated correctly")
        print("\n🎯 The cashier shift details should show comprehensive shift information!")
        
        # Run the application
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 