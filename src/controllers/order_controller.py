"""
Controller for order management operations.
"""
from typing import List, Optional, Dict
from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session
from models.order import Order, OrderStatus
from models.product import Product
from models.user import User
import uuid

class OrderController:
    """Controller for handling order operations."""
    
    def __init__(self):
        """Initialize the order controller."""
        self.session = Session()
    
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
        self.session.commit()
        return order
    
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
            order.update_totals()
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error adding items to order: {e}")
            return False
    
    def get_active_orders(self) -> List[Order]:
        """
        Get all active orders.
        
        Returns:
            List[Order]: List of active orders
        """
        return self.session.query(Order).filter(
            Order.status == OrderStatus.ACTIVE
        ).order_by(Order.created_at.desc()).all()
    
    def get_completed_orders(self, limit: int = 50) -> List[Order]:
        """
        Get completed orders.
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of completed orders
        """
        return self.session.query(Order).filter(
            Order.status == OrderStatus.COMPLETED
        ).order_by(Order.completed_at.desc()).limit(limit).all()
    
    def get_cancelled_orders(self, limit: int = 50) -> List[Order]:
        """
        Get cancelled orders.
        
        Args:
            limit: Maximum number of orders to return
            
        Returns:
            List[Order]: List of cancelled orders
        """
        return self.session.query(Order).filter(
            Order.status == OrderStatus.CANCELLED
        ).order_by(Order.cancelled_at.desc()).limit(limit).all()
    
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
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error completing order: {e}")
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
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error cancelling order: {e}")
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
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error updating order customer name: {e}")
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
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error updating order notes: {e}")
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
        return self.session.query(Order).filter(
            Order.status == status
        ).order_by(Order.updated_at.desc()).limit(limit).all()
    
    def get_orders_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Order]:
        """
        Get orders within a date range.
        
        Args:
            start_date: Start date for the range
            end_date: End date for the range
            
        Returns:
            List[Order]: List of orders within the date range
        """
        return self.session.query(Order).filter(
            Order.created_at >= start_date,
            Order.created_at <= end_date
        ).order_by(Order.created_at.desc()).all()
    
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
            self.session.close() 