"""
Database migration script to add order management tables.
"""
from database.db_config import engine, Base, Session
from models.order import Order, OrderStatus, order_products
from models.user import User
from models.product import Product
import sqlalchemy

def migrate_add_orders():
    """Add order management tables to the database."""
    print("Starting order management migration...")
    
    try:
        # Create the new tables
        Base.metadata.create_all(engine, tables=[Order.__table__, order_products])
        print("✓ Order tables created successfully")
        
        # Verify the tables exist
        session = Session()
        
        # Check if orders table exists
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='orders'")
        if result.fetchone():
            print("✓ Orders table verified")
        else:
            print("✗ Orders table not found")
            return False
        
        # Check if order_products table exists
        result = session.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='order_products'")
        if result.fetchone():
            print("✓ Order products table verified")
        else:
            print("✗ Order products table not found")
            return False
        
        session.close()
        print("✓ Order management migration completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        return False

if __name__ == "__main__":
    migrate_add_orders() 