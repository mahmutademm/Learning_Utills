"""
Configuration constants for the Wall Street 101 application.
"""

# Market cap classifications
MARKET_CAP_THRESHOLDS = {
    'large_cap': 10_000_000_000,  # >$10B
    'mid_cap': 2_000_000_000,     # $2B-$10B
    'small_cap': 300_000_000,     # $300M-$2B (micro cap < $300M)
}

# Technical analysis constants
RSI_OVERBOUGHT = 70
RSI_OVERSOLD = 30
BEAR_MARKET_THRESHOLD = 0.20  # 20% decline
BULL_MARKET_THRESHOLD = 0.20  # 20% rise

# Chart display constants
CHART_HEIGHT_SIMPLE = 400
CHART_HEIGHT_ANALYTICAL = 500
MOVING_AVERAGE_PERIODS = {
    'short': 50,
    'long': 200
}

# Cache timeouts (in seconds)
CACHE_TIMEOUT_SHORT = 600   # 10 minutes for stock data
CACHE_TIMEOUT_LONG = 3600   # 1 hour for full history

# UI Constants
COLS_PER_ROW_SHIELDS = 3
MAX_NEWS_ITEMS = 5
DEFAULT_CHART_PERIOD = "3y"

# Badge system constants
BADGES_CONFIG = {
    'charts_viewed_threshold': 10,
    'facts_read_threshold': 5,
    'analyzer_uses_threshold': 5,
    'what_if_uses_threshold': 5
}

# Color scheme
COLORS = {
    'primary': '#00A693',
    'secondary': '#262730',
    'success': '#28a745',
    'warning': '#ffc107',
    'danger': '#dc3545',
    'info': '#17a2b8',
    'light': '#FAFAFA',
    'dark': '#0E1117',
    'sidebar': '#1A1C23'
}

# Default values
DEFAULT_VALUES = {
    'what_if_symbol': 'NVDA',
    'what_if_amount': 1000,
    'analyzer_symbol': 'AAPL'
}