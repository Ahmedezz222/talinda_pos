"""
Models for order management and tracking.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String, Enum, Text, Table, text
from sqlalchemy.orm import relationship
from database.db_config import Base, get_fresh_session, safe_commit
from models.product import Product
from models.user import User
import enum
import logging

# Set up logging
logger = logging.getLogger(__name__)

class OrderStatus(enum.Enum):
    """Enum for order status."""
    ACTIVE = "active"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    PENDING = "pending"

# Many-to-many relationship table for orders and products
order_products = Table(
    'order_products',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('price_at_order', Float, nullable=False),
    Column('notes', Text, nullable=True)
)

class Order(Base):
    """Order model for managing orders with status tracking."""
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True)
    order_number = Column(String(20), unique=True, nullable=False)
    customer_name = Column(String(100), nullable=True)  # Name tag for the order
    status = Column(Enum(OrderStatus), default=OrderStatus.ACTIVE, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    cancelled_at = Column(DateTime, nullable=True)
    cancelled_by = Column(Integer, ForeignKey('users.id'), nullable=True)
    cancelled_reason = Column(Text, nullable=True)
    
    # Relationships
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", foreign_keys=[user_id])
    cancelled_user = relationship("User", foreign_keys=[cancelled_by])
    products = relationship("Product", secondary=order_products)
    
    # Order totals
    subtotal = Column(Float, nullable=False, default=0.0)
    discount_amount = Column(Float, nullable=False, default=0.0)
    tax_amount = Column(Float, nullable=False, default=0.0)
    total_amount = Column(Float, nullable=False, default=0.0)
    
    # Notes and special instructions
    notes = Column(Text, nullable=True)
    
    def __repr__(self):
        """String representation of the order."""
        return f"<Order(id={self.id}, number={self.order_number}, status={self.status.value})>"
    
    def get_order_items(self):
        """Get order items with quantities and prices."""
        session = get_fresh_session()
        try:
            # Get order items from the association table using SQLAlchemy
            from models.order import order_products
            result = session.execute(
                order_products.select().where(order_products.c.order_id == self.id)
            )
            items = []
            for row in result:
                product = session.query(Product).filter_by(id=row.product_id).first()
                if product:
                    items.append({
                        'product': product,
                        'quantity': row.quantity,
                        'price': row.price_at_order,
                        'notes': row.notes
                    })
            return items
        except Exception as e:
            logger.error(f"Error getting order items: {e}")
            return []
        finally:
            session.close()
    
    def update_totals(self):
        """Update order totals based on items."""
        try:
            items = self.get_order_items()
            self.subtotal = sum(item['price'] * item['quantity'] for item in items)
            # Apply any discounts and tax calculations here
            self.total_amount = self.subtotal - self.discount_amount + self.tax_amount
        except Exception as e:
            logger.error(f"Error updating order totals: {e}")
            # Set default values if calculation fails
            self.subtotal = 0.0
            self.discount_amount = 0.0
            self.tax_amount = 0.0
            self.total_amount = 0.0
    
    def complete_order(self):
        """Mark order as completed."""
        try:
            self.status = OrderStatus.COMPLETED
            self.completed_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            logger.info(f"Order {self.order_number} marked as completed")
        except Exception as e:
            logger.error(f"Error completing order: {e}")
    
    def cancel_order(self, user_id, reason=None):
        """Cancel the order."""
        try:
            self.status = OrderStatus.CANCELLED
            self.cancelled_at = datetime.utcnow()
            self.cancelled_by = user_id
            self.cancelled_reason = reason
            self.updated_at = datetime.utcnow()
            logger.info(f"Order {self.order_number} cancelled by user {user_id}")
        except Exception as e:
            logger.error(f"Error cancelling order: {e}")
    
    def get_status_display(self):
        """Get human-readable status."""
        status_map = {
            OrderStatus.ACTIVE: "Active",
            OrderStatus.COMPLETED: "Completed",
            OrderStatus.CANCELLED: "Cancelled",
            OrderStatus.PENDING: "Pending"
        }
        return status_map.get(self.status, self.status.value.title()) 