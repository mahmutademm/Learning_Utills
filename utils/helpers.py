"""
Utility functions for the Wall Street 101 application.
Contains data fetching, session state management, and chart functions.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import datetime

from config.constants import (
    CACHE_TIMEOUT_SHORT, CACHE_TIMEOUT_LONG, DEFAULT_CHART_PERIOD,
    CHART_HEIGHT_SIMPLE, CHART_HEIGHT_ANALYTICAL, MOVING_AVERAGE_PERIODS,
    BADGES_CONFIG
)
from data.vocabulary import VOCAB, BADGES


# --- Data Fetching Functions ---

@st.cache_data(ttl=CACHE_TIMEOUT_SHORT)
def get_stock_data(symbol, period=DEFAULT_CHART_PERIOD):
    """Fetch stock data with caching."""
    try:
        return yf.Ticker(symbol).history(period=period, auto_adjust=True)
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=CACHE_TIMEOUT_LONG)
def get_full_history(symbol):
    """Gets the entire price history for a stock to find its first trading day."""
    try:
        return yf.Ticker(symbol).history(period="max", auto_adjust=True)
    except Exception:
        return pd.DataFrame()


def safe_last_close(symbol: str):
    """Safe last price helper for robust analyzer fallback."""
    try:
        d = yf.download(symbol, period="2d", interval="1d", progress=False, auto_adjust=True)
        if isinstance(d, pd.DataFrame) and not d.empty and "Close" in d.columns:
            return float(d["Close"].dropna().iloc[-1])
    except Exception:
        pass
    try:
        t = yf.Ticker(symbol)
        fi = getattr(t, "fast_info", None)
        p = getattr(fi, "last_price", None) if fi else None
        if p is not None and not pd.isna(p):
            return float(p)
    except Exception:
        pass
    return None


# --- Session State Management ---

def init_session_state():
    """Initialize all session state variables."""
    if 'current_module' not in st.session_state:
        st.session_state.current_module = list(VOCAB.keys())[0]
    if 'card_indices' not in st.session_state:
        st.session_state.card_indices = {module: 0 for module in VOCAB.keys()}
    if 'module_progress' not in st.session_state:
        st.session_state.module_progress = {module: 0 for module in VOCAB.keys()}
    if 'badges' not in st.session_state:
        st.session_state.badges = set()
    if 'charts_viewed' not in st.session_state:
        st.session_state.charts_viewed = 0
    if 'facts_read' not in st.session_state:
        st.session_state.facts_read = 0
    if 'analyzer_uses' not in st.session_state:
        st.session_state.analyzer_uses = 0
    if 'what_if_uses' not in st.session_state:
        st.session_state.what_if_uses = 0
    if 'active_quiz' not in st.session_state:
        st.session_state.active_quiz = None
    if 'what_if_symbol' not in st.session_state:
        st.session_state.what_if_symbol = "NVDA"
    if 'what_if_start_date' not in st.session_state:
        st.session_state.what_if_start_date = datetime.date(2015, 1, 1)
    if 'what_if_amount' not in st.session_state:
        st.session_state.what_if_amount = 1000
    if 'module_questions_answered' not in st.session_state:
        st.session_state.module_questions_answered = {module: set() for module in VOCAB.keys()}
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"


def check_and_award_badges():
    """Checks progress and awards badges."""
    if any(v > 0 for v in st.session_state.module_progress.values()):
        st.session_state.badges.add("Wall Street Rookie")
    
    if st.session_state.charts_viewed >= BADGES_CONFIG['charts_viewed_threshold']:
        st.session_state.badges.add("Chart Master")
    
    if st.session_state.facts_read >= BADGES_CONFIG['facts_read_threshold']:
        st.session_state.badges.add("Fact Finder")
    
    if 'fund_page_visited' in st.session_state and st.session_state.fund_page_visited:
        st.session_state.badges.add("Fund Explorer")
    
    if st.session_state.analyzer_uses >= BADGES_CONFIG['analyzer_uses_threshold']:
        st.session_state.badges.add("Market Analyst")
    
    if st.session_state.what_if_uses >= BADGES_CONFIG['what_if_uses_threshold']:
        st.session_state.badges.add("Portfolio Visionary")

    all_modules_completed = all(st.session_state.module_progress[m] >= len(VOCAB[m]) for m in VOCAB)
    if all_modules_completed:
        st.session_state.badges.add("Knowledge Titan")

    if len(st.session_state.badges) >= len(BADGES) - 1:
        st.session_state.badges.add("Trading Legend")


# --- Chart Functions ---

def create_simple_chart(symbol, data, concept):
    """Create a simplified educational chart."""
    fig_simple = go.Figure()
    fig_simple.add_trace(go.Scatter(
        x=data.index, 
        y=data['Close'], 
        mode='lines', 
        name='Price', 
        line=dict(color='#00A693', width=2)
    ))

    if concept in ['support', 'resistance', 'breakout']:
        level = data['Close'][-200:].median() if concept == 'support' else data['Close'][-200:].quantile(0.75)
        color = 'lime' if concept == 'support' else 'red'
        fig_simple.add_hline(
            y=level, 
            line_width=2, 
            line_dash="dash", 
            line_color=color,
            annotation_text=concept.title(), 
            annotation_position="bottom right"
        )
    elif concept == 'ma':
        data['MA50'] = data['Close'].rolling(window=MOVING_AVERAGE_PERIODS['short']).mean()
        fig_simple.add_trace(go.Scatter(
            x=data.index, 
            y=data['MA50'], 
            mode='lines', 
            name='50-Day MA', 
            line=dict(color='orange', width=1.5)
        ))
    elif concept == 'cross':
        data['MA50'] = data['Close'].rolling(window=MOVING_AVERAGE_PERIODS['short']).mean()
        data['MA200'] = data['Close'].rolling(window=MOVING_AVERAGE_PERIODS['long']).mean()
        fig_simple.add_trace(go.Scatter(
            x=data.index, 
            y=data['MA50'], 
            mode='lines', 
            name='50-Day MA', 
            line=dict(color='orange', width=1.5)
        ))
        fig_simple.add_trace(go.Scatter(
            x=data.index, 
            y=data['MA200'], 
            mode='lines', 
            name='200-Day MA', 
            line=dict(color='purple', width=1.5)
        ))

    fig_simple.update_layout(
        title=f"Simplified View: {symbol}", 
        template="plotly_dark", 
        height=CHART_HEIGHT_SIMPLE
    )
    return fig_simple


def create_analytical_chart(symbol, data):
    """Create a detailed analytical chart with technical indicators."""
    fig = make_subplots(
        rows=2, cols=1, 
        shared_xaxes=True, 
        vertical_spacing=0.05,
        subplot_titles=(f'{symbol.upper()} Price Action', 'Volume'), 
        row_heights=[0.7, 0.3]
    )
    
    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=data.index,
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close'],
        name='Price'
    ), row=1, col=1)
    
    # Volume chart
    fig.add_trace(go.Bar(
        x=data.index, 
        y=data['Volume'], 
        name='Volume', 
        marker_color='rgba(0, 166, 147, 0.5)'
    ), row=2, col=1)
    
    # Moving averages
    data['MA50'] = data['Close'].rolling(window=MOVING_AVERAGE_PERIODS['short']).mean()
    data['MA200'] = data['Close'].rolling(window=MOVING_AVERAGE_PERIODS['long']).mean()
    
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['MA50'], 
        mode='lines', 
        name='50-Day MA', 
        line=dict(color='orange', width=1)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['MA200'], 
        mode='lines', 
        name='200-Day MA', 
        line=dict(color='purple', width=1)
    ), row=1, col=1)

    fig.update_layout(
        height=CHART_HEIGHT_ANALYTICAL, 
        template="plotly_dark", 
        xaxis_rangeslider_visible=False,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig


def show_dual_charts(symbol, concept):
    """Displays both a simplified educational chart and a full analytical chart."""
    data = get_stock_data(symbol)
    if data.empty:
        st.warning(f"Could not retrieve data for '{symbol}'.")
        return

    st.session_state.charts_viewed += 1

    simplified_tab, analytical_tab = st.tabs(["🎓 Simplified View", "🔬 Analytical View"])

    with simplified_tab:
        st.markdown(f"**Visualizing: {concept.replace('_', ' ').title()}**")
        fig_simple = create_simple_chart(symbol, data, concept)
        
        # Add educational info based on concept
        if concept in ['support', 'resistance', 'breakout']:
            st.info(f"This simplified chart highlights a key price level. Notice how the price interacts with the {concept} line.")
        elif concept == 'ma':
            st.info("The orange line is the 50-day moving average. It smooths out price action to show the trend more clearly.")
        elif concept == 'cross':
            st.info("This chart shows the 50-day (orange) and 200-day (purple) moving averages. A 'Golden Cross' (orange over purple) is bullish.")
        
        st.plotly_chart(fig_simple, use_container_width=True)

    with analytical_tab:
        st.markdown("**Real-World Chart with Technical Indicators**")
        fig_analytical = create_analytical_chart(symbol, data)
        st.plotly_chart(fig_analytical, use_container_width=True)


# --- Shield Visualization Functions ---

def create_shield_svg(module_name, progress_pct, shield_level, shield_color):
    """Creates an SVG shield visualization for module progress."""
    safe_id = ''.join(ch for ch in module_name if ch.isalnum()) or 'mod'
    svg_height = 115
    fill_h = int((progress_pct / 100.0) * svg_height)
    rect_y = svg_height - fill_h

    return f'''<div style="text-align:center">
    <svg viewBox="0 0 100 120" width="140" height="168" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <clipPath id="clip_{safe_id}">
          <rect x="0" y="{rect_y}" width="100" height="{fill_h}" />
        </clipPath>
      </defs>
      <!-- Shield outline -->
      <path d="M50 6 L86 22 L74 86 L50 114 L26 86 L14 22 Z" fill="#2b2d33" stroke="#4a4a4a" stroke-width="2"/>
      <!-- Filled portion (clipped) -->
      <path d="M50 6 L86 22 L74 86 L50 114 L26 86 L14 22 Z" fill="{shield_color}" clip-path="url(#clip_{safe_id})" opacity="0.95"/>
      <!-- Inner glow -->
      <path d="M50 12 L80 26 L70 82 L50 106 L30 82 L20 26 Z" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="6" />
      <!-- Percentage label -->
      <text x="50" y="64" text-anchor="middle" fill="#FAFAFA" font-size="16" font-weight="600">{progress_pct}%</text>
    </svg>
    </div>'''


def get_shield_level_and_color(module_name):
    """Determines shield level and color based on quiz completion."""
    total_questions = sum(len(card.get('quiz', [])) for card in VOCAB.get(module_name, [])) or 0
    answered_questions = len(st.session_state.module_questions_answered.get(module_name, set())) if 'module_questions_answered' in st.session_state else 0

    if total_questions > 0:
        if answered_questions >= total_questions:
            return 3, "#FFD700", "Level 3 (Max)"  # gold
        elif answered_questions > (total_questions / 2):
            return 2, "#D9382C", "Level 2"  # red
        else:
            return 1, "#00A693", "Level 1"  # default green
    else:
        return 1, "#00A693", "Level 1"