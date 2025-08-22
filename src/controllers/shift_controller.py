"""
Shift controller for managing shifts and shift operations.
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date, time
from sqlalchemy import func, and_, desc
from database.db_config import Session, safe_commit, get_fresh_session
from models.user import User, Shift, ShiftStatus
from models.sale import Sale, sale_products
from models.order import Order, OrderStatus
from models.product import Product, Category
from utils.localization import get_current_local_time
from database.database_manager import DatabaseManager
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ShiftController:
    """Controller for handling shift operations."""
    
    def __init__(self):
        """Initialize the shift controller."""
        self.session = get_fresh_session()
        self.db_manager = DatabaseManager()
    
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
                    # Get username safely to avoid session binding issues
                    try:
                        username = any_open_shift.user.username if any_open_shift.user else "Unknown"
                    except Exception as e:
                        logger.warning(f"Error accessing user for shift {any_open_shift.id}: {e}")
                        username = "Unknown"
                    logger.warning(f"There's already an open shift by user {username}")
                    return None
            finally:
                check_session.close()
            
            # Create new shift using the main session
            shift = Shift(
                user_id=user.id,
                opening_amount=opening_amount,
                status=ShiftStatus.OPEN,
                open_time=get_current_local_time()
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
                shift.close_time = get_current_local_time()
                
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
    
    # Sale report methods have been removed
            # Sale report functionality has been removed
    
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
        Reset daily sales data and automatically close all open shifts at midnight.
        This ensures all cashiers must re-authenticate for the new day.
        """
        try:
            logger.info("Daily sales reset and automatic shift closing triggered")
            
            # Close all open shifts automatically
            closed_shifts = self.close_all_open_shifts()
            
            logger.info(f"Automatically closed {closed_shifts} open shifts at midnight")
            
            # In a real implementation, you might want to archive old data
            # or perform other cleanup operations
            
        except Exception as e:
            logger.error(f"Error resetting daily sales: {e}")
    
    def close_all_open_shifts(self) -> int:
        """
        Automatically close all open shifts at the end of the day.
        This forces cashiers to re-authenticate for the new day.
        
        Returns:
            int: Number of shifts that were closed
        """
        try:
            # Get all open shifts
            open_shifts = self.session.query(Shift).filter_by(status=ShiftStatus.OPEN).all()
            
            closed_count = 0
            for shift in open_shifts:
                try:
                    # Close the shift with current time
                    shift.status = ShiftStatus.CLOSED
                    shift.close_time = get_current_local_time()
                    
                    # Calculate shift duration
                    if shift.open_time and shift.close_time:
                        duration = shift.close_time - shift.open_time
                        # Get username safely to avoid session binding issues
                        try:
                            username = shift.user.username if shift.user else "Unknown"
                        except Exception as e:
                            logger.warning(f"Error accessing user for shift {shift.id}: {e}")
                            username = "Unknown"
                        logger.info(f"Shift {shift.id} for user {username} "
                                  f"closed automatically. Duration: {duration}")
                    
                    closed_count += 1
                    
                except Exception as e:
                    logger.error(f"Error closing shift {shift.id}: {e}")
                    continue
            
            # Commit all changes
            if safe_commit(self.session):
                logger.info(f"Successfully closed {closed_count} open shifts")
                return closed_count
            else:
                logger.error("Failed to commit shift closures")
                return 0
                
        except Exception as e:
            logger.error(f"Error in close_all_open_shifts: {e}")
            return 0
    
    # Accurate sales report method has been removed
    
    def get_shift_details_report(self, shift_id: int) -> Optional[Dict[str, Any]]:
        """
        Get complete shift details report including sales, products, and orders.
        
        Args:
            shift_id: The ID of the shift to get details for
            
        Returns:
            Dict: Complete shift details report or None if shift not found
        """
        try:
            # Get basic shift details
            shift_details = self.db_manager.get_shift_details(shift_id)
            if not shift_details:
                logger.warning(f"Shift {shift_id} not found")
                return None
            
            # Get sales by payment method
            sales_by_payment = self.db_manager.get_shift_sales_by_payment(shift_id)
            
            # Get sales by cashier
            sales_by_cashier = self.db_manager.get_shift_sales_by_cashier(shift_id)
            
            # Get product sales details
            product_sales = self.db_manager.get_shift_product_sales(shift_id)
            
            # Get orders during the shift
            orders = self.db_manager.get_shift_orders(shift_id)
            
            # Calculate totals
            total_sales = sum(item['total_amount'] for item in sales_by_payment)
            total_products_sold = sum(item['quantity'] for item in product_sales)
            total_orders = len(orders)
            
            # Compile the complete report
            report = {
                'shift_details': shift_details,
                'sales_by_payment': sales_by_payment,
                'sales_by_cashier': sales_by_cashier,
                'product_sales': product_sales,
                'orders': orders,
                'summary': {
                    'total_sales': total_sales,
                    'total_products_sold': total_products_sold,
                    'total_orders': total_orders,
                    'unique_products': len(product_sales)
                }
            }
            
            logger.info(f"Generated shift details report for shift {shift_id}")
            return report
            
        except Exception as e:
            logger.error(f"Error generating shift details report for shift {shift_id}: {e}")
            return None
    
    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}") 