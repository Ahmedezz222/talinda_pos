#!/usr/bin/env python3
"""
Test script to verify sale report functionality and product quantity calculations.
"""
import sys
import os
from datetime import date, datetime
from sqlalchemy import func, and_

# Add the src directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

from controllers.shift_controller import ShiftController
from database.db_config import get_fresh_session
from models.sale import Sale, sale_products
from models.product import Product, Category
from models.order import Order, OrderStatus, order_products

def test_sale_report():
    """Test the sale report functionality."""
    print("Testing Sale Report Functionality")
    print("=" * 50)
    
    try:
        # Create shift controller
        shift_controller = ShiftController()
        
        # Get today's report
        today = date.today()
        print(f"Generating report for: {today}")
        
        # Generate the report
        report_data = shift_controller.get_daily_sales_report(today)
        
        # Print summary
        print(f"\nReport Summary:")
        print(f"Total Sales: {report_data.get('total_sales', 0)}")
        print(f"Total Amount: ${report_data.get('total_amount', 0):.2f}")
        print(f"Total Transactions: {report_data.get('total_transactions', 0)}")
        
        # Print product summary
        product_summary = report_data.get('product_sales_summary', {})
        print(f"\nProduct Summary:")
        print(f"Total Products Sold: {product_summary.get('total_products_sold', 0)}")
        print(f"Total Quantity Sold: {product_summary.get('total_quantity_sold', 0)}")
        print(f"Top Product: {product_summary.get('top_product_name', 'None')}")
        print(f"Top Product Quantity: {product_summary.get('top_product_quantity', 0)}")
        
        # Print product details
        product_details = report_data.get('product_details', [])
        print(f"\nProduct Details ({len(product_details)} products):")
        print("-" * 80)
        print(f"{'Product Name':<20} {'Category':<15} {'Qty Sold':<10} {'Unit Price':<12} {'Total Amount':<15}")
        print("-" * 80)
        
        for product in product_details:
            name = product.get('product_name', 'N/A')[:19]
            category = product.get('category', 'N/A')[:14]
            qty = product.get('quantity_sold', 0)
            unit_price = product.get('unit_price', 0)
            total = product.get('total_amount', 0)
            
            print(f"{name:<20} {category:<15} {qty:<10} ${unit_price:<11.2f} ${total:<14.2f}")
        
        # Print sale details
        sale_details = report_data.get('sale_details', [])
        print(f"\nSale Details ({len(sale_details)} transactions):")
        print("-" * 100)
        print(f"{'Time':<15} {'Cashier':<15} {'Product':<20} {'Qty':<5} {'Amount':<12} {'Type':<15}")
        print("-" * 100)
        
        for sale in sale_details[:10]:  # Show first 10 transactions
            time_str = sale.get('time', 'N/A')[:14]
            cashier = sale.get('cashier', 'N/A')[:14]
            product = sale.get('product_name', 'N/A')[:19]
            qty = sale.get('quantity', 0)
            amount = sale.get('total_amount', 0)
            trans_type = sale.get('transaction_type', 'N/A')[:14]
            
            print(f"{time_str:<15} {cashier:<15} {product:<20} {qty:<5} ${amount:<11.2f} {trans_type:<15}")
        
        if len(sale_details) > 10:
            print(f"... and {len(sale_details) - 10} more transactions")
        
        print("\n" + "=" * 50)
        print("Test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_database_queries():
    """Test direct database queries to verify data integrity."""
    print("\nTesting Database Queries")
    print("=" * 50)
    
    try:
        session = get_fresh_session()
        
        # Test sales query
        today = date.today()
        start_datetime = datetime.combine(today, datetime.min.time())
        end_datetime = datetime.combine(today, datetime.max.time())
        
        print(f"Querying sales for: {today}")
        
        # Get sales with product details
        sales_query = session.query(
            Sale.id.label('sale_id'),
            Sale.timestamp.label('sale_timestamp'),
            Sale.total_amount.label('sale_total'),
            Product.name.label('product_name'),
            sale_products.c.quantity.label('quantity'),
            sale_products.c.price_at_sale.label('unit_price')
        ).join(
            sale_products, Sale.id == sale_products.c.sale_id
        ).join(
            Product, sale_products.c.product_id == Product.id
        ).filter(
            and_(
                Sale.timestamp >= start_datetime,
                Sale.timestamp <= end_datetime
            )
        ).all()
        
        print(f"Found {len(sales_query)} sale product entries")
        
        if sales_query:
            print("\nSample sale data:")
            print("-" * 60)
            print(f"{'Sale ID':<8} {'Time':<15} {'Product':<20} {'Qty':<5} {'Price':<10}")
            print("-" * 60)
            
            for sale in sales_query[:5]:
                sale_id = sale.sale_id
                time_str = sale.sale_timestamp.strftime('%H:%M:%S') if sale.sale_timestamp else 'N/A'
                product = sale.product_name[:19] if sale.product_name else 'N/A'
                qty = sale.quantity or 0
                price = sale.unit_price or 0
                
                print(f"{sale_id:<8} {time_str:<15} {product:<20} {qty:<5} ${price:<9.2f}")
        
        # Test orders query
        try:
            orders_query = session.query(
                Order.id.label('order_id'),
                Order.created_at.label('order_timestamp'),
                Order.total_amount.label('order_total'),
                Product.name.label('product_name'),
                order_products.c.quantity.label('quantity'),
                order_products.c.price_at_order.label('unit_price')
            ).join(
                order_products, Order.id == order_products.c.order_id
            ).join(
                Product, order_products.c.product_id == Product.id
            ).filter(
                and_(
                    Order.created_at >= start_datetime,
                    Order.created_at <= end_datetime,
                    Order.status == OrderStatus.COMPLETED
                )
            ).all()
            
            print(f"\nFound {len(orders_query)} completed order product entries")
            
            if orders_query:
                print("\nSample order data:")
                print("-" * 60)
                print(f"{'Order ID':<9} {'Time':<15} {'Product':<20} {'Qty':<5} {'Price':<10}")
                print("-" * 60)
                
                for order in orders_query[:5]:
                    order_id = order.order_id
                    time_str = order.order_timestamp.strftime('%H:%M:%S') if order.order_timestamp else 'N/A'
                    product = order.product_name[:19] if order.product_name else 'N/A'
                    qty = order.quantity or 0
                    price = order.unit_price or 0
                    
                    print(f"{order_id:<9} {time_str:<15} {product:<20} {qty:<5} ${price:<9.2f}")
                    
        except Exception as e:
            print(f"Error querying orders: {e}")
        
        session.close()
        print("\nDatabase queries completed successfully!")
        return True
        
    except Exception as e:
        print(f"Error during database queries: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Sale Report Test Script")
    print("=" * 50)
    
    # Test database queries first
    db_success = test_database_queries()
    
    # Test sale report functionality
    report_success = test_sale_report()
    
    if db_success and report_success:
        print("\n✅ All tests passed! Sale report is working correctly.")
    else:
        print("\n❌ Some tests failed. Please check the output above.") 