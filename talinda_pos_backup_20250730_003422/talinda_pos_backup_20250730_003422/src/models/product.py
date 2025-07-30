"""
Models for product-related data.
"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from database.db_config import Base
import enum

class CategoryType(enum.Enum):
    """Enum for product categories."""
    FOOD = "Food"
    BEVERAGE = "Beverage"
    DESSERT = "Dessert"
    OTHER = "Other"

class Category(Base):
    """Category model for products."""
    __tablename__ = 'categories'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    tax_rate = Column(Float, default=0.0)  # Tax rate as percentage (e.g., 14.0 for 14%)
    
    products = relationship("Product", back_populates="category")
    
    def __repr__(self):
        """String representation of the category."""
        return f"<Category(name={self.name}, tax_rate={self.tax_rate}%)>"

class Product(Base):
    """Product model."""
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))
    barcode = Column(String, unique=True, nullable=True)
    image_path = Column(String)
    
    category = relationship("Category", back_populates="products")
    
    def __repr__(self):
        """String representation of the product."""
        return f"<Product(name={self.name}, price={self.price})>"
