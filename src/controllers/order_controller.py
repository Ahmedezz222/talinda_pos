"""
Controller for order management operations.
"""
from typing import List, Optional, Dict
from datetime import datetime, timedelta, date, time
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session, safe_commit, get_fresh_session
from models.order import Order, OrderStatus
from models.product import Product
from models.user import User
from utils.localization import get_current_local_time
import uuid
import logging
from sqlalchemy import and_, or_

# Set up logging
logger = logging.getLogger(__name__)

class OrderController:
    """Controller for handling order operations."""
    
    def __init__(self):
        """Initialize the order controller."""
        self.session = get_fresh_session()
    
    def create_order(self, user: User, customer_name: str = None, notes: str = None) -> Order:
        """
        Create a new order.
        
        Args:
            user: The user creating the order
            customer_name: Optional customer name for the order
            notes: Optional notes for the order
            
        Returns:
            Order: The created order
        """
        try:
            # Generate unique order number
            order_number = self._generate_order_number()
            
            order = Order(
                order_number=order_number,
                customer_name=customer_name,
                user_id=user.id,
                notes=notes,
                status=OrderStatus.ACTIVE
            )
            
            self.session.add(order)
            
            # Use safe commit to handle potential database locks
            if safe_commit(self.session):
                logger.info(f"Order created successfully: {order_number}")
                return order
            else:
                logger.error("Failed to commit order creation")
                raise Exception("Failed to create order due to database lock")
                
        except Exception as e:
            logger.error(f"Error creating order: {e}")
            self.session.rollback()
            raise e
    
    def add_items_to_order(self, order: Order, items: List[Dict]) -> bool:
        """
        Add items to an order.
        
        Args:
            order: The order to add items to
            items: List of items with product_id, quantity, price, and optional notes
            
        Returns:
            bool: True if items added successfully
        """
        try:
            for item in items:
                product_id = item['product_id']
                quantity = item['quantity']
                price = item['price']
                notes = item.get('notes')
                
                # Add to order_products table using SQLAlchemy
                from models.order import order_products
                self.session.execute(
                    order_products.insert().values(
                        order_id=order.id,
                        product_id=product_id,
                        quantity=quantity,
                        price_at_order=price,
                        notes=notes
                    )
                )
            
            # Update order totals
            self._update_order_totals(order)
            
            # Use safe commit to handle potential database locks
            if safe_commit(self.session):
                logger.info(f"Items added to order {order.order_number} successfully")
                return True
            else:
                logger.error("Failed to commit items to order")
                return False
                
        except Exception as e:
            logger.error(f"Error adding items to order: {e}")
            self.session.rollback()
            return False
    
    def _update_order_totals(self, order: Order) -> None:
        """
        Update order totals based on items and apply any discounts/tax.
        
        Args:
            order: The order to update totals for
        """
        try:
            # Get order items
            items = order.get_order_items()
            
            # Calculate subtotal
            subtotal = sum(item['price'] * item['quantity'] for item in items)
            order.subtotal = subtotal
            
            # Apply any existing discounts (could be set when creating order)
            if not hasattr(order, 'discount_amount') or order.discount_amount is None:
                order.discount_amount = 0.0
            
            # Calculate tax based on product categories
            total_tax = 0.0
            for item in items:
                product = item['product']
                item_total = item['price'] * item['quantity']
                
                # Get product with category from session to avoid lazy loading issues
                try:
                    session_product = self.session.query(Product).filter_by(id=product.id).first()
                    if session_product and hasattr(session_product, 'category') and session_product.category:
                        tax_rate = getattr(session_product.category, 'tax_rate', 0.0)
                        item_tax = item_total * (tax_rate / 100.0)
                        total_tax += item_tax
                except Exception as e:
                    # If we can't get the category, just use 0 tax rate
                    logger.warning(f"Could not get tax rate for product {product.id}: {e}")
                    continue
            
            order.tax_amount = total_tax
            
            # Calculate total
            order.total_amount = subtotal - order.discount_amount + order.tax_amount
            
            # Update the order in the session
            self.session.merge(order)
            
        except Exception as e:
            logger.error(f"Error updating order totals: {e}")
            # Set default values if calculation fails
            order.subtotal = 0.0
            order.discount_amount = 0.0
            order.tax_amount = 0.0
            order.total_amount = 0.0
    
    def refresh_session(self):
        """Refresh the database session."""
        try:
            if safe_commit(self.session):
                logger.debug("Session refreshed successfully")
            else:
                logger.warning("Failed to commit during session refresh")
        except Exception as e:
            logger.error(f"Error refreshing session: {e}")
            self.session.rollback()
            # Get a fresh session
            self.session.close()
            self.session = get_fresh_session()
    
    def get_active_orders(self) -> List[Order]:
        """
        Get all active orders (excluding archived ones).
        
        Returns:
            List[Order]: List of active orders
        """
        try:
            orders = self.session.query(Order).filter(
                and_(
                    Order.status == OrderStatus.ACTIVE,
                    or_(
                        Order.notes.is_(None),
                        ~Order.notes.like('[ARCHIVED]%')  # Exclude archived orders
                    )
                )
            ).order_by(Order.created_at.desc()).all()
            
            # Ensure all orders have proper tax calculation
            for order in orders:
                if order.tax_amount == 0.0 and order.subtotal > 0:
                    self._update_order_totals(order)
            
            return orders
        except Exception as e:
            logger.error(f"Error getting active orders: {e}")
            return []
    
    def get_completed_orders(self, limit: int = 50) -> List[Order]:
        """
        Get completed orders (excluding archived ones).
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of completed orders
        """
        try:
            orders = self.session.query(Order).filter(
                and_(
                    Order.status == OrderStatus.COMPLETED,
                    or_(
                        Order.notes.is_(None),
                        ~Order.notes.like('[ARCHIVED]%')  # Exclude archived orders
                    )
                )
            ).order_by(Order.completed_at.desc()).limit(limit).all()
            
            # Ensure all orders have proper tax calculation
            for order in orders:
                if order.tax_amount == 0.0 and order.subtotal > 0:
                    self._update_order_totals(order)
            
            return orders
        except Exception as e:
            logger.error(f"Error getting completed orders: {e}")
            return []
    
    def get_cancelled_orders(self, limit: int = 50) -> List[Order]:
        """
        Get cancelled orders (excluding archived ones).
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of cancelled orders
        """
        try:
            orders = self.session.query(Order).filter(
                and_(
                    Order.status == OrderStatus.CANCELLED,
                    or_(
                        Order.notes.is_(None),
                        ~Order.notes.like('[ARCHIVED]%')  # Exclude archived orders
                    )
                )
            ).order_by(Order.cancelled_at.desc()).limit(limit).all()
            
            # Ensure all orders have proper tax calculation
            for order in orders:
                if order.tax_amount == 0.0 and order.subtotal > 0:
                    self._update_order_totals(order)
            
            return orders
        except Exception as e:
            logger.error(f"Error getting cancelled orders: {e}")
            return []
    
    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        """
        Get an order by its ID.
        
        Args:
            order_id: ID of the order to retrieve
            
        Returns:
            Optional[Order]: The order if found, None otherwise
        """
        try:
            order = self.session.query(Order).filter_by(id=order_id).one()
            
            # Ensure order has proper tax calculation
            if order and order.tax_amount == 0.0 and order.subtotal > 0:
                self._update_order_totals(order)
            
            return order
        except NoResultFound:
            return None
        except Exception as e:
            logger.error(f"Error getting order by ID {order_id}: {e}")
            return None
    
    def get_order_by_number(self, order_number: str) -> Optional[Order]:
        """
        Get an order by its order number.
        
        Args:
            order_number: Order number to search for
            
        Returns:
            Optional[Order]: The order if found, None otherwise
        """
        try:
            order = self.session.query(Order).filter_by(order_number=order_number).one()
            
            # Ensure order has proper tax calculation
            if order and order.tax_amount == 0.0 and order.subtotal > 0:
                self._update_order_totals(order)
            
            return order
        except NoResultFound:
            return None
        except Exception as e:
            logger.error(f"Error getting order by number {order_number}: {e}")
            return None
    
    def complete_order(self, order: Order) -> bool:
        """
        Mark an order as completed.
        
        Args:
            order: The order to complete
            
        Returns:
            bool: True if order completed successfully
        """
        try:
            order.complete_order()
            if safe_commit(self.session):
                logger.info(f"Order {order.order_number} completed successfully")
                return True
            else:
                logger.error("Failed to commit order completion")
                return False
        except Exception as e:
            logger.error(f"Error completing order: {e}")
            self.session.rollback()
            return False
    
    def cancel_order(self, order: Order, user: User, reason: str = None) -> bool:
        """
        Cancel an order.
        
        Args:
            order: The order to cancel
            user: The user cancelling the order
            reason: Optional reason for cancellation
            
        Returns:
            bool: True if order cancelled successfully
        """
        try:
            order.cancel_order(user.id, reason)
            if safe_commit(self.session):
                logger.info(f"Order {order.order_number} cancelled successfully")
                return True
            else:
                logger.error("Failed to commit order cancellation")
                return False
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
            self.session.rollback()
            return False
    
    def update_order_customer_name(self, order: Order, customer_name: str) -> bool:
        """
        Update the customer name for an order.
        
        Args:
            order: The order to update
            customer_name: New customer name
            
        Returns:
            bool: True if updated successfully
        """
        try:
            order.customer_name = customer_name
            order.updated_at = get_current_local_time()
            if safe_commit(self.session):
                logger.info(f"Order {order.order_number} customer name updated")
                return True
            else:
                logger.error("Failed to commit customer name update")
                return False
        except Exception as e:
            logger.error(f"Error updating order customer name: {e}")
            self.session.rollback()
            return False
    
    def update_order_notes(self, order: Order, notes: str) -> bool:
        """
        Update the notes for an order.
        
        Args:
            order: The order to update
            notes: New notes
            
        Returns:
            bool: True if updated successfully
        """
        try:
            order.notes = notes
            order.updated_at = get_current_local_time()
            if safe_commit(self.session):
                logger.info(f"Order {order.order_number} notes updated")
                return True
            else:
                logger.error("Failed to commit notes update")
                return False
        except Exception as e:
            logger.error(f"Error updating order notes: {e}")
            self.session.rollback()
            return False
    
    def get_orders_by_status(self, status: OrderStatus, limit: int = 50) -> List[Order]:
        """
        Get orders by status.
        
        Args:
            status: The status to filter by
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of orders with the specified status
        """
        try:
            return self.session.query(Order).filter(
                Order.status == status
            ).order_by(Order.updated_at.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting orders by status {status}: {e}")
            return []
    
    def get_orders_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        """
        Get orders within a date range.
        
        Args:
            start_date: Start date for the range
            end_date: End date for the range
            
        Returns:
            List[Order]: List of orders within the date range
        """
        try:
            return self.session.query(Order).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ).order_by(Order.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting orders by date range: {e}")
            return []
    
    def get_today_order_count(self) -> int:
        """
        Get the number of orders created today.
        
        Returns:
            int: Number of orders created today
        """
        try:
            # Use local time for consistent timezone handling
            now = get_current_local_time()
            today = now.date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            count = self.session.query(Order).filter(
                Order.created_at >= today_start,
                Order.created_at <= today_end
            ).count()
            
            return count
        except Exception as e:
            logger.error(f"Error getting today's order count: {e}")
            return 0
    
    def get_today_orders(self) -> List[Order]:
        """
        Get all orders created today.
        
        Returns:
            List[Order]: List of orders created today
        """
        try:
            # Use local time for consistent timezone handling
            now = get_current_local_time()
            today = now.date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            return self.session.query(Order).filter(
                Order.created_at >= today_start,
                Order.created_at <= today_end
            ).order_by(Order.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting today's orders: {e}")
            return []
    
    def cleanup_old_completed_orders(self, hours_old: int = 24) -> int:
        """
        Remove completed and cancelled orders older than specified hours.
        
        Args:
            hours_old: Number of hours after which to remove orders (default: 24)
            
        Returns:
            int: Number of orders removed
        """
        try:
            cutoff_time = get_current_local_time() - timedelta(hours=hours_old)
            
            # Find completed and cancelled orders older than cutoff time
            old_orders = self.session.query(Order).filter(
                Order.status.in_([OrderStatus.COMPLETED, OrderStatus.CANCELLED]),
                Order.updated_at < cutoff_time
            ).all()
            
            removed_count = 0
            
            for order in old_orders:
                try:
                    # Delete order items first (due to foreign key constraints)
                    from models.order import order_products
                    self.session.execute(
                        order_products.delete().where(order_products.c.order_id == order.id)
                    )
                    
                    # Delete the order
                    self.session.delete(order)
                    removed_count += 1
                    
                    logger.info(f"Removed old order {order.order_number} (status: {order.status.value}, updated: {order.updated_at})")
                    
                except Exception as e:
                    logger.error(f"Error removing old order {order.order_number}: {e}")
                    continue
            
            # Commit all changes
            if safe_commit(self.session):
                logger.info(f"Successfully removed {removed_count} old completed/cancelled orders")
                return removed_count
            else:
                logger.error("Failed to commit order cleanup")
                return 0
                
        except Exception as e:
            logger.error(f"Error cleaning up old orders: {e}")
            self.session.rollback()
            return 0
    
    def _generate_order_number(self) -> str:
        """
        Generate a unique order number that resets daily.
        
        Returns:
            str: Unique order number in format ORD-YYYYMMDD-XXX
        """
        try:
            # Get today's date
            today = datetime.now().strftime("%Y%m%d")
            
            # Find the highest order number for today
            today_prefix = f"ORD-{today}-"
            
            # Get all orders from today
            today_orders = self.session.query(Order).filter(
                Order.order_number.like(f"{today_prefix}%")
            ).all()
            
            # Find the highest sequence number for today
            max_sequence = 0
            for order in today_orders:
                try:
                    # Extract sequence number from order number (e.g., "ORD-20241201-001" -> 1)
                    sequence_part = order.order_number.split('-')[-1]
                    sequence_num = int(sequence_part)
                    max_sequence = max(max_sequence, sequence_num)
                except (ValueError, IndexError):
                    # If parsing fails, continue to next order
                    continue
            
            # Generate next sequence number
            next_sequence = max_sequence + 1
            
            # Format order number with leading zeros (e.g., 001, 002, etc.)
            order_number = f"ORD-{today}-{next_sequence:03d}"
            
            # Ensure uniqueness (in case of race conditions)
            while self.get_order_by_number(order_number):
                next_sequence += 1
                order_number = f"ORD-{today}-{next_sequence:03d}"
            
            logger.info(f"Generated order number: {order_number}")
            return order_number
            
        except Exception as e:
            logger.error(f"Error generating order number: {e}")
            # Fallback to timestamp-based number if daily numbering fails
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            unique_id = str(uuid.uuid4())[:8]
            order_number = f"ORD-{timestamp}-{unique_id}"
            
            # Ensure uniqueness
            while self.get_order_by_number(order_number):
                unique_id = str(uuid.uuid4())[:8]
                order_number = f"ORD-{timestamp}-{unique_id}"
            
            return order_number

    def reset_order_manager(self, reset_type: str = "all", user: User = None) -> Dict[str, any]:
        """
        Reset the order management system based on the specified type.
        Instead of deleting orders, this method moves them to an archived state
        to preserve data for sales reports.
        
        Args:
            reset_type: Type of reset to perform
                - "active": Archive all active orders
                - "completed": Archive all completed orders
                - "cancelled": Archive all cancelled orders
                - "old": Clean up old orders (older than 24 hours)
                - "all": Perform all resets
            user: User performing the reset (for logging)
            
        Returns:
            Dict[str, any]: Results of the reset operation
        """
        try:
            results = {
                "success": True,
                "active_archived": 0,
                "completed_archived": 0,
                "cancelled_archived": 0,
                "old_cleared": 0,
                "errors": []
            }
            
            user_name = user.username if user else "Unknown"
            logger.info(f"Order manager reset initiated by {user_name} - Type: {reset_type}")
            
            if reset_type in ["active", "all"]:
                # Archive active orders instead of deleting them
                active_orders = self.get_active_orders()
                for order in active_orders:
                    try:
                        # Mark order as archived by adding a special note
                        order.notes = f"[ARCHIVED] {order.notes or ''}"
                        order.status = OrderStatus.CANCELLED  # Change status to cancelled
                        order.cancelled_by = user.id if user else None
                        order.cancelled_reason = "Archived during order manager reset"
                        order.updated_at = get_current_local_time()
                        
                        results["active_archived"] += 1
                        logger.info(f"Archived active order {order.order_number}")
                    except Exception as e:
                        error_msg = f"Error archiving active order {order.order_number}: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
            
            if reset_type in ["completed", "all"]:
                # Archive completed orders instead of deleting them
                completed_orders = self.get_completed_orders(limit=1000)  # Get all completed orders
                for order in completed_orders:
                    try:
                        # Mark order as archived by adding a special note
                        order.notes = f"[ARCHIVED] {order.notes or ''}"
                        order.updated_at = get_current_local_time()
                        
                        results["completed_archived"] += 1
                        logger.info(f"Archived completed order {order.order_number}")
                    except Exception as e:
                        error_msg = f"Error archiving completed order {order.order_number}: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
            
            if reset_type in ["cancelled", "all"]:
                # Archive cancelled orders instead of deleting them
                cancelled_orders = self.get_cancelled_orders(limit=1000)  # Get all cancelled orders
                for order in cancelled_orders:
                    try:
                        # Mark order as archived by adding a special note
                        order.notes = f"[ARCHIVED] {order.notes or ''}"
                        order.updated_at = get_current_local_time()
                        
                        results["cancelled_archived"] += 1
                        logger.info(f"Archived cancelled order {order.order_number}")
                    except Exception as e:
                        error_msg = f"Error archiving cancelled order {order.order_number}: {e}"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
            
            if reset_type in ["old", "all"]:
                # Clean up old orders (older than 24 hours) - this still deletes them
                results["old_cleared"] = self.cleanup_old_completed_orders(hours_old=24)
            
            # Commit all changes
            if safe_commit(self.session):
                total_archived = (results["active_archived"] + results["completed_archived"] + 
                                results["cancelled_archived"])
                
                logger.info(f"Order manager reset completed by {user_name}. "
                           f"Total orders archived: {total_archived}, old orders cleared: {results['old_cleared']}")
                
                if results["errors"]:
                    results["success"] = False
                    logger.warning(f"Order manager reset completed with {len(results['errors'])} errors")
                
                return results
            else:
                error_msg = "Failed to commit order manager reset"
                logger.error(error_msg)
                results["success"] = False
                results["errors"].append(error_msg)
                return results
                
        except Exception as e:
            error_msg = f"Error during order manager reset: {e}"
            logger.error(error_msg)
            results["success"] = False
            results["errors"].append(error_msg)
            self.session.rollback()
            return results

    def get_order_manager_stats(self) -> Dict[str, int]:
        """
        Get statistics about the order manager.
        
        Returns:
            Dict[str, int]: Statistics about orders
        """
        try:
            active_orders = len(self.get_active_orders())
            completed_orders = len(self.get_completed_orders(limit=1000))
            cancelled_orders = len(self.get_cancelled_orders(limit=1000))
            
            # Get today's orders
            today = datetime.now().date()
            today_orders = self.get_orders_by_date_range(
                datetime.combine(today, time.min),
                datetime.combine(today, time.max)
            )
            
            # Get total orders
            total_orders = self.session.query(Order).count()
            
            return {
                'active_orders': active_orders,
                'completed_orders': completed_orders,
                'cancelled_orders': cancelled_orders,
                'today_orders': len(today_orders),
                'total_orders': total_orders
            }
        except Exception as e:
            logger.error(f"Error getting order manager stats: {e}")
            return {
                'active_orders': 0,
                'completed_orders': 0,
                'cancelled_orders': 0,
                'today_orders': 0,
                'total_orders': 0
            }
    
    def has_order_data_for_date(self, target_date: date) -> bool:
        """
        Check if order data exists for a given date (including archived orders).
        
        Args:
            target_date: The date to check for order data
            
        Returns:
            bool: True if order data exists for the date, False otherwise
        """
        try:
            start_datetime = datetime.combine(target_date, time.min)
            end_datetime = datetime.combine(target_date, time.max)
            
            order_count = self.session.query(Order).filter(
                and_(
                    Order.created_at >= start_datetime,
                    Order.created_at <= end_datetime
                )
            ).count()
            
            return order_count > 0
        except Exception as e:
            logger.error(f"Error checking order data for date {target_date}: {e}")
            return False
    
    def get_all_orders_for_date(self, target_date: date) -> List[Order]:
        """
        Get all orders for a given date (including archived ones) for reporting purposes.
        
        Args:
            target_date: The date to get orders for
            
        Returns:
            List[Order]: List of all orders for the date
        """
        try:
            start_datetime = datetime.combine(target_date, time.min)
            end_datetime = datetime.combine(target_date, time.max)
            
            orders = self.session.query(Order).filter(
                and_(
                    Order.created_at >= start_datetime,
                    Order.created_at <= end_datetime
                )
            ).order_by(Order.created_at.desc()).all()
            
            return orders
        except Exception as e:
            logger.error(f"Error getting orders for date {target_date}: {e}")
            return []
    
    def recalculate_all_orders_tax(self) -> Dict[str, int]:
        """
        Recalculate tax amounts for all orders based on current product categories.
        This is useful after updating tax rates or when fixing existing orders.
        
        Returns:
            Dict[str, int]: Results of the recalculation
        """
        try:
            results = {
                "success": True,
                "orders_updated": 0,
                "orders_skipped": 0,
                "errors": []
            }
            
            # Get all orders
            all_orders = self.session.query(Order).all()
            
            for order in all_orders:
                try:
                    # Store original values for comparison
                    original_tax = order.tax_amount
                    original_total = order.total_amount
                    
                    # Update totals (this will recalculate tax)
                    self._update_order_totals(order)
                    
                    # Check if values changed
                    if (abs(order.tax_amount - original_tax) > 0.01 or 
                        abs(order.total_amount - original_total) > 0.01):
                        results["orders_updated"] += 1
                        logger.info(f"Updated tax for order {order.order_number}: "
                                  f"tax ${original_tax:.2f} -> ${order.tax_amount:.2f}, "
                                  f"total ${original_total:.2f} -> ${order.total_amount:.2f}")
                    else:
                        results["orders_skipped"] += 1
                        
                except Exception as e:
                    error_msg = f"Error updating order {order.order_number}: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
            
            # Commit all changes
            if safe_commit(self.session):
                logger.info(f"Tax recalculation completed: {results['orders_updated']} updated, "
                           f"{results['orders_skipped']} skipped")
                return results
            else:
                error_msg = "Failed to commit tax recalculation"
                logger.error(error_msg)
                results["success"] = False
                results["errors"].append(error_msg)
                return results
                
        except Exception as e:
            error_msg = f"Error during tax recalculation: {e}"
            logger.error(error_msg)
            results["success"] = False
            results["errors"].append(error_msg)
            self.session.rollback()
            return results

    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}") 