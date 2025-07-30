"""
Controller for product-related operations.
"""
from typing import List, Optional, Dict
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session, safe_commit, get_fresh_session
from models.product import Product, Category, CategoryType
import logging

# Set up logging
logger = logging.getLogger(__name__)

class ProductController:
    """Controller for handling product operations."""
    
    def __init__(self):
        """Initialize the product controller."""
        self.session = get_fresh_session()
    
    def get_categories(self) -> List[Category]:
        """
        Get all product categories.
        
        Returns:
            List[Category]: List of all categories
        """
        try:
            return self.session.query(Category).all()
        except Exception as e:
            logger.error(f"Error getting categories: {e}")
            return []
    
    def get_products(self, category: Optional[Category] = None) -> List[Product]:
        """
        Get products, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            
        Returns:
            List[Product]: List of matching products
        """
        try:
            query = self.session.query(Product)
            if category:
                query = query.filter(Product.category_id == category.id)
            return query.all()
        except Exception as e:
            logger.error(f"Error getting products: {e}")
            return []
    
    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        """
        Get a product by its ID.
        
        Args:
            product_id: ID of the product to retrieve
            
        Returns:
            Optional[Product]: The product if found, None otherwise
        """
        try:
            return self.session.query(Product).filter_by(id=product_id).one()
        except NoResultFound:
            return None
        except Exception as e:
            logger.error(f"Error getting product by ID {product_id}: {e}")
            return None
    
    def add_product(self, name, description, price, category_id, barcode=None, image_path=None):
        """
        Add a new product to the database.
        Args:
            name (str): Product name
            description (str): Product description
            price (float): Product price
            category_id (int): Category ID
            barcode (str): Product barcode
            image_path (str): Path to product image
        Returns:
            Product: The created product instance
        """
        try:
            # Handle empty barcode - convert empty string to None to avoid unique constraint issues
            if barcode == '' or barcode is None:
                barcode = None
            else:
                # Check if barcode already exists (only if barcode is not None)
                existing_product = self.session.query(Product).filter_by(barcode=barcode).first()
                if existing_product:
                    raise ValueError(f'Product with barcode "{barcode}" already exists')
            
            product = Product(
                name=name,
                description=description,
                price=price,
                category_id=category_id,
                barcode=barcode,
                image_path=image_path
            )
            
            self.session.add(product)
            
            if safe_commit(self.session):
                logger.info(f"Product added successfully: {name}")
                return product
            else:
                logger.error("Failed to commit product addition")
                raise Exception("Failed to add product due to database lock")
                
        except Exception as e:
            logger.error(f"Error adding product: {e}")
            self.session.rollback()
            raise e
    
    def add_category(self, name: str, tax_rate: float = 14.0) -> Category:
        """
        Add a new category to the database.
        Args:
            name (str): Category name
            tax_rate (float): Tax rate as percentage (default 14.0 for 14%)
        Returns:
            Category: The created category instance
        """
        # Check if category already exists
        existing_category = self.session.query(Category).filter_by(name=name).first()
        if existing_category:
            raise ValueError(f'Category "{name}" already exists')
        
        category = Category(name=name, description=f"{name} category", tax_rate=tax_rate)
        self.session.add(category)
        self.session.commit()
        return category

    def delete_category(self, category_id: int):
        """
        Delete a category by its ID. Raises an exception if the category is in use.
        Args:
            category_id (int): The ID of the category to delete
        """
        category = self.session.query(Category).filter_by(id=category_id).first()
        if not category:
            raise ValueError('Category not found')
        # Check if any product uses this category
        if self.session.query(Product).filter_by(category_id=category_id).count() > 0:
            raise Exception('Category is in use by products')
        self.session.delete(category)
        self.session.commit()

    def update_category(self, category_id: int, name: str, description: str = None, tax_rate: float = None) -> Category:
        """
        Update a category by its ID.
        Args:
            category_id (int): The ID of the category to update
            name (str): New category name
            description (str): New category description (optional)
            tax_rate (float): New tax rate as percentage (optional)
        Returns:
            Category: The updated category instance
        """
        category = self.session.query(Category).filter_by(id=category_id).first()
        if not category:
            raise ValueError('Category not found')
        
        # Check if new name already exists (excluding current category)
        if name != category.name:
            existing_category = self.session.query(Category).filter_by(name=name).first()
            if existing_category:
                raise ValueError(f'Category "{name}" already exists')
        
        # Update fields
        category.name = name.strip()
        if description is not None:
            category.description = description.strip() if description else None
        if tax_rate is not None:
            category.tax_rate = tax_rate
        
        if safe_commit(self.session):
            logger.info(f"Category updated successfully: {category.name}")
            return category
        else:
            logger.error("Failed to commit category update")
            raise Exception("Failed to update category")

    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product by its ID.
        
        Args:
            product_id: ID of the product to delete
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            product = self.session.query(Product).filter_by(id=product_id).one()
            self.session.delete(product)
            
            if safe_commit(self.session):
                logger.info(f"Product deleted successfully: {product.name}")
                return True
            else:
                logger.error("Failed to commit product deletion")
                return False
                
        except NoResultFound:
            logger.warning(f"Product with ID {product_id} not found")
            return False
        except Exception as e:
            logger.error(f"Error deleting product {product_id}: {e}")
            self.session.rollback()
            return False

    def update_product(self, product_id: int, name: str = None, description: str = None, 
                      price: float = None, category_id: int = None, barcode: str = None, 
                      image_path: str = None) -> bool:
        """
        Update a product by its ID.
        
        Args:
            product_id: ID of the product to update
            name: New product name
            description: New product description
            price: New product price
            category_id: New category ID
            barcode: New barcode
            image_path: New image path
            
        Returns:
            bool: True if updated successfully, False otherwise
        """
        try:
            product = self.session.query(Product).filter_by(id=product_id).one()
            
            # Update fields if provided
            if name is not None:
                # Validate name is not empty
                if not name.strip():
                    raise ValueError("Product name cannot be empty")
                product.name = name.strip()
            if description is not None:
                product.description = description.strip() if description else None
            if price is not None:
                # Validate price is positive
                if price <= 0:
                    raise ValueError("Product price must be greater than 0")
                product.price = price
            if category_id is not None:
                product.category_id = category_id
            if barcode is not None:
                # Check if barcode already exists (only if barcode is not None and different from current)
                if barcode != product.barcode:
                    existing_product = self.session.query(Product).filter_by(barcode=barcode).first()
                    if existing_product and existing_product.id != product_id:
                        raise ValueError(f'Product with barcode "{barcode}" already exists')
                product.barcode = barcode.strip() if barcode else None
            if image_path is not None:
                product.image_path = image_path.strip() if image_path else None
            
            if safe_commit(self.session):
                logger.info(f"Product updated successfully: {product.name}")
                return True
            else:
                logger.error("Failed to commit product update")
                return False
                
        except NoResultFound:
            logger.warning(f"Product with ID {product_id} not found")
            return False
        except ValueError as e:
            logger.error(f"Validation error updating product {product_id}: {e}")
            raise e
        except Exception as e:
            logger.error(f"Error updating product {product_id}: {e}")
            self.session.rollback()
            return False

    def reset_product_manager(self, reset_type: str = "all", user=None) -> Dict[str, any]:
        """
        Reset the product management system based on the specified type.
        
        Args:
            reset_type: Type of reset to perform
                - "products": Clear all products only
                - "categories": Clear all categories (and their products)
                - "all": Clear all products and categories
            user: User performing the reset (for logging)
            
        Returns:
            Dict[str, any]: Results of the reset operation
        """
        try:
            results = {
                "success": True,
                "products_cleared": 0,
                "categories_cleared": 0,
                "errors": []
            }
            
            user_name = user.username if user else "Unknown"
            logger.info(f"Product manager reset initiated by {user_name} - Type: {reset_type}")
            
            if reset_type in ["products", "all"]:
                # Clear all products first (to avoid foreign key constraints)
                try:
                    products = self.session.query(Product).all()
                    for product in products:
                        try:
                            self.session.delete(product)
                            results["products_cleared"] += 1
                            logger.info(f"Cleared product: {product.name}")
                        except Exception as e:
                            error_msg = f"Error clearing product {product.name}: {e}"
                            logger.error(error_msg)
                            results["errors"].append(error_msg)
                    
                    # Commit products deletion first
                    if safe_commit(self.session):
                        logger.info(f"Successfully cleared {results['products_cleared']} products")
                    else:
                        error_msg = "Failed to commit products deletion"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
                        results["success"] = False
                        return results
                        
                except Exception as e:
                    error_msg = f"Error querying products: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    results["success"] = False
                    return results
            
            if reset_type in ["categories", "all"]:
                # Clear all categories (products should already be cleared)
                try:
                    categories = self.session.query(Category).all()
                    for category in categories:
                        try:
                            self.session.delete(category)
                            results["categories_cleared"] += 1
                            logger.info(f"Cleared category: {category.name}")
                        except Exception as e:
                            error_msg = f"Error clearing category {category.name}: {e}"
                            logger.error(error_msg)
                            results["errors"].append(error_msg)
                    
                    # Commit categories deletion
                    if safe_commit(self.session):
                        logger.info(f"Successfully cleared {results['categories_cleared']} categories")
                    else:
                        error_msg = "Failed to commit categories deletion"
                        logger.error(error_msg)
                        results["errors"].append(error_msg)
                        results["success"] = False
                        return results
                        
                except Exception as e:
                    error_msg = f"Error querying categories: {e}"
                    logger.error(error_msg)
                    results["errors"].append(error_msg)
                    results["success"] = False
                    return results
            
            total_cleared = results["products_cleared"] + results["categories_cleared"]
            
            logger.info(f"Product manager reset completed by {user_name}. "
                       f"Total items cleared: {total_cleared}")
            
            if results["errors"]:
                results["success"] = False
                logger.warning(f"Product manager reset completed with {len(results['errors'])} errors")
            
            return results
                
        except Exception as e:
            error_msg = f"Error during product manager reset: {e}"
            logger.error(error_msg)
            results["success"] = False
            results["errors"].append(error_msg)
            self.session.rollback()
            return results

    def get_product_manager_stats(self) -> Dict[str, int]:
        """
        Get statistics about the product management system.
        
        Returns:
            Dict[str, int]: Statistics about products and categories
        """
        try:
            stats = {
                "total_products": 0,
                "total_categories": 0,
                "products_with_barcodes": 0,
                "products_with_images": 0,
                "categories_with_products": 0
            }
            
            # Count total products
            stats["total_products"] = self.session.query(Product).count()
            
            # Count total categories
            stats["total_categories"] = self.session.query(Category).count()
            
            # Count products with barcodes
            stats["products_with_barcodes"] = self.session.query(Product).filter(
                Product.barcode.isnot(None)
            ).count()
            
            # Count products with images
            stats["products_with_images"] = self.session.query(Product).filter(
                Product.image_path.isnot(None)
            ).count()
            
            # Count categories that have products
            categories_with_products = self.session.query(Category).join(Product).distinct().count()
            stats["categories_with_products"] = categories_with_products
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting product manager stats: {e}")
            return {
                "total_products": 0,
                "total_categories": 0,
                "products_with_barcodes": 0,
                "products_with_images": 0,
                "categories_with_products": 0
            }

    def seed_default_categories(self) -> bool:
        """
        Seed the database with default categories.
        
        Returns:
            bool: True if seeded successfully
        """
        try:
            default_categories = [
                {"name": "Food", "description": "Food items", "tax_rate": 14.0},
                {"name": "Beverage", "description": "Beverages and drinks", "tax_rate": 14.0},
                {"name": "Dessert", "description": "Desserts and sweets", "tax_rate": 14.0},
                {"name": "Other", "description": "Other items", "tax_rate": 14.0}
            ]
            
            categories_added = 0
            for cat_data in default_categories:
                # Check if category already exists
                existing = self.session.query(Category).filter_by(name=cat_data["name"]).first()
                if not existing:
                    category = Category(
                        name=cat_data["name"],
                        description=cat_data["description"],
                        tax_rate=cat_data["tax_rate"]
                    )
                    self.session.add(category)
                    categories_added += 1
                    logger.info(f"Added default category: {cat_data['name']}")
            
            if safe_commit(self.session):
                logger.info(f"Successfully seeded {categories_added} default categories")
                return True
            else:
                logger.error("Failed to commit default categories")
                return False
                
        except Exception as e:
            logger.error(f"Error seeding default categories: {e}")
            self.session.rollback()
            return False

    def get_product_sales_info(self, product_id: int) -> Dict:
        """
        Get sales information for a specific product.
        
        Args:
            product_id: ID of the product
            
        Returns:
            Dict: Sales information including count and details
        """
        try:
            from models.sale import sale_products
            
            # Get sales count
            sales_count = self.session.query(sale_products).filter_by(product_id=product_id).count()
            
            # Get sales details
            sales_details = []
            if sales_count > 0:
                # Get sales with this product
                sales_query = self.session.query(sale_products).filter_by(product_id=product_id).all()
                
                for sale_product in sales_query:
                    # Get the sale details
                    from models.sale import Sale
                    sale = self.session.query(Sale).filter_by(id=sale_product.sale_id).first()
                    if sale:
                        sales_details.append({
                            'sale_id': sale.id,
                            'timestamp': sale.timestamp,
                            'quantity': sale_product.quantity,
                            'price_at_sale': sale_product.price_at_sale,
                            'total_amount': sale.total_amount
                        })
            
            return {
                'sales_count': sales_count,
                'sales_details': sales_details
            }
            
        except Exception as e:
            logger.error(f"Error getting sales info for product {product_id}: {e}")
            return {
                'sales_count': 0,
                'sales_details': []
            }

    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}")
