"""
Wall Street 101: The Ultimate Trading Hub
A comprehensive, interactive financial education platform built with Streamlit.

This is the main application file that coordinates all components.
"""

import streamlit as st
import sys
import os

# Add the current directory to the Python path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Import configuration and utilities
from config.constants import DEFAULT_VALUES
from styles.css import get_custom_css
from utils.helpers import init_session_state
from utils.performance import ComponentLoader, PerformanceMonitor

# Import page modules (lazy loading will be applied)
from pages.home_page import page_home
from pages.learning_page import page_learning_modules
from pages.analyzer_page import page_stock_analyzer
from pages.whatif_page import page_what_if_calculator
from pages.misc_pages import page_funds_explorer, page_achievements


def configure_app():
    """Configure the Streamlit app settings and styling."""
    st.set_page_config(
        page_title="Wall Street 101: The Ultimate Trading Hub",
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Apply custom CSS
    st.markdown(get_custom_css(), unsafe_allow_html=True)


def setup_navigation():
    """Setup the sidebar navigation system."""
    st.sidebar.title("Wall Street 101")
    st.sidebar.markdown("---")

    # Page definitions
    pages = {
        "🏠 Home": page_home,
        "📚 Learning Modules": page_learning_modules,
        "🕵️ Stock Analyzer": page_stock_analyzer,
        "💸 'What If' Calculator": page_what_if_calculator,
        "🧭 Funds Explorer": page_funds_explorer,
        "🏅 Achievements": page_achievements
    }

    # Custom navigation menu
    for page_name in pages.keys():
        # For the currently selected page, display styled text
        if st.session_state.page == page_name:
            st.sidebar.markdown(f'<p class="nav-item-active">{page_name}</p>', unsafe_allow_html=True)
        # For other pages, display a clickable button
        else:
            if st.sidebar.button(page_name, key=f"nav_{page_name}", use_container_width=True):
                st.session_state.page = page_name
                # Reset quiz state if navigating away from the learning page for better UX
                if page_name != "📚 Learning Modules":
                    st.session_state.active_quiz = None
                st.rerun()

    return pages


def add_sidebar_info():
    """Add informational content to the sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.info("This is an educational tool. All data is for informational purposes only. Not financial advice.")
    
    # Development utilities (only show in debug mode)
    if st.sidebar.checkbox("Debug Mode", key="debug_mode"):
        if st.sidebar.button("Reset Session State"):
            keys = list(st.session_state.keys())
            for k in keys:
                if k != "debug_mode":  # Keep debug mode active
                    del st.session_state[k]
            st.rerun()
        
        if st.sidebar.button("Clear Component Cache"):
            ComponentLoader.reset()
            st.sidebar.success("Cache cleared!")


def load_page_with_performance_monitoring(page_func, page_name):
    """Load a page with performance monitoring."""
    with PerformanceMonitor(f"Load {page_name}"):
        try:
            page_func()
        except Exception as e:
            st.error(f"Error loading {page_name}: {str(e)}")
            st.info("Please refresh the page or contact support if the issue persists.")


def main():
    """Main application entry point."""
    # Configure the app
    configure_app()
    
    # Initialize session state
    init_session_state()
    
    # Setup navigation and get pages
    pages = setup_navigation()
    
    # Add sidebar information
    add_sidebar_info()
    
    # Load and render the current page
    current_page_name = st.session_state.page
    current_page_func = pages[current_page_name]
    
    # Load page with performance monitoring
    load_page_with_performance_monitoring(current_page_func, current_page_name)


if __name__ == "__main__":
    main()