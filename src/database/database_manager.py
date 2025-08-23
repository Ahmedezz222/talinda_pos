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
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func, and_, desc, select
from datetime import datetime

from .db_config import get_fresh_session, safe_commit
from models.product import Product, Category
from models.user import User, Shift
from models.sale import Sale, sale_products
from models.order import Order, order_products

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
            query = session.query(Product).options(joinedload(Product.category))
            
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
        """Get products by category ID."""
        session = self.get_session()
        try:
            products = session.query(Product).filter(
                Product.category_id == category_id
            ).order_by(Product.name).all()
            return products
        except Exception as e:
            self.logger.error(f"Error getting products by category {category_id}: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_shift_details(self, shift_id: int) -> Optional[Dict[str, Any]]:
        """Get complete details for a specific shift."""
        session = self.get_session()
        try:
            shift = session.query(Shift).filter(Shift.id == shift_id).first()
            if not shift:
                return None
            
            # Get user information
            user = session.query(User).filter(User.id == shift.user_id).first()
            
            return {
                'shift_id': shift.id,
                'user_id': shift.user_id,
                'username': user.username if user else 'Unknown',
                'full_name': user.full_name if user else '',
                'opening_amount': shift.opening_amount,
                'open_time': shift.open_time,
                'close_time': shift.close_time,
                'status': shift.status.value,
                'duration': (shift.close_time - shift.open_time) if shift.close_time else None
            }
        except Exception as e:
            self.logger.error(f"Error getting shift details for shift {shift_id}: {str(e)}")
            return None
        finally:
            session.close()
    
    def get_shift_sales_by_payment(self, shift_id: int) -> List[Dict[str, Any]]:
        """Get sales breakdown by payment method for a shift."""
        session = self.get_session()
        try:
            # Get the shift to determine time range
            shift = session.query(Shift).filter(Shift.id == shift_id).first()
            if not shift:
                return []
            
            # Get sales during this shift period
            query = session.query(Sale).filter(
                and_(
                    Sale.timestamp >= shift.open_time,
                    Sale.timestamp <= (shift.close_time or datetime.utcnow())
                )
            )
            
            # For now, we'll group by total amount since payment method isn't stored
            # In a real implementation, you'd have a payment_method field in Sale
            sales = query.all()
            
            # Group by payment method (placeholder - assuming all are cash for now)
            payment_breakdown = {
                'Cash': sum(sale.total_amount for sale in sales),
                'Card': 0.0,
                'Other': 0.0
            }
            
            return [
                {'payment_method': method, 'total_amount': amount}
                for method, amount in payment_breakdown.items()
                if amount > 0
            ]
        except Exception as e:
            self.logger.error(f"Error getting shift sales by payment for shift {shift_id}: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_shift_product_sales(self, shift_id: int) -> List[Dict[str, Any]]:
        """Get product sales details for a shift."""
        session = self.get_session()
        try:
            # Get the shift to determine time range
            shift = session.query(Shift).filter(Shift.id == shift_id).first()
            if not shift:
                return []
            
            # Get sales during this shift period with product details
            sales = session.query(Sale).filter(
                and_(
                    Sale.timestamp >= shift.open_time,
                    Sale.timestamp <= (shift.close_time or datetime.utcnow())
                )
            ).all()
            
            # Get product sales from sale_products table
            product_sales = {}
            for sale in sales:
                # Get products for this sale
                sale_items = session.execute(
                    sale_products.select().where(sale_products.c.sale_id == sale.id)
                )
                
                for item in sale_items:
                    product_id = item.product_id
                    quantity = item.quantity
                    price = item.price_at_sale
                    total = quantity * price
                    
                    if product_id not in product_sales:
                        product_sales[product_id] = {
                            'product_id': product_id,
                            'quantity': 0,
                            'total_amount': 0.0
                        }
                    
                    product_sales[product_id]['quantity'] += quantity
                    product_sales[product_id]['total_amount'] += total
            
            # Get product names and format results
            result = []
            for product_id, data in product_sales.items():
                product = session.query(Product).filter(Product.id == product_id).first()
                if product:
                    result.append({
                        'product_name': product.name,
                        'quantity': data['quantity'],
                        'unit_price': data['total_amount'] / data['quantity'] if data['quantity'] > 0 else 0,
                        'total_amount': data['total_amount']
                    })
            
            # Sort by total amount descending
            result.sort(key=lambda x: x['total_amount'], reverse=True)
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting shift product sales for shift {shift_id}: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_shift_orders(self, shift_id: int) -> List[Dict[str, Any]]:
        """Get orders created during a shift."""
        session = self.get_session()
        try:
            # Get the shift to determine time range
            shift = session.query(Shift).filter(Shift.id == shift_id).first()
            if not shift:
                return []
            
            # Get orders created during this shift period
            orders = session.query(Order).filter(
                and_(
                    Order.created_at >= shift.open_time,
                    Order.created_at <= (shift.close_time or datetime.utcnow())
                )
            ).order_by(Order.created_at).all()
            
            result = []
            for order in orders:
                result.append({
                    'order_id': order.id,
                    'order_number': order.order_number,
                    'customer_name': order.customer_name or 'Walk-in',
                    'status': order.status.value,
                    'created_at': order.created_at,
                    'total_amount': order.total_amount,
                    'subtotal': order.subtotal,
                    'discount_amount': order.discount_amount,
                    'tax_amount': order.tax_amount
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting shift orders for shift {shift_id}: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_shift_sales_by_cashier(self, shift_id: int) -> List[Dict[str, Any]]:
        """Get sales breakdown by cashier for a shift."""
        session = self.get_session()
        try:
            # Get the shift to determine time range
            shift = session.query(Shift).filter(Shift.id == shift_id).first()
            if not shift:
                return []
            
            # Get sales during this shift period grouped by cashier
            sales_by_cashier = session.query(
                Sale.user_id,
                User.username,
                func.count(Sale.id).label('total_transactions'),
                func.sum(Sale.total_amount).label('total_amount')
            ).join(User, Sale.user_id == User.id).filter(
                and_(
                    Sale.timestamp >= shift.open_time,
                    Sale.timestamp <= (shift.close_time or datetime.utcnow())
                )
            ).group_by(Sale.user_id, User.username).all()
            
            result = []
            for cashier_id, username, transactions, amount in sales_by_cashier:
                result.append({
                    'cashier_id': cashier_id,
                    'cashier_name': username,
                    'total_transactions': transactions,
                    'total_amount': float(amount) if amount else 0.0
                })
            
            # Sort by total amount descending
            result.sort(key=lambda x: x['total_amount'], reverse=True)
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting shift sales by cashier for shift {shift_id}: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_all_shifts(self) -> List[Dict[str, Any]]:
        """Get all shifts with basic information."""
        session = self.get_session()
        try:
            shifts = session.query(Shift).order_by(desc(Shift.open_time)).all()
            result = []
            
            for shift in shifts:
                user = session.query(User).filter(User.id == shift.user_id).first()
                result.append({
                    'shift_id': shift.id,
                    'username': user.username if user else 'Unknown',
                    'open_time': shift.open_time,
                    'close_time': shift.close_time,
                    'status': shift.status.value,
                    'opening_amount': shift.opening_amount
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting all shifts: {str(e)}")
            return []
        finally:
            session.close()
    
    def get_shifts_by_date(self, target_date: datetime.date) -> List[Dict[str, Any]]:
        """Get shifts for a specific date."""
        session = self.get_session()
        try:
            # Convert date to datetime for comparison
            start_datetime = datetime.combine(target_date, datetime.min.time())
            end_datetime = datetime.combine(target_date, datetime.max.time())
            
            shifts = session.query(Shift).filter(
                and_(
                    Shift.open_time >= start_datetime,
                    Shift.open_time <= end_datetime
                )
            ).order_by(desc(Shift.open_time)).all()
            
            result = []
            for shift in shifts:
                user = session.query(User).filter(User.id == shift.user_id).first()
                result.append({
                    'shift_id': shift.id,
                    'username': user.username if user else 'Unknown',
                    'open_time': shift.open_time,
                    'close_time': shift.close_time,
                    'status': shift.status.value,
                    'opening_amount': shift.opening_amount
                })
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting shifts for date {target_date}: {str(e)}")
            return []
        finally:
            session.close() 