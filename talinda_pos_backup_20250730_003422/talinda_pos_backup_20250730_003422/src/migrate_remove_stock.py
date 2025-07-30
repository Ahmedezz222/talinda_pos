"""
Database migration script to remove stock column from products table.
"""
import sys
import os

# Add the src directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

from database.db_config import engine, safe_commit
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_remove_stock():
    """Remove stock column from products table."""
    try:
        # Create a new connection
        connection = engine.connect()
        
        # Check if stock column exists
        result = connection.execute(text("PRAGMA table_info(products)"))
        columns = [row[1] for row in result.fetchall()]
        
        if 'stock' in columns:
            logger.info("Removing stock column from products table...")
            
            # Drop the new table if it exists from a previous failed migration
            try:
                connection.execute(text("DROP TABLE IF EXISTS products_new"))
            except:
                pass
            
            # Create a new table without the stock column
            connection.execute(text("""
                CREATE TABLE products_new (
                    id INTEGER PRIMARY KEY,
                    name VARCHAR NOT NULL,
                    description VARCHAR,
                    price FLOAT NOT NULL,
                    category_id INTEGER,
                    barcode VARCHAR UNIQUE,
                    image_path VARCHAR
                )
            """))
            
            # Copy data from old table to new table (excluding stock column)
            connection.execute(text("""
                INSERT INTO products_new (id, name, description, price, category_id, barcode, image_path)
                SELECT id, name, description, price, category_id, barcode, image_path
                FROM products
            """))
            
            # Drop the old table (disable foreign key checks first)
            connection.execute(text("PRAGMA foreign_keys=OFF"))
            connection.execute(text("DROP TABLE products"))
            connection.execute(text("ALTER TABLE products_new RENAME TO products"))
            connection.execute(text("PRAGMA foreign_keys=ON"))
            
            # Commit the changes
            connection.commit()
            
            logger.info("Successfully removed stock column from products table")
        else:
            logger.info("Stock column does not exist in products table - no migration needed")
        
        connection.close()
        return True
        
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        return False

if __name__ == "__main__":
    print("Starting stock column removal migration...")
    if migrate_remove_stock():
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!")
        sys.exit(1) 