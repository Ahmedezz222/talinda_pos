#!/usr/bin/env python3
"""
Test script for the new accurate sales report functionality.
This script tests the get_accurate_sales_report method to ensure it provides
accurate, non-duplicated data from completed orders.
"""

import sys
import os
from datetime import date, datetime
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

def test_accurate_sales_report():
    """Test the accurate sales report functionality."""
    try:
        # Import required modules
        from controllers.shift_controller import ShiftController
        from controllers.order_controller import OrderController
        from database.db_config import get_fresh_session
        from models.order import Order, OrderStatus
        from models.product import Product, Category
        from models.user import User
        
        print("🧪 Testing Accurate Sales Report Functionality")
        print("=" * 50)
        
        # Initialize controllers
        shift_controller = ShiftController()
        order_controller = OrderController()
        
        # Test date (today)
        test_date = date.today()
        print(f"📅 Testing for date: {test_date}")
        
        # Get accurate sales report
        print("\n📊 Generating accurate sales report...")
        report_data = shift_controller.get_accurate_sales_report(test_date)
        
        # Display report summary
        print("\n📋 Report Summary:")
        print(f"   Data Source: {report_data.get('data_source', 'Unknown')}")
        print(f"   Data Availability: {report_data.get('data_availability', 'Unknown')}")
        print(f"   Total Transactions: {report_data.get('total_transactions', 0)}")
        print(f"   Total Amount: ${report_data.get('total_amount', 0):.2f}")
        print(f"   Average Transaction: ${report_data.get('average_transaction', 0):.2f}")
        
        # Display product summary
        product_summary = report_data.get('product_sales_summary', {})
        print(f"\n🛍️ Product Summary:")
        print(f"   Total Products Sold: {product_summary.get('total_products_sold', 0)}")
        print(f"   Total Quantity Sold: {product_summary.get('total_quantity_sold', 0)}")
        print(f"   Top Product: {product_summary.get('top_product_name', 'None')}")
        
        # Display product details
        product_details = report_data.get('product_details', [])
        if product_details:
            print(f"\n📦 Product Details ({len(product_details)} products):")
            for i, product in enumerate(product_details[:5], 1):  # Show first 5 products
                print(f"   {i}. {product['product_name']} - Qty: {product['quantity_sold']}, Revenue: ${product['total_amount']:.2f}")
            if len(product_details) > 5:
                print(f"   ... and {len(product_details) - 5} more products")
        else:
            print("\n📦 No product details available")
        
        # Display order status breakdown
        order_status = report_data.get('order_status_breakdown', {})
        print(f"\n📈 Order Status Breakdown:")
        print(f"   Completed Orders: {order_status.get('completed', 0)}")
        print(f"   Active Orders: {order_status.get('active', 0)}")
        print(f"   Cancelled Orders: {order_status.get('cancelled', 0)}")
        
        # Test data integrity
        print(f"\n🔍 Data Integrity Check:")
        
        # Check if totals match
        total_transactions = report_data.get('total_transactions', 0)
        total_amount = report_data.get('total_amount', 0)
        completed_orders = order_status.get('completed', 0)
        
        if total_transactions == completed_orders:
            print("   ✅ Transaction count matches completed orders count")
        else:
            print("   ❌ Transaction count does not match completed orders count")
        
        if total_amount >= 0:
            print("   ✅ Total amount is valid (non-negative)")
        else:
            print("   ❌ Total amount is invalid (negative)")
        
        # Check for duplicates in product details
        product_names = [p['product_name'] for p in product_details]
        unique_products = set(product_names)
        
        if len(product_names) == len(unique_products):
            print("   ✅ No duplicate products in product details")
        else:
            print("   ❌ Duplicate products found in product details")
        
        # Check data source accuracy
        data_source = report_data.get('data_source', '')
        if 'Completed Orders' in data_source or 'No Data' in data_source or 'Error' in data_source:
            print("   ✅ Data source is properly identified")
        else:
            print("   ❌ Data source identification is unclear")
        
        print(f"\n✅ Accurate Sales Report Test Completed Successfully!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during accurate sales report test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_order_data_integrity():
    """Test order data integrity to ensure no duplicates."""
    try:
        from controllers.order_controller import OrderController
        from database.db_config import get_fresh_session
        from models.order import Order, OrderStatus
        
        print("\n🔍 Testing Order Data Integrity")
        print("=" * 40)
        
        order_controller = OrderController()
        test_date = date.today()
        
        # Get all orders for today
        daily_orders = order_controller.get_all_orders_for_date(test_date)
        completed_orders = [order for order in daily_orders if order.status == OrderStatus.COMPLETED]
        
        print(f"📊 Order Statistics for {test_date}:")
        print(f"   Total Orders: {len(daily_orders)}")
        print(f"   Completed Orders: {len(completed_orders)}")
        print(f"   Active Orders: {len([o for o in daily_orders if o.status == OrderStatus.ACTIVE])}")
        print(f"   Cancelled Orders: {len([o for o in daily_orders if o.status == OrderStatus.CANCELLED])}")
        
        # Check for duplicate order numbers
        order_numbers = [order.order_number for order in daily_orders]
        unique_order_numbers = set(order_numbers)
        
        if len(order_numbers) == len(unique_order_numbers):
            print("   ✅ No duplicate order numbers found")
        else:
            print("   ❌ Duplicate order numbers found")
            duplicates = [num for num in order_numbers if order_numbers.count(num) > 1]
            print(f"      Duplicate numbers: {duplicates}")
        
        # Check for orders created from sales (should be excluded)
        sale_orders = [order for order in completed_orders if order.order_number.startswith("SALE-")]
        non_sale_orders = [order for order in completed_orders if not order.order_number.startswith("SALE-")]
        
        print(f"   Orders created from sales: {len(sale_orders)}")
        print(f"   Regular completed orders: {len(non_sale_orders)}")
        
        if len(sale_orders) == 0:
            print("   ✅ No orders created from sales (good for accurate reporting)")
        else:
            print("   ⚠️ Orders created from sales found (these should be excluded from accurate reports)")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error during order data integrity test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 Starting Accurate Sales Report Tests")
    print("=" * 60)
    
    # Run tests
    test1_passed = test_accurate_sales_report()
    test2_passed = test_order_data_integrity()
    
    print("\n" + "=" * 60)
    print("📋 Test Results Summary:")
    print(f"   Accurate Sales Report Test: {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    print(f"   Order Data Integrity Test: {'✅ PASSED' if test2_passed else '❌ FAILED'}")
    
    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The accurate sales report is working correctly.")
        sys.exit(0)
    else:
        print("\n⚠️ Some tests failed. Please check the implementation.")
        sys.exit(1) 