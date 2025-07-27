"""
Controller for order management operations.
"""
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session, safe_commit, get_fresh_session
from models.order import Order, OrderStatus
from models.product import Product
from models.user import User
import uuid
import logging

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
            
            # Calculate tax (could be based on product categories)
            if not hasattr(order, 'tax_amount') or order.tax_amount is None:
                order.tax_amount = 0.0
            
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
        Get all active orders.
        
        Returns:
            List[Order]: List of active orders
        """
        try:
            return self.session.query(Order).filter(
                Order.status == OrderStatus.ACTIVE
            ).order_by(Order.created_at.desc()).all()
        except Exception as e:
            logger.error(f"Error getting active orders: {e}")
            return []
    
    def get_completed_orders(self, limit: int = 50) -> List[Order]:
        """
        Get completed orders.
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of completed orders
        """
        try:
            return self.session.query(Order).filter(
                Order.status == OrderStatus.COMPLETED
            ).order_by(Order.completed_at.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting completed orders: {e}")
            return []
    
    def get_cancelled_orders(self, limit: int = 50) -> List[Order]:
        """
        Get cancelled orders.
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of cancelled orders
        """
        try:
            return self.session.query(Order).filter(
                Order.status == OrderStatus.CANCELLED
            ).order_by(Order.cancelled_at.desc()).limit(limit).all()
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
            return self.session.query(Order).filter_by(id=order_id).one()
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
            return self.session.query(Order).filter_by(order_number=order_number).one()
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
            order.updated_at = datetime.utcnow()
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
            order.updated_at = datetime.utcnow()
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
    
    def _generate_order_number(self) -> str:
        """
        Generate a unique order number.
        
        Returns:
            str: Unique order number
        """
        # Generate a timestamp-based order number
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        order_number = f"ORD-{timestamp}-{unique_id}"
        
        # Ensure uniqueness
        while self.get_order_by_number(order_number):
            unique_id = str(uuid.uuid4())[:8]
            order_number = f"ORD-{timestamp}-{unique_id}"
        
        return order_number
    
    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}") 