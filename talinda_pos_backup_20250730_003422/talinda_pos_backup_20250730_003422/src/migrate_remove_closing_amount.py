#!/usr/bin/env python3
"""
Database migration to remove closing_amount column from shifts table.
"""
import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent.absolute()
sys.path.insert(0, str(current_dir))

from database.db_config import Session, engine
from sqlalchemy import text
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_remove_closing_amount():
    """Remove closing_amount column from shifts table."""
    session = Session()
    
    try:
        logger.info("Starting migration: Remove closing_amount column from shifts table")
        
        # Check if the column exists
        result = session.execute(text("""
            SELECT COUNT(*) FROM pragma_table_info('shifts') 
            WHERE name = 'closing_amount'
        """))
        
        column_exists = result.scalar() > 0
        
        if not column_exists:
            logger.info("Column 'closing_amount' does not exist in shifts table")
            return True
        
        # Remove the closing_amount column
        # Note: SQLite doesn't support DROP COLUMN directly, so we need to recreate the table
        logger.info("Removing closing_amount column...")
        
        # Create new table without closing_amount column
        session.execute(text("""
            CREATE TABLE shifts_new (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                open_time DATETIME NOT NULL,
                close_time DATETIME,
                opening_amount REAL NOT NULL,
                status VARCHAR(10) NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """))
        
        # Copy data from old table to new table
        session.execute(text("""
            INSERT INTO shifts_new (id, user_id, open_time, close_time, opening_amount, status)
            SELECT id, user_id, open_time, close_time, opening_amount, status
            FROM shifts
        """))
        
        # Drop old table
        session.execute(text("DROP TABLE shifts"))
        
        # Rename new table to original name
        session.execute(text("ALTER TABLE shifts_new RENAME TO shifts"))
        
        session.commit()
        logger.info("Successfully removed closing_amount column from shifts table")
        return True
        
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = migrate_remove_closing_amount()
    if success:
        print("✅ Migration completed successfully")
    else:
        print("❌ Migration failed")
        sys.exit(1) 