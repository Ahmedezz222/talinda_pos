#!/usr/bin/env python3
"""
Responsive UI Utilities for Talinda POS
=======================================

Dynamic sizing and responsive design utilities for PyQt5.
"""

import math
from typing import Tuple, Optional
from PyQt5.QtWidgets import QApplication, QWidget, QScreen
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QFont


class ResponsiveUI:
    """Responsive UI utilities for dynamic sizing."""
    
    # Base sizes for 96 DPI (standard)
    BASE_FONT_SIZE = 12
    BASE_BUTTON_HEIGHT = 40
    BASE_CARD_WIDTH = 150
    BASE_CARD_HEIGHT = 120
    BASE_WINDOW_WIDTH = 1200
    BASE_WINDOW_HEIGHT = 800
    
    @staticmethod
    def get_screen_info() -> Tuple[int, int, float]:
        """Get screen width, height, and DPI scaling factor."""
        app = QApplication.instance()
        if not app:
            return 1920, 1080, 1.0
        
        screen = app.primaryScreen()
        if not screen:
            return 1920, 1080, 1.0
        
        size = screen.size()
        dpi = screen.logicalDotsPerInch()
        scaling_factor = dpi / 96.0  # 96 DPI is standard
        
        return size.width(), size.height(), scaling_factor
    
    @staticmethod
    def get_scaled_size(base_size: int) -> int:
        """Get scaled size based on screen DPI."""
        _, _, scaling_factor = ResponsiveUI.get_screen_info()
        return int(base_size * scaling_factor)
    
    @staticmethod
    def get_responsive_font_size(base_size: int = None) -> int:
        """Get responsive font size."""
        if base_size is None:
            base_size = ResponsiveUI.BASE_FONT_SIZE
        return ResponsiveUI.get_scaled_size(base_size)
    
    @staticmethod
    def get_responsive_button_size() -> QSize:
        """Get responsive button size."""
        width = ResponsiveUI.get_scaled_size(120)
        height = ResponsiveUI.get_scaled_size(ResponsiveUI.BASE_BUTTON_HEIGHT)
        return QSize(width, height)
    
    @staticmethod
    def get_responsive_card_size() -> QSize:
        """Get responsive card size."""
        width = ResponsiveUI.get_scaled_size(ResponsiveUI.BASE_CARD_WIDTH)
        height = ResponsiveUI.get_scaled_size(ResponsiveUI.BASE_CARD_HEIGHT)
        return QSize(width, height)
    
    @staticmethod
    def get_responsive_window_size() -> QSize:
        """Get responsive window size."""
        screen_width, screen_height, _ = ResponsiveUI.get_screen_info()
        
        # Calculate window size as percentage of screen size
        window_width = int(screen_width * 0.8)  # 80% of screen width
        window_height = int(screen_height * 0.8)  # 80% of screen height
        
        # Ensure minimum size
        min_width = ResponsiveUI.get_scaled_size(800)
        min_height = ResponsiveUI.get_scaled_size(600)
        
        return QSize(max(window_width, min_width), max(window_height, min_height))
    
    @staticmethod
    def calculate_grid_columns(container_width: int, card_width: int, 
                             min_cols: int = 3, max_cols: int = 8) -> int:
        """Calculate optimal number of columns for grid layout."""
        if card_width <= 0:
            return min_cols
        
        cols = max(min_cols, min(max_cols, int(container_width / card_width)))
        return cols
    
    @staticmethod
    def get_optimal_card_size(container_width: int, container_height: int,
                            num_items: int, aspect_ratio: float = 1.25) -> QSize:
        """Calculate optimal card size for given container and number of items."""
        if num_items <= 0:
            return ResponsiveUI.get_responsive_card_size()
        
        # Calculate grid dimensions
        cols = math.ceil(math.sqrt(num_items * aspect_ratio))
        rows = math.ceil(num_items / cols)
        
        # Calculate card size
        card_width = max(100, (container_width - (cols + 1) * 10) // cols)
        card_height = int(card_width / aspect_ratio)
        
        # Ensure cards fit in container height
        max_height = (container_height - (rows + 1) * 10) // rows
        if card_height > max_height:
            card_height = max_height
            card_width = int(card_height * aspect_ratio)
        
        return QSize(card_width, card_height)
    
    @staticmethod
    def apply_responsive_font(widget: QWidget, base_size: int = None):
        """Apply responsive font to widget."""
        font_size = ResponsiveUI.get_responsive_font_size(base_size)
        font = widget.font()
        font.setPointSize(font_size)
        widget.setFont(font)
    
    @staticmethod
    def apply_responsive_stylesheet(widget: QWidget, base_stylesheet: str) -> str:
        """Apply responsive sizing to stylesheet."""
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        # Replace size values in stylesheet
        responsive_stylesheet = base_stylesheet
        
        # Common size replacements
        size_replacements = {
            '12px': f'{int(12 * scaling_factor)}px',
            '14px': f'{int(14 * scaling_factor)}px',
            '16px': f'{int(16 * scaling_factor)}px',
            '18px': f'{int(18 * scaling_factor)}px',
            '20px': f'{int(20 * scaling_factor)}px',
            '24px': f'{int(24 * scaling_factor)}px',
            '32px': f'{int(32 * scaling_factor)}px',
            '40px': f'{int(40 * scaling_factor)}px',
            '8px': f'{int(8 * scaling_factor)}px',
            '10px': f'{int(10 * scaling_factor)}px',
        }
        
        for old_size, new_size in size_replacements.items():
            responsive_stylesheet = responsive_stylesheet.replace(old_size, new_size)
        
        return responsive_stylesheet


class ResponsiveLayout:
    """Responsive layout utilities."""
    
    @staticmethod
    def get_margin_for_screen() -> int:
        """Get appropriate margin size for current screen."""
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        return int(10 * scaling_factor)
    
    @staticmethod
    def get_spacing_for_screen() -> int:
        """Get appropriate spacing size for current screen."""
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        return int(5 * scaling_factor)
    
    @staticmethod
    def get_padding_for_screen() -> int:
        """Get appropriate padding size for current screen."""
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        return int(15 * scaling_factor)


class ResponsiveBreakpoints:
    """Responsive breakpoints for different screen sizes."""
    
    # Breakpoints in pixels
    MOBILE = 768
    TABLET = 1024
    DESKTOP = 1200
    LARGE_DESKTOP = 1600
    
    @staticmethod
    def get_screen_size_category() -> str:
        """Get current screen size category."""
        screen_width, _, _ = ResponsiveUI.get_screen_info()
        
        if screen_width < ResponsiveBreakpoints.MOBILE:
            return 'mobile'
        elif screen_width < ResponsiveBreakpoints.TABLET:
            return 'tablet'
        elif screen_width < ResponsiveBreakpoints.DESKTOP:
            return 'desktop'
        elif screen_width < ResponsiveBreakpoints.LARGE_DESKTOP:
            return 'large_desktop'
        else:
            return 'extra_large'
    
    @staticmethod
    def get_columns_for_screen() -> int:
        """Get optimal number of columns for current screen size."""
        category = ResponsiveBreakpoints.get_screen_size_category()
        
        column_map = {
            'mobile': 2,
            'tablet': 3,
            'desktop': 4,
            'large_desktop': 5,
            'extra_large': 6
        }
        
        return column_map.get(category, 4)
    
    @staticmethod
    def get_card_size_for_screen() -> QSize:
        """Get optimal card size for current screen size."""
        category = ResponsiveBreakpoints.get_screen_size_category()
        
        size_map = {
            'mobile': QSize(120, 100),
            'tablet': QSize(140, 110),
            'desktop': QSize(160, 120),
            'large_desktop': QSize(180, 130),
            'extra_large': QSize(200, 140)
        }
        
        base_size = size_map.get(category, QSize(160, 120))
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        return QSize(
            int(base_size.width() * scaling_factor),
            int(base_size.height() * scaling_factor)
        )


# Convenience functions
def get_responsive_size(base_size: int) -> int:
    """Get responsive size for given base size."""
    return ResponsiveUI.get_scaled_size(base_size)


def get_responsive_font(base_size: int = 12) -> QFont:
    """Get responsive font."""
    font = QFont()
    font.setPointSize(ResponsiveUI.get_responsive_font_size(base_size))
    return font


def apply_responsive_style(widget: QWidget, base_style: str) -> None:
    """Apply responsive style to widget."""
    responsive_style = ResponsiveUI.apply_responsive_stylesheet(widget, base_style)
    widget.setStyleSheet(responsive_style) 