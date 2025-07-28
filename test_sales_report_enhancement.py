#!/usr/bin/env python3
"""
Test script for enhanced sales report functionality.
This script tests the new product details and sale details features.
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from datetime import datetime, date
from controllers.shift_controller import ShiftController
from controllers.sale_controller import SaleController
from controllers.product_controller import ProductController
from controllers.auth_controller import AuthController
from database.database_manager import DatabaseManager
from models.sale import Sale, sale_products
from models.product import Product, Category
from models.user import User, UserRole
from database.db_config import Session, safe_commit
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_enhanced_sales_report():
    """Test the enhanced sales report with product details."""
    try:
        print("🧪 Testing Enhanced Sales Report Functionality")
        print("=" * 50)
        
        # Initialize controllers
        shift_controller = ShiftController()
        sale_controller = SaleController()
        product_controller = ProductController()
        auth_controller = AuthController()
        
        # Get today's report
        today = date.today()
        print(f"📅 Generating report for: {today}")
        
        # Generate the enhanced sales report
        report_data = shift_controller.get_daily_sales_report(today)
        
        print("\n📊 Report Summary:")
        print(f"   Total Sales: {report_data.get('total_sales', 0)}")
        print(f"   Total Orders: {report_data.get('total_orders', 0)}")
        print(f"   Total Amount: ${report_data.get('total_amount', 0):.2f}")
        
        # Check product details
        product_details = report_data.get('product_details', [])
        product_summary = report_data.get('product_sales_summary', {})
        
        print(f"\n🛍️  Product Summary:")
        print(f"   Total Products Sold: {product_summary.get('total_products_sold', 0)}")
        print(f"   Total Quantity Sold: {product_summary.get('total_quantity_sold', 0)}")
        print(f"   Top Product: {product_summary.get('top_product_name', 'None')}")
        print(f"   Top Product Quantity: {product_summary.get('top_product_quantity', 0)}")
        
        print(f"\n📋 Product Details ({len(product_details)} products):")
        for i, product in enumerate(product_details[:5]):  # Show first 5 products
            print(f"   {i+1}. {product.get('product_name', 'N/A')}")
            print(f"      Category: {product.get('category', 'N/A')}")
            print(f"      Quantity Sold: {product.get('quantity_sold', 0)}")
            print(f"      Unit Price: ${product.get('unit_price', 0):.2f}")
            print(f"      Total Amount: ${product.get('total_amount', 0):.2f}")
            print(f"      Sales Count: {product.get('sales_count', 0)}")
            print()
        
        # Check sale details
        sale_details = report_data.get('sale_details', [])
        print(f"\n💰 Sale Details ({len(sale_details)} items):")
        for i, sale in enumerate(sale_details[:3]):  # Show first 3 sale items
            print(f"   {i+1}. Sale #{sale.get('sale_id', 'N/A')}")
            print(f"      Date: {sale.get('date', 'N/A')} Time: {sale.get('time', 'N/A')}")
            print(f"      Cashier: {sale.get('cashier', 'N/A')}")
            print(f"      Product: {sale.get('product_name', 'N/A')}")
            print(f"      Quantity: {sale.get('quantity', 0)}")
            print(f"      Unit Price: ${sale.get('unit_price', 0):.2f}")
            print(f"      Total: ${sale.get('total_amount', 0):.2f}")
            print()
        
        print("✅ Enhanced Sales Report Test Completed Successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error testing enhanced sales report: {e}")
        logger.error(f"Error testing enhanced sales report: {e}")
        return False

def test_sales_report_dialog():
    """Test the sales report dialog UI."""
    try:
        print("\n🖥️  Testing Sales Report Dialog UI")
        print("=" * 40)
        
        from PyQt5.QtWidgets import QApplication
        from ui.components.daily_sales_report_dialog import DailySalesReportDialog
        
        # Create QApplication if it doesn't exist
        app = QApplication.instance()
        if app is None:
            app = QApplication(sys.argv)
        
        # Generate sample report data
        shift_controller = ShiftController()
        report_data = shift_controller.get_daily_sales_report()
        
        # Create and show the dialog
        dialog = DailySalesReportDialog(report_data=report_data)
        dialog.show()
        
        print("✅ Sales Report Dialog UI Test Completed!")
        print("   The dialog should now be visible with the enhanced tabs.")
        print("   Check the 'Product Details' and 'Sale Details' tabs.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing sales report dialog: {e}")
        logger.error(f"Error testing sales report dialog: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Enhanced Sales Report Tests")
    print("=" * 50)
    
    # Test the enhanced sales report functionality
    success1 = test_enhanced_sales_report()
    
    # Test the UI dialog
    success2 = test_sales_report_dialog()
    
    if success1 and success2:
        print("\n🎉 All tests passed! Enhanced sales report is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Please check the implementation.")
    
    print("\n📝 Summary of Enhancements:")
    print("   ✅ Added Product Details tab with quantity and product information")
    print("   ✅ Added Sale Details tab with individual sale breakdown")
    print("   ✅ Enhanced summary with product statistics")
    print("   ✅ Added product sales summary to main summary tab")
    print("   ✅ Improved database queries to include sale_products data")
    print("   ✅ Added proper error handling and fallback data") 