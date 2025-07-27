#!/usr/bin/env python3
"""
Test script to verify category add logic is working correctly.
"""
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from controllers.product_controller import ProductController
from models.product import Category

def test_category_add():
    """Test the category add functionality."""
    controller = ProductController()
    
    print("Testing category add logic...")
    
    # Test 1: Add a new category
    try:
        new_category = controller.add_category("Test Category")
        print(f"✓ Successfully added category: {new_category.name}")
    except Exception as e:
        print(f"✗ Failed to add category: {e}")
        return False
    
    # Test 2: Try to add the same category again (should fail)
    try:
        controller.add_category("Test Category")
        print("✗ Should have failed to add duplicate category")
        return False
    except ValueError as e:
        print(f"✓ Correctly prevented duplicate category: {e}")
    
    # Test 3: Get all categories
    try:
        categories = controller.get_categories()
        print(f"✓ Retrieved {len(categories)} categories")
        for cat in categories:
            print(f"  - {cat.name} (active: {cat.is_active})")
    except Exception as e:
        print(f"✗ Failed to get categories: {e}")
        return False
    
    # Test 4: Add another category
    try:
        another_category = controller.add_category("Another Test Category")
        print(f"✓ Successfully added another category: {another_category.name}")
    except Exception as e:
        print(f"✗ Failed to add another category: {e}")
        return False
    
    print("\nAll tests passed! Category add logic is working correctly.")
    return True

if __name__ == "__main__":
    test_category_add()