from typing import Optional, Dict
"""
Controller for sales and transaction operations.
"""
from typing import Optional, Dict, cast # type: ignore
from typing import Optional, Dict
from datetime import datetime, timezone
from database.db_config import Session
from models.sale import Sale, sale_products
from models.product import Product
from models.user import User
from sqlalchemy import update

class CartItem:
    """Class representing an item in the shopping cart."""
    def __init__(self, product: Product, quantity: int = 1):
        self.product = product
        self.quantity = quantity
        # Ensure price is a float, not a SQLAlchemy column
        self.price: float = float(getattr(product, 'price', 0.0))
        self.discount_percentage: float = 0.0  # Discount as percentage (0-100)
        self.discount_amount: float = 0.0      # Fixed discount amount
        
    @property
    def subtotal(self) -> float:
        """Calculate subtotal price for this item (before discount)."""
        return self.price * self.quantity
    
    @property
    def discount_total(self) -> float:
        """Calculate total discount for this item."""
        percentage_discount = self.subtotal * (self.discount_percentage / 100)
        return percentage_discount + self.discount_amount
    
    @property
    def total(self) -> float:
        """Calculate total price for this item (after discount)."""
        return self.subtotal - self.discount_total

class SaleController:
    """Controller for handling sale operations."""
    
    def __init__(self):
        """Initialize the sale controller."""
        self.session = Session()
        self.cart: Dict[int, CartItem] = {}
        self.current_user: Optional[User] = None
        self.cart_discount_percentage: float = 0.0  # Cart-wide discount percentage
        self.cart_discount_amount: float = 0.0      # Cart-wide fixed discount
    
    def add_to_cart(self, product: Product, quantity: int = 1) -> bool:
        """
        Add a product to the cart.
        
        Args:
            product: The product to add
            quantity: Quantity to add (default: 1)
        Returns:
            bool: True if added successfully, False if insufficient stock
        """
        current_stock = int(getattr(product, 'stock', 0))
        product_id = int(getattr(product, 'id', 0))
        if current_stock >= quantity:
            if product_id in self.cart:
                self.cart[product_id].quantity += quantity
            else:
                self.cart[product_id] = CartItem(product, quantity)
            return True
        return False
    
    def remove_from_cart(self, product_id: int) -> None:
        """
        Remove a product from the cart.
        
        Args:
            product_id: ID of the product to remove
        """
        if product_id in self.cart:
            del self.cart[product_id]
    
    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """
        Update the quantity of a product in the cart.
        
        Args:
            product_id: ID of the product to update
            quantity: New quantity
        Returns:
            bool: True if updated successfully, False if insufficient stock
        """
        if product_id in self.cart:
            product = self.cart[product_id].product
            current_stock = int(getattr(product, 'stock', 0))
            if current_stock >= quantity:
                self.cart[product_id].quantity = quantity
                return True
        return False
    
    def apply_item_discount(self, product_id: int, discount_percentage: float = 0.0, discount_amount: float = 0.0) -> bool:
        """
        Apply discount to a specific cart item.
        
        Args:
            product_id: ID of the product to discount
            discount_percentage: Discount percentage (0-100)
            discount_amount: Fixed discount amount
        Returns:
            bool: True if discount applied successfully
        """
        if product_id in self.cart:
            self.cart[product_id].discount_percentage = max(0.0, min(100.0, discount_percentage))
            self.cart[product_id].discount_amount = max(0.0, discount_amount)
            return True
        return False
    
    def apply_cart_discount(self, discount_percentage: float = 0.0, discount_amount: float = 0.0) -> None:
        """
        Apply discount to the entire cart.
        
        Args:
            discount_percentage: Discount percentage (0-100)
            discount_amount: Fixed discount amount
        """
        self.cart_discount_percentage = max(0.0, min(100.0, discount_percentage))
        self.cart_discount_amount = max(0.0, discount_amount)
    
    def get_cart_subtotal(self) -> float:
        """
        Calculate the subtotal of items in the cart (before any discounts).
        
        Returns:
            float: Subtotal price
        """
        return sum(item.subtotal for item in self.cart.values())
    
    def get_cart_discount_total(self) -> float:
        """
        Calculate the total discount amount for the cart.
        
        Returns:
            float: Total discount amount
        """
        item_discounts = sum(item.discount_total for item in self.cart.values())
        subtotal = self.get_cart_subtotal()
        cart_percentage_discount = subtotal * (self.cart_discount_percentage / 100)
        return item_discounts + cart_percentage_discount + self.cart_discount_amount
    
    def get_cart_total(self) -> float:
        """
        Calculate the total price of items in the cart (after all discounts).
        
        Returns:
            float: Total price
        """
        subtotal = self.get_cart_subtotal()
        discount_total = self.get_cart_discount_total()
        return max(0.0, subtotal - discount_total)
    
    def get_cart_tax_total(self) -> float:
        """
        Calculate the total tax amount for all items in the cart based on their category tax rates.
        
        Returns:
            float: Total tax amount
        """
        total_tax = 0.0
        for cart_item in self.cart.values():
            product = cart_item.product
            # Get the category's tax rate
            if hasattr(product, 'category') and product.category:
                tax_rate = getattr(product.category, 'tax_rate', 0.0)
                # Calculate tax on the item's total (after item discounts)
                item_total = cart_item.total
                item_tax = item_total * (tax_rate / 100.0)
                total_tax += item_tax
        return total_tax
    
    def get_cart_total_with_tax(self) -> float:
        """
        Calculate the total price of items in the cart including tax (after all discounts).
        
        Returns:
            float: Total price including tax
        """
        total_before_tax = self.get_cart_total()
        tax_total = self.get_cart_tax_total()
        return total_before_tax + tax_total
    
    def clear_cart(self) -> None:
        """Clear all items from the cart."""
        self.cart.clear()
        self.cart_discount_percentage = 0.0
        self.cart_discount_amount = 0.0
    
    def load_order_to_cart(self, order) -> None:
        """
        Load order items into the cart.
        
        Args:
            order: The order to load into cart
        """
        # Clear current cart
        self.clear_cart()
        
        # Load order items
        order_items = order.get_order_items()
        for item in order_items:
            # Re-attach the product to the current session to avoid detached instance errors
            product = item['product']
            if product.id:
                # Get the product from the current session to ensure it's attached
                attached_product = self.session.query(Product).filter_by(id=product.id).first()
                if attached_product:
                    self.add_to_cart(attached_product, item['quantity'])
    
    def complete_sale(self, user: User) -> bool:
        """
        Complete the sale transaction.
        
        Args:
            user: The user completing the sale
        Returns:
            bool: True if sale completed successfully, False otherwise
        """
        if not self.cart:
            return False
        try:
            sale = Sale(
                total_amount=self.get_cart_total_with_tax(),
                user_id=int(getattr(user, 'id', 0)),
                timestamp=datetime.now(timezone.utc)
            )
            self.session.add(sale)
            for cart_item in self.cart.values():
                product = cart_item.product
                # Update product stock using SQLAlchemy update
                self.session.execute(
                    update(Product)
                    .where(Product.id == int(getattr(product, 'id', 0)))
                    .values(stock=int(getattr(product, 'stock', 0)) - cart_item.quantity)
                )
                # Add to sale_products table
                self.session.execute(
                    sale_products.insert().values(
                        sale_id=sale.id,
                        product_id=int(getattr(product, 'id', 0)),
                        quantity=cart_item.quantity,
                        price_at_sale=cart_item.price
                    )
                )
            self.session.commit()
            self.clear_cart()
            return True
        except Exception:
            self.session.rollback()
            return False

    def get_sales_for_shift(self, user):
        """Return all sales for the user's current open shift."""
        from models.user import Shift, ShiftStatus
        shift = self.session.query(Shift).filter_by(user_id=user.id, status=ShiftStatus.OPEN).first()
        if not shift:
            return []
        return self.session.query(Sale).filter_by(user_id=user.id, shift_id=shift.id).all()
