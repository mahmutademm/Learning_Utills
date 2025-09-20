"""
What If calculator page functionality for the Wall Street 101 application.
"""

import streamlit as st
import yfinance as yf
import datetime
import random
import plotly.graph_objs as go

from data.vocabulary import FUN_FACTS
from utils.helpers import get_full_history, check_and_award_badges


def page_what_if_calculator():
    """Renders the What If calculator page."""
    st.title("💸 The 'What If' Time Machine")
    st.markdown("Ever wonder how much you'd have if you invested in a company years ago? Let's find out!")

    # Show random fun fact with button to try it
    _show_fun_fact()

    # Get current symbol for validation
    symbol_for_validation = st.session_state.what_if_symbol.upper()
    history_data = get_full_history(symbol_for_validation)

    first_trading_day, last_trading_day = _get_trading_date_range(history_data)

    # Create input form
    _show_input_form(first_trading_day, last_trading_day)


def _show_fun_fact():
    """Shows a random fun fact with option to try it."""
    fact = random.choice(FUN_FACTS)
    if st.button("Try this fun fact!"):
        st.session_state.what_if_symbol = fact['symbol']
        st.session_state.what_if_start_date = datetime.datetime.strptime(fact['start'], "%Y-%m-%d").date()
        st.session_state.what_if_amount = 1000
        st.rerun()
    st.info(f"💡 **Fun Fact:** {fact['fact']}")


def _get_trading_date_range(history_data):
    """Gets the first and last trading days from history data."""
    first_trading_day = None
    last_trading_day = None

    if not history_data.empty:
        first_trading_day = history_data.index[0].date()
        last_trading_day = history_data.index[-1].date()

    return first_trading_day, last_trading_day


def _show_input_form(first_trading_day, last_trading_day):
    """Shows the input form for the what-if calculation."""
    with st.form(key='what_if_form'):
        cols = st.columns([2, 1, 1])
        
        symbol = cols[0].text_input(
            "Stock/Crypto Symbol", 
            value=st.session_state.what_if_symbol
        ).upper()
    
        start_date = cols[1].date_input(
            "Investment Date", 
            value=st.session_state.what_if_start_date,
            min_value=first_trading_day,
            max_value=last_trading_day
        )
        
        amount = cols[2].number_input(
            "Investment Amount ($)", 
            min_value=1, 
            value=st.session_state.what_if_amount
        )
        
        submit_button = st.form_submit_button(label='Calculate My Fortune!')

    if submit_button:
        _handle_calculation(symbol, start_date, amount, first_trading_day)


def _handle_calculation(symbol, start_date, amount, first_trading_day):
    """Handles the what-if calculation."""
    # Update session state
    st.session_state.what_if_symbol = symbol
    st.session_state.what_if_start_date = start_date
    st.session_state.what_if_amount = amount
    st.session_state.what_if_uses += 1
    check_and_award_badges()

    # Re-check history if symbol changed
    history_data = get_full_history(symbol)
    if not history_data.empty:
        first_trading_day = history_data.index[0].date()

    # Validate inputs
    if history_data.empty:
        st.error(f"Invalid symbol '{symbol}'. Please enter a valid stock or crypto symbol.")
        return

    if start_date < first_trading_day:
        st.error(f"Error: This stock did not exist on the selected date. Please pick a date after {first_trading_day.strftime('%Y-%m-%d')}.")
        return

    # Perform calculation
    _calculate_investment_growth(symbol, start_date, amount)


def _calculate_investment_growth(symbol, start_date, amount):
    """Calculates and displays investment growth."""
    end_date = datetime.date.today()
    
    try:
        data = yf.download(
            symbol, 
            start=start_date.strftime('%Y-%m-%d'), 
            end=end_date.strftime('%Y-%m-%d'), 
            progress=False
        )
        
        if data.empty:
            st.error(f"No data found for '{symbol}' in the specified date range. It may not have been trading yet.")
            return
    
        start_price = float(data.iloc[0]['Close'])
        end_price = float(data.iloc[-1]['Close'])
        amount_float = float(amount)
    
        shares = amount_float / start_price
        final_value = shares * end_price
    
        # Display results
        st.success(f"An investment of **${amount_float:,.2f}** in **{symbol}** on **{start_date}** would be worth...")
        st.header(f"💰 **${final_value:,.2f}** today!")
    
        roi = ((final_value - amount_float) / amount_float) * 100
        st.metric("Total Return on Investment", f"{roi:,.2f}%")

        # Create and display growth chart
        _create_growth_chart(data, shares, amount_float, symbol)

    except Exception as e:
        st.error(f"An error occurred. Please check the symbol and date. Error: {e}")


def _create_growth_chart(data, shares, amount_float, symbol):
    """Creates and displays the investment growth chart."""
    data['Investment Value'] = (shares * data['Close'])
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, 
        y=data['Investment Value'], 
        mode='lines', 
        name='Investment Growth', 
        fill='tozeroy', 
        line_color='#00A693'
    ))
    
    fig.update_layout(
        title=f'Growth of ${amount_float:,.2f} in {symbol}', 
        yaxis_title='Value (USD)', 
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.session_state.charts_viewed += 1