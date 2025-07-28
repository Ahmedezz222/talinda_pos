"""
Controller for product-related operations.
"""
from typing import List, Optional
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

    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product by its ID.
        
        Args:
            product_id (int): The ID of the product to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            product = self.session.query(Product).filter_by(id=product_id).first()
            if not product:
                logger.warning(f"Product not found for deletion: {product_id}")
                return False
            
            # Check if product is used in any sales BEFORE attempting deletion
            from models.sale import sale_products
            sales_count = self.session.query(sale_products).filter_by(product_id=product_id).count()
            
            if sales_count > 0:
                logger.warning(f"Cannot delete product {product_id} - it is used in {sales_count} sales")
                raise ValueError(f"Cannot delete product '{product.name}' because it is used in {sales_count} sales.\n\nTo delete this product, you must first delete all sales containing this product using the product deletion interface.")
            
            product_name = product.name
            
            # Now attempt the deletion
            self.session.delete(product)
            
            if safe_commit(self.session):
                logger.info(f"Product deleted successfully: {product_name} (ID: {product_id})")
                return True
            else:
                logger.error("Failed to commit product deletion")
                return False
                
        except ValueError as e:
            # Re-raise ValueError for proper error handling in UI
            raise e
        except Exception as e:
            # Handle any other exceptions, including database constraint errors
            logger.error(f"Error deleting product {product_id}: {e}")
            self.session.rollback()
            
            # Check if this is a foreign key constraint error
            if "FOREIGN KEY constraint failed" in str(e):
                # Get sales info for better error message
                try:
                    from models.sale import sale_products
                    sales_count = self.session.query(sale_products).filter_by(product_id=product_id).count()
                    product = self.session.query(Product).filter_by(id=product_id).first()
                    if product:
                        raise ValueError(f"Cannot delete product '{product.name}' because it is used in {sales_count} sales.\n\nTo delete this product, you must first delete all sales containing this product using the product deletion interface.")
                except Exception:
                    pass
                
                raise ValueError(f"Cannot delete product because it is referenced by other records in the database.")
            
            return False

    def get_product_sales_info(self, product_id: int) -> dict:
        """
        Get information about sales that use a specific product.
        
        Args:
            product_id (int): The ID of the product
            
        Returns:
            dict: Dictionary containing sales information
        """
        try:
            from models.sale import sale_products, Sale
            
            # Get sales that contain this product
            sales_info = self.session.query(
                Sale.id,
                Sale.timestamp,
                Sale.total_amount,
                sale_products.c.quantity,
                sale_products.c.price_at_sale
            ).join(
                sale_products, Sale.id == sale_products.c.sale_id
            ).filter(
                sale_products.c.product_id == product_id
            ).all()
            
            return {
                'sales_count': len(sales_info),
                'sales_details': [
                    {
                        'sale_id': row[0],  # Sale.id
                        'timestamp': row[1],  # Sale.timestamp
                        'total_amount': row[2],  # Sale.total_amount
                        'quantity': row[3],  # sale_products.c.quantity
                        'price_at_sale': row[4]  # sale_products.c.price_at_sale
                    }
                    for row in sales_info
                ]
            }
            
        except Exception as e:
            logger.error(f"Error getting sales info for product {product_id}: {e}")
            return {'sales_count': 0, 'sales_details': []}

    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}")
