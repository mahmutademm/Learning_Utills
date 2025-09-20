"""
Home page functionality for the Wall Street 101 application.
"""

import streamlit as st
from config.constants import COLS_PER_ROW_SHIELDS
from data.vocabulary import VOCAB, BADGES
from utils.helpers import check_and_award_badges, get_shield_level_and_color, create_shield_svg


def page_home():
    """Renders the home page with progress tracking and module mastery shields."""
    st.title("🚀 Welcome to Wall Street 101")
    st.markdown("Your interactive launchpad into the world of financial markets. Start with the learning modules, test your knowledge, and analyze real stocks.")

    st.subheader("Your Progress")
    cols = st.columns(2)
    total_cards = sum(len(v) for v in VOCAB.values())
    completed_cards = sum(st.session_state.module_progress.values())
    progress = completed_cards / total_cards if total_cards > 0 else 0

    cols[0].metric("Learning Progress", f"{completed_cards}/{total_cards} Concepts", f"{progress:.0%} Mastered")
    cols[1].metric("Badges Earned", f"{len(st.session_state.badges)}/{len(BADGES)}", "Keep it up!")
    st.progress(progress)

    # Module Mastery Shields
    st.subheader("🛡️ Module Mastery Shields")
    st.markdown("Visualize your mastery for each learning module. Each shield fills from the bottom up as you complete concepts.")

    modules = list(VOCAB.keys())
    rows = [modules[i:i+COLS_PER_ROW_SHIELDS] for i in range(0, len(modules), COLS_PER_ROW_SHIELDS)]

    for row in rows:
        cols = st.columns(len(row))
        for i, module_name in enumerate(row):
            with cols[i]:
                prog = st.session_state.module_progress.get(module_name, 0)
                total = len(VOCAB.get(module_name, [])) or 1
                pct = int((prog / total) * 100)

                shield_level, shield_color, level_text = get_shield_level_and_color(module_name)
                svg = create_shield_svg(module_name, pct, shield_level, shield_color)

                st.markdown(svg, unsafe_allow_html=True)
                st.markdown(f"**{module_name}** — {pct}% mastered ({prog}/{total} concepts)  <br><small style='color:#BDBDBD'>{level_text}</small>", unsafe_allow_html=True)

                # Expandable details for the shield
                _show_shield_details(module_name, shield_level)

    st.markdown("---")

    # Recently Earned Badges
    st.subheader("🏅 Recently Earned Badges")
    if not st.session_state.badges:
        st.info("Start learning in the 'Learning Modules' to earn your first badge!")
    else:
        _show_earned_badges()


def _show_shield_details(module_name, shield_level):
    """Shows expandable details for a shield."""
    total_questions = sum(len(card.get('quiz', [])) for card in VOCAB.get(module_name, [])) or 0
    answered_questions = len(st.session_state.module_questions_answered.get(module_name, set())) if 'module_questions_answered' in st.session_state else 0

    with st.expander("▸ Details", expanded=False):
        st.markdown(f"**Questions answered:** {answered_questions}/{total_questions} ( {int((answered_questions/total_questions*100) if total_questions else 0)}% )")
        
        if shield_level < 3:
            needed = (total_questions if shield_level == 2 else int(total_questions/2) + 1) - answered_questions
            needed = max(0, needed)
            st.markdown(f"**More needed for next level:** {needed} question(s)")
        else:
            st.markdown("**You have completed all questions for this module.**")

        st.markdown("**Shield Levels:**")
        st.markdown("• Level 1 — Basic mastery: Complete the primary concept questions (level 1) for each card.")
        st.markdown("• Level 2 — Advanced mastery: Answer more than 50% of the total available questions in this module.")
        st.markdown("• Level 3 (Max) — Full mastery: Answer all available questions across every concept in this module.")


def _show_earned_badges():
    """Shows recently earned badges."""
    badges_to_show = [b for b in BADGES if b['name'] in st.session_state.badges]
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