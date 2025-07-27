"""
Database configuration and session management.
"""
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import threading
import time

# Create the SQLAlchemy engine with better connection management for SQLite
engine = create_engine(
    'sqlite:///pos_database.db',
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=3600,   # Recycle connections after 1 hour
    pool_timeout=30,     # 30 second timeout for getting connection from pool
    max_overflow=10,     # Allow up to 10 connections beyond pool size
    connect_args={
        'timeout': 30,   # SQLite timeout for busy database
        'check_same_thread': False,  # Allow multi-threading
        'isolation_level': None  # Enable autocommit mode for better concurrency
    }
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

# Thread-local storage for sessions
_session_local = threading.local()

def get_session():
    """Get a thread-local database session."""
    if not hasattr(_session_local, 'session'):
        _session_local.session = Session()
    return _session_local.session

def close_session():
    """Close the current thread-local session."""
    if hasattr(_session_local, 'session'):
        _session_local.session.close()
        del _session_local.session

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configure SQLite for better concurrency."""
    if isinstance(dbapi_connection, sqlite3.Connection):
        # Enable WAL mode for better concurrency
        dbapi_connection.execute("PRAGMA journal_mode=WAL")
        # Set busy timeout
        dbapi_connection.execute("PRAGMA busy_timeout=30000")
        # Enable foreign keys
        dbapi_connection.execute("PRAGMA foreign_keys=ON")
        # Set synchronous mode to NORMAL for better performance
        dbapi_connection.execute("PRAGMA synchronous=NORMAL")
        # Set cache size
        dbapi_connection.execute("PRAGMA cache_size=10000")

def refresh_engine():
    """Refresh the database engine to reload metadata."""
    global engine, Session
    engine.dispose()
    engine = create_engine(
        'sqlite:///pos_database.db',
        pool_pre_ping=True,
        pool_recycle=3600,
        pool_timeout=30,
        max_overflow=10,
        connect_args={
            'timeout': 30,
            'check_same_thread': False,
            'isolation_level': None
        }
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

def safe_commit(session, max_retries=3, retry_delay=0.1):
    """
    Safely commit a session with retry logic for SQLite locks.
    
    Args:
        session: The database session to commit
        max_retries: Maximum number of retry attempts
        retry_delay: Delay between retries in seconds
        
    Returns:
        bool: True if commit successful, False otherwise
    """
    for attempt in range(max_retries):
        try:
            session.commit()
            return True
        except Exception as e:
            if "database is locked" in str(e).lower() and attempt < max_retries - 1:
                session.rollback()
                time.sleep(retry_delay * (attempt + 1))  # Exponential backoff
                continue
            else:
                session.rollback()
                raise e
    return False
