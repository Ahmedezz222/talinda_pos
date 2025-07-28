"""
Shift controller for managing shifts, daily sales reports, and shift operations.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from sqlalchemy import func, and_, desc
from database.db_config import Session, safe_commit, get_fresh_session
from models.user import User, Shift, ShiftStatus
from models.sale import Sale, sale_products
from models.order import Order, OrderStatus
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ShiftController:
    """Controller for handling shift operations and daily sales reports."""
    
    def __init__(self):
        """Initialize the shift controller."""
        self.session = get_fresh_session()
    
    def _get_fresh_session(self):
        """Get a fresh session for read operations to avoid stale data."""
        return get_fresh_session()
    
    def open_shift(self, user: User, opening_amount: float) -> Optional[Shift]:
        """
        Open a new shift for the given user.
        
        Args:
            user: The user opening the shift
            opening_amount: The opening cash amount
            
        Returns:
            Shift: The opened shift or None if failed
        """
        try:
            # Use fresh session for checking existing shifts
            check_session = self._get_fresh_session()
            
            try:
                # Check if there's already an open shift for this user
                existing_shift = check_session.query(Shift).filter_by(
                    user_id=user.id, status=ShiftStatus.OPEN
                ).first()
                
                if existing_shift:
                    logger.warning(f"User {user.username} already has an open shift")
                    return None
                
                # Check if there's any open shift in the system (only one shift can be open at a time)
                any_open_shift = check_session.query(Shift).filter_by(status=ShiftStatus.OPEN).first()
                if any_open_shift:
                    logger.warning(f"There's already an open shift by user {any_open_shift.user.username}")
                    return None
            finally:
                check_session.close()
            
            # Create new shift using the main session
            shift = Shift(
                user_id=user.id,
                opening_amount=opening_amount,
                status=ShiftStatus.OPEN,
                open_time=datetime.utcnow()
            )
            
            self.session.add(shift)
            
            if safe_commit(self.session):
                logger.info(f"Shift opened for user {user.username} with amount {opening_amount}")
                return shift
            else:
                logger.error("Failed to commit shift opening")
                return None
                
        except Exception as e:
            logger.error(f"Error opening shift: {e}")
            self.session.rollback()
            return None
    
    def close_shift(self, user: User) -> Optional[Shift]:
        """
        Close the current shift for the given user.
        
        Args:
            user: The user closing the shift
            
        Returns:
            Shift: The closed shift or None if failed
        """
        try:
            # Use fresh session for finding the shift
            check_session = self._get_fresh_session()
            
            try:
                # Find the open shift for this user
                shift = check_session.query(Shift).filter_by(
                    user_id=user.id, status=ShiftStatus.OPEN
                ).first()
                
                if not shift:
                    logger.warning(f"No open shift found for user {user.username}")
                    return None
                
                # Update shift with closing information
                shift.status = ShiftStatus.CLOSED
                shift.close_time = datetime.utcnow()
                
                if safe_commit(check_session):
                    logger.info(f"Shift closed for user {user.username}")
                    return shift
                else:
                    logger.error("Failed to commit shift closing")
                    return None
            finally:
                check_session.close()
                
        except Exception as e:
            logger.error(f"Error closing shift: {e}")
            return None
    
    def close_shift_with_auth(self, user: User, password: str) -> Optional[Shift]:
        """
        Close the current shift for the given user with password authentication.
        
        Args:
            user: The user closing the shift
            password: The user's password for authentication
            
        Returns:
            Shift: The closed shift or None if failed
        """
        try:
            # First verify the password
            if not self.verify_user_password(user, password):
                logger.warning(f"Password verification failed for user {user.username}")
                return None
            
            # If password is correct, proceed with closing the shift
            return self.close_shift(user)
            
        except Exception as e:
            logger.error(f"Error closing shift with authentication: {e}")
            return None
    
    def verify_user_password(self, user: User, password: str) -> bool:
        """
        Verify the user's password.
        
        Args:
            user: The user to verify
            password: The password to verify
            
        Returns:
            bool: True if password is correct, False otherwise
        """
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password for user {user.username}: {e}")
            return False
    
    def get_current_shift(self, user: User) -> Optional[Shift]:
        """
        Get the current open shift for the given user.
        
        Args:
            user: The user to get the shift for
            
        Returns:
            Shift: The current shift or None if not found
        """
        try:
            # Use fresh session to avoid stale data
            session = self._get_fresh_session()
            try:
                return session.query(Shift).filter_by(
                    user_id=user.id, status=ShiftStatus.OPEN
                ).first()
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Error getting current shift: {e}")
            return None
    
    def get_any_open_shift(self) -> Optional[Shift]:
        """
        Get any open shift in the system.
        
        Returns:
            Shift: Any open shift or None if no shift is open
        """
        try:
            # Use fresh session to avoid stale data
            session = self._get_fresh_session()
            try:
                return session.query(Shift).filter_by(status=ShiftStatus.OPEN).first()
            finally:
                session.close()
        except Exception as e:
            logger.error(f"Error getting any open shift: {e}")
            return None
    
    def get_daily_sales_report(self, report_date: date = None) -> Dict[str, Any]:
        """
        Get daily sales report for the specified date (defaults to today).
        Includes both sales and orders for comprehensive reporting.
        
        Args:
            report_date: The date to get the report for (defaults to today)
            
        Returns:
            Dict: Daily sales report data including orders and product details
        """
        if report_date is None:
            report_date = date.today()
        
        try:
            # Get start and end of the day
            start_datetime = datetime.combine(report_date, time.min)
            end_datetime = datetime.combine(report_date, time.max)
            
            # Get all sales for the day
            daily_sales = self.session.query(Sale).filter(
                and_(
                    Sale.timestamp >= start_datetime,
                    Sale.timestamp <= end_datetime
                )
            ).all()
            
            # Get all orders for the day (including active, completed, and cancelled)
            from models.order import Order, OrderStatus
            daily_orders = self.session.query(Order).filter(
                and_(
                    Order.created_at >= start_datetime,
                    Order.created_at <= end_datetime
                )
            ).all()
            
            # Calculate sales totals
            total_sales = len(daily_sales)
            total_sales_amount = sum(sale.total_amount for sale in daily_sales)
            
            # Calculate order totals
            total_orders = len(daily_orders)
            total_orders_amount = sum(order.total_amount for order in daily_orders)
            
            # Calculate order status breakdown
            active_orders = len([o for o in daily_orders if o.status == OrderStatus.ACTIVE])
            completed_orders = len([o for o in daily_orders if o.status == OrderStatus.COMPLETED])
            cancelled_orders = len([o for o in daily_orders if o.status == OrderStatus.CANCELLED])
            
            # Get sales by hour
            hourly_sales = {}
            for sale in daily_sales:
                hour = sale.timestamp.hour
                if hour not in hourly_sales:
                    hourly_sales[hour] = {'count': 0, 'amount': 0.0}
                hourly_sales[hour]['count'] += 1
                hourly_sales[hour]['amount'] += sale.total_amount
            
            # Get orders by hour
            hourly_orders = {}
            for order in daily_orders:
                hour = order.created_at.hour
                if hour not in hourly_orders:
                    hourly_orders[hour] = {'count': 0, 'amount': 0.0}
                hourly_orders[hour]['count'] += 1
                hourly_orders[hour]['amount'] += order.total_amount
            
            # Combine hourly data
            hourly_combined = {}
            for hour in range(24):
                sales_data = hourly_sales.get(hour, {'count': 0, 'amount': 0.0})
                orders_data = hourly_orders.get(hour, {'count': 0, 'amount': 0.0})
                hourly_combined[hour] = {
                    'sales_count': sales_data['count'],
                    'sales_amount': sales_data['amount'],
                    'orders_count': orders_data['count'],
                    'orders_amount': orders_data['amount'],
                    'total_count': sales_data['count'] + orders_data['count'],
                    'total_amount': sales_data['amount'] + orders_data['amount']
                }
            
            # Get detailed product information from sales
            from models.product import Product, Category
            from sqlalchemy import func
            
            # Query to get product details with quantities from sale_products table
            product_details_query = self.session.query(
                Product.name.label('product_name'),
                Category.name.label('category_name'),
                func.sum(sale_products.c.quantity).label('quantity_sold'),
                func.avg(sale_products.c.price_at_sale).label('avg_unit_price'),
                func.sum(sale_products.c.quantity * sale_products.c.price_at_sale).label('total_amount'),
                func.count(sale_products.c.sale_id.distinct()).label('sales_count')
            ).join(
                sale_products, Product.id == sale_products.c.product_id
            ).join(
                Sale, sale_products.c.sale_id == Sale.id
            ).join(
                Category, Product.category_id == Category.id
            ).filter(
                and_(
                    Sale.timestamp >= start_datetime,
                    Sale.timestamp <= end_datetime
                )
            ).group_by(
                Product.id, Product.name, Category.name
            ).order_by(
                func.sum(sale_products.c.quantity).desc()
            ).all()
            
            # Convert query results to list of dictionaries
            product_details = []
            total_quantity_sold = 0
            top_product_name = "None"
            top_product_quantity = 0
            
            for row in product_details_query:
                quantity_sold = int(row.quantity_sold) if row.quantity_sold else 0
                avg_unit_price = float(row.avg_unit_price) if row.avg_unit_price else 0.0
                total_amount = float(row.total_amount) if row.total_amount else 0.0
                sales_count = int(row.sales_count) if row.sales_count else 0
                average_per_sale = total_amount / sales_count if sales_count > 0 else 0.0
                
                product_detail = {
                    'product_name': row.product_name,
                    'category': row.category_name,
                    'quantity_sold': quantity_sold,
                    'unit_price': avg_unit_price,
                    'total_amount': total_amount,
                    'sales_count': sales_count,
                    'average_per_sale': average_per_sale
                }
                
                product_details.append(product_detail)
                total_quantity_sold += quantity_sold
                
                # Track top selling product
                if quantity_sold > top_product_quantity:
                    top_product_quantity = quantity_sold
                    top_product_name = row.product_name
            
            # Create product sales summary
            product_sales_summary = {
                'total_products_sold': len(product_details),
                'total_quantity_sold': total_quantity_sold,
                'top_product_name': top_product_name,
                'top_product_quantity': top_product_quantity
            }
            
            # Get detailed sale information with product breakdown
            sale_details_query = self.session.query(
                Sale.id.label('sale_id'),
                Sale.timestamp.label('sale_timestamp'),
                Sale.total_amount.label('sale_total'),
                User.username.label('cashier_name'),
                Product.name.label('product_name'),
                sale_products.c.quantity.label('quantity'),
                sale_products.c.price_at_sale.label('unit_price'),
                (sale_products.c.quantity * sale_products.c.price_at_sale).label('item_total')
            ).join(
                sale_products, Sale.id == sale_products.c.sale_id
            ).join(
                Product, sale_products.c.product_id == Product.id
            ).join(
                User, Sale.user_id == User.id
            ).filter(
                and_(
                    Sale.timestamp >= start_datetime,
                    Sale.timestamp <= end_datetime
                )
            ).order_by(
                Sale.timestamp.desc(), Sale.id, Product.name
            ).all()
            
            # Convert sale details query results to list of dictionaries
            sale_details = []
            for row in sale_details_query:
                sale_detail = {
                    'sale_id': row.sale_id,
                    'date': row.sale_timestamp.strftime('%Y-%m-%d'),
                    'time': row.sale_timestamp.strftime('%H:%M:%S'),
                    'cashier': row.cashier_name,
                    'product_name': row.product_name,
                    'quantity': int(row.quantity) if row.quantity else 0,
                    'unit_price': float(row.unit_price) if row.unit_price else 0.0,
                    'total_amount': float(row.item_total) if row.item_total else 0.0
                }
                sale_details.append(sale_detail)
            
            # Get shifts for the day
            daily_shifts = self.session.query(Shift).filter(
                and_(
                    Shift.open_time >= start_datetime,
                    Shift.open_time <= end_datetime
                )
            ).all()
            
            shift_summary = []
            for shift in daily_shifts:
                shift_data = {
                    'user': shift.user.username if shift.user else 'Unknown',
                    'opening_amount': shift.opening_amount,
                    'open_time': shift.open_time,
                    'close_time': getattr(shift, 'close_time', None),
                    'status': shift.status.value,
                    'duration': None
                }
                
                if shift.close_time:
                    duration = shift.close_time - shift.open_time
                    shift_data['duration'] = str(duration).split('.')[0]  # Remove microseconds
                
                shift_summary.append(shift_data)
            
            return {
                'date': report_date.isoformat(),
                'total_sales': total_sales,
                'total_sales_amount': total_sales_amount,
                'total_orders': total_orders,
                'total_orders_amount': total_orders_amount,
                'total_transactions': total_sales + total_orders,
                'total_amount': total_sales_amount + total_orders_amount,
                'order_status_breakdown': {
                    'active': active_orders,
                    'completed': completed_orders,
                    'cancelled': cancelled_orders
                },
                'hourly_sales': hourly_sales,
                'hourly_orders': hourly_orders,
                'hourly_combined': hourly_combined,
                'product_details': product_details,
                'product_sales_summary': product_sales_summary,
                'sale_details': sale_details, # Added sale_details to the report
                'shifts': shift_summary,
                'average_sale': total_sales_amount / total_sales if total_sales > 0 else 0,
                'average_order': total_orders_amount / total_orders if total_orders > 0 else 0,
                'average_transaction': (total_sales_amount + total_orders_amount) / (total_sales + total_orders) if (total_sales + total_orders) > 0 else 0
            }
            
        except Exception as e:
            logger.error(f"Error generating daily sales report: {e}")
            return {
                'date': report_date.isoformat(),
                'total_sales': 0,
                'total_sales_amount': 0.0,
                'total_orders': 0,
                'total_orders_amount': 0.0,
                'total_transactions': 0,
                'total_amount': 0.0,
                'order_status_breakdown': {
                    'active': 0,
                    'completed': 0,
                    'cancelled': 0
                },
                'hourly_sales': {},
                'hourly_orders': {},
                'hourly_combined': {},
                'product_details': [],
                'product_sales_summary': {
                    'total_products_sold': 0,
                    'total_quantity_sold': 0,
                    'top_product_name': 'None',
                    'top_product_quantity': 0
                },
                'sale_details': [], # Added sale_details to the report
                'shifts': [],
                'average_sale': 0.0,
                'average_order': 0.0,
                'average_transaction': 0.0
            }
    
    def get_shift_summary(self, shift: Shift) -> Dict[str, Any]:
        """
        Get a summary of a specific shift including sales data.
        
        Args:
            shift: The shift to get summary for
            
        Returns:
            Dict: Shift summary data
        """
        try:
            # Use fresh session to avoid session binding issues
            session = self._get_fresh_session()
            
            try:
                # Reload the shift with fresh session to ensure relationships work
                fresh_shift = session.query(Shift).filter_by(id=shift.id).first()
                if not fresh_shift:
                    return {
                        'shift_id': shift.id,
                        'error': 'Shift not found'
                    }
                
                # Get sales during this shift
                shift_sales = session.query(Sale).filter(
                    and_(
                        Sale.timestamp >= fresh_shift.open_time,
                        Sale.timestamp <= (fresh_shift.close_time or datetime.utcnow())
                    )
                ).all()
                
                total_sales = len(shift_sales)
                total_amount = sum(sale.total_amount for sale in shift_sales)
                
                return {
                    'shift_id': fresh_shift.id,
                    'user': fresh_shift.user.username if fresh_shift.user else 'Unknown',
                    'opening_amount': fresh_shift.opening_amount,
                    'open_time': fresh_shift.open_time,
                    'close_time': getattr(fresh_shift, 'close_time', None),
                    'status': fresh_shift.status.value,
                    'total_sales': total_sales,
                    'total_amount': total_amount
                }
            finally:
                session.close()
            
        except Exception as e:
            logger.error(f"Error generating shift summary: {e}")
            return {
                'shift_id': shift.id,
                'error': str(e)
            }
    
    def reset_daily_sales(self):
        """
        Reset daily sales data (called automatically at midnight).
        This is a placeholder for future implementation.
        """
        try:
            logger.info("Daily sales reset triggered")
            # In a real implementation, you might want to archive old data
            # or perform other cleanup operations
        except Exception as e:
            logger.error(f"Error resetting daily sales: {e}")
    
    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}") 