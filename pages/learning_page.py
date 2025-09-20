"""
Learning modules page functionality for the Wall Street 101 application.
"""

import streamlit as st
from data.vocabulary import VOCAB
from utils.helpers import show_dual_charts, check_and_award_badges


def page_learning_modules():
    """Renders the learning modules page with flashcards and quizzes."""
    st.title("📚 Learning Modules")
    st.sidebar.title("Modules")

    # Module selector
    current_selection = st.sidebar.radio(
        "Select a learning module:", 
        list(VOCAB.keys()), 
        key="module_selector_radio", 
        label_visibility="collapsed"
    )
    
    if st.session_state.current_module != current_selection:
        st.session_state.current_module = current_selection
        st.session_state.active_quiz = None 
        st.rerun()

    module_name = st.session_state.current_module
    module_vocab = VOCAB[module_name]
    card_index = st.session_state.card_indices.get(module_name, 0)
    card = module_vocab[card_index]

    # Main logic for displaying either the quiz or the flashcard
    if st.session_state.active_quiz and st.session_state.active_quiz['card_index'] == card_index:
        _handle_quiz_display(card, module_name, card_index, module_vocab)
    else:
        _show_flashcard(card, module_name, card_index, module_vocab)


def _handle_quiz_display(card, module_name, card_index, module_vocab):
    """Handles the quiz display and logic."""
    quiz_status = st.session_state.active_quiz.get('status')
    quiz_level = st.session_state.active_quiz['level']
    quiz_data = card['quiz'][quiz_level - 1]

    if quiz_status == 'pending':
        _display_quiz(card, module_name, card_index)
    elif quiz_status == 'passed':
        _handle_quiz_success(card, module_name, card_index, module_vocab, quiz_level, quiz_data)
    elif quiz_status == 'failed':
        _handle_quiz_failure(quiz_data)


def _display_quiz(card, module_name, card_index):
    """Displays the quiz interface."""
    quiz_info = st.session_state.active_quiz
    level = quiz_info['level']
    quiz_data = card['quiz'][level - 1]

    st.subheader(f"📝 Test Your Knowledge: Level {level}")
    st.markdown(f"#### {quiz_data['q']}")
    st.write("")

    # Create quiz buttons
    num_options = len(quiz_data['options'])
    cols = st.columns(2 if num_options > 2 else num_options)

    for i, option in enumerate(quiz_data['options']):
        with cols[i % 2]:
            if st.button(
                option['text'], 
                key=f"quiz_{module_name}_{card_index}_{level}_{i}", 
                use_container_width=True
            ):
                st.session_state.active_quiz['user_answer'] = i
                if i == quiz_data['correct']:
                    st.session_state.active_quiz['status'] = 'passed'
                    try:
                        st.session_state.module_questions_answered[module_name].add((card_index, level))
                    except Exception:
                        st.session_state.module_questions_answered[module_name] = {(card_index, level)}
                else:
                    st.session_state.active_quiz['status'] = 'failed'
                st.rerun()


def _handle_quiz_success(card, module_name, card_index, module_vocab, quiz_level, quiz_data):
    """Handles successful quiz completion."""
    correct_index = quiz_data['correct']
    st.success("### Correct! 🎉")
    st.info(f"**Explanation:** {quiz_data['options'][correct_index]['reasoning']}")

    # Award progress only on the first successful completion of level 1
    if quiz_level == 1 and st.session_state.module_progress[module_name] == card_index:
        st.session_state.module_progress[module_name] += 1
        check_and_award_badges()

    st.markdown("---")
    cols = st.columns(2)
    
    # Option to try a harder question
    if quiz_level < len(card['quiz']):
        if cols[0].button(f"Try Level {quiz_level + 1} Question", use_container_width=True):
            st.session_state.active_quiz['level'] += 1
            st.session_state.active_quiz['status'] = 'pending'
            st.session_state.active_quiz.pop('user_answer', None)
            st.rerun()

    # Option to move to the next card
    with cols[1]:
        if card_index < len(module_vocab) - 1:
            if st.button("Continue to Next Concept →", type="primary", use_container_width=True):
                st.session_state.card_indices[module_name] = min(card_index + 1, len(module_vocab) - 1)
                st.session_state.active_quiz = None
                st.rerun()
        else:
            st.balloons()
            st.success("🎉 You've completed the module! Select a new one from the sidebar.")


def _handle_quiz_failure(quiz_data):
    """Handles failed quiz attempts."""
    user_answer_index = st.session_state.active_quiz['user_answer']
    st.error("### Not quite...")
    st.warning(f"**Here's a common point of confusion:** {quiz_data['options'][user_answer_index]['reasoning']}")
    
    st.markdown("---")
    if st.button("Try Again", use_container_width=True, type="primary"):
        st.session_state.active_quiz['status'] = 'pending'
        st.session_state.active_quiz.pop('user_answer', None)
        st.rerun()


def _show_flashcard(card, module_name, card_index, module_vocab):
    """Shows the flashcard content."""
    st.header(f"{module_name} ({card_index + 1}/{len(module_vocab)})")
    st.markdown(f"""
    <div class="flashcard">
        <h3>{card['term']}</h3>
        <p>{card['definition']}</p>
        <p><strong>Example:</strong> <em>{card['example']}</em></p>
    </div>
    """, unsafe_allow_html=True)

    if card.get("chart"):
        show_dual_charts(card["chart"], card.get("concept", "price"))

    # Show quiz buttons
    _show_quiz_buttons(card, module_name, card_index)

    # Navigation buttons
    _show_navigation_buttons(module_name, card_index, module_vocab)


def _show_quiz_buttons(card, module_name, card_index):
    """Shows quiz-related buttons."""
    if card_index >= st.session_state.module_progress.get(module_name, 0):
        if st.button("Test My Understanding", key=f"test_{card_index}", type="primary", use_container_width=True):
            st.session_state.active_quiz = {
                'module': module_name, 
                'card_index': card_index, 
                'level': 1, 
                'status': 'pending'
            }
            st.rerun()
    else:
        st.success("✅ You've mastered this topic. Feel free to review or move on.")
        with st.expander("Quick Review (Key Points)"):
            card = VOCAB[st.session_state.current_module][card_index]
            st.markdown(f"- Term: {card['term']}")
            st.markdown(f"- Definition (one-liner): {card['definition'][:180]}{'...' if len(card['definition'])>180 else ''}")
            if card.get("example"):
                st.markdown(f"- Example: {card['example'][:180]}{'...' if len(card['example'])>180 else ''}")
        
        if st.button("Review Quiz", key=f"review_{card_index}", use_container_width=True):
            st.session_state.active_quiz = {
                'module': st.session_state.current_module, 
                'card_index': card_index, 
                'level': 1, 
                'status': 'pending'
            }
            st.rerun()


def _show_navigation_buttons(module_name, card_index, module_vocab):
    """Shows navigation buttons for moving between cards."""
    st.markdown("---")
    cols = st.columns(2)
    
    with cols[0]:
        if card_index > 0:
            if st.button("← Previous"):
                st.session_state.card_indices[module_name] -= 1
                st.session_state.active_quiz = None
                st.rerun()
    
    with cols[1]:
        # Allow moving to the next card if it has been unlocked
        if (card_index < st.session_state.module_progress.get(module_name, 0) and 
            card_index < len(module_vocab) - 1):
            if st.button("Next →"):
                st.session_state.card_indices[module_name] += 1
                st.session_state.active_quiz = None
                st.rerun()