from typing import Optional, Dict, List
"""
Controller for sales and transaction operations.
"""
from typing import Optional, Dict, cast # type: ignore
from typing import Optional, Dict
from datetime import datetime, timezone
from database.db_config import Session, safe_commit, get_fresh_session
from models.sale import Sale, sale_products
from models.product import Product
from models.user import User
from models.order import Order, OrderStatus, order_products
from sqlalchemy import update
import logging

# Set up logging
logger = logging.getLogger(__name__)

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
        self.session = get_fresh_session()
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
            bool: True if added successfully
        """
        product_id = int(getattr(product, 'id', 0))
        if product_id in self.cart:
            self.cart[product_id].quantity += quantity
        else:
            self.cart[product_id] = CartItem(product, quantity)
        logger.debug(f"Added {quantity} of {product.name} to cart")
        return True
    
    def remove_from_cart(self, product_id: int) -> None:
        """
        Remove a product from the cart.
        
        Args:
            product_id: ID of the product to remove
        """
        if product_id in self.cart:
            product_name = self.cart[product_id].product.name
            del self.cart[product_id]
            logger.debug(f"Removed {product_name} from cart")
    
    def update_quantity(self, product_id: int, quantity: int) -> bool:
        """
        Update the quantity of a product in the cart.
        
        Args:
            product_id: ID of the product to update
            quantity: New quantity
        Returns:
            bool: True if updated successfully
        """
        if product_id in self.cart:
            self.cart[product_id].quantity = quantity
            logger.debug(f"Updated quantity of {self.cart[product_id].product.name} to {quantity}")
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
            logger.debug(f"Applied discount to product {product_id}")
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
        logger.debug(f"Applied cart-wide discount: {discount_percentage}% + ${discount_amount}")
    
    def get_cart_subtotal(self) -> float:
        """
        Calculate the subtotal of items in the cart (before any discounts).
        
        Returns:
            float: Subtotal price
        """
        return sum(item.subtotal for item in self.cart.values())
    
    def get_cart_discount_total(self) -> float:
        """
        Calculate the total discount for the cart.
        
        Returns:
            float: Total discount amount
        """
        # Item-level discounts
        item_discounts = sum(item.discount_total for item in self.cart.values())
        
        # Cart-level discounts
        cart_subtotal = self.get_cart_subtotal()
        cart_percentage_discount = cart_subtotal * (self.cart_discount_percentage / 100)
        cart_total_discount = cart_percentage_discount + self.cart_discount_amount
        
        return item_discounts + cart_total_discount
    
    def get_cart_total(self) -> float:
        """
        Calculate the total price for the cart (after all discounts).
        
        Returns:
            float: Total price
        """
        return self.get_cart_subtotal() - self.get_cart_discount_total()

    def get_cart_tax_total(self) -> float:
        """
        Calculate the total tax for the cart based on product categories.
        
        Returns:
            float: Total tax amount
        """
        try:
            total_tax = 0.0
            for cart_item in self.cart.values():
                product = cart_item.product
                if hasattr(product, 'category') and product.category:
                    tax_rate = getattr(product.category, 'tax_rate', 0.0)
                    item_total = cart_item.total  # After item discounts
                    item_tax = item_total * (tax_rate / 100.0)
                    total_tax += item_tax
            
            # Apply cart-level discount to tax calculation
            if self.cart_discount_percentage > 0 or self.cart_discount_amount > 0:
                # Recalculate tax based on final cart total
                cart_subtotal = self.get_cart_subtotal()
                cart_discount = self.get_cart_discount_total()
                discount_ratio = cart_discount / cart_subtotal if cart_subtotal > 0 else 0
                total_tax *= (1 - discount_ratio)
            
            return total_tax
        except Exception as e:
            logger.error(f"Error calculating cart tax: {e}")
            return 0.0

    def get_cart_total_with_tax(self) -> float:
        """
        Calculate the total price for the cart including tax.
        
        Returns:
            float: Total price with tax
        """
        return self.get_cart_total() + self.get_cart_tax_total()

    def load_order_to_cart(self, order) -> bool:
        """
        Load an order's items into the cart.
        
        Args:
            order: Order object to load into cart
            
        Returns:
            bool: True if loaded successfully, False otherwise
        """
        try:
            # Clear current cart first
            self.clear_cart()
            
            # Get order items
            order_items = order.get_order_items()
            
            # Add each item to cart
            for item in order_items:
                product = item['product']
                quantity = item['quantity']
                
                # Check if product still exists
                current_product = self.session.query(Product).filter_by(id=product.id).first()
                if not current_product:
                    logger.warning(f"Product {product.name} (ID: {product.id}) no longer exists")
                    continue
                
                # Add to cart with the original price from the order
                cart_item = CartItem(current_product, quantity)
                cart_item.price = item['price']  # Use the price from the order
                self.cart[current_product.id] = cart_item
                logger.info(f"Added {quantity} of {current_product.name} to cart from order")
            
            logger.info(f"Loaded {len(self.cart)} items from order {order.order_number}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading order to cart: {e}")
            self.clear_cart()  # Clear cart on error
            return False

    def complete_sale(self, user) -> bool:
        """
        Complete a sale from the current cart.
        
        Args:
            user: User object who is completing the sale
            
        Returns:
            bool: True if sale completed successfully, False otherwise
        """
        try:
            if not self.cart:
                logger.warning("Cannot complete sale with empty cart")
                return False
            
            # Set the current user for the sale
            self.current_user = user
            
            # Process the sale using the existing process_sale method
            sale = self.process_sale()
            
            if sale:
                logger.info(f"Sale completed successfully by user {user.id}")
                return True
            else:
                logger.error("Failed to process sale")
                return False
                
        except Exception as e:
            logger.error(f"Error completing sale: {e}")
            return False

    def clear_cart(self) -> None:
        """Clear all items from the cart."""
        self.cart.clear()
        self.cart_discount_percentage = 0.0
        self.cart_discount_amount = 0.0
        logger.debug("Cart cleared")
    
    def process_sale(self, payment_method: str = "cash") -> Optional[Sale]:
        """
        Process the current cart as a sale and create a completed order.
        
        Args:
            payment_method: Method of payment (cash, card, etc.)
            
        Returns:
            Optional[Sale]: The created sale if successful, None otherwise
        """
        if not self.current_user:
            logger.error("No current user for sale processing")
            return None
        
        if not self.cart:
            logger.warning("Cannot process sale with empty cart")
            return None
        
        try:
            # Create the sale record
            total_amount = self.get_cart_total_with_tax()  # Use total with tax
            sale = Sale(
                total_amount=total_amount,
                user_id=self.current_user.id
            )
            
            self.session.add(sale)
            # Flush to get the sale ID
            self.session.flush()
            
            # Add products to the sale
            for product_id, cart_item in self.cart.items():
                # Add to sale_products table
                self.session.execute(
                    sale_products.insert().values(
                        sale_id=sale.id,
                        product_id=product_id,
                        quantity=cart_item.quantity,
                        price_at_sale=cart_item.price
                    )
                )
            
            # Create a completed order for the sale
            self._create_completed_order_from_sale(sale)
            
            # Commit the transaction
            if safe_commit(self.session):
                logger.info(f"Sale processed successfully: ${total_amount:.2f}")
                # Clear the cart after successful sale
                self.clear_cart()
                return sale
            else:
                logger.error("Failed to commit sale transaction")
                return None
                
        except Exception as e:
            logger.error(f"Error processing sale: {e}")
            self.session.rollback()
            return None
    
    def _create_completed_order_from_sale(self, sale: Sale) -> None:
        """
        Create a completed order from a sale for order history tracking.
        
        Args:
            sale: The sale object to create order from
        """
        try:
            from controllers.order_controller import OrderController
            from models.order import Order, OrderStatus
            
            # Create order controller
            order_controller = OrderController()
            
            # Generate order number based on sale
            order_number = f"SALE-{sale.id:06d}"
            
            # Create the order
            order = Order(
                order_number=order_number,
                customer_name=f"Sale #{sale.id}",
                user_id=sale.user_id,
                status=OrderStatus.COMPLETED,
                created_at=sale.timestamp,
                completed_at=sale.timestamp,
                subtotal=sale.total_amount,
                total_amount=sale.total_amount,
                notes=f"Completed sale - Payment processed"
            )
            
            # Add order to session
            self.session.add(order)
            self.session.flush()  # Get the order ID
            
            # Add order items from sale
            for product_id, cart_item in self.cart.items():
                # Add to order_products table
                from models.order import order_products
                self.session.execute(
                    order_products.insert().values(
                        order_id=order.id,
                        product_id=product_id,
                        quantity=cart_item.quantity,
                        price_at_order=cart_item.price,
                        notes=None
                    )
                )
            
            logger.info(f"Created completed order {order_number} from sale {sale.id}")
            
        except Exception as e:
            logger.error(f"Error creating completed order from sale: {e}")
            # Don't fail the sale if order creation fails
            pass
    
    def get_sales_history(self, limit: int = 50) -> List[Sale]:
        """
        Get recent sales history.
        
        Args:
            limit: Maximum number of sales to return
            
        Returns:
            List[Sale]: List of recent sales
        """
        try:
            return self.session.query(Sale).order_by(Sale.timestamp.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error getting sales history: {e}")
            return []

    def delete_sale(self, sale_id: int) -> bool:
        """
        Delete a sale.
        
        Args:
            sale_id: ID of the sale to delete
            
        Returns:
            bool: True if deletion successful, False otherwise
        """
        try:
            # Get the sale with its products
            sale = self.session.query(Sale).filter_by(id=sale_id).first()
            if not sale:
                logger.warning(f"Sale not found for deletion: {sale_id}")
                return False
            
            # Get the products in this sale
            sale_products_data = self.session.execute(
                sale_products.select().where(sale_products.c.sale_id == sale_id)
            ).fetchall()
            

            
            # Delete the sale
            self.session.delete(sale)
            
            if safe_commit(self.session):
                logger.info(f"Sale {sale_id} deleted successfully")
                return True
            else:
                logger.error("Failed to commit sale deletion")
                return False
                
        except Exception as e:
            logger.error(f"Error deleting sale {sale_id}: {e}")
            self.session.rollback()
            return False

    def __del__(self):
        """Clean up the session."""
        if hasattr(self, 'session'):
            try:
                self.session.close()
            except Exception as e:
                logger.error(f"Error closing session: {e}")
