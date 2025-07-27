from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QProgressBar
from PyQt5.QtCore import Qt, QTimer
import logging

class ClosingAmountDialog(QDialog):
    def __init__(self, parent=None, shift=None, auth_controller=None):
        super().__init__(parent)
        self.setWindowTitle('Enter Closing Amount')
        self.setFixedSize(400, 250)
        self.amount = None
        self.shift = shift
        self.auth_controller = auth_controller
        self.logger = logging.getLogger(__name__)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title_label = QLabel('Shift Closing')
        title_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # Instructions
        instruction_label = QLabel('Please enter the closing cash amount:')
        instruction_label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        layout.addWidget(instruction_label)
        
        # Amount input
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText('e.g. 1000.00')
        self.amount_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px 15px;
                font-size: 16px;
                background-color: white;
            }
            QLineEdit:focus {
                border-color: #1976d2;
                background-color: #f8f9fa;
            }
        """)
        self.amount_input.setFixedHeight(45)
        layout.addWidget(self.amount_input)
        
        # Progress bar (hidden initially)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #ccc;
                border-radius: 5px;
                text-align: center;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: #1976d2;
                border-radius: 4px;
            }
        """)
        layout.addWidget(self.progress_bar)
        
        # Status label (hidden initially)
        self.status_label = QLabel()
        self.status_label.setVisible(False)
        self.status_label.setStyleSheet("color: #7f8c8d; font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        self.cancel_btn.clicked.connect(self.reject)
        
        self.ok_btn = QPushButton('Close Shift & Generate Report')
        self.ok_btn.setStyleSheet("""
            QPushButton {
                background-color: #1976d2;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 20px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QPushButton:disabled {
                background-color: #bdbdbd;
            }
        """)
        self.ok_btn.clicked.connect(self.handle_ok)
        
        button_layout.addWidget(self.cancel_btn)
        button_layout.addWidget(self.ok_btn)
        layout.addLayout(button_layout)
        
        # Connect return pressed to handle_ok
        self.amount_input.returnPressed.connect(self.handle_ok)

    def handle_ok(self):
        try:
            value = float(self.amount_input.text())
            if value < 0:
                raise ValueError
            self.amount = value
            
            # Show progress and generate report
            self._show_progress()
            self._generate_report_and_close()
            
        except ValueError:
            QMessageBox.warning(self, 'Invalid Amount', 'Please enter a valid positive number.')

    def _show_progress(self):
        """Show progress bar and status."""
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)
        self.ok_btn.setEnabled(False)
        self.cancel_btn.setEnabled(False)
        self.amount_input.setEnabled(False)
        
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.status_label.setText("Closing shift and generating report...")
        QTimer.singleShot(100, self._update_progress)

    def _update_progress(self):
        """Update progress bar."""
        current_value = self.progress_bar.value()
        if current_value < 90:
            self.progress_bar.setValue(current_value + 10)
            QTimer.singleShot(200, self._update_progress)
        else:
            self.progress_bar.setValue(100)
            self.status_label.setText("Report generated successfully!")

    def _generate_report_and_close(self):
        """Generate Excel report and close the dialog."""
        try:
            # Close the shift first
            if self.auth_controller and self.shift:
                self.auth_controller.close_shift(self.shift.user, self.amount)
                self.logger.info(f"Shift closed for user {self.shift.user.username}")
            
            # Generate Excel report
            self._generate_excel_report()
            
            # Close dialog after a short delay to show completion
            QTimer.singleShot(1500, self.accept)
            
        except Exception as e:
            self.logger.error(f"Error during shift closing: {str(e)}")
            self.status_label.setText("Error occurred. Please try again.")
            self.ok_btn.setEnabled(True)
            self.cancel_btn.setEnabled(True)
            self.amount_input.setEnabled(True)
            self.progress_bar.setVisible(False)

    def _generate_excel_report(self):
        """Generate and open Excel report."""
        try:
            from utils.excel_report_generator import ExcelReportGenerator
            
            if not self.shift:
                self.logger.warning("No shift data available for report generation")
                return
            
            # Generate the report
            report_generator = ExcelReportGenerator()
            filepath = report_generator.generate_shift_report(self.shift, self.amount)
            
            if filepath:
                # Open the Excel file
                if report_generator.open_excel_file(filepath):
                    self.logger.info(f"Excel report opened successfully: {filepath}")
                    self.status_label.setText("Report generated and opened!")
                else:
                    self.logger.warning("Report generated but could not open automatically")
                    self.status_label.setText("Report generated! Check the reports folder.")
            else:
                self.logger.error("Failed to generate Excel report")
                self.status_label.setText("Report generation failed.")
                
        except ImportError:
            self.logger.error("Excel functionality not available. Install openpyxl: pip install openpyxl")
            self.status_label.setText("Excel functionality not available.")
        except Exception as e:
            self.logger.error(f"Error generating Excel report: {str(e)}")
            self.status_label.setText("Report generation failed.") 