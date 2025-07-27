"""
Fix database by adding tax_rate column to categories table.
"""
import sqlite3
import os

def fix_database():
    """Add tax_rate column to categories table."""
    
    db_path = "pos_database.db"
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if tax_rate column exists
        cursor.execute("PRAGMA table_info(categories)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'tax_rate' not in columns:
            print("Adding tax_rate column to categories table...")
            
            # Add the tax_rate column
            cursor.execute("""
                ALTER TABLE categories 
                ADD COLUMN tax_rate REAL DEFAULT 14.0
            """)
            
            conn.commit()
            print("Successfully added tax_rate column")
        else:
            print("tax_rate column already exists")
        
        # Create some categories with 14% tax rate
        cursor.execute("SELECT COUNT(*) FROM categories")
        count = cursor.fetchone()[0]
        
        if count == 0:
            print("Creating initial categories with 14% tax rate...")
            categories = [
                ("Food", "Food category", 14.0),
                ("Beverage", "Beverage category", 14.0),
                ("Dessert", "Dessert category", 14.0),
                ("Other", "Other category", 14.0)
            ]
            
            cursor.executemany("""
                INSERT INTO categories (name, description, tax_rate) 
                VALUES (?, ?, ?)
            """, categories)
            
            conn.commit()
            print("Categories created successfully!")
        
        # Verify the data
        cursor.execute("SELECT name, tax_rate FROM categories")
        categories = cursor.fetchall()
        print("\nCurrent categories and their tax rates:")
        for name, tax_rate in categories:
            print(f"  {name}: {tax_rate}%")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == "__main__":
    fix_database() 