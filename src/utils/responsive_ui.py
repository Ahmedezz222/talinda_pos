#!/usr/bin/env python3
"""
Responsive UI Utilities for Talinda POS
=======================================

Dynamic sizing and responsive design utilities for PyQt5.
Enhanced for better support across all screen resolutions.
"""

import math
from typing import Tuple, Optional
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt, QSize, QRect
from PyQt5.QtGui import QFont, QScreen


class ResponsiveUI:
    """Responsive UI utilities for dynamic sizing."""
    
    # Base sizes for 96 DPI (standard)
    BASE_FONT_SIZE = 12
    BASE_BUTTON_HEIGHT = 40
    BASE_CARD_WIDTH = 150
    BASE_CARD_HEIGHT = 120
    BASE_WINDOW_WIDTH = 1200
    BASE_WINDOW_HEIGHT = 800
    
    # Enhanced breakpoints for better resolution support
    BREAKPOINTS = {
        'mobile': 768,
        'tablet': 1024,
        'desktop': 1366,
        'large_desktop': 1920,
        'ultra_wide': 2560
    }
    
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
    def get_screen_category() -> str:
        """Get the current screen size category."""
        screen_width, _, _ = ResponsiveUI.get_screen_info()
        
        if screen_width < ResponsiveUI.BREAKPOINTS['mobile']:
            return 'mobile'
        elif screen_width < ResponsiveUI.BREAKPOINTS['tablet']:
            return 'tablet'
        elif screen_width < ResponsiveUI.BREAKPOINTS['desktop']:
            return 'desktop'
        elif screen_width < ResponsiveUI.BREAKPOINTS['large_desktop']:
            return 'large_desktop'
        elif screen_width < ResponsiveUI.BREAKPOINTS['ultra_wide']:
            return 'ultra_wide'
        else:
            return 'extra_large'
    
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
        
        screen_category = ResponsiveUI.get_screen_category()
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        # Adjust font size based on screen category
        category_multipliers = {
            'mobile': 0.9,
            'tablet': 1.0,
            'desktop': 1.1,
            'large_desktop': 1.2,
            'ultra_wide': 1.3,
            'extra_large': 1.4
        }
        
        multiplier = category_multipliers.get(screen_category, 1.0)
        return int(base_size * scaling_factor * multiplier)
    
    @staticmethod
    def get_responsive_button_size() -> QSize:
        """Get responsive button size."""
        screen_category = ResponsiveUI.get_screen_category()
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        # Button sizes for different screen categories
        button_sizes = {
            'mobile': (100, 35),
            'tablet': (110, 38),
            'desktop': (120, 40),
            'large_desktop': (130, 42),
            'ultra_wide': (140, 45),
            'extra_large': (150, 48)
        }
        
        width, height = button_sizes.get(screen_category, (120, 40))
        return QSize(int(width * scaling_factor), int(height * scaling_factor))
    
    @staticmethod
    def get_responsive_card_size() -> QSize:
        """Get responsive card size."""
        screen_category = ResponsiveUI.get_screen_category()
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        # Card sizes for different screen categories
        card_sizes = {
            'mobile': (140, 160),
            'tablet': (150, 170),
            'desktop': (160, 180),
            'large_desktop': (170, 190),
            'ultra_wide': (180, 200),
            'extra_large': (190, 210)
        }
        
        width, height = card_sizes.get(screen_category, (180, 130))
        return QSize(int(width * scaling_factor), int(height * scaling_factor))
    
    @staticmethod
    def get_responsive_window_size() -> QSize:
        """Get responsive window size."""
        screen_width, screen_height, scaling_factor = ResponsiveUI.get_screen_info()
        screen_category = ResponsiveUI.get_screen_category()
        
        # Window size percentages for different screen categories
        size_percentages = {
            'mobile': (0.95, 0.95),      # Almost full screen
            'tablet': (0.9, 0.9),        # 90% of screen
            'desktop': (0.85, 0.85),     # 85% of screen
            'large_desktop': (0.8, 0.8), # 80% of screen
            'ultra_wide': (0.75, 0.75),  # 75% of screen
            'extra_large': (0.7, 0.7)    # 70% of screen
        }
        
        width_pct, height_pct = size_percentages.get(screen_category, (0.8, 0.8))
        
        # Calculate window size as percentage of screen size
        window_width = int(screen_width * width_pct)
        window_height = int(screen_height * height_pct)
        
        # Ensure minimum size
        min_width = ResponsiveUI.get_scaled_size(800)
        min_height = ResponsiveUI.get_scaled_size(600)
        
        return QSize(max(window_width, min_width), max(window_height, min_height))
    
    @staticmethod
    def get_responsive_sidebar_width() -> int:
        """Get responsive sidebar width."""
        screen_category = ResponsiveUI.get_screen_category()
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        # Sidebar widths for different screen categories
        sidebar_widths = {
            'mobile': 180,
            'tablet': 200,
            'desktop': 220,
            'large_desktop': 250,
            'ultra_wide': 280,
            'extra_large': 300
        }
        
        width = sidebar_widths.get(screen_category, 220)
        return int(width * scaling_factor)
    
    @staticmethod
    def get_responsive_dialog_size(dialog_type: str = 'standard') -> QSize:
        """Get responsive dialog size."""
        screen_category = ResponsiveUI.get_screen_category()
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        
        # Dialog sizes for different types and screen categories
        dialog_sizes = {
            'login': {
                'mobile': (320, 420),
                'tablet': (350, 450),
                'desktop': (380, 480),
                'large_desktop': (400, 500),
                'ultra_wide': (420, 520),
                'extra_large': (450, 550)
            },
            'standard': {
                'mobile': (280, 200),
                'tablet': (300, 220),
                'desktop': (320, 240),
                'large_desktop': (350, 260),
                'ultra_wide': (380, 280),
                'extra_large': (400, 300)
            },
            'large': {
                'mobile': (400, 300),
                'tablet': (450, 350),
                'desktop': (500, 400),
                'large_desktop': (550, 450),
                'ultra_wide': (600, 500),
                'extra_large': (650, 550)
            }
        }
        
        sizes = dialog_sizes.get(dialog_type, dialog_sizes['standard'])
        width, height = sizes.get(screen_category, (320, 240))
        return QSize(int(width * scaling_factor), int(height * scaling_factor))
    
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
        screen_category = ResponsiveUI.get_screen_category()
        
        # Replace size values in stylesheet
        responsive_stylesheet = base_stylesheet
        
        # Common size replacements with category-specific adjustments
        category_multipliers = {
            'mobile': 0.9,
            'tablet': 1.0,
            'desktop': 1.1,
            'large_desktop': 1.2,
            'ultra_wide': 1.3,
            'extra_large': 1.4
        }
        
        multiplier = category_multipliers.get(screen_category, 1.0)
        
        # Common size replacements
        size_replacements = {
            '8px': f'{int(8 * scaling_factor * multiplier)}px',
            '10px': f'{int(10 * scaling_factor * multiplier)}px',
            '12px': f'{int(12 * scaling_factor * multiplier)}px',
            '14px': f'{int(14 * scaling_factor * multiplier)}px',
            '16px': f'{int(16 * scaling_factor * multiplier)}px',
            '18px': f'{int(18 * scaling_factor * multiplier)}px',
            '20px': f'{int(20 * scaling_factor * multiplier)}px',
            '24px': f'{int(24 * scaling_factor * multiplier)}px',
            '32px': f'{int(32 * scaling_factor * multiplier)}px',
            '40px': f'{int(40 * scaling_factor * multiplier)}px',
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
        screen_category = ResponsiveUI.get_screen_category()
        
        # Margin sizes for different screen categories
        margins = {
            'mobile': 8,
            'tablet': 10,
            'desktop': 12,
            'large_desktop': 15,
            'ultra_wide': 18,
            'extra_large': 20
        }
        
        base_margin = margins.get(screen_category, 10)
        return int(base_margin * scaling_factor)
    
    @staticmethod
    def get_spacing_for_screen() -> int:
        """Get appropriate spacing size for current screen."""
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        screen_category = ResponsiveUI.get_screen_category()
        
        # Spacing sizes for different screen categories
        spacings = {
            'mobile': 4,
            'tablet': 5,
            'desktop': 6,
            'large_desktop': 8,
            'ultra_wide': 10,
            'extra_large': 12
        }
        
        base_spacing = spacings.get(screen_category, 5)
        return int(base_spacing * scaling_factor)
    
    @staticmethod
    def get_padding_for_screen() -> int:
        """Get appropriate padding size for current screen."""
        scaling_factor = ResponsiveUI.get_screen_info()[2]
        screen_category = ResponsiveUI.get_screen_category()
        
        # Padding sizes for different screen categories
        paddings = {
            'mobile': 12,
            'tablet': 15,
            'desktop': 18,
            'large_desktop': 20,
            'ultra_wide': 25,
            'extra_large': 30
        }
        
        base_padding = paddings.get(screen_category, 15)
        return int(base_padding * scaling_factor)


class ResponsiveBreakpoints:
    """Responsive breakpoints for different screen sizes."""
    
    # Breakpoints in pixels
    MOBILE = 768
    TABLET = 1024
    DESKTOP = 1366
    LARGE_DESKTOP = 1920
    ULTRA_WIDE = 2560
    
    @staticmethod
    def get_screen_size_category() -> str:
        """Get current screen size category."""
        return ResponsiveUI.get_screen_category()
    
    @staticmethod
    def get_columns_for_screen() -> int:
        """Get optimal number of columns for current screen size."""
        category = ResponsiveBreakpoints.get_screen_size_category()
        
        column_map = {
            'mobile': 2,
            'tablet': 3,
            'desktop': 4,
            'large_desktop': 5,
            'ultra_wide': 6,
            'extra_large': 7
        }
        
        return column_map.get(category, 4)
    
    @staticmethod
    def get_card_size_for_screen() -> QSize:
        """Get optimal card size for current screen size."""
        return ResponsiveUI.get_responsive_card_size()


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


def get_window_size_for_screen() -> QSize:
    """Get optimal window size for current screen."""
    return ResponsiveUI.get_responsive_window_size()


def get_dialog_size_for_screen(dialog_type: str = 'standard') -> QSize:
    """Get optimal dialog size for current screen."""
    return ResponsiveUI.get_responsive_dialog_size(dialog_type)


def get_sidebar_width_for_screen() -> int:
    """Get optimal sidebar width for current screen."""
    return ResponsiveUI.get_responsive_sidebar_width() 