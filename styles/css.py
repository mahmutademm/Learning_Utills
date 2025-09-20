"""
Custom CSS styles for the Wall Street 101 application.
"""

def get_custom_css():
    """Returns the custom CSS for the application."""
    return """
    <style>
        /* Main App Styling */
        .main {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        /* Sidebar Styling */
        .css-1d391kg {
            background-color: #1A1C23;
        }
        /* Flashcard Styling */
        .flashcard {
            background-color: #262730;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid #4A4A4A;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            transition: 0.3s;
        }
        .flashcard:hover {
            box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
            border: 1px solid #00A693;
        }
        .flashcard h3 {
            color: #00A693;
            font-size: 24px;
        }
        /* Original Button Styling (for main content area) */
        .stButton>button {
            border-radius: 20px;
            border: 1px solid #00A693;
            background-color: transparent;
            color: #00A693;
            padding: 10px 24px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #00A693;
            color: white;
            border: 1px solid #00A693;
        }
        .stButton>button:focus {
            background-color: #00A693;
            color: white;
            box-shadow: none;
        }
        /* Badge Styling */
        .badge {
            background-color: #262730;
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            margin-bottom: 10px;
            border: 1px solid #00A693;
        }
        .badge h4 {
            margin: 0;
            font-size: 18px;
        }
        .badge p {
            margin: 0;
            font-size: 14px;
            color: #BDBDBD;
        }
        /* Quiz Answer Button Styling */
        div[data-testid="stButton"] > button.quiz-option {
            background-color: #262730;
            border: 1px solid #4A4A4A;
            color: #FAFAFA;
            padding: 20px;
            border-radius: 10px;
            height: 100%;
            width: 100%;
            text-align: left;
            font-weight: normal;
            transition: 0.2s;
        }
        div[data-testid="stButton"] > button.quiz-option:hover {
            border-color: #00A693;
            color: #00A693;
            background-color: #1c1e25;
        }
        div[data-testid="stButton"] > button.quiz-option:focus {
            background-color: #262730;
            color: #FAFAFA;
            border-color: #00A693;
            box-shadow: 0 0 0 2px #00A693;
        }

        /* --- NEW Sidebar Navigation Styling --- */
        /* This targets the container for the buttons in the sidebar */
        .css-1d391kg .stButton {
            margin-bottom: -10px; /* Reduce space between buttons */
        }
        /* This targets the button element itself for inactive pages */
        .css-1d391kg .stButton > button {
            background-color: transparent;
            border: none;
            color: #BDBDBD; /* Dim color for inactive items */
            text-align: left;
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            transition: background-color 0.2s, color 0.2s;
            width: 100%;
        }
        .css-1d391kg .stButton > button:hover {
            background-color: #262730;
            color: #FAFAFA; /* Brighten on hover */
            border: none;
        }
        .css-1d391kg .stButton > button:focus {
            background-color: #262730;
            color: #FAFAFA;
            box-shadow: none;
            border: none;
        }
        /* Style for the active page (which is rendered as markdown) */
        .nav-item-active {
            background-color: #00A693;
            color: white !important; /* Use important to override default p color */
            padding: 12px 20px;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            margin: 0px 0px 4px 0px; /* Match button spacing */
        }
    </style>
    """