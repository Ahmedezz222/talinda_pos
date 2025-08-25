#!/usr/bin/env python3
"""
Database initialization script for Talinda POS system.
"""
from database.db_config import engine, Base
from models.product import Category, Product
from models.user import User
from models.sale import Sale

def init_database():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_database()