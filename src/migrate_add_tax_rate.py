"""
Migration script to add tax_rate column to categories table.
"""
import sqlite3
import os
from pathlib import Path

def migrate_add_tax_rate():
    """Add tax_rate column to categories table and set default value to 14.0."""
    
    # Get the database path
    db_path = Path(__file__).parent / "pos_database.db"
    
    if not db_path.exists():
        print(f"Database not found at {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tax_rate column already exists
        cursor.execute("PRAGMA table_info(categories)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'tax_rate' not in columns:
            print("Adding tax_rate column to categories table...")
            
            # Add the tax_rate column with default value 14.0
            cursor.execute("""
                ALTER TABLE categories 
                ADD COLUMN tax_rate REAL DEFAULT 14.0
            """)
            
            # Update existing categories to have 14% tax rate
            cursor.execute("""
                UPDATE categories 
                SET tax_rate = 14.0 
                WHERE tax_rate IS NULL OR tax_rate = 0.0
            """)
            
            conn.commit()
            print("Successfully added tax_rate column and set default tax rate to 14%")
        else:
            print("tax_rate column already exists in categories table")
        
        # Verify the migration
        cursor.execute("SELECT name, tax_rate FROM categories")
        categories = cursor.fetchall()
        print("\nCurrent categories and their tax rates:")
        for name, tax_rate in categories:
            print(f"  {name}: {tax_rate}%")
        
        conn.close()
        
    except Exception as e:
        print(f"Error during migration: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    migrate_add_tax_rate() 