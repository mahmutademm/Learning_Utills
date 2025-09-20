"""
Funds explorer and achievements pages for the Wall Street 101 application.
"""

import streamlit as st
from data.vocabulary import FUNDS, BADGES
from utils.helpers import show_dual_charts, check_and_award_badges


def page_funds_explorer():
    """Renders the funds and ETFs explorer page."""
    st.title("🧭 Funds & ETFs Explorer")
    st.markdown("ETFs (Exchange-Traded Funds) are a popular way to instantly diversify your portfolio. Explore some of the most common types.")
    
    st.session_state.fund_page_visited = True
    check_and_award_badges()

    for fund in FUNDS:
        with st.container():
            st.markdown(f"### {fund['name']}")
            st.markdown(f"**Fund Type:** `{fund['type']}` | **Typical Annual Return:** `{fund['avg_return']}`")
            st.write(fund['description'])
            
            if fund.get("symbol"):
                with st.expander(f"View Chart for {fund['symbol']}"):
                    show_dual_charts(fund['symbol'], 'price')
            
            st.markdown("---")


def page_achievements():
    """Renders the achievements page."""
    st.title("🏅 Your Achievements")
    st.markdown("Track your progress and celebrate your learning milestones!")
    check_and_award_badges()

    if not st.session_state.badges:
        st.info("No badges yet. Complete learning modules and use the app's tools to start earning them!")
        return

    # Show earned badges
    st.subheader("Earned Badges")
    earned_badges = [b for b in BADGES if b['name'] in st.session_state.badges]
    _display_badges(earned_badges)

    st.markdown("---")
    
    # Show badges to unlock
    st.subheader("Badges to Unlock")
    unlocked_badges = [b for b in BADGES if b['name'] not in st.session_state.badges]
    
    if not unlocked_badges:
        st.success("👑 You are a Trading Legend! You've collected all the badges!")
    else:
        for badge in unlocked_badges:
            st.write(f"**{badge['icon']} {badge['name']}:** *{badge['desc']}*")


def _display_badges(badges_to_show):
    """Displays badges in a grid layout."""
    if not badges_to_show:
        return
        
    num_columns = min(len(badges_to_show), 4)
    cols = st.columns(num_columns or 1)
    
    for i, badge in enumerate(badges_to_show):
        with cols[i % num_columns]:
            st.markdown(f"""
            <div class="badge">
                <h4>{badge['icon']} {badge['name']}</h4>
                <p>{badge['desc']}</p>
            </div>
            """, unsafe_allow_html=True)