#!/usr/bin/env python3
"""
Test script to check categories in the database
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
current_dir = Path(__file__).parent
src_dir = current_dir / "src"
sys.path.insert(0, str(src_dir))

from controllers.product_controller import ProductController
from database.db_config import get_fresh_session
from models.product import Category

def test_categories():
    """Test what categories exist in the database."""
    print("Testing categories in database...")
    
    # Create a fresh session
    session = get_fresh_session()
    
    try:
        # Get all categories
        categories = session.query(Category).all()
        print(f"Found {len(categories)} categories:")
        
        for cat in categories:
            print(f"  - ID: {cat.id}, Name: '{cat.name}', Description: '{cat.description}'")
        
        if len(categories) == 0:
            print("No categories found! Seeding default categories...")
            controller = ProductController()
            if controller.seed_default_categories():
                print("Default categories seeded successfully!")
                # Get categories again
                categories = session.query(Category).all()
                print(f"Now found {len(categories)} categories:")
                for cat in categories:
                    print(f"  - ID: {cat.id}, Name: '{cat.name}', Description: '{cat.description}'")
            else:
                print("Failed to seed default categories!")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    test_categories() 