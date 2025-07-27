"""
Controller for product-related operations.
"""
from typing import List, Optional
from sqlalchemy.orm.exc import NoResultFound
from database.db_config import Session
from models.product import Product, Category, CategoryType

class ProductController:
    """Controller for handling product operations."""
    
    def __init__(self):
        """Initialize the product controller."""
        self.session = Session()
    
    def get_categories(self) -> List[Category]:
        """
        Get all product categories.
        
        Returns:
            List[Category]: List of all categories
        """
        return self.session.query(Category).all()
    
    def get_products(self, category: Optional[Category] = None) -> List[Product]:
        """
        Get products, optionally filtered by category.
        
        Args:
            category: Optional category to filter by
            
        Returns:
            List[Product]: List of matching products
        """
        query = self.session.query(Product)
        if category:
            query = query.filter(Product.category_id == category.id)
        return query.all()
    
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
    
    def update_stock(self, product_id: int, quantity_change: int) -> bool:
        """
        Update the stock level of a product.
        
        Args:
            product_id: ID of the product to update
            quantity_change: Amount to change the stock by (positive or negative)
            
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            product = self.session.query(Product).filter_by(id=product_id).one()
            new_stock = product.stock + quantity_change
            if new_stock >= 0:
                product.stock = new_stock
                self.session.commit()
                return True
            return False
        except NoResultFound:
            return False

    def add_product(self, name, description, price, category_id, stock=0, barcode=None, image_path=None):
        """
        Add a new product to the database.
        Args:
            name (str): Product name
            description (str): Product description
            price (float): Product price
            category_id (int): Category ID
            stock (int): Initial stock
            barcode (str): Product barcode
            image_path (str): Path to product image
        Returns:
            Product: The created product instance
        """
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
            stock=stock,
            barcode=barcode,
            image_path=image_path
        )
        self.session.add(product)
        self.session.commit()
        return product

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
