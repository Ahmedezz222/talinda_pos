"""
Migration script to add price column to products table.
"""
from sqlalchemy import create_engine, text
from database.db_config import engine, Base

def migrate():
    """Add price column to products table."""
    
    # Add price column
    with engine.begin() as connection:
        try:
            print("Adding price column to products table...")
            connection.execute(text("ALTER TABLE products ADD COLUMN price FLOAT NOT NULL DEFAULT 0.0"))
            print("Price column added successfully!")
        except Exception as e:
            print(f"Error adding price column: {str(e)}")
            # If column already exists, this is fine
            pass

if __name__ == "__main__":
    migrate()
