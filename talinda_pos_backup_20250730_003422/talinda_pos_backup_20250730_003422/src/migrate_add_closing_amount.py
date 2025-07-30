#!/usr/bin/env python3
"""
Database migration to add closing_amount column to shifts table.
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

def migrate_add_closing_amount():
    """Add closing_amount column to shifts table."""
    session = Session()
    
    try:
        logger.info("Starting migration: Add closing_amount column to shifts table")
        
        # Check if the column already exists
        result = session.execute(text("""
            SELECT COUNT(*) FROM pragma_table_info('shifts') 
            WHERE name = 'closing_amount'
        """))
        
        column_exists = result.scalar() > 0
        
        if column_exists:
            logger.info("Column 'closing_amount' already exists in shifts table")
            return True
        
        # Add the closing_amount column
        session.execute(text("""
            ALTER TABLE shifts 
            ADD COLUMN closing_amount REAL
        """))
        
        session.commit()
        logger.info("Successfully added closing_amount column to shifts table")
        return True
        
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        session.rollback()
        return False
    finally:
        session.close()

if __name__ == "__main__":
    success = migrate_add_closing_amount()
    if success:
        print("✅ Migration completed successfully")
    else:
        print("❌ Migration failed")
        sys.exit(1) 