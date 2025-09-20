"""
Performance optimization utilities for the Wall Street 101 application.
Includes lazy loading, improved caching, and memory management.
"""

import streamlit as st
import functools
from typing import Callable, Any
import gc
import time


def lazy_import(module_name: str):
    """Lazy import decorator to defer module loading until needed."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if module_name not in globals():
                globals()[module_name] = __import__(module_name)
            return func(*args, **kwargs)
        return wrapper
    return decorator


def memory_efficient_cache(ttl: int = 600, max_entries: int = 10):
    """
    Memory-efficient caching decorator with LRU eviction.
    Automatically cleans up old entries to prevent memory bloat.
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        access_times = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            # Check if cached result exists and is still valid
            if key in cache:
                cached_time, result = cache[key]
                if current_time - cached_time < ttl:
                    access_times[key] = current_time
                    return result
                else:
                    # Remove expired entry
                    del cache[key]
                    del access_times[key]
            
            # Evict oldest entries if cache is full
            if len(cache) >= max_entries:
                oldest_key = min(access_times.keys(), key=access_times.get)
                del cache[oldest_key]
                del access_times[oldest_key]
                # Trigger garbage collection
                gc.collect()
            
            # Compute and cache result
            result = func(*args, **kwargs)
            cache[key] = (current_time, result)
            access_times[key] = current_time
            
            return result
        
        wrapper.cache_info = lambda: {
            'hits': len(cache),
            'max_size': max_entries,
            'ttl': ttl
        }
        wrapper.cache_clear = lambda: (cache.clear(), access_times.clear())
        
        return wrapper
    return decorator


class ComponentLoader:
    """Lazy component loader to improve initial app load time."""
    
    _loaded_components = set()
    
    @classmethod
    def load_component(cls, component_name: str, loader_func: Callable):
        """Load a component only once and cache the result."""
        if component_name not in cls._loaded_components:
            with st.spinner(f"Loading {component_name}..."):
                result = loader_func()
                cls._loaded_components.add(component_name)
                return result
        return None
    
    @classmethod
    def reset(cls):
        """Reset loaded components (useful for development)."""
        cls._loaded_components.clear()


def optimize_dataframe(df):
    """Optimize pandas DataFrame memory usage."""
    if df.empty:
        return df
    
    # Optimize numeric columns
    for col in df.select_dtypes(include=['float64']).columns:
        df[col] = df[col].astype('float32')
    
    for col in df.select_dtypes(include=['int64']).columns:
        if df[col].min() >= 0:
            if df[col].max() < 255:
                df[col] = df[col].astype('uint8')
            elif df[col].max() < 65535:
                df[col] = df[col].astype('uint16')
            else:
                df[col] = df[col].astype('uint32')
        else:
            if df[col].min() > -128 and df[col].max() < 127:
                df[col] = df[col].astype('int8')
            elif df[col].min() > -32768 and df[col].max() < 32767:
                df[col] = df[col].astype('int16')
            else:
                df[col] = df[col].astype('int32')
    
    return df


def batch_process(items, batch_size: int = 100):
    """Process items in batches to avoid memory issues with large datasets."""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


class PerformanceMonitor:
    """Simple performance monitoring for development."""
    
    def __init__(self, name: str):
        self.name = name
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        duration = end_time - self.start_time
        if st.session_state.get('debug_mode', False):
            st.sidebar.text(f"{self.name}: {duration:.3f}s")


# Streamlit-specific optimizations
def optimize_streamlit_config():
    """Apply Streamlit-specific optimizations."""
    # These would be set in streamlit config.toml, but we can track them here
    optimizations = {
        'dataFrameSerialization': 'arrow',  # Faster DataFrame serialization
        'allowRunOnSave': False,  # Prevent auto-rerun on file save
        'showErrorDetails': False,  # Hide detailed errors in production
        'fastReruns': True,  # Enable fast reruns
        'allowDuplicateWidgetID': False  # Catch widget ID conflicts early
    }
    return optimizations


# Precomputed constants to avoid recalculation
PRECOMPUTED_VALUES = {
    'common_date_ranges': {
        '1d': 1,
        '5d': 5,
        '1mo': 30,
        '3mo': 90,
        '6mo': 180,
        '1y': 365,
        '2y': 730,
        '5y': 1825
    },
    'percentage_thresholds': {
        'bull_market': 0.20,
        'bear_market': -0.20,
        'correction': -0.10,
        'rally': 0.10
    }
}