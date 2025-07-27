#!/usr/bin/env python3
"""
Excel Report Generator for Talinda POS System
============================================

Generates comprehensive Excel reports for shift summaries including:
- Opening amount
- All product sales during the shift
- Closing amount
- Sales totals and statistics

Author: Talinda POS Team
Version: 1.0.0
"""

import os
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from database.db_config import get_fresh_session
from models.user import Shift, User
from models.sale import Sale, sale_products
from models.product import Product
from sqlalchemy import func, and_

try:
    import openpyxl
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter
    from openpyxl.worksheet.worksheet import Worksheet
    EXCEL_AVAILABLE = True
except ImportError:
    EXCEL_AVAILABLE = False
    logging.warning("openpyxl not available. Excel reports will not be generated.")

logger = logging.getLogger(__name__)


class ExcelReportGenerator:
    """Generates Excel reports for shift summaries."""
    
    def __init__(self):
        """Initialize the Excel report generator."""
        self.session = get_fresh_session()
        self.reports_dir = Path("reports")
        self.reports_dir.mkdir(exist_ok=True)
        
        # Excel styling constants
        self.header_font = Font(bold=True, size=12, color="FFFFFF")
        self.header_fill = PatternFill(start_color="1976D2", end_color="1976D2", fill_type="solid")
        self.subheader_font = Font(bold=True, size=11, color="2C3E50")
        self.subheader_fill = PatternFill(start_color="ECF0F1", end_color="ECF0F1", fill_type="solid")
        self.border = Border(
            left=Side(style='thin'),
            right=Side(style='thin'),
            top=Side(style='thin'),
            bottom=Side(style='thin')
        )
    
    def generate_shift_report(self, shift: Shift, closing_amount: float) -> Optional[str]:
        """
        Generate a comprehensive Excel report for a shift.
        
        Args:
            shift: The shift object containing shift data
            closing_amount: The closing amount entered by the cashier
            
        Returns:
            Optional[str]: Path to the generated Excel file, or None if failed
        """
        if not EXCEL_AVAILABLE:
            logger.error("Excel functionality not available. Install openpyxl: pip install openpyxl")
            return None
        
        try:
            # Create workbook and worksheet
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Shift Report"
            
            # Generate report content
            self._create_header(ws, shift)
            self._create_shift_summary(ws, shift, closing_amount)
            self._create_sales_summary(ws, shift)
            self._create_detailed_sales(ws, shift)
            self._create_product_summary(ws, shift)
            
            # Auto-adjust column widths
            self._auto_adjust_columns(ws)
            
            # Save the file
            filename = self._generate_filename(shift)
            filepath = self.reports_dir / filename
            wb.save(str(filepath))
            
            logger.info(f"Shift report generated: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Error generating shift report: {str(e)}")
            return None
    
    def _create_header(self, ws: Worksheet, shift: Shift):
        """Create the report header."""
        # Company title
        ws['A1'] = "TALINDA POS SYSTEM"
        ws['A1'].font = Font(bold=True, size=16, color="1976D2")
        ws.merge_cells('A1:H1')
        ws['A1'].alignment = Alignment(horizontal='center')
        
        # Report title
        ws['A2'] = "SHIFT SUMMARY REPORT"
        ws['A2'].font = Font(bold=True, size=14, color="2C3E50")
        ws.merge_cells('A2:H2')
        ws['A2'].alignment = Alignment(horizontal='center')
        
        # Shift information
        ws['A4'] = "Shift Details:"
        ws['A4'].font = self.subheader_font
        
        ws['A5'] = f"Cashier: {shift.user.full_name or shift.user.username}"
        ws['B5'] = f"User ID: {shift.user_id}"
        
        ws['A6'] = f"Shift ID: {shift.id}"
        ws['B6'] = f"Status: {shift.status.value.upper()}"
        
        ws['A7'] = f"Open Time: {shift.open_time.strftime('%Y-%m-%d %H:%M:%S')}"
        if shift.close_time:
            ws['B7'] = f"Close Time: {shift.close_time.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Report generation time
        ws['A9'] = f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        ws['A9'].font = Font(italic=True, size=10, color="7F8C8D")
    
    def _create_shift_summary(self, ws: Worksheet, shift: Shift, closing_amount: float):
        """Create the shift summary section."""
        # Section header
        row = 12
        ws[f'A{row}'] = "SHIFT SUMMARY"
        ws[f'A{row}'].font = self.header_font
        ws[f'A{row}'].fill = self.header_fill
        ws.merge_cells(f'A{row}:H{row}')
        ws[f'A{row}'].alignment = Alignment(horizontal='center')
        
        # Summary data
        row += 2
        ws[f'A{row}'] = "Opening Amount:"
        ws[f'B{row}'] = f"${shift.opening_amount:.2f}"
        ws[f'B{row}'].font = Font(bold=True, color="27AE60")
        
        row += 1
        ws[f'A{row}'] = "Closing Amount:"
        ws[f'B{row}'] = f"${closing_amount:.2f}"
        ws[f'B{row}'].font = Font(bold=True, color="E74C3C")
        
        # Calculate total sales
        total_sales = self._get_shift_total_sales(shift)
        row += 1
        ws[f'A{row}'] = "Total Sales:"
        ws[f'B{row}'] = f"${total_sales:.2f}"
        ws[f'B{row}'].font = Font(bold=True, color="3498DB")
        
        # Calculate expected cash
        expected_cash = shift.opening_amount + total_sales
        row += 1
        ws[f'A{row}'] = "Expected Cash:"
        ws[f'B{row}'] = f"${expected_cash:.2f}"
        ws[f'B{row}'].font = Font(bold=True, color="F39C12")
        
        # Calculate difference
        difference = closing_amount - expected_cash
        row += 1
        ws[f'A{row}'] = "Difference:"
        ws[f'B{row}'] = f"${difference:.2f}"
        if difference >= 0:
            ws[f'B{row}'].font = Font(bold=True, color="27AE60")
        else:
            ws[f'B{row}'].font = Font(bold=True, color="E74C3C")
    
    def _create_sales_summary(self, ws: Worksheet, shift: Shift):
        """Create the sales summary section."""
        # Section header
        row = 22
        ws[f'A{row}'] = "SALES SUMMARY"
        ws[f'A{row}'].font = self.header_font
        ws[f'A{row}'].fill = self.header_fill
        ws.merge_cells(f'A{row}:H{row}')
        ws[f'A{row}'].alignment = Alignment(horizontal='center')
        
        # Get sales data
        sales_data = self._get_shift_sales_data(shift)
        
        # Sales statistics
        row += 2
        ws[f'A{row}'] = "Total Transactions:"
        ws[f'B{row}'] = len(sales_data)
        ws[f'B{row}'].font = Font(bold=True)
        
        row += 1
        ws[f'A{row}'] = "Total Items Sold:"
        total_items = sum(sale['total_items'] for sale in sales_data)
        ws[f'B{row}'] = total_items
        ws[f'B{row}'].font = Font(bold=True)
        
        row += 1
        ws[f'A{row}'] = "Average Transaction:"
        if sales_data:
            avg_transaction = sum(sale['total_amount'] for sale in sales_data) / len(sales_data)
            ws[f'B{row}'] = f"${avg_transaction:.2f}"
            ws[f'B{row}'].font = Font(bold=True)
    
    def _create_detailed_sales(self, ws: Worksheet, shift: Shift):
        """Create the detailed sales section."""
        # Section header
        row = 30
        ws[f'A{row}'] = "DETAILED SALES"
        ws[f'A{row}'].font = self.header_font
        ws[f'A{row}'].fill = self.header_fill
        ws.merge_cells(f'A{row}:H{row}')
        ws[f'A{row}'].alignment = Alignment(horizontal='center')
        
        # Table headers
        row += 2
        headers = ['Sale ID', 'Time', 'Items', 'Total Amount', 'Cashier']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.font = self.subheader_font
            cell.fill = self.subheader_fill
            cell.border = self.border
            cell.alignment = Alignment(horizontal='center')
        
        # Get sales data
        sales_data = self._get_shift_sales_data(shift)
        
        # Sales rows
        for sale in sales_data:
            row += 1
            ws.cell(row=row, column=1, value=sale['id'])
            ws.cell(row=row, column=2, value=sale['timestamp'].strftime('%H:%M:%S'))
            ws.cell(row=row, column=3, value=sale['total_items'])
            ws.cell(row=row, column=4, value=f"${sale['total_amount']:.2f}")
            ws.cell(row=row, column=5, value=sale['cashier_name'])
            
            # Apply borders to all cells in the row
            for col in range(1, 6):
                ws.cell(row=row, column=col).border = self.border
    
    def _create_product_summary(self, ws: Worksheet, shift: Shift):
        """Create the product summary section."""
        # Section header
        row = 35 + len(self._get_shift_sales_data(shift))  # Start after detailed sales
        ws[f'A{row}'] = "PRODUCT SUMMARY"
        ws[f'A{row}'].font = self.header_font
        ws[f'A{row}'].fill = self.header_fill
        ws.merge_cells(f'A{row}:H{row}')
        ws[f'A{row}'].alignment = Alignment(horizontal='center')
        
        # Table headers
        row += 2
        headers = ['Product Name', 'Category', 'Quantity Sold', 'Unit Price', 'Total Revenue']
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=row, column=col, value=header)
            cell.font = self.subheader_font
            cell.fill = self.subheader_fill
            cell.border = self.border
            cell.alignment = Alignment(horizontal='center')
        
        # Get product sales data
        product_data = self._get_shift_product_data(shift)
        
        # Product rows
        for product in product_data:
            row += 1
            ws.cell(row=row, column=1, value=product['name'])
            ws.cell(row=row, column=2, value=product['category'])
            ws.cell(row=row, column=3, value=product['quantity'])
            ws.cell(row=row, column=4, value=f"${product['unit_price']:.2f}")
            ws.cell(row=row, column=5, value=f"${product['total_revenue']:.2f}")
            
            # Apply borders to all cells in the row
            for col in range(1, 6):
                ws.cell(row=row, column=col).border = self.border
    
    def _get_shift_total_sales(self, shift: Shift) -> float:
        """Get total sales amount for the shift."""
        try:
            result = self.session.query(func.sum(Sale.total_amount)).filter(
                and_(
                    Sale.user_id == shift.user_id,
                    Sale.timestamp >= shift.open_time,
                    Sale.timestamp <= (shift.close_time or datetime.now())
                )
            ).scalar()
            return float(result or 0)
        except Exception as e:
            logger.error(f"Error getting shift total sales: {e}")
            return 0.0
    
    def _get_shift_sales_data(self, shift: Shift) -> List[Dict]:
        """Get detailed sales data for the shift."""
        try:
            sales = self.session.query(Sale).filter(
                and_(
                    Sale.user_id == shift.user_id,
                    Sale.timestamp >= shift.open_time,
                    Sale.timestamp <= (shift.close_time or datetime.now())
                )
            ).order_by(Sale.timestamp).all()
            
            sales_data = []
            for sale in sales:
                # Count total items in this sale
                total_items = self.session.query(func.sum(sale_products.c.quantity)).filter(
                    sale_products.c.sale_id == sale.id
                ).scalar() or 0
                
                sales_data.append({
                    'id': sale.id,
                    'timestamp': sale.timestamp,
                    'total_amount': sale.total_amount,
                    'total_items': total_items,
                    'cashier_name': shift.user.full_name or shift.user.username
                })
            
            return sales_data
        except Exception as e:
            logger.error(f"Error getting shift sales data: {e}")
            return []
    
    def _get_shift_product_data(self, shift: Shift) -> List[Dict]:
        """Get product sales data for the shift."""
        try:
            # Get all sales for this shift
            sales = self.session.query(Sale.id).filter(
                and_(
                    Sale.user_id == shift.user_id,
                    Sale.timestamp >= shift.open_time,
                    Sale.timestamp <= (shift.close_time or datetime.now())
                )
            ).all()
            
            sale_ids = [sale.id for sale in sales]
            
            if not sale_ids:
                return []
            
            # Get product sales data
            product_sales = self.session.query(
                Product.name,
                Product.category_id,
                func.sum(sale_products.c.quantity).label('total_quantity'),
                func.avg(sale_products.c.price_at_sale).label('avg_price'),
                func.sum(sale_products.c.quantity * sale_products.c.price_at_sale).label('total_revenue')
            ).join(sale_products, Product.id == sale_products.c.product_id).filter(
                sale_products.c.sale_id.in_(sale_ids)
            ).group_by(Product.id, Product.name, Product.category_id).all()
            
            # Get category names
            category_names = {}
            categories = self.session.query(Product.category_id, func.count(Product.id)).group_by(Product.category_id).all()
            for cat_id, _ in categories:
                if cat_id:
                    category = self.session.query(Product).filter_by(category_id=cat_id).first()
                    if category and category.category:
                        category_names[cat_id] = category.category.name
                    else:
                        category_names[cat_id] = "Unknown"
            
            product_data = []
            for product in product_sales:
                product_data.append({
                    'name': product.name,
                    'category': category_names.get(product.category_id, "Unknown"),
                    'quantity': int(product.total_quantity),
                    'unit_price': float(product.avg_price),
                    'total_revenue': float(product.total_revenue)
                })
            
            return product_data
        except Exception as e:
            logger.error(f"Error getting shift product data: {e}")
            return []
    
    def _auto_adjust_columns(self, ws: Worksheet):
        """Auto-adjust column widths based on content."""
        for column in ws.columns:
            max_length = 0
            column_letter = get_column_letter(column[0].column)
            
            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass
            
            adjusted_width = min(max_length + 2, 50)  # Cap at 50 characters
            ws.column_dimensions[column_letter].width = adjusted_width
    
    def _generate_filename(self, shift: Shift) -> str:
        """Generate filename for the Excel report."""
        timestamp = shift.close_time or datetime.now()
        return f"shift_report_{shift.user.username}_{timestamp.strftime('%Y%m%d_%H%M%S')}.xlsx"
    
    def open_excel_file(self, filepath: str) -> bool:
        """
        Open the Excel file with the default system application.
        
        Args:
            filepath: Path to the Excel file
            
        Returns:
            bool: True if opened successfully, False otherwise
        """
        try:
            import subprocess
            import platform
            
            system = platform.system()
            
            if system == "Windows":
                os.startfile(filepath)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", filepath], check=True)
            else:  # Linux
                subprocess.run(["xdg-open", filepath], check=True)
            
            logger.info(f"Excel file opened: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error opening Excel file: {e}")
            return False 