#!/usr/bin/env python3
"""
Configuration Management for Talinda POS
========================================

Centralized configuration management using environment variables.
"""

import os
import logging
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, continue without it
    pass


class Config:
    """Application configuration class."""
    
    # Application settings
    APP_NAME = os.getenv('APP_NAME', 'Talinda POS')
    APP_VERSION = os.getenv('APP_VERSION', '2.0.0')
    APP_AUTHOR = os.getenv('APP_AUTHOR', 'Talinda POS Team')
    
    # Database settings
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///pos_database.db')
    DATABASE_ECHO = os.getenv('DATABASE_ECHO', 'false').lower() == 'true'
    
    # Logging settings
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/talinda_pos.log')
    LOG_FORMAT = os.getenv('LOG_FORMAT', 
                          '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # UI settings
    WINDOW_WIDTH = int(os.getenv('WINDOW_WIDTH', '1200'))
    WINDOW_HEIGHT = int(os.getenv('WINDOW_HEIGHT', '800'))
    THEME = os.getenv('THEME', 'default')
    
    # Security settings
    SESSION_TIMEOUT = int(os.getenv('SESSION_TIMEOUT', '3600'))  # 1 hour
    MAX_LOGIN_ATTEMPTS = int(os.getenv('MAX_LOGIN_ATTEMPTS', '3'))
    PASSWORD_MIN_LENGTH = int(os.getenv('PASSWORD_MIN_LENGTH', '8'))
    
    # Shift management settings
    AUTO_CLOSE_SHIFTS_AT_MIDNIGHT = os.getenv('AUTO_CLOSE_SHIFTS_AT_MIDNIGHT', 'true').lower() == 'true'
    SHIFT_CLOSE_NOTIFICATION_ENABLED = os.getenv('SHIFT_CLOSE_NOTIFICATION_ENABLED', 'true').lower() == 'true'
    SHIFT_AUTO_CLOSE_TIME = os.getenv('SHIFT_AUTO_CLOSE_TIME', '00:00')  # HH:MM format
    
    # File paths
    CSS_FILE = os.getenv('CSS_FILE', 'resources/styles/main.qss')
    LOGO_FILE = os.getenv('LOGO_FILE', 'resources/images/logo.png')
    
    # Colors
    PRIMARY_COLOR = os.getenv('PRIMARY_COLOR', '#1976d2')
    SECONDARY_COLOR = os.getenv('SECONDARY_COLOR', '#424242')
    SUCCESS_COLOR = os.getenv('SUCCESS_COLOR', '#4caf50')
    ERROR_COLOR = os.getenv('ERROR_COLOR', '#f44336')
    WARNING_COLOR = os.getenv('WARNING_COLOR', '#ff9800')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings."""
        try:
            # Validate numeric settings
            assert cls.WINDOW_WIDTH > 0, "Window width must be positive"
            assert cls.WINDOW_HEIGHT > 0, "Window height must be positive"
            assert cls.SESSION_TIMEOUT > 0, "Session timeout must be positive"
            assert cls.MAX_LOGIN_ATTEMPTS > 0, "Max login attempts must be positive"
            assert cls.PASSWORD_MIN_LENGTH >= 6, "Password min length must be at least 6"
            
            # Validate file paths exist
            css_path = Path(cls.CSS_FILE)
            if not css_path.exists():
                logging.warning(f"CSS file not found: {css_path}")
            
            return True
            
        except AssertionError as e:
            logging.error(f"Configuration validation failed: {e}")
            return False
    
    @classmethod
    def get_database_url(cls) -> str:
        """Get database URL with proper formatting."""
        if cls.DATABASE_URL.startswith('sqlite:///'):
            # Ensure SQLite database is in the correct location
            db_path = cls.DATABASE_URL.replace('sqlite:///', '')
            if not db_path.startswith('/'):
                # Relative path, make it absolute
                db_path = str(Path.cwd() / db_path)
            return f"sqlite:///{db_path}"
        return cls.DATABASE_URL
    
    @classmethod
    def get_log_level(cls) -> int:
        """Get logging level from string."""
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        return level_map.get(cls.LOG_LEVEL.upper(), logging.INFO)


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    
    DATABASE_ECHO = True
    LOG_LEVEL = 'DEBUG'
    WINDOW_WIDTH = 1400
    WINDOW_HEIGHT = 900


class ProductionConfig(Config):
    """Production-specific configuration."""
    
    DATABASE_ECHO = False
    LOG_LEVEL = 'WARNING'
    SESSION_TIMEOUT = 1800  # 30 minutes
    MAX_LOGIN_ATTEMPTS = 5


class TestingConfig(Config):
    """Testing-specific configuration."""
    
    DATABASE_URL = 'sqlite:///:memory:'
    DATABASE_ECHO = False
    LOG_LEVEL = 'ERROR'


def get_config(environment: Optional[str] = None) -> Config:
    """Get configuration based on environment."""
    if environment is None:
        environment = os.getenv('ENVIRONMENT', 'development')
    
    config_map = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig
    }
    
    return config_map.get(environment.lower(), DevelopmentConfig)


# Global configuration instance
config = get_config() 