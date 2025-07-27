"""
Database configuration and session management.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create the SQLAlchemy engine with better connection management
engine = create_engine(
    'sqlite:///pos_database.db',
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_timeout=30,     # 30 second timeout for getting connection from pool
    max_overflow=10      # Allow up to 10 connections beyond pool size
)

# Create a sessionmaker with better session management
Session = sessionmaker(
    bind=engine,
    expire_on_commit=False,  # Don't expire objects after commit
    autoflush=True,          # Auto-flush changes
    autocommit=False         # Don't auto-commit
)

# Create a base class for declarative models
Base = declarative_base()

def refresh_engine():
    """Refresh the database engine to reload metadata."""
    global engine, Session
    engine.dispose()
    engine = create_engine(
        'sqlite:///pos_database.db',
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_timeout=30,
        max_overflow=10
    )
    Session = sessionmaker(
        bind=engine,
        expire_on_commit=False,
        autoflush=True,
        autocommit=False
    )

def get_fresh_session():
    """Get a fresh database session with proper error handling."""
    try:
        return Session()
    except Exception:
        # If session creation fails, refresh engine and try again
        refresh_engine()
        return Session()
