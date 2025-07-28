#!/usr/bin/env python3
"""
Database Manager for Talinda POS System
======================================

A simple wrapper around the database configuration to provide
a consistent interface for database operations.

Author: Talinda POS Team
Version: 1.0.0
"""

import logging
from typing import List, Optional
from sqlalchemy.orm import Session

from .db_config import get_fresh_session, safe_commit
from models.product import Product, Category
from models.user import User

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Simple database manager for POS operations."""
    
    def __init__(self):
        """Initialize the database manager."""
        self.logger = logging.getLogger(__name__)
    
    def get_session(self) -> Session:
        """Get a fresh database session."""
        return get_fresh_session()
    
    def initialize_database(self):
        """Initialize the database (placeholder for compatibility)."""
        # The database is already initialized by the main application
        self.logger.info("Database manager initialized")
    
    def get_categories(self) -> List[Category]:
        """Get all categories."""
        session = self.get_session()
        try:
            categories = session.query(Category).order_by(Category.name).all()
            return categories
        except Exception as e:
            self.logger.error(f"Error getting categories: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_products(self, category: Optional[Category] = None) -> List[Product]:
        """Get all products, optionally filtered by category."""
        session = self.get_session()
        try:
            query = session.query(Product)
            
            if category:
                query = query.filter(Product.category_id == category.id)
            
            products = query.order_by(Product.name).all()
            return products
        except Exception as e:
            self.logger.error(f"Error getting products: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID."""
        session = self.get_session()
        try:
            product = session.query(Product).filter(Product.id == product_id).first()
            return product
        except Exception as e:
            self.logger.error(f"Error getting product by ID {product_id}: {str(e)}")
            return None
        finally:
            session.close()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            return user
        except Exception as e:
            self.logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            return None
        finally:
            session.close()
    
    def search_products(self, search_term: str) -> List[Product]:
        """Search products by name or description."""
        session = self.get_session()
        try:
            search_pattern = f"%{search_term}%"
            products = session.query(Product).filter(
                Product.name.ilike(search_pattern)
            ).order_by(Product.name).all()
            return products
        except Exception as e:
            self.logger.error(f"Error searching products: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_products_by_category(self, category_id: int) -> List[Product]:
        """Get all products in a specific category."""
        session = self.get_session()
        try:
            products = session.query(Product).filter(
                Product.is_active == True,
                Product.category_id == category_id
            ).order_by(Product.name).all()
            return products
        except Exception as e:
            self.logger.error(f"Error getting products by category {category_id}: {str(e)}")
            return []
        finally:
            session.close() 