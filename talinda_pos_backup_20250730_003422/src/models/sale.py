"""
Models for sales and transactions.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database.db_config import Base
from models.product import Product
from models.user import User

# Many-to-many relationship table for sales and products
sale_products = Table(
    'sale_products',
    Base.metadata,
    Column('sale_id', Integer, ForeignKey('sales.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True),
    Column('quantity', Integer, nullable=False),
    Column('price_at_sale', Float, nullable=False)
)

class Sale(Base):
    """Sale model for transactions."""
    __tablename__ = 'sales'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    total_amount = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    user = relationship("User")
    products = relationship("Product", secondary=sale_products)
    
    def __repr__(self):
        """String representation of the sale."""
        return f"<Sale(id={self.id}, total={self.total_amount})>"
