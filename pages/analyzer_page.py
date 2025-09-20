"""
Stock analyzer page functionality for the Wall Street 101 application.
"""

import streamlit as st
import yfinance as yf
from utils.helpers import show_dual_charts, safe_last_close, check_and_award_badges
from config.constants import DEFAULT_VALUES


def page_stock_analyzer():
    """Renders the stock analyzer page."""
    st.title("🕵️ Stock Analyzer")
    st.markdown("Get a complete snapshot of any stock or crypto. View charts, key data, and news all in one place.")

    symbol = st.text_input(
        "Enter a US Stock or Crypto Symbol (e.g., AAPL, TSLA, BTC-USD)", 
        value=DEFAULT_VALUES['analyzer_symbol']
    ).upper()

    if st.button("Analyze"):
        st.session_state.analyzer_uses += 1
        check_and_award_badges()
        _analyze_stock(symbol)


def _analyze_stock(symbol):
    """Analyzes a stock and displays comprehensive information."""
    ticker = yf.Ticker(symbol)
    
    # Get stock info
    try:
        info = ticker.info
    except Exception:
        info = {}
    
    # Get current price with fallback
    price = _get_current_price(symbol, info)
    if not price:
        st.error(f"Could not find data for '{symbol}'. Please enter a valid symbol.")
        return

    # Display stock header and metrics
    _display_stock_header(symbol, info, price)
    
    # Display interactive chart
    st.subheader("Interactive Chart")
    show_dual_charts(symbol, 'price')

    # Display company info and news
    _display_company_info_and_news(info, ticker)


def _get_current_price(symbol, info):
    """Gets the current price with fallback methods."""
    price = None
    try:
        price = info.get('regularMarketPrice')
    except Exception:
        pass
    
    if price is None:
        price = safe_last_close(symbol)
    
    return price


def _display_stock_header(symbol, info, price):
    """Displays stock name, price, and key metrics."""
    st.header(f"{info.get('longName', symbol) or symbol} ({symbol})")
    
    # Calculate price change
    prev_close = _get_previous_close(symbol, info, price)
    change = price - prev_close if prev_close else 0
    change_pct = (change / prev_close) * 100 if prev_close else 0

    # Display metrics
    cols = st.columns(3)
    cols[0].metric("Current Price", f"${price:,.2f}", f"{change:,.2f} ({change_pct:.2f}%)")
    cols[1].metric(
        "Market Cap", 
        f"${info.get('marketCap', 0):,}" if info.get('marketCap') else "N/A"
    )
    
    pe_ratio = info.get('trailingPE')
    cols[2].metric(
        "P/E Ratio", 
        f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"
    )


def _get_previous_close(symbol, info, current_price):
    """Gets the previous close price with fallback."""
    prev_close = info.get('previousClose')
    if prev_close is None:
        try:
            import yfinance as yf
            d2 = yf.download(symbol, period="2d", interval="1d", progress=False, auto_adjust=True)
            if len(d2["Close"].dropna()) >= 2:
                prev_close = float(d2["Close"].dropna().iloc[-2])
            else:
                prev_close = current_price
        except Exception:
            prev_close = current_price
    return prev_close


def _display_company_info_and_news(info, ticker):
    """Displays company profile and recent news."""
    cols = st.columns(2)
    
    with cols[0]:
        st.subheader("Company Profile")
        st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
        st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
        
        website = info.get('website', 'N/A')
        if website != 'N/A':
            st.markdown(f"**Website:** [{website}]({website})")
        else:
            st.markdown("**Website:** N/A")
            
        with st.expander("Business Summary"):
            st.write(info.get('longBusinessSummary', 'No summary available.'))

    with cols[1]:
        st.subheader("Recent News")
        _display_news(ticker)


def _display_news(ticker):
    """Displays recent news for the stock."""
    try:
        news = ticker.news
        if not news:
            st.write("No recent news found.")
            return
            
        for item in news[:5]:  # Show top 5 news items
            title = item.get('title', 'No Title')
            link = item.get('link', '#')
            publisher = item.get('publisher', 'No Publisher')
            st.markdown(f"**[{title}]({link})** - *{publisher}*")
    except Exception as e:
        st.warning(f"Could not retrieve news. Error: {e}")