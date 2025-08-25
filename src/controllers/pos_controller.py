#!/usr/bin/env python3
"""
POS Controller for Talinda POS System
====================================

Controller for managing POS operations including:
- Product and category management
- Search functionality
- Data retrieval for the POS interface

Author: Talinda POS Team
Version: 1.0.0
"""

import logging
from typing import List, Optional, Dict, Any
from models.product import Product, Category
from models.user import User
from controllers.sale_controller import SaleController

logger = logging.getLogger(__name__)


class POSController:
    """Controller for POS operations."""
    
    def __init__(self, database_manager=None, current_user=None, settings=None):
        """Initialize the POS controller."""
        self.database_manager = database_manager
        self.current_user = current_user
        self.settings = settings
        self.logger = logging.getLogger(__name__)
        self.sale_controller = SaleController()
    
    def get_categories(self) -> List[Category]:
        """Get all active categories."""
        try:
            if self.database_manager:
                return self.database_manager.get_categories()
            else:
                self.logger.warning("Database manager not available")
                return []
        except Exception as e:
            self.logger.error(f"Error getting categories: {str(e)}")
            return []
    
    def get_products(self, category: Optional[Category] = None) -> List[Product]:
        """Get all active products, optionally filtered by category."""
        try:
            if self.database_manager:
                return self.database_manager.get_products(category)
            else:
                self.logger.warning("Database manager not available")
                return []
        except Exception as e:
            self.logger.error(f"Error getting products: {str(e)}")
            return []
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """Get a product by its ID."""
        try:
            if self.database_manager:
                return self.database_manager.get_product_by_id(product_id)
            else:
                self.logger.warning("Database manager not available")
                return None
        except Exception as e:
            self.logger.error(f"Error getting product by ID {product_id}: {str(e)}")
            return None
    
    def search_products(self, search_term: str) -> List[Product]:
        """Search products by name or description."""
        try:
            if self.database_manager:
                return self.database_manager.search_products(search_term)
            else:
                self.logger.warning("Database manager not available")
                return []
        except Exception as e:
            self.logger.error(f"Error searching products: {str(e)}")
            return []
    
    def get_products_by_category(self, category_id: int) -> List[Product]:
        """Get all products in a specific category."""
        try:
            if self.database_manager:
                return self.database_manager.get_products_by_category(category_id)
            else:
                self.logger.warning("Database manager not available")
                return []
        except Exception as e:
            self.logger.error(f"Error getting products by category {category_id}: {str(e)}")
            return []
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get a user by their ID."""
        try:
            if self.database_manager:
                return self.database_manager.get_user_by_id(user_id)
            else:
                self.logger.warning("Database manager not available")
                return None
        except Exception as e:
            self.logger.error(f"Error getting user by ID {user_id}: {str(e)}")
            return None
    
    def get_current_user(self) -> Optional[User]:
        """Get the current user."""
        return self.current_user
    
    def set_current_user(self, user: User) -> None:
        """Set the current user."""
        self.current_user = user
        # Update sale controller user as well
        self.sale_controller.current_user = user
    
    def get_settings(self) -> Optional[Dict[str, Any]]:
        """Get the current settings."""
        return self.settings

    def add_to_cart(self, product: Product, quantity: int = 1) -> bool:
        """Add a product to the cart."""
        if not self.current_user:
            self.logger.error("Attempted to add to cart without a logged-in user")
            return False

        try:
            # First update the sale controller's user if needed
            if self.sale_controller.current_user != self.current_user:
                self.sale_controller.current_user = self.current_user
            
            # Then add the product to cart
            added = self.sale_controller.add_to_cart(product, quantity)
            if added:
                self.logger.info(f"Added {quantity} of {product.name} to cart")
                return True
            else:
                self.logger.error(f"Failed to add {product.name} to cart")
                return False
        except Exception as e:
            self.logger.error(f"Error adding product to cart: {str(e)}")
            return False
    
    def is_product_available(self, product: Product) -> bool:
        """Check if a product is available."""
        try:
            return True  # All products are always available
        except Exception as e:
            self.logger.error(f"Error checking product availability: {str(e)}")
            return False
    
    def get_product_stock_status(self, product: Product) -> str:
        """Get the availability status of a product."""
        try:
            return "available"  # All products are always available
        except Exception as e:
            self.logger.error(f"Error getting product availability status: {str(e)}")
            return "available"
    
    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Get a category by its ID."""
        try:
            categories = self.get_categories()
            for category in categories:
                if category.id == category_id:
                    return category
            return None
        except Exception as e:
            self.logger.error(f"Error getting category by ID {category_id}: {str(e)}")
            return None
    
    def get_category_by_name(self, category_name: str) -> Optional[Category]:
        """Get a category by its name."""
        try:
            categories = self.get_categories()
            for category in categories:
                if category.name.lower() == category_name.lower():
                    return category
            return None
        except Exception as e:
            self.logger.error(f"Error getting category by name {category_name}: {str(e)}")
            return None 