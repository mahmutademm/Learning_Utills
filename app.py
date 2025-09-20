import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import random
import datetime

# --- Page Configuration ---
st.set_page_config(
    page_title="Wall Street 101: The Ultimate Trading Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for a Modern & Sleek Look ---
st.markdown("""
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
""", unsafe_allow_html=True)


# --- EXPANDED Data with QUIZ content for every card ---
# --- NEW VOCAB with detailed reasoning for each quiz option ---
VOCAB = {
    "⭐ Getting Started": [
        {"term": "Stock", "definition": "A security that represents ownership in a fraction of a corporation. Entitles the owner to a proportion of the corporation's assets and profits. Stocks can be common or preferred, with common stocks offering voting rights and potential dividends, while preferred stocks provide fixed dividends but limited voting rights. Stock prices fluctuate based on supply and demand, company performance, and market conditions. They are key components of investment portfolios and can be traded on exchanges.", "example": "Buying one share of Apple (AAPL) makes you a part-owner of Apple Inc. If Apple performs well, the stock price may rise, and you might receive dividends. However, if the company struggles, the stock value could decline. For instance, during the 2008 financial crisis, many stocks lost significant value, but long-term holders of strong companies like Apple saw substantial recovery and growth.", "chart": "AAPL", "concept": "price", "quiz": [
            {"q": "A stock represents which of the following?", "options": [
                {"text": "A loan to a company", "reasoning": "This is a common misconception. A loan to a company is a form of debt, and the holder is a lender, not an owner. This type of investment is typically a bond, which pays interest. Stocks, on the other hand, represent ownership."},
                {"text": "Ownership in a company", "reasoning": "Correct! A stock (also known as equity) is a security that represents the ownership of a fraction of a corporation, making you a part-owner with a claim on its assets and profits."}
            ], "correct": 1},
            {"q": "If you own a stock, you are entitled to...", "options": [
                {"text": "A fixed interest payment", "reasoning": "This describes a bond or other debt instrument. Stockholders are owners, not lenders, so they don't receive fixed interest. Their returns come from stock price appreciation and potential dividends, which are not guaranteed."},
                {"text": "A piece of the company's debt", "reasoning": "This is the opposite of what a stock represents. As a stockholder, you own a piece of the company's equity (ownership). The company's debt is owed to its lenders, such as bondholders."},
                {"text": "A portion of the company's assets and profits", "reasoning": "Exactly! As a part-owner, you have a claim on the company's assets and any profits it distributes (as dividends). Your share's value grows as the company becomes more valuable."},
                {"text": "The right to manage the company's daily operations", "reasoning": "While stockholders are owners, they don't run the company day-to-day. They elect a board of directors, who in turn hire executives (like the CEO) to manage operations. Your power is in voting, not managing."}
            ], "correct": 2},
            {"q": "Which of the following is NOT true about owning a stock?", "options": [
                {"text": "It gives you a claim on assets", "reasoning": "This statement is actually true. As an owner, you have a claim on the company's assets, although debt holders get paid first in a bankruptcy."},
                {"text": "It means the company owes you a specific amount of money back", "reasoning": "Correct! This is the statement that is NOT true. A stock's value fluctuates and is not a guaranteed loan. The company does not owe you your initial investment back; you must sell the stock on the market to another investor to get your money out."},
                {"text": "It represents equity", "reasoning": "This statement is true. 'Stock' and 'equity' are often used interchangeably to mean ownership in a company."},
                {"text": "You can profit if the company does well", "reasoning": "This statement is true. If the company's profits and value grow, the stock price is likely to increase, leading to a profit for you when you sell."},
                {"text": "You have voting rights in major decisions", "reasoning": "This is true for common stocks, which allow voting on issues like board elections."},
                {"text": "You are protected from company debts", "reasoning": "This is true; stockholders have limited liability and aren't personally responsible for debts."}
            ], "correct": 1},
            {"q": "In a bankruptcy, who gets paid before common stockholders?", "options": [
                {"text": "Preferred stockholders", "reasoning": "Preferred stockholders get paid before common stockholders but after debt holders."},
                {"text": "Bondholders and creditors", "reasoning": "Correct! In liquidation, debt holders (bondholders and creditors) are paid first, followed by preferred stockholders, and common stockholders last."},
                {"text": "Employees", "reasoning": "Employees are often paid as operational expenses, but in bankruptcy, secured creditors come first."},
                {"text": "Government taxes", "reasoning": "Taxes are a form of debt and are paid before stockholders."},
                {"text": "Suppliers", "reasoning": "Suppliers are unsecured creditors and get paid before stockholders but after secured creditors."},
                {"text": "No one; stockholders are first", "reasoning": "This is incorrect; stockholders are last in line."},
                {"text": "The CEO and executives", "reasoning": "Executives may have claims as employees or through contracts, but they are not prioritized over creditors."}
            ], "correct": 1},
            {"q": "Which type of stock typically offers voting rights but no fixed dividends?", "options": [
                {"text": "Preferred stock", "reasoning": "Preferred stock offers fixed dividends but usually no voting rights."},
                {"text": "Common stock", "reasoning": "Correct! Common stock provides voting rights and potential dividends based on company performance, but they are not fixed."},
                {"text": "Treasury stock", "reasoning": "Treasury stock is repurchased by the company and has no rights."},
                {"text": "Convertible stock", "reasoning": "Convertible stock can be converted to common stock, but it's a type of preferred."},
                {"text": "Restricted stock", "reasoning": "Restricted stock has limitations on sale but is usually common stock."},
                {"text": "All stocks offer fixed dividends", "reasoning": "Not all stocks offer fixed dividends; common stocks do not."},
                {"text": "Bonds", "reasoning": "Bonds are debt, not stock."},
                {"text": "ETFs", "reasoning": "ETFs are funds, not individual stocks."}
            ], "correct": 1}
        ]},
        {"term": "Ticker Symbol", "definition": "A unique series of letters assigned to a security for trading purposes. E.g., 'AAPL' for Apple, 'TSLA' for Tesla. Ticker symbols are used to identify stocks, ETFs, and other securities on exchanges, facilitating quick trading and data retrieval. They can vary by exchange and may include suffixes for different share classes or types.", "example": "To buy or analyze a stock, you almost always start with its ticker symbol. For example, 'AAPL' is Apple on NASDAQ, while 'BRK.A' and 'BRK.B' represent different classes of Berkshire Hathaway shares on NYSE. Tickers help in avoiding confusion between similar company names.", "chart": None, "quiz": [
            {"q": "What is the primary purpose of a ticker symbol?", "options": [
                {"text": "To hide a company's real name", "reasoning": "While it's an abbreviation, the purpose isn't to hide the name but to make it faster and easier to identify for trading, where speed and accuracy are critical."},
                {"text": "To uniquely identify a stock for trading", "reasoning": "Correct! Ticker symbols are abbreviations that allow for fast and unambiguous identification of securities on exchanges and trading platforms."}
            ], "correct": 1},
            {"q": "Which of these is a ticker symbol?", "options": [
                {"text": "Microsoft Corporation", "reasoning": "This is the full legal name of the company, not its ticker symbol used for trading."},
                {"text": "The S&P 500 Index", "reasoning": "This is the name of a major stock market index, not a specific security you can trade directly (though you can trade ETFs that track it, like SPY)."},
                {"text": "MSFT", "reasoning": "Correct! 'MSFT' is the unique ticker for Microsoft Corporation on the NASDAQ exchange."},
                {"text": "New York Stock Exchange", "reasoning": "This is the name of a stock exchange, which is a marketplace, not a security itself."}
            ], "correct": 2},
            {"q": "Which of the following is a valid use of a ticker symbol?", "options": [
                {"text": "To name a company in legal documents", "reasoning": "Legal documents use the full company name, not the ticker."},
                {"text": "To quickly look up stock prices on a trading platform", "reasoning": "Correct! Tickers are designed for quick identification in trading systems."},
                {"text": "To represent the company's address", "reasoning": "Tickers have no relation to physical locations."},
                {"text": "To indicate the company's founding year", "reasoning": "Tickers are arbitrary letters, not related to dates."},
                {"text": "To hide sensitive financial data", "reasoning": "Tickers are public identifiers."},
                {"text": "To confuse investors", "reasoning": "The purpose is to simplify, not confuse."}
            ], "correct": 1},
            {"q": "What does a suffix like '.B' in a ticker (e.g., BRK.B) typically indicate?", "options": [
                {"text": "A foreign listing", "reasoning": "Foreign listings may have different suffixes, but '.B' is for share class."},
                {"text": "A different share class", "reasoning": "Correct! Suffixes like '.A' or '.B' denote different classes of stock with varying rights."},
                {"text": "A bond instead of stock", "reasoning": "Bonds have different identifiers."},
                {"text": "A delisted stock", "reasoning": "Delisted stocks are removed from trading."},
                {"text": "An ETF", "reasoning": "ETFs have their own tickers without standard suffixes for classes."},
                {"text": "A preferred stock", "reasoning": "Preferred stocks may have suffixes, but '.B' is often for common class B."},
                {"text": "A mutual fund", "reasoning": "Mutual funds have different symbols."}
            ], "correct": 1},
            {"q": "Which statement about ticker symbols is FALSE?", "options": [
                {"text": "They are unique to each security", "reasoning": "True; each is unique on its exchange."},
                {"text": "They can be reused after a company delists", "reasoning": "True; tickers can be reassigned."},
                {"text": "They are always 4 letters long", "reasoning": "Correct! Tickers can be 1-5 letters or more with suffixes."},
                {"text": "They facilitate quick trading", "reasoning": "True."},
                {"text": "They vary by exchange", "reasoning": "True; different exchanges have different formats."},
                {"text": "They help in data retrieval", "reasoning": "True."},
                {"text": "They may include numbers in some markets", "reasoning": "True in some international markets."},
                {"text": "They are case-sensitive in some systems", "reasoning": "False in most cases, but the statement is about false ones."}
            ], "correct": 2}
        ]},
        {"term": "Stock Exchange", "definition": "A marketplace where securities like stocks and bonds are bought and sold. The two main US exchanges are the NYSE and the NASDAQ. Exchanges provide liquidity, price discovery, and regulatory oversight. They have listing requirements for companies, such as minimum market cap and financial reporting standards. Trading on exchanges is facilitated by brokers and can be electronic or floor-based.", "example": "The New York Stock Exchange (NYSE) is known for its physical trading floor and blue-chip companies. NASDAQ is electronic and tech-focused. For example, Apple is listed on NASDAQ, while Coca-Cola is on NYSE. Exchanges ensure fair trading and publish real-time data.", "chart": None, "quiz": [
            {"q": "A stock exchange is essentially a...", "options": [
                {"text": "Government regulatory body", "reasoning": "While exchanges are heavily regulated by government bodies like the SEC, the exchange itself is a private or public company whose main function is to be a marketplace."},
                {"text": "Marketplace for securities", "reasoning": "Correct! An exchange's core function is to be a marketplace where buyers and sellers can transact securities in a fair and orderly way."}
            ], "correct": 1},
            {"q": "The two major stock exchanges in the United States are:", "options": [
                {"text": "Dow Jones and S&P 500", "reasoning": "This is a very common point of confusion. The Dow Jones and S&P 500 are stock market *indexes*, which are like a report card for a segment of the market. They are not exchanges where trading happens."},
                {"text": "NYSE and NASDAQ", "reasoning": "Correct! The New York Stock Exchange (NYSE) and the NASDAQ are the primary exchanges where the vast majority of U.S. stock trading occurs."},
                {"text": "The Fed and the Treasury", "reasoning": "These are major U.S. government financial institutions. The Federal Reserve (Fed) controls monetary policy, and the Treasury manages government finances. They are not stock exchanges."},
                {"text": "Robinhood and Fidelity", "reasoning": "These are brokerage firms. You use a broker to place orders, and the broker then sends those orders to an exchange (like the NYSE or NASDAQ) to be executed."}
            ], "correct": 1},
            {"q": "Which is a key function of a stock exchange?", "options": [
                {"text": "Setting interest rates", "reasoning": "That's the central bank's role."},
                {"text": "Providing liquidity for trading", "reasoning": "Correct! Exchanges allow easy buying and selling."},
                {"text": "Printing money", "reasoning": "That's the mint or central bank."},
                {"text": "Managing company operations", "reasoning": "Companies manage themselves."},
                {"text": "Taxing investors", "reasoning": "That's the government's role."},
                {"text": "Guaranteeing profits", "reasoning": "No exchange guarantees profits."}
            ], "correct": 1},
            {"q": "What is a listing requirement for companies on major exchanges?", "options": [
                {"text": "Minimum market cap", "reasoning": "Correct! Exchanges require a certain size and financial health."},
                {"text": "Physical office in New York", "reasoning": "Not required; exchanges are global."},
                {"text": "Government ownership", "reasoning": "Exchanges are for public companies."},
                {"text": "No debt allowed", "reasoning": "Companies can have debt."},
                {"text": "Only tech companies", "reasoning": "All industries are listed."},
                {"text": "Annual parties for traders", "reasoning": "Not a requirement."},
                {"text": "CEO must be famous", "reasoning": "Irrelevant to listing."}
            ], "correct": 0},
            {"q": "Which statement about stock exchanges is FALSE?", "options": [
                {"text": "They provide regulatory oversight", "reasoning": "True; they enforce rules."},
                {"text": "They are all physical floors", "reasoning": "Correct! Many are electronic like NASDAQ."},
                {"text": "They facilitate price discovery", "reasoning": "True."},
                {"text": "They have listing standards", "reasoning": "True."},
                {"text": "They publish real-time data", "reasoning": "True."},
                {"text": "They can be global", "reasoning": "True."},
                {"text": "They work with brokers", "reasoning": "True."},
                {"text": "They ensure fair trading", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Bull Market", "definition": "A market condition where security prices are rising or are expected to rise. Characterized by optimism and investor confidence. Bull markets are often associated with economic expansion, low unemployment, and increasing corporate profits. They can last for years and are typically defined as a 20% rise from recent lows. However, they can end abruptly due to overvaluation or external shocks.", "example": "The period from 2009 to early 2020 was one of the longest bull markets in U.S. history, driven by tech innovation and low interest rates. During this time, the S&P 500 rose over 400%. Bull markets encourage investment but can lead to bubbles if optimism turns to euphoria.", "chart": "SPY", "concept": "trend", "quiz": [
            {"q": "A bull market is characterized by:", "options": [
                {"text": "Falling prices", "reasoning": "Falling prices are characteristic of a 'bear market,' the opposite of a bull market. Think of a bear swiping its paws downwards."},
                {"text": "Rising prices", "reasoning": "Correct! A bull market is defined by a sustained upward trend in prices. Think of a bull thrusting its horns upwards."}
            ], "correct": 1},
            {"q": "Which emotion best describes a bull market?", "options": [
                {"text": "Fear", "reasoning": "Fear is the dominant emotion in a bear market, leading to selling and falling prices."},
                {"text": "Indifference", "reasoning": "Indifference might describe a sideways or stagnant market, but a bull market is characterized by strong positive sentiment."},
                {"text": "Optimism", "reasoning": "Correct! Optimism and confidence are the hallmarks of a bull market, as investors expect prices to continue rising."},
                {"text": "Panic", "reasoning": "Panic is an extreme form of fear, often leading to market crashes or sharp sell-offs, which are features of a bear market."}
            ], "correct": 2},
            {"q": "A bull market is typically defined as a rise of at least what percentage from recent lows?", "options": [
                {"text": "5%", "reasoning": "5% is a small rally, not a bull market."},
                {"text": "10%", "reasoning": "10% is a correction in reverse, but not a full bull market."},
                {"text": "20%", "reasoning": "Correct! A 20% rise from lows signals a bull market."},
                {"text": "30%", "reasoning": "30% is a strong rally, but the standard is 20%."},
                {"text": "50%", "reasoning": "50% is exceptional, but not the definition."},
                {"text": "100%", "reasoning": "Doubling is rare and not the threshold."}
            ], "correct": 2},
            {"q": "Which economic factor is often associated with bull markets?", "options": [
                {"text": "High unemployment", "reasoning": "High unemployment is more common in recessions and bear markets."},
                {"text": "Low interest rates", "reasoning": "Correct! Low rates encourage borrowing and investment, fueling bull markets."},
                {"text": "Rising inflation", "reasoning": "High inflation can hurt bull markets by raising costs."},
                {"text": "Decreasing GDP", "reasoning": "Falling GDP signals recession, not bull markets."},
                {"text": "Trade deficits", "reasoning": "Trade deficits can be neutral or negative."},
                {"text": "High taxes", "reasoning": "High taxes can discourage investment."},
                {"text": "Global conflicts", "reasoning": "Conflicts often lead to uncertainty and bear markets."}
            ], "correct": 1},
            {"q": "Which statement about bull markets is FALSE?", "options": [
                {"text": "They are driven by optimism", "reasoning": "True."},
                {"text": "They always last at least 10 years", "reasoning": "Correct! Bull markets can vary in length; some are short."},
                {"text": "They can lead to asset bubbles", "reasoning": "True."},
                {"text": "They are associated with economic growth", "reasoning": "True."},
                {"text": "They encourage risk-taking", "reasoning": "True."},
                {"text": "They can end with overvaluation", "reasoning": "True."},
                {"text": "They are defined by 20% rises", "reasoning": "True."},
                {"text": "They benefit long-term investors", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Bear Market", "definition": "A market condition where security prices fall, and widespread pessimism causes the negative sentiment to be self-sustaining. Bear markets are typically defined as a 20% decline from recent highs and can be triggered by recessions, high inflation, or geopolitical events. They often lead to reduced investment and economic contraction but can create buying opportunities for long-term investors.", "example": "A bear market is officially declared after a 20% drop from recent highs, as seen in 2022 due to inflation and rate hikes. The 2008 financial crisis bear market saw the S&P 500 drop over 50%. Bear markets test investor patience but historically precede recoveries.", "chart": "QQQ", "concept": "trend", "quiz": [
            {"q": "A bear market is characterized by:", "options": [
                {"text": "Falling prices", "reasoning": "Correct! In a bear market, the overall trend is downward, driven by pessimism and fear."},
                {"text": "Rising prices", "reasoning": "Rising prices are characteristic of a 'bull market,' the opposite of a bear market. Think of a bull thrusting its horns upwards."}
            ], "correct": 0},
            {"q": "A market is officially considered a 'bear market' after what percentage decline from its peak?", "options": [
                {"text": "5%", "reasoning": "A 5% drop is a minor pullback and happens quite frequently in healthy markets."},
                {"text": "10%", "reasoning": "A 10% decline from a peak is known as a 'correction,' which is significant but not yet a bear market."},
                {"text": "20%", "reasoning": "Correct! A 20% or greater decline from recent highs is the technical definition of a bear market."},
                {"text": "50%", "reasoning": "A 50% decline is a severe bear market or a crash, but the official threshold is crossed at 20%."}
            ], "correct": 2},
            {"q": "Which is often a trigger for a bear market?", "options": [
                {"text": "Economic recession", "reasoning": "Correct! Recessions lead to falling profits and bear markets."},
                {"text": "Low interest rates", "reasoning": "Low rates support bull markets."},
                {"text": "Rising employment", "reasoning": "Rising employment supports bull markets."},
                {"text": "Strong GDP growth", "reasoning": "Growth supports bull markets."},
                {"text": "Investor optimism", "reasoning": "Optimism drives bull markets."},
                {"text": "Technological innovation", "reasoning": "Innovation can fuel bull markets."}
            ], "correct": 0},
            {"q": "What is a potential positive aspect of a bear market?", "options": [
                {"text": "Higher stock prices", "reasoning": "Prices fall in bear markets."},
                {"text": "Buying opportunities for undervalued stocks", "reasoning": "Correct! Bear markets can create bargains for long-term investors."},
                {"text": "Increased volatility for day traders", "reasoning": "Volatility is high, but not always positive."},
                {"text": "More IPOs", "reasoning": "IPOs decrease in bear markets."},
                {"text": "Higher dividends", "reasoning": "Dividends may be cut."},
                {"text": "Easier borrowing", "reasoning": "Borrowing becomes harder."},
                {"text": "Global expansion", "reasoning": "Bear markets often coincide with contraction."}
            ], "correct": 1},
            {"q": "Which statement about bear markets is FALSE?", "options": [
                {"text": "They are defined by 20% declines", "reasoning": "True."},
                {"text": "They always lead to depressions", "reasoning": "Correct! Not all bear markets cause depressions; many are short-lived."},
                {"text": "They are driven by pessimism", "reasoning": "True."},
                {"text": "They can create buying opportunities", "reasoning": "True."},
                {"text": "They often follow bull markets", "reasoning": "True."},
                {"text": "They test investor patience", "reasoning": "True."},
                {"text": "They precede recoveries", "reasoning": "True."},
                {"text": "They can be triggered by events", "reasoning": "True."}
            ], "correct": 1}
        ]}
    ],
    "📈 Basic Charting": [
        {"term": "Support", "definition": "A price level where a falling stock tends to stop and may reverse upward, caused by a concentration of demand. Support levels are formed by previous lows and can be horizontal or trending. Breaking support can lead to further declines, while bouncing off support signals strength. Traders use support for entry points in long positions.", "example": "In 2022, the S&P 500 (SPY) found strong support around the $360 level, bouncing off it multiple times before eventually breaking lower. This level was a key psychological and technical point, attracting buyers each time the index approached it.", "chart": "SPY", "concept": "support", "quiz": [
            {"q": "Support is a price level that acts as a...", "options": [
                {"text": "Floor", "reasoning": "Correct! Support acts as a floor where buying pressure (demand) is strong enough to stop a price from falling further."},
                {"text": "Ceiling", "reasoning": "A price ceiling is known as 'resistance,' which is the opposite of support. Resistance is where selling pressure stops a price from rising."}
            ], "correct": 0},
            {"q": "At a support level, which is stronger?", "options": [
                {"text": "Selling pressure (Supply)", "reasoning": "If selling pressure were stronger, the price would break through the support level and continue to fall."},
                {"text": "Buying pressure (Demand)", "reasoning": "Correct! A support level forms because the demand from buyers is greater than the supply from sellers at that price, causing the price to bounce upwards."},
                {"text": "Government intervention", "reasoning": "While government actions can influence markets, a technical support level is created by the organic buying and selling of market participants, not direct intervention."},
                {"text": "Media attention", "reasoning": "Media attention can influence buying or selling, but the support level itself is the price point where the balance of power shifts to buyers, regardless of the reason."}
            ], "correct": 1},
            {"q": "What happens if a stock breaks below support?", "options": [
                {"text": "It becomes new resistance", "reasoning": "Correct! Broken support often turns into resistance on pullbacks."},
                {"text": "It guarantees a reversal", "reasoning": "No guarantee; it can continue falling."},
                {"text": "Trading halts", "reasoning": "Not necessarily; halts are for volatility."},
                {"text": "Volume decreases", "reasoning": "Volume often increases on breaks."},
                {"text": "The stock is delisted", "reasoning": "Delisting is unrelated to support breaks."},
                {"text": "It signals a bull market", "reasoning": "Breaking support is bearish."}
            ], "correct": 0},
            {"q": "Which tool can help identify support levels?", "options": [
                {"text": "Trendlines", "reasoning": "Correct! Trendlines connect lows to show support."},
                {"text": "Moving averages", "reasoning": "Moving averages can act as dynamic support."},
                {"text": "Fibonacci retracements", "reasoning": "Fib levels often coincide with support."},
                {"text": "Volume profiles", "reasoning": "High volume areas can indicate support."},
                {"text": "Pivot points", "reasoning": "Pivots calculate potential support."},
                {"text": "All of the above", "reasoning": "Correct! All these tools help identify support."},
                {"text": "None of the above", "reasoning": "Incorrect; all are useful."}
            ], "correct": 5},
            {"q": "Which statement about support levels is FALSE?", "options": [
                {"text": "They are formed by previous lows", "reasoning": "True."},
                {"text": "They always hold forever", "reasoning": "Correct! Support can break, leading to further declines."},
                {"text": "They attract buyers", "reasoning": "True."},
                {"text": "They can be horizontal or trending", "reasoning": "True."},
                {"text": "Breaking them is bearish", "reasoning": "True."},
                {"text": "They are used for entry points", "reasoning": "True."},
                {"text": "They can turn into resistance", "reasoning": "True."},
                {"text": "They are psychological barriers", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Resistance", "definition": "A price level where a rising stock tends to stop and may reverse downward, caused by a concentration of supply. Resistance levels are formed by previous highs and can be horizontal or trending. Breaking resistance can lead to further gains, while rejection signals weakness. Traders use resistance for exit points or short positions.", "example": "Tesla (TSLA) faced major resistance at the $300 mark throughout 2023 before its breakout, where sellers repeatedly emerged to push the price down. Once broken, $300 became support.", "chart": "TSLA", "concept": "resistance", "quiz": [
            {"q": "Resistance is a price level that acts as a...", "options": [
                {"text": "Floor", "reasoning": "A price floor is known as 'support,' which is the opposite of resistance. Support is where buying pressure stops a price from falling."},
                {"text": "Ceiling", "reasoning": "Correct! Resistance acts as a ceiling where selling pressure (supply) is strong enough to stop a price from rising further."}
            ], "correct": 1},
            {"q": "A breakout occurs when...", "options": [
                {"text": "Price fails to pass resistance", "reasoning": "When a price fails to pass resistance, it is said to be 'rejected' from that level. A breakout is the opposite of this."},
                {"text": "Price moves decisively through resistance on high volume", "reasoning": "Correct! A breakout is a key bullish signal where buyers have absorbed all the selling pressure at the resistance level and are strong enough to push the price higher, confirmed by high volume."},
                {"text": "Price bounces off support", "reasoning": "This is a successful test of a support level, which is a bullish sign, but the specific term for passing resistance is a 'breakout'."},
                {"text": "The RSI is over 70", "reasoning": "An RSI over 70 indicates an 'overbought' condition, which sometimes happens during a breakout, but it is not the definition of the breakout itself."}
            ], "correct": 1},
            {"q": "What happens if a stock breaks above resistance?", "options": [
                {"text": "It becomes new support", "reasoning": "Correct! Broken resistance often turns into support."},
                {"text": "It guarantees a crash", "reasoning": "No guarantee; it can continue rising."},
                {"text": "Volume decreases", "reasoning": "Volume often increases on breaks."},
                {"text": "The stock is relisted", "reasoning": "Unrelated to resistance breaks."},
                {"text": "It signals a bear market", "reasoning": "Breaking resistance is bullish."},
                {"text": "Trading volume surges", "reasoning": "Often true for confirmation."}
            ], "correct": 0},
            {"q": "Which tool can help identify resistance levels?", "options": [
                {"text": "Trendlines", "reasoning": "Correct! Trendlines connect highs to show resistance."},
                {"text": "Moving averages", "reasoning": "Moving averages can act as dynamic resistance."},
                {"text": "Fibonacci extensions", "reasoning": "Fib levels often coincide with resistance."},
                {"text": "Volume profiles", "reasoning": "High volume areas can indicate resistance."},
                {"text": "Pivot points", "reasoning": "Pivots calculate potential resistance."},
                {"text": "All of the above", "reasoning": "Correct! All these tools help identify resistance."},
                {"text": "None of the above", "reasoning": "Incorrect; all are useful."}
            ], "correct": 5},
            {"q": "Which statement about resistance levels is FALSE?", "options": [
                {"text": "They are formed by previous highs", "reasoning": "True."},
                {"text": "They always prevent price rises", "reasoning": "Correct! Resistance can be broken, leading to breakouts."},
                {"text": "They attract sellers", "reasoning": "True."},
                {"text": "They can be horizontal or trending", "reasoning": "True."},
                {"text": "Breaking them is bullish", "reasoning": "True."},
                {"text": "They are used for exit points", "reasoning": "True."},
                {"text": "They can turn into support", "reasoning": "True."},
                {"text": "They are psychological barriers", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Breakout", "definition": "When a stock's price moves decisively above a resistance level or below a support level, often on high volume. Breakouts can signal the start of a new trend and are confirmed by increased volume and follow-through. False breakouts (fakeouts) occur when the price reverses after breaking the level. Traders use breakouts for entry points in the direction of the break.", "example": "Nvidia (NVDA) had a massive breakout past $500 in early 2024, signaling a new uptrend and leading to further gains. The breakout was confirmed by high volume and a close above the level.", "chart": "NVDA", "concept": "breakout", "quiz": [
            {"q": "A breakout is confirmed by...", "options": [
                {"text": "Low volume", "reasoning": "A breakout on low volume is often a red flag, called a 'fakeout.' It suggests there isn't enough conviction behind the move, and it may quickly reverse."},
                {"text": "High volume", "reasoning": "Correct! High volume indicates strong conviction from buyers (in an upward breakout) and confirms that the move is genuine and has momentum."}
            ], "correct": 1},
            {"q": "After a breakout above resistance, what often happens next?", "options": [
                {"text": "The stock is immediately delisted", "reasoning": "Delisting is the removal of a stock from an exchange and is unrelated to technical chart patterns like breakouts."},
                {"text": "The old resistance level becomes a new support level", "reasoning": "Correct! This is a classic technical analysis principle called 'polarity' or 'role reversal.' The old ceiling becomes the new floor, and traders will watch for the price to 'retest' this new support level."},
                {"text": "The price always returns to its pre-breakout level", "reasoning": "While some breakouts fail, a successful one typically signals the start of a new, higher trading range. An immediate return would indicate a 'failed breakout' or 'fakeout'."},
                {"text": "Trading is halted for the day", "reasoning": "Trading halts are regulatory actions usually triggered by extreme volatility or pending major news, not by standard chart patterns like breakouts."}
            ], "correct": 1},
            {"q": "What is a 'fakeout' in the context of breakouts?", "options": [
                {"text": "A successful breakout", "reasoning": "A successful breakout continues in the direction of the break."},
                {"text": "A breakout that reverses quickly", "reasoning": "Correct! A fakeout is a false breakout where the price breaks a level but then reverses, trapping traders."},
                {"text": "Low volume trading", "reasoning": "Low volume is a warning sign, but not the definition of fakeout."},
                {"text": "A sideways market", "reasoning": "Sideways is consolidation, not a breakout."},
                {"text": "A bearish signal", "reasoning": "Fakeouts can be bearish or bullish depending on direction."},
                {"text": "High volatility", "reasoning": "Volatility is present, but not the term."}
            ], "correct": 1},
            {"q": "Which factor confirms a breakout?", "options": [
                {"text": "High volume", "reasoning": "Correct! High volume shows conviction."},
                {"text": "Follow-through buying", "reasoning": "Correct! Continued price movement confirms."},
                {"text": "Close above the level", "reasoning": "Correct! A close above resistance confirms."},
                {"text": "All of the above", "reasoning": "Correct! All are confirmation factors."},
                {"text": "Low volatility", "reasoning": "Breakouts often have high volatility."},
                {"text": "Decreasing price", "reasoning": "That's a breakdown, not breakout."},
                {"text": "Negative news", "reasoning": "Negative news would contradict a bullish breakout."}
            ], "correct": 3},
            {"q": "Which statement about breakouts is FALSE?", "options": [
                {"text": "They signal new trends", "reasoning": "True."},
                {"text": "They require high volume for confirmation", "reasoning": "True."},
                {"text": "They always succeed", "reasoning": "Correct! Many breakouts fail as fakeouts."},
                {"text": "They can be bullish or bearish", "reasoning": "True; up or down."},
                {"text": "They are used for entry points", "reasoning": "True."},
                {"text": "They often follow consolidation", "reasoning": "True."},
                {"text": "They can lead to role reversal", "reasoning": "True."},
                {"text": "They are technical patterns", "reasoning": "True."}
            ], "correct": 2}
        ]},
        {"term": "Volume", "definition": "The number of shares traded during a given period. High volume can confirm the strength of a price move, indicating strong interest. Low volume may suggest weakness or lack of conviction. Volume is a key indicator in technical analysis, often used to confirm trends, breakouts, and reversals. Average daily volume helps gauge liquidity.", "example": "A breakout on high volume is a strong confirmation signal. Low volume suggests a lack of conviction. For example, during the GameStop (GME) squeeze in 2021, volume spiked to billions of shares, confirming the massive price move.", "chart": "AMC", "concept": "volume", "quiz": [
            {"q": "Volume measures the number of...", "options": [
                {"text": "Shares traded", "reasoning": "Correct! Volume specifically refers to the number of shares that change hands, regardless of their price."},
                {"text": "Dollars traded", "reasoning": "The total dollar amount traded is a different metric, sometimes called 'dollar volume.' Standard volume on a chart always refers to the number of shares."}
            ], "correct": 0},
            {"q": "High volume during a price increase is generally considered...", "options": [
                {"text": "Bearish (a bad sign)", "reasoning": "High volume on a price *decrease* would be bearish. But when price and volume rise together, it signals strength."},
                {"text": "Bullish (a good sign)", "reasoning": "Correct! High volume shows that many participants are driving the price up, which confirms the strength and conviction of the uptrend."},
                {"text": "Irrelevant", "reasoning": "Volume is a critical secondary indicator. A price move without confirming volume is often viewed with suspicion by traders."},
                {"text": "A sign of low interest", "reasoning": "High volume is the definition of high interest and high participation in a stock at that moment."}
            ], "correct": 1},
            {"q": "What does low volume during a price move suggest?", "options": [
                {"text": "Strong conviction", "reasoning": "Low volume suggests weak conviction."},
                {"text": "Lack of interest", "reasoning": "Correct! Low volume indicates few participants, suggesting the move may not sustain."},
                {"text": "A guaranteed reversal", "reasoning": "Not guaranteed; it just raises suspicion."},
                {"text": "High liquidity", "reasoning": "Low volume means low liquidity."},
                {"text": "Bullish signal", "reasoning": "Low volume is often a warning."},
                {"text": "Bearish signal", "reasoning": "Depends on context; it's generally weak."}
            ], "correct": 1},
            {"q": "Which scenario is confirmed by high volume?", "options": [
                {"text": "Breakout from resistance", "reasoning": "Correct! High volume confirms breakouts."},
                {"text": "Trend reversal", "reasoning": "High volume can confirm reversals."},
                {"text": "Continuation of trend", "reasoning": "High volume supports trends."},
                {"text": "All of the above", "reasoning": "Correct! High volume confirms various moves."},
                {"text": "Sideways market", "reasoning": "Sideways often have low volume."},
                {"text": "Fakeout", "reasoning": "Fakeouts have low volume."},
                {"text": "Delisting", "reasoning": "Unrelated to volume."}
            ], "correct": 3},
            {"q": "Which statement about volume is FALSE?", "options": [
                {"text": "It measures shares traded", "reasoning": "True."},
                {"text": "High volume always means a bull market", "reasoning": "Correct! High volume can occur in bull or bear moves."},
                {"text": "It confirms price moves", "reasoning": "True."},
                {"text": "Low volume suggests weakness", "reasoning": "True."},
                {"text": "It's used in technical analysis", "reasoning": "True."},
                {"text": "Average daily volume gauges liquidity", "reasoning": "True."},
                {"text": "Spikes can indicate news events", "reasoning": "True."},
                {"text": "It's a key indicator", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Moving Average (MA)", "definition": "The average price of a stock over a specific period (e.g., 50-day, 200-day). Used to identify trend direction and smooth out price fluctuations. There are simple (SMA) and exponential (EMA) moving averages, with EMA giving more weight to recent prices. Crossovers between MAs can signal buy or sell opportunities.", "example": "When the price is above the 50-day MA, the short-term trend is generally considered bullish. For instance, in a strong uptrend, the price stays above the 200-day MA, which acts as dynamic support.", "chart": "AAPL", "concept": "ma", "quiz": [
            {"q": "A moving average is used to...", "options": [
                {"text": "Predict the exact future price", "reasoning": "No indicator can predict the future with certainty. Moving averages are 'lagging' indicators, meaning they are based on past price data."},
                {"text": "Smooth out price data to see the trend", "reasoning": "Correct! By averaging prices over a period, MAs filter out short-term 'noise' and make the underlying trend easier to identify."}
            ], "correct": 1},
            {"q": "A 200-day moving average represents the average price over...", "options": [
                {"text": "The last 200 minutes", "reasoning": "This would be a 200-minute moving average, used by very short-term day traders. A 200-day MA has a much longer-term focus."},
                {"text": "The next 200 days", "reasoning": "Moving averages are based on past data; they cannot use future data that doesn't exist yet."},
                {"text": "The last 200 trading days", "reasoning": "Correct! The 'day' in a moving average refers to trading days. The 200-day MA is a key indicator for the long-term trend."},
                {"text": "The entire history of the stock", "reasoning": "This would be a single, almost static number. A moving average is 'moving' because it always calculates the average of the most recent period (e.g., the last 200 days)."}
            ], "correct": 2},
            {"q": "What is the difference between SMA and EMA?", "options": [
                {"text": "SMA weights all prices equally", "reasoning": "Correct! SMA is simple average; EMA weights recent prices more."},
                {"text": "EMA is lagging", "reasoning": "Both are lagging, but EMA is less so."},
                {"text": "SMA is for short-term only", "reasoning": "SMA can be any period."},
                {"text": "EMA ignores past data", "reasoning": "EMA includes all data but weights recent."},
                {"text": "They are the same", "reasoning": "They are different types."},
                {"text": "SMA is exponential", "reasoning": "No, SMA is simple."}
            ], "correct": 0},
            {"q": "A crossover where a short MA moves above a long MA is called...", "options": [
                {"text": "Golden Cross", "reasoning": "Correct! It's a bullish signal."},
                {"text": "Death Cross", "reasoning": "Death Cross is short below long."},
                {"text": "Bullish reversal", "reasoning": "It's a type of bullish signal."},
                {"text": "Bearish signal", "reasoning": "No, it's bullish."},
                {"text": "Neutral", "reasoning": "It's directional."},
                {"text": "Lagging indicator", "reasoning": "True, but not the name."},
                {"text": "Leading indicator", "reasoning": "It's lagging."}
            ], "correct": 0},
            {"q": "Which statement about moving averages is FALSE?", "options": [
                {"text": "They smooth price data", "reasoning": "True."},
                {"text": "They predict exact prices", "reasoning": "Correct! They are lagging and don't predict precisely."},
                {"text": "They identify trends", "reasoning": "True."},
                {"text": "EMA weights recent prices", "reasoning": "True."},
                {"text": "They can act as support/resistance", "reasoning": "True."},
                {"text": "Crossovers signal changes", "reasoning": "True."},
                {"text": "They are used in technical analysis", "reasoning": "True."},
                {"text": "Longer periods are for long-term trends", "reasoning": "True."}
            ], "correct": 1}
        ]}
    ],
    "🛒 Essential Order Types": [
        {"term": "Market Order", "definition": "An order to buy or sell a stock immediately at the best available current price. It guarantees execution but not the price. Market orders are useful in liquid markets but can lead to slippage in volatile or illiquid stocks. They are the default order type for quick entry or exit.", "example": "Use a market order when you want to get in or out of a stock quickly and are less concerned about the exact price. For example, if news breaks and you want to buy immediately, a market order ensures execution, but you might pay a higher price in a fast-moving market.", "chart": None, "quiz": [
            {"q": "A market order guarantees...", "options": [
                {"text": "The price you want", "reasoning": "This describes a 'limit order.' A market order prioritizes speed, meaning you get whatever price is available at that instant, which might be different from what you saw a second ago."},
                {"text": "That your order will be executed", "reasoning": "Correct! A market order prioritizes speed and execution over price. As long as there are buyers and sellers, your order will be filled almost instantly."}
            ], "correct": 1},
            {"q": "What is the biggest risk of using a market order, especially on a volatile stock?", "options": [
                {"text": "The order might not execute", "reasoning": "The main benefit of a market order is that it almost always executes. The risk lies in the price you get, not in the execution itself."},
                {"text": "The order might take days to fill", "reasoning": "Market orders are designed to be filled almost instantaneously. A limit order might take days to fill, or never fill at all."},
                {"text": "You might get a much worse price than you expected (slippage)", "reasoning": "Correct! 'Slippage' is the difference between the expected price and the price at which the trade is actually executed. In fast-moving or thinly-traded stocks, this can be significant."},
                {"text": "The broker might reject the order", "reasoning": "A broker would only reject a valid market order if you lacked the funds or shares to complete it. The order type itself is standard."}
            ], "correct": 2},
            {"q": "In which situation is a market order most appropriate?", "options": [
                {"text": "When you want a specific price", "reasoning": "Use limit for specific prices."},
                {"text": "When speed is more important than price", "reasoning": "Correct! Market orders prioritize execution."},
                {"text": "In illiquid stocks", "reasoning": "Illiquid stocks have high slippage risk."},
                {"text": "During after-hours trading", "reasoning": "After-hours has lower liquidity."},
                {"text": "For long-term holds", "reasoning": "Price matters more for long-term."},
                {"text": "When volatility is low", "reasoning": "Low volatility reduces slippage, but speed is key."}
            ], "correct": 1},
            {"q": "What is slippage in market orders?", "options": [
                {"text": "The difference between expected and executed price", "reasoning": "Correct! Slippage is the price difference due to market movement."},
                {"text": "A type of order cancellation", "reasoning": "Not cancellation."},
                {"text": "A broker fee", "reasoning": "Fees are separate."},
                {"text": "A guaranteed profit", "reasoning": "No guarantees."},
                {"text": "High volume trading", "reasoning": "Unrelated."},
                {"text": "Low liquidity effect", "reasoning": "Low liquidity causes slippage."},
                {"text": "A bullish signal", "reasoning": "Not a signal."}
            ], "correct": 0},
            {"q": "Which statement about market orders is FALSE?", "options": [
                {"text": "They guarantee execution", "reasoning": "True in liquid markets."},
                {"text": "They guarantee the best price", "reasoning": "Correct! They don't guarantee price, only execution."},
                {"text": "They are for immediate trades", "reasoning": "True."},
                {"text": "They can lead to slippage", "reasoning": "True."},
                {"text": "They are default for quick trades", "reasoning": "True."},
                {"text": "They are useful in volatile markets", "reasoning": "They can be risky in volatility."},
                {"text": "They prioritize speed", "reasoning": "True."},
                {"text": "They are common for retail traders", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Limit Order", "definition": "An order to buy or sell a stock at a specific price or better. A buy limit order can only be executed at the limit price or lower, while a sell limit is at or above. Limit orders provide price control but may not execute if the market doesn't reach the price. They are useful for precise entry/exit and can be day or GTC (good 'til canceled).", "example": "If AAPL is at $175, you can set a buy limit order at $170 to purchase it only if the price drops. This ensures you don't pay more than $170, but if the price never hits $170, the order won't fill, and you might miss the trade.", "chart": None, "quiz": [
            {"q": "A limit order guarantees...", "options": [
                {"text": "The price you want (or better)", "reasoning": "Correct! A limit order prioritizes price over execution. It will only fill at your specified price or a more favorable one."},
                {"text": "That your order will be executed", "reasoning": "This describes a 'market order.' A limit order has no guarantee of execution; if the stock's price never reaches your limit price, your order will not be filled."}
            ], "correct": 0},
            {"q": "What is the biggest risk of using a limit order?", "options": [
                {"text": "You might get a bad price", "reasoning": "The entire purpose of a limit order is to prevent you from getting a bad price. The risk is the opposite of this."},
                {"text": "The order might never be executed if the price doesn't reach your limit", "reasoning": "Correct! If you are trying to buy a stock that is taking off, you might set a limit price that is too low and miss the move entirely as the stock price runs away from your limit."},
                {"text": "It guarantees a loss", "reasoning": "No order type guarantees a loss or a profit. That depends on how the stock performs after you buy it."},
                {"text": "It's more expensive than a market order", "reasoning": "Commissions for market and limit orders are typically identical at modern brokerages."}
            ], "correct": 1},
            {"q": "For a buy limit order, the execution price is...", "options": [
                {"text": "At or below the limit price", "reasoning": "Correct! Buy limits fill at or better (lower) than specified."},
                {"text": "At or above the limit price", "reasoning": "That's for sell limits."},
                {"text": "Exactly the limit price", "reasoning": "It can be better."},
                {"text": "Any price", "reasoning": "No, it's limited."},
                {"text": "During after-hours only", "reasoning": "Unrelated to timing."},
                {"text": "Guaranteed", "reasoning": "Execution is not guaranteed."}
            ], "correct": 0},
            {"q": "When is a limit order most useful?", "options": [
                {"text": "In volatile markets for price control", "reasoning": "Correct! Limits protect against bad fills in volatility."},
                {"text": "For immediate execution", "reasoning": "Use market for immediacy."},
                {"text": "When you don't care about price", "reasoning": "Limits are for price control."},
                {"text": "In illiquid stocks", "reasoning": "Illiquid stocks may not hit the limit."},
                {"text": "For day trading only", "reasoning": "Useful for all timeframes."},
                {"text": "With GTC duration", "reasoning": "GTC is an option, but not the most useful aspect."},
                {"text": "To avoid slippage", "reasoning": "Correct! Limits prevent slippage by setting price bounds."}
            ], "correct": 0},
            {"q": "Which statement about limit orders is FALSE?", "options": [
                {"text": "They provide price control", "reasoning": "True."},
                {"text": "They guarantee execution", "reasoning": "Correct! Execution is not guaranteed if price doesn't reach the limit."},
                {"text": "They can be buy or sell", "reasoning": "True."},
                {"text": "They are useful in volatility", "reasoning": "True."},
                {"text": "They can be GTC", "reasoning": "True."},
                {"text": "They prevent overpaying", "reasoning": "True."},
                {"text": "They are for precise trades", "reasoning": "True."},
                {"text": "They may expire unfilled", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Stop-Loss Order", "definition": "An order placed to sell a security when it reaches a certain price. It is designed to limit an investor's loss on a position. Stop-loss can be market or limit types, and they become active only when the stop price is hit. They are essential for risk management but can be triggered by short-term fluctuations or gaps.", "example": "If you buy a stock at $50, you might place a stop-loss at $45 to automatically sell if it drops 10%, protecting you from further losses. However, if the stock gaps down to $40 overnight, your stop may execute at $40, not $45.", "chart": None, "quiz": [
            {"q": "What is the main purpose of a stop-loss order?", "options": [
                {"text": "To guarantee a profit", "reasoning": "A stop-loss order is a risk management tool for limiting losses, not for locking in profits. An order to lock in profits is called a 'take-profit' or limit sell order."},
                {"text": "To limit potential losses", "reasoning": "Correct! As the name implies, it's a tool for risk management designed to automatically sell your position and stop your losses from getting out of control."}
            ], "correct": 1},
            {"q": "You buy a stock at $100 and set a stop-loss at $90. The stock releases terrible news overnight and opens the next day at $75. At what price will your stop-loss order likely execute?", "options": [
                {"text": "At exactly $90", "reasoning": "This is a critical misunderstanding of how stop-loss orders work. The $90 price is the 'trigger,' not the execution price. Once triggered, it becomes a market order."},
                {"text": "At exactly $100", "reasoning": "$100 was your purchase price. The stop-loss is designed to sell at a lower price to limit your loss."},
                {"text": "Around $75", "reasoning": "Correct! This is a critical risk of stop-loss orders called 'gapping.' The order is triggered when the price hits or passes $90, but it becomes a market order that executes at the next available price. In this case, the first available price is $75."},
                {"text": "The order will be cancelled", "reasoning": "The order will not be cancelled; it will be triggered and executed, just at a much worse price than expected due to the price gap."}
            ], "correct": 2},
            {"q": "What is a risk of stop-loss orders?", "options": [
                {"text": "Gapping through the stop price", "reasoning": "Correct! Gaps can cause execution at worse prices."},
                {"text": "No execution guarantee", "reasoning": "Stops trigger into market orders, which execute."},
                {"text": "High fees", "reasoning": "Fees are standard."},
                {"text": "They only work for buys", "reasoning": "They are for sells to limit losses."},
                {"text": "They expire daily", "reasoning": "They can be GTC."},
                {"text": "They prevent all losses", "reasoning": "They limit, not prevent losses."}
            ], "correct": 0},
            {"q": "A stop-limit order differs from a stop-loss by...", "options": [
                {"text": "Turning into a limit order after trigger", "reasoning": "Correct! Stop-limit specifies a price range after trigger."},
                {"text": "Guaranteeing execution", "reasoning": "Stop-limit may not execute if limit not met."},
                {"text": "Being only for profits", "reasoning": "It's for losses or profits."},
                {"text": "Working in after-hours", "reasoning": "Depends on broker."},
                {"text": "Having no trigger price", "reasoning": "It has a trigger."},
                {"text": "Being more expensive", "reasoning": "Fees are similar."},
                {"text": "Limiting upside", "reasoning": "No, it's for downside protection."}
            ], "correct": 0},
            {"q": "Which statement about stop-loss orders is FALSE?", "options": [
                {"text": "They limit losses", "reasoning": "True."},
                {"text": "They protect against all declines", "reasoning": "Correct! They don't protect against gaps."},
                {"text": "They trigger at a set price", "reasoning": "True."},
                {"text": "They become market orders", "reasoning": "True for standard stops."},
                {"text": "They are for risk management", "reasoning": "True."},
                {"text": "They can be adjusted", "reasoning": "True."},
                {"text": "They are essential for traders", "reasoning": "True for many."},
                {"text": "They can cause sales at lows", "reasoning": "True if triggered by dips."}
            ], "correct": 1}
        ]}
    ],
    "📊 Advanced Charting": [
        {"term": "Golden Cross / Death Cross", "definition": "A chart pattern where a short-term moving average crosses over a long-term moving average. The Golden Cross (short above long) is bullish, signaling potential uptrend. The Death Cross (short below long) is bearish. These are lagging indicators and best used with other confirmation. They are popular in trend-following strategies.", "example": "A Golden Cross (50-day MA crosses above 200-day MA) is a very bullish signal. A Death Cross (50-day MA crosses below 200-day MA) is bearish. For example, the S&P 500 saw a Golden Cross in 2023, preceding a rally.", "chart": "SPY", "concept": "cross", "quiz": [
            {"q": "A 'Golden Cross' is considered a...", "options": [
                {"text": "Bullish signal", "reasoning": "Correct! A Golden Cross, where the faster 50-day MA crosses above the slower 200-day MA, suggests that momentum is shifting to the upside and a long-term uptrend may be starting."},
                {"text": "Bearish signal", "reasoning": "This describes a 'Death Cross,' the opposite of a Golden Cross. A Death Cross is when the 50-day MA crosses below the 200-day MA."}
            ], "correct": 0},
            {"q": "Golden and Death Crosses are considered what type of indicators?", "options": [
                {"text": "Leading indicators (predict future moves)", "reasoning": "Because these crosses rely on moving averages of past prices, they can only confirm a trend that is already underway. They don't predict the future."},
                {"text": "Lagging indicators (confirm past moves)", "reasoning": "Correct! Because they are based on moving averages of past prices, these crosses confirm that a trend has already shifted. They are useful for confirmation, not prediction."},
                {"text": "Coincident indicators (happen at the same time)", "reasoning": "Coincident indicators, like GDP, move in line with the economy. Chart patterns like these lag behind the most recent price action."},
                {"text": "Fundamental indicators (measure company health)", "reasoning": "Fundamental indicators relate to a company's business (like earnings or revenue). These crosses are part of 'technical analysis,' which studies price and volume charts."}
            ], "correct": 1},
            {"q": "A Death Cross typically signals...", "options": [
                {"text": "The start of a bull market", "reasoning": "No, it's bearish."},
                {"text": "A potential downtrend", "reasoning": "Correct! Short MA below long MA is bearish."},
                {"text": "Sideways movement", "reasoning": "It's directional."},
                {"text": "High volatility", "reasoning": "Not specifically."},
                {"text": "Buy opportunity", "reasoning": "It's a sell signal."},
                {"text": "Economic expansion", "reasoning": "Opposite; it's contractionary."}
            ], "correct": 1},
            {"q": "Why are crossovers lagging indicators?", "options": [
                {"text": "They use past data", "reasoning": "Correct! They confirm trends after they start."},
                {"text": "They predict future", "reasoning": "No, they don't predict."},
                {"text": "They are real-time", "reasoning": "They lag price action."},
                {"text": "They ignore volume", "reasoning": "Volume is separate."},
                {"text": "They are fundamental", "reasoning": "They are technical."},
                {"text": "They require confirmation", "reasoning": "True, but not why lagging."},
                {"text": "They are for short-term only", "reasoning": "They can be long-term."}
            ], "correct": 0},
            {"q": "Which statement about Golden/Death Cross is FALSE?", "options": [
                {"text": "Golden Cross is bullish", "reasoning": "True."},
                {"text": "They are always accurate", "reasoning": "Correct! They can give false signals."},
                {"text": "Death Cross is bearish", "reasoning": "True."},
                {"text": "They use moving averages", "reasoning": "True."},
                {"text": "They are lagging", "reasoning": "True."},
                {"text": "They need confirmation", "reasoning": "True."},
                {"text": "They are trend signals", "reasoning": "True."},
                {"text": "They are popular in trading", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Relative Strength Index (RSI)", "definition": "A momentum oscillator that measures the speed and change of price movements on a scale of 0-100. Values over 70 indicate overbought conditions; below 30 indicate oversold. RSI can signal divergences, where price and RSI move oppositely, indicating potential reversals. It's calculated using average gains and losses over a period, typically 14 days.", "example": "Buying a stock when its RSI is below 30 (oversold) can be a profitable strategy, but requires other confirmations. For example, if a stock is making higher highs but RSI is making lower highs, it's a bearish divergence signaling weakness.", "chart": "MSFT", "concept": "rsi", "quiz": [
            {"q": "An RSI reading of 75 suggests a stock is...", "options": [
                {"text": "Oversold", "reasoning": "Oversold conditions are indicated by a low RSI, typically below 30."},
                {"text": "Overbought", "reasoning": "Correct! A reading above 70 indicates that the stock has risen quickly and may be due for a pullback or consolidation. It suggests the buying momentum may be exhausted."}
            ], "correct": 1},
            {"q": "RSI is what kind of indicator?", "options": [
                {"text": "Trend indicator", "reasoning": "While RSI can help gauge the strength of a trend, its primary job isn't to show the trend's direction like a moving average does. Its main purpose is to measure momentum."},
                {"text": "Volatility indicator", "reasoning": "Volatility is better measured by indicators like Bollinger Bands or ATR. RSI measures the magnitude of price changes, not their volatility."},
                {"text": "Momentum indicator", "reasoning": "Correct! RSI is an oscillator that measures the speed and magnitude of recent price changes to evaluate overbought or oversold conditions. This is a direct measure of price momentum."},
                {"text": "Volume indicator", "reasoning": "RSI is calculated purely from price data and does not incorporate volume information at all."}
            ], "correct": 2},
            {"q": "What does a bearish divergence in RSI indicate?", "options": [
                {"text": "Price higher highs, RSI lower highs", "reasoning": "Correct! It suggests weakening momentum despite rising prices."},
                {"text": "Price lower lows, RSI higher lows", "reasoning": "That's bullish divergence."},
                {"text": "Overbought conditions", "reasoning": "Overbought is RSI >70."},
                {"text": "Oversold conditions", "reasoning": "Oversold is RSI <30."},
                {"text": "Strong trend", "reasoning": "Divergence indicates weakening."},
                {"text": "No change", "reasoning": "Divergence signals potential reversal."}
            ], "correct": 0},
            {"q": "The standard period for RSI calculation is...", "options": [
                {"text": "14 days", "reasoning": "Correct! RSI is typically calculated over 14 periods."},
                {"text": "50 days", "reasoning": "That's a moving average period."},
                {"text": "200 days", "reasoning": "Long-term MA."},
                {"text": "1 day", "reasoning": "Too short for meaningful RSI."},
                {"text": "1 year", "reasoning": "Too long; RSI is for momentum."},
                {"text": "Customizable", "reasoning": "True, but standard is 14."},
                {"text": "7 days", "reasoning": "Possible, but not standard."}
            ], "correct": 0},
            {"q": "Which statement about RSI is FALSE?", "options": [
                {"text": "It ranges from 0-100", "reasoning": "True."},
                {"text": "It predicts exact reversals", "reasoning": "Correct! RSI indicates conditions but doesn't predict precisely."},
                {"text": "Over 70 is overbought", "reasoning": "True."},
                {"text": "Under 30 is oversold", "reasoning": "True."},
                {"text": "It measures momentum", "reasoning": "True."},
                {"text": "Divergences signal reversals", "reasoning": "True."},
                {"text": "It's an oscillator", "reasoning": "True."},
                {"text": "It's price-based", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Bollinger Bands", "definition": "Bands placed two standard deviations above and below a simple moving average. They show volatility and potential overbought/oversold conditions. The bands expand in high volatility and contract (squeeze) in low volatility. Touches of the upper band suggest overbought, lower band oversold. Used for volatility breakouts and mean reversion trades.", "example": "When the bands 'squeeze', it often signals a period of low volatility that is a precursor to a large price move. When price touches the upper band, it's considered overbought. For example, during earnings season, bands expand due to volatility spikes.", "chart": "GOOGL", "concept": "bollinger", "quiz": [
            {"q": "Bollinger Bands are primarily used to measure...", "options": [
                {"text": "A company's earnings", "reasoning": "Company earnings are a fundamental metric. Bollinger Bands are a tool of technical analysis and are calculated purely from a stock's price and volatility."},
                {"text": "Market volatility", "reasoning": "Correct! The bands are plotted based on standard deviation, which is a direct measure of volatility. The bands widen when volatility is high and narrow (squeeze) when volatility is low."}
            ], "correct": 1},
            {"q": "When Bollinger Bands 'squeeze' or get very narrow, it often signals...", "options": [
                {"text": "The stock is about to be delisted", "reasoning": "A squeeze is a common technical pattern related to volatility and has no connection to a company's listing status."},
                {"text": "A period of low volatility that may precede a large price move", "reasoning": "Correct! This period of low volatility is often seen as the 'calm before the storm.' A squeeze suggests that energy is building up for a significant breakout or breakdown."},
                {"text": "The market is closing", "reasoning": "The bands reflect volatility over a set period (e.g., 20 days) and are not directly tied to the time of day."},
                {"text": "The stock has become risk-free", "reasoning": "Low volatility means lower price fluctuation at that moment, but it doesn't mean the stock is risk-free. In fact, it can often signal an impending increase in risk and volatility."}
            ], "correct": 1},
            {"q": "Touching the upper Bollinger Band suggests...", "options": [
                {"text": "Overbought conditions", "reasoning": "Correct! Upper band touch indicates potential overbought."},
                {"text": "Oversold conditions", "reasoning": "That's the lower band."},
                {"text": "Breakout", "reasoning": "Breakouts can happen, but touch alone is overbought."},
                {"text": "Squeeze", "reasoning": "Squeeze is narrow bands."},
                {"text": "Mean reversion", "reasoning": "Possible, but indicates extension."},
                {"text": "Strong trend", "reasoning": "In trends, price can hug the band."}
            ], "correct": 0},
            {"q": "The middle line of Bollinger Bands is...", "options": [
                {"text": "A simple moving average", "reasoning": "Correct! Typically a 20-period SMA."},
                {"text": "An exponential MA", "reasoning": "Can be, but standard is SMA."},
                {"text": "The median price", "reasoning": "No, it's an average."},
                {"text": "A trendline", "reasoning": "No, it's a moving average."},
                {"text": "The VWAP", "reasoning": "VWAP is volume-weighted."},
                {"text": "Customizable period", "reasoning": "True, but it's an SMA."},
                {"text": "The zero line", "reasoning": "No, it's price-based."}
            ], "correct": 0},
            {"q": "Which statement about Bollinger Bands is FALSE?", "options": [
                {"text": "They measure volatility", "reasoning": "True."},
                {"text": "They predict exact prices", "reasoning": "Correct! They indicate conditions, not predict prices."},
                {"text": "Squeezes precede moves", "reasoning": "True."},
                {"text": "Upper band is overbought", "reasoning": "True."},
                {"text": "They use standard deviation", "reasoning": "True."},
                {"text": "They expand in volatility", "reasoning": "True."},
                {"text": "They are for mean reversion", "reasoning": "True in some strategies."},
                {"text": "They work with other indicators", "reasoning": "True."}
            ], "correct": 1}
        ]}
    ],
    "🏢 Deeper Fundamental Metrics": [
        {"term": "Market Capitalization (Market Cap)", "definition": "The total market value of a company's outstanding shares (Share Price x Number of Shares). It categorizes companies as large-cap (> $10B), mid-cap ($2B-$10B), small-cap (<$2B), and micro-cap. Market cap reflects investor perception of value and is used for index weighting and investment strategies.", "example": "Companies are categorized by market cap: Large-Cap (>$10B), Mid-Cap ($2B-$10B), and Small-Cap (<$2B). For example, Apple has a market cap over $2 trillion, making it a mega-cap, while a small-cap might be a emerging tech firm with $500M cap.", "chart": "AAPL", "concept": "price", "quiz": [
            {"q": "Market Cap is calculated by multiplying the share price by...", "options": [
                {"text": "The number of employees", "reasoning": "While the number of employees is a business metric, it is not used to calculate the company's market value."},
                {"text": "The number of outstanding shares", "reasoning": "Correct! Market Cap = (Current Share Price) x (Total Number of Outstanding Shares). It represents the total market value of the company."}
            ], "correct": 1},
            {"q": "Which of these factors would NOT directly change a company's market cap?", "options": [
                {"text": "The stock price going up", "reasoning": "This would directly increase the market cap, since Market Cap = Price x Shares."},
                {"text": "The company issuing new shares", "reasoning": "This would directly increase the market cap by increasing the number of shares, assuming the price doesn't drop proportionally."},
                {"text": "The company buying back its own shares", "reasoning": "This would directly decrease the market cap by reducing the number of outstanding shares."},
                {"text": "A 2-for-1 stock split", "reasoning": "Correct! This is the factor that does NOT change the market cap. A 2-for-1 stock split doubles the number of shares but halves the price of each share. The total market cap (Shares x Price) remains the same immediately after the split."}
            ], "correct": 3},
            {"q": "A company with a market cap of $5B is classified as...", "options": [
                {"text": "Large-cap", "reasoning": "Large-cap is >$10B."},
                {"text": "Mid-cap", "reasoning": "Correct! Mid-cap is $2B-$10B."},
                {"text": "Small-cap", "reasoning": "Small-cap is <$2B."},
                {"text": "Mega-cap", "reasoning": "Mega-cap is >$200B."},
                {"text": "Micro-cap", "reasoning": "Micro-cap is <$300M."},
                {"text": "Nano-cap", "reasoning": "Nano-cap is very small, <$50M."}
            ], "correct": 1},
            {"q": "Market cap is used for...", "options": [
                {"text": "Index weighting", "reasoning": "Correct! Many indexes are market-cap weighted."},
                {"text": "Investment categorization", "reasoning": "Correct! For large/mid/small-cap funds."},
                {"text": "Valuation comparison", "reasoning": "Correct! To compare company sizes."},
                {"text": "All of the above", "reasoning": "Correct! All are uses."},
                {"text": "Predicting earnings", "reasoning": "Not directly."},
                {"text": "Setting dividends", "reasoning": "Dividends are based on profits."},
                {"text": "Tax calculations", "reasoning": "Taxes are on gains, not cap."}
            ], "correct": 3},
            {"q": "Which statement about market cap is FALSE?", "options": [
                {"text": "It reflects total value", "reasoning": "True."},
                {"text": "It's unaffected by splits", "reasoning": "True; splits don't change cap."},
                {"text": "It's the same as enterprise value", "reasoning": "Correct! Enterprise value includes debt."},
                {"text": "It's price times shares", "reasoning": "True."},
                {"text": "It categorizes companies", "reasoning": "True."},
                {"text": "It changes with price", "reasoning": "True."},
                {"text": "It's for stocks only", "reasoning": "Can be for crypto too."},
                {"text": "It's a valuation metric", "reasoning": "True."}
            ], "correct": 2}
        ]},
        {"term": "P/E Ratio (Price-to-Earnings)", "definition": "A valuation ratio of a company's current share price compared to its per-share earnings. High P/E suggests growth expectations, low P/E may indicate value or issues. There are trailing (past earnings) and forward (projected) P/E. It's used to compare companies within industries but can be misleading for loss-making firms.", "example": "Growth stocks often have high P/E ratios, while value stocks tend to have lower P/E ratios. For example, a tech company like Amazon might have a P/E of 50+, reflecting high growth expectations, while a utility might have a P/E of 15.", "chart": "NVDA", "concept": "price", "quiz": [
            {"q": "A high P/E ratio often suggests that investors expect...", "options": [
                {"text": "Low future growth", "reasoning": "A low P/E ratio is what typically suggests low growth expectations, as investors are not willing to pay a premium for future earnings."},
                {"text": "High future growth", "reasoning": "Correct! A high P/E means investors are willing to pay a premium for the stock today because they expect earnings to grow significantly in the future, which will eventually make the current price look cheap."}
            ], "correct": 1},
            {"q": "A company with a share price of $100 and earnings per share of $5 has a P/E ratio of...", "options": [
                {"text": "5", "reasoning": "This would be the result of dividing Earnings by Price ($5 / $100). The P/E ratio is Price divided by Earnings."},
                {"text": "20", "reasoning": "Correct! P/E Ratio = (Price per Share) / (Earnings per Share) = $100 / $5 = 20."},
                {"text": "100", "reasoning": "This is the share price, not the P/E ratio."},
                {"text": "500", "reasoning": "This would be the result of multiplying Price by Earnings ($100 * $5). The correct formula is division."}
            ], "correct": 1},
            {"q": "What is a limitation of P/E ratio?", "options": [
                {"text": "Doesn't work for loss-making companies", "reasoning": "Correct! Negative earnings make P/E meaningless."},
                {"text": "Ignores growth", "reasoning": "High P/E reflects growth."},
                {"text": "Only for tech stocks", "reasoning": "Used across industries."},
                {"text": "Always low for value stocks", "reasoning": "Generally true, but not a limitation."},
                {"text": "Includes debt", "reasoning": "P/E is equity-based."},
                {"text": "Not comparable across industries", "reasoning": "Correct! P/E varies by industry."}
            ], "correct": 0},
            {"q": "Forward P/E uses...", "options": [
                {"text": "Projected earnings", "reasoning": "Correct! Forward P/E is based on future estimates."},
                {"text": "Past earnings", "reasoning": "That's trailing P/E."},
                {"text": "Current price only", "reasoning": "No, it includes earnings."},
                {"text": "Average earnings", "reasoning": "Not specifically."},
                {"text": "Adjusted earnings", "reasoning": "Possible, but forward is projected."},
                {"text": "All of the above", "reasoning": "No, specifically projected."},
                {"text": "None of the above", "reasoning": "Incorrect."}
            ], "correct": 0},
            {"q": "Which statement about P/E ratio is FALSE?", "options": [
                {"text": "High P/E indicates growth expectations", "reasoning": "True."},
                {"text": "It's always reliable for all companies", "reasoning": "Correct! Not reliable for losses or cyclical firms."},
                {"text": "Low P/E may indicate value", "reasoning": "True."},
                {"text": "There are trailing and forward types", "reasoning": "True."},
                {"text": "It's price over EPS", "reasoning": "True."},
                {"text": "Used for comparisons", "reasoning": "True."},
                {"text": "Can be misleading", "reasoning": "True."},
                {"text": "Fundamental metric", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Dividend Yield", "definition": "The annual dividend per share divided by the stock's price. It's the return an investor can expect from dividends. Yield decreases as price increases (if dividend stays the same) and is higher for income-focused stocks. It's a key metric for dividend investors but should be considered with payout ratio and sustainability.", "example": "Utility and consumer staples companies like Coca-Cola (KO) are known for their consistent dividend yields. If KO pays $1.76 annually at $60 price, yield is 2.93%. High yields can signal risk if unsustainable.", "chart": "KO", "concept": "price", "quiz": [
            {"q": "If a stock priced at $100 pays an annual dividend of $2 per share, what is its dividend yield?", "options": [
                {"text": "0.5%", "reasoning": "This would be the yield if the dividend were $0.50, not $2.00."},
                {"text": "2%", "reasoning": "Correct! Dividend Yield = (Annual Dividend per Share) / (Price per Share) = $2 / $100 = 0.02, or 2%."},
                {"text": "5%", "reasoning": "This would be the yield if the dividend were $5.00, not $2.00."},
                {"text": "50%", "reasoning": "This would be the result of dividing Price by Dividend ($100 / $2). The correct formula is Dividend divided by Price."}
            ], "correct": 1},
            {"q": "If a company's stock price increases significantly but the dividend payment stays the same, what happens to the dividend yield?", "options": [
                {"text": "It increases", "reasoning": "For the yield to increase, either the dividend would have to go up or the price would have to go down."},
                {"text": "It decreases", "reasoning": "Correct! The yield is (Dividend / Price). If the denominator (Price) goes up while the numerator (Dividend) stays the same, the overall value of the fraction decreases."},
                {"text": "It stays the same", "reasoning": "The yield can only stay the same if the price and dividend both don't change, or if they both change by the exact same percentage."},
                {"text": "The company must increase the dividend", "reasoning": "A company is never obligated to increase its dividend. The yield is simply a reflection of the current dividend and price."}
            ], "correct": 1},
            {"q": "A high dividend yield may indicate...", "options": [
                {"text": "Unsustainable dividends", "reasoning": "Correct! Very high yields can signal risk if payout ratio is high."},
                {"text": "Income-focused stock", "reasoning": "True for stable high-yield stocks."},
                {"text": "Falling stock price", "reasoning": "If price falls and dividend stays, yield rises."},
                {"text": "All of the above", "reasoning": "Correct! High yield can mean various things."},
                {"text": "Growth stock", "reasoning": "Growth stocks have low or no yields."},
                {"text": "Low risk", "reasoning": "High yield often means higher risk."}
            ], "correct": 3},
            {"q": "Dividend yield is calculated as...", "options": [
                {"text": "Annual dividend / price", "reasoning": "Correct! That's the formula."},
                {"text": "Price / annual dividend", "reasoning": "That's the inverse."},
                {"text": "EPS / price", "reasoning": "That's earnings yield."},
                {"text": "Dividend / EPS", "reasoning": "That's payout ratio."},
                {"text": "Total dividends / shares", "reasoning": "That's dividend per share."},
                {"text": "Yield + growth", "reasoning": "That's Gordon model."},
                {"text": "Forward dividend / price", "reasoning": "Possible for forward yield."}
            ], "correct": 0},
            {"q": "Which statement about dividend yield is FALSE?", "options": [
                {"text": "It's for income return", "reasoning": "True."},
                {"text": "High yield always means safe", "reasoning": "Correct! High yield can indicate risk."},
                {"text": "It decreases with rising price", "reasoning": "True."},
                {"text": "It's annual dividend over price", "reasoning": "True."},
                {"text": "Used by dividend investors", "reasoning": "True."},
                {"text": "Consider with payout ratio", "reasoning": "True."},
                {"text": "Higher in utilities", "reasoning": "True."},
                {"text": "Can be trailing or forward", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Free Cash Flow (FCF)", "definition": "The cash a company produces after accounting for cash outflows to support operations and maintain its capital assets. FCF is used for dividends, buybacks, debt reduction, or reinvestment. It's a key measure of financial health and is calculated as operating cash flow minus capital expenditures. Positive FCF indicates a company can self-fund growth.", "example": "Positive and growing FCF is a sign of a very healthy company that can fund its growth, pay dividends, or reduce debt. For example, Microsoft generates billions in FCF annually, allowing it to pay dividends and acquire companies like Activision.", "chart": "MSFT", "concept": "price", "quiz": [
            {"q": "Free Cash Flow is the cash left over after a company pays for...", "options": [
                {"text": "Dividends and stock buybacks", "reasoning": "Dividends and buybacks are *uses* of Free Cash Flow. FCF is the cash available *before* these shareholder returns are made."},
                {"text": "Operating expenses and capital expenditures", "reasoning": "Correct! FCF is the cash generated by the core business (operations) after reinvesting in itself (capital expenditures). It's the 'free' cash available for other things."}
            ], "correct": 1},
            {"q": "Which of the following is the LEAST likely use for a company's Free Cash Flow?", "options": [
                {"text": "Paying dividends", "reasoning": "This is a very common use of FCF, returning cash directly to shareholders."},
                {"text": "Buying back shares", "reasoning": "This is another very common use of FCF, which reduces the share count and increases the value of remaining shares."},
                {"text": "Acquiring other companies", "reasoning": "Using FCF for acquisitions is a common growth strategy."},
                {"text": "Paying employee salaries", "reasoning": "Correct! This is the LEAST likely use. Employee salaries are an operating expense and are paid *before* Free Cash Flow is calculated. FCF is the cash that's left *after* all such operational costs are paid."}
            ], "correct": 3},
            {"q": "How is FCF calculated?", "options": [
                {"text": "Operating cash flow - capex", "reasoning": "Correct! That's the standard formula."},
                {"text": "Net income + depreciation", "reasoning": "That's part of cash flow, but not FCF."},
                {"text": "Revenue - expenses", "reasoning": "That's profit, not cash flow."},
                {"text": "EBITDA - taxes", "reasoning": "Not FCF."},
                {"text": "Cash from investing", "reasoning": "Investing is part of it."},
                {"text": "All cash inflows", "reasoning": "Too broad."}
            ], "correct": 0},
            {"q": "Positive FCF indicates...", "options": [
                {"text": "Ability to self-fund growth", "reasoning": "Correct! Companies with positive FCF don't need external financing."},
                {"text": "High debt levels", "reasoning": "FCF can be used to reduce debt."},
                {"text": "Low profitability", "reasoning": "Positive FCF suggests profitability."},
                {"text": "All of the above", "reasoning": "No, only the first."},
                {"text": "Need for borrowing", "reasoning": "Opposite; positive FCF reduces need."},
                {"text": "Sustainable dividends", "reasoning": "Correct! FCF supports dividends."},
                {"text": "Financial health", "reasoning": "True."}
            ], "correct": 0},
            {"q": "Which statement about FCF is FALSE?", "options": [
                {"text": "It's after capex", "reasoning": "True."},
                {"text": "It's always positive for healthy companies", "reasoning": "Correct! Even healthy companies can have temporary negative FCF."},
                {"text": "Used for buybacks", "reasoning": "True."},
                {"text": "Key for valuation", "reasoning": "True."},
                {"text": "Operating cash - capex", "reasoning": "True."},
                {"text": "Indicates self-funding", "reasoning": "True."},
                {"text": "Better than net income", "reasoning": "True, as it's cash-based."},
                {"text": "Used in DCF models", "reasoning": "True."}
            ], "correct": 1}
        ]}
    ],
    "⛓️ Crypto & Digital Assets": [
        {"term": "Cryptocurrency", "definition": "A digital or virtual currency that uses cryptography for security. It is decentralized and not controlled by any central authority. Cryptocurrencies operate on blockchain technology, enabling peer-to-peer transactions without intermediaries. They can be used for payments, investments, or as utility tokens. Volatility is high due to market speculation and regulatory changes.", "example": "Bitcoin (BTC) is the first and most well-known cryptocurrency. Ethereum (ETH) introduced smart contracts, enabling decentralized applications. For instance, Bitcoin has been used as 'digital gold' for store of value, while ETH powers DeFi platforms.", "chart": "BTC-USD", "concept": "price", "quiz": [
            {"q": "The key feature of cryptocurrencies like Bitcoin is that they are...", "options": [
                {"text": "Controlled by a central bank", "reasoning": "This describes traditional 'fiat' currencies like the US Dollar or the Euro. The entire point of most cryptocurrencies is to exist outside the control of central authorities."},
                {"text": "Decentralized", "reasoning": "Correct! Unlike traditional currencies, cryptocurrencies are not issued or controlled by a single entity like a government or central bank. Their network is maintained by a distributed group of participants."}
            ], "correct": 1},
            {"q": "Which technology underlies most cryptocurrencies?", "options": [
                {"text": "Blockchain", "reasoning": "Correct! Blockchain is the distributed ledger technology."},
                {"text": "Central database", "reasoning": "Cryptos are decentralized."},
                {"text": "Cloud computing", "reasoning": "Not specific to cryptos."},
                {"text": "AI algorithms", "reasoning": "Not the core technology."}
            ], "correct": 0},
            {"q": "What is a common use of cryptocurrencies?", "options": [
                {"text": "Peer-to-peer payments", "reasoning": "Correct! They enable direct transactions."},
                {"text": "Investments", "reasoning": "True, as speculative assets."},
                {"text": "Utility tokens", "reasoning": "True, for platform access."},
                {"text": "All of the above", "reasoning": "Correct! Multiple uses."},
                {"text": "Government reserves", "reasoning": "Governments use fiat."},
                {"text": "Physical goods", "reasoning": "They are digital."}
            ], "correct": 3},
            {"q": "Why are cryptocurrencies volatile?", "options": [
                {"text": "Market speculation", "reasoning": "Correct! Speculation drives price swings."},
                {"text": "Regulatory changes", "reasoning": "True."},
                {"text": "Limited supply", "reasoning": "For some like Bitcoin."},
                {"text": "All of the above", "reasoning": "Correct! Multiple factors."},
                {"text": "Central control", "reasoning": "They lack central control."},
                {"text": "Fixed prices", "reasoning": "Prices are not fixed."},
                {"text": "Low adoption", "reasoning": "Adoption is growing."}
            ], "correct": 3},
            {"q": "Which statement about cryptocurrencies is FALSE?", "options": [
                {"text": "They use cryptography", "reasoning": "True."},
                {"text": "They are always centralized", "reasoning": "Correct! They are decentralized."},
                {"text": "They operate on blockchain", "reasoning": "True."},
                {"text": "They enable P2P transactions", "reasoning": "True."},
                {"text": "They can be volatile", "reasoning": "True."},
                {"text": "They have no intermediaries", "reasoning": "True."},
                {"text": "Bitcoin is the first", "reasoning": "True."},
                {"text": "They are digital assets", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "Blockchain", "definition": "A distributed, immutable digital ledger that records transactions. It's the core technology behind most cryptocurrencies, ensuring transparency and security through consensus mechanisms like proof-of-work or proof-of-stake. Blocks are linked cryptographically, making alterations difficult. Blockchain has applications beyond crypto, like supply chain and voting.", "example": "Each 'block' in the chain contains a number of transactions, and every new block is cryptographically linked to the previous one. For example, Bitcoin's blockchain records all BTC transactions publicly, preventing double-spending.", "chart": None, "quiz": [
            {"q": "A blockchain is best described as a...", "options": [
                {"text": "Digital bank account", "reasoning": "A bank account holds your assets, but the blockchain itself is the underlying ledger that records the movement of those assets between all accounts on the network."},
                {"text": "Distributed digital ledger", "reasoning": "Correct! It's a ledger or database that is shared (distributed) across a network of computers, making it transparent and very difficult to alter."}
            ], "correct": 1},
            {"q": "The term 'immutable' in the context of a blockchain means that data, once written, is...", "options": [
                {"text": "Easy to change", "reasoning": "This is the opposite of immutable. The security of a blockchain comes from the fact that it's extremely difficult to change past records."},
                {"text": "Very difficult or impossible to change", "reasoning": "Correct! Because each block is cryptographically linked to the previous one, changing a transaction in an old block would require re-doing all subsequent blocks, which is computationally infeasible on a large network."},
                {"text": "Private", "reasoning": "While user identities can be pseudonymous, the transactions on most public blockchains (like Bitcoin) are transparent and visible to everyone, not private."},
                {"text": "Temporary", "reasoning": "Data on a blockchain is designed to be permanent. The ledger grows over time but old transactions are not deleted."}
            ], "correct": 1},
            {"q": "What prevents double-spending on blockchain?", "options": [
                {"text": "Consensus mechanisms", "reasoning": "Correct! Mechanisms like proof-of-work ensure validation."},
                {"text": "Central authority", "reasoning": "Blockchain is decentralized."},
                {"text": "Private keys", "reasoning": "Keys secure ownership, but consensus prevents double-spend."},
                {"text": "All of the above", "reasoning": "No, no central authority."},
                {"text": "Government regulation", "reasoning": "Not inherent to blockchain."},
                {"text": "High fees", "reasoning": "Fees deter spam, not double-spending."}
            ], "correct": 0},
            {"q": "A common consensus mechanism is...", "options": [
                {"text": "Proof-of-work", "reasoning": "Correct! Used by Bitcoin, involves mining."},
                {"text": "Proof-of-stake", "reasoning": "Correct! Used by Ethereum, energy-efficient."},
                {"text": "Delegated proof-of-stake", "reasoning": "A variant."},
                {"text": "All of the above", "reasoning": "Correct! Various mechanisms exist."},
                {"text": "Central voting", "reasoning": "Not decentralized."},
                {"text": "Random selection", "reasoning": "Not standard."},
                {"text": "Proof-of-authority", "reasoning": "Used in private chains."}
            ], "correct": 3},
            {"q": "Which statement about blockchain is FALSE?", "options": [
                {"text": "It's distributed", "reasoning": "True."},
                {"text": "It's always public", "reasoning": "Correct! There are private blockchains."},
                {"text": "It's immutable", "reasoning": "True."},
                {"text": "It uses cryptography", "reasoning": "True."},
                {"text": "It records transactions", "reasoning": "True."},
                {"text": "It has non-crypto uses", "reasoning": "True."},
                {"text": "It prevents alterations", "reasoning": "True."},
                {"text": "It enables decentralization", "reasoning": "True."}
            ], "correct": 1}
        ]},
        {"term": "DeFi (Decentralized Finance)", "definition": "An umbrella term for financial services on public blockchains, primarily Ethereum. It aims to build an open-source, permissionless financial system without intermediaries. DeFi includes lending, borrowing, trading, and yield farming, using smart contracts. It offers high yields but comes with risks like smart contract bugs and impermanent loss.", "example": "DeFi platforms allow users to lend, borrow, and trade crypto without traditional intermediaries like banks. For example, on Uniswap, you can swap tokens permissionlessly, or on Aave, lend assets to earn interest.", "chart": "ETH-USD", "concept": "price", "quiz": [
            {"q": "The goal of DeFi is to rebuild traditional financial services without...", "options": [
                {"text": "The internet", "reasoning": "DeFi is built entirely on the internet and public blockchains; it couldn't exist without it."},
                {"text": "Central intermediaries like banks", "reasoning": "Correct! DeFi aims to create a financial system that is open to everyone and doesn't require trusting a central party like a bank or brokerage. Instead, trust is placed in the code (smart contracts)."}
            ], "correct": 1},
            {"q": "The term 'permissionless' in DeFi means...", "options": [
                {"text": "You need government permission to use it", "reasoning": "This is the opposite of permissionless. The 'permissionless' nature of DeFi is often a point of contention with regulators."},
                {"text": "Anyone can access the financial services without needing approval from a central authority", "reasoning": "Correct! Unlike a traditional bank that can deny you service, DeFi protocols are open for anyone with an internet connection and a crypto wallet to use, regardless of their location or status."},
                {"text": "It is not allowed in most countries", "reasoning": "While the regulatory landscape is evolving, being 'permissionless' refers to how the protocol operates, not its legal status in a particular country."},
                {"text": "It is free to use", "reasoning": "While you don't need permission, you do have to pay transaction fees (known as 'gas fees') to the network to use DeFi applications."}
            ], "correct": 1},
            {"q": "What is a common DeFi application?", "options": [
                {"text": "Lending and borrowing", "reasoning": "Correct! Platforms like Aave allow this."},
                {"text": "Decentralized exchanges", "reasoning": "Like Uniswap for trading."},
                {"text": "Yield farming", "reasoning": "Earning rewards by providing liquidity."},
                {"text": "All of the above", "reasoning": "Correct! DeFi offers various services."},
                {"text": "Central banking", "reasoning": "DeFi is decentralized."},
                {"text": "Fiat currency issuance", "reasoning": "DeFi is crypto-based."}
            ], "correct": 3},
            {"q": "A risk of DeFi is...", "options": [
                {"text": "Smart contract bugs", "reasoning": "Correct! Code vulnerabilities can lead to hacks."},
                {"text": "Impermanent loss", "reasoning": "In liquidity pools."},
                {"text": "High gas fees", "reasoning": "Transaction costs."},
                {"text": "All of the above", "reasoning": "Correct! Multiple risks."},
                {"text": "Central control", "reasoning": "DeFi lacks central control."},
                {"text": "Low yields", "reasoning": "Yields can be high."},
                {"text": "Government bans", "reasoning": "Regulatory risk, but not inherent."}
            ], "correct": 3},
            {"q": "Which statement about DeFi is FALSE?", "options": [
                {"text": "It's on public blockchains", "reasoning": "True."},
                {"text": "It's completely risk-free", "reasoning": "Correct! DeFi has high risks like hacks and volatility."},
                {"text": "It uses smart contracts", "reasoning": "True."},
                {"text": "It's permissionless", "reasoning": "True."},
                {"text": "It aims to replace banks", "reasoning": "True in some aspects."},
                {"text": "It offers high yields", "reasoning": "True, but risky."},
                {"text": "It's primarily on Ethereum", "reasoning": "True."},
                {"text": "It includes trading", "reasoning": "True."}
            ], "correct": 1}
        ]}
    ]
}

# Corrected and cleaned up FUN_FACTS list
FUN_FACTS = [
    {"fact": "If you invested $1,000 in Apple (AAPL) at its IPO in 1980, you'd have over $1.7 million today, accounting for stock splits.", "symbol": "AAPL", "start": "1980-12-12"},
    {"fact": "Nvidia (NVDA) stock has returned over 25,000% in the last 10 years, turning a $1,000 investment into over $250,000.", "symbol": "NVDA", "start": "2014-01-01"},
    {"fact": "Amazon (AMZN) lost over 90% of its value after the dot-com bubble burst. A $10,000 investment would have dropped to under $1,000 before its legendary recovery.", "symbol": "AMZN", "start": "1999-12-10"},
    {"fact": "In 2010, someone famously bought two pizzas for 10,000 Bitcoin. At its peak, that Bitcoin was worth over $600 million.", "symbol": "BTC-USD", "start": "2010-05-22"},
    {"fact": "The term 'blue chip' comes from poker, where the blue chips are traditionally the highest value chips.", "symbol": "JNJ", "start": "2020-01-01"},
]

FUNDS = [
    {"name": "S&P 500 Index Fund (e.g., VOO, SPY)", "type": "Index ETF", "avg_return": "~10% annually", "description": "Tracks the 500 largest U.S. companies. The bedrock of many portfolios, offering broad market exposure and diversification.", "symbol": "VOO"},
    {"name": "Nasdaq 100 Index Fund (e.g., QQQ)", "type": "Index ETF", "avg_return": "~13% annually (higher volatility)", "description": "Tracks the 100 largest non-financial companies on the Nasdaq. Heavily weighted towards technology and growth.", "symbol": "QQQ"},
    {"name": "Vanguard Total Stock Market ETF (VTI)", "type": "Index ETF", "avg_return": "~9.8% annually", "description": "Own a piece of the entire U.S. stock market (over 3,000 stocks), including large, mid, and small-cap companies.", "symbol": "VTI"},
    {"name": "ARK Innovation ETF (ARKK)", "type": "Actively Managed ETF", "avg_return": "Highly volatile", "description": "Invests in companies poised to benefit from 'disruptive innovation' like AI, robotics, and genomics. High risk, high potential reward.", "symbol": "ARKK"},
    {"name": "Schwab U.S. Dividend Equity ETF (SCHD)", "type": "Dividend ETF", "avg_return": "~12% annually (with dividends)", "description": "Focuses on high-quality, dividend-paying U.S. stocks with a track record of financial strength.", "symbol": "SCHD"},
]

BADGES = [
    {"name": "Wall Street Rookie", "desc": "Completed your first learning module!", "icon": "🔰"},
    {"name": "Chart Master", "desc": "Analyzed 10 interactive charts.", "icon": "📊"},
    {"name": "Fact Finder", "desc": "Discovered 5 mind-blowing market facts.", "icon": "💡"},
    {"name": "Fund Explorer", "desc": "Explored the world of ETFs and Funds.", "icon": "🧭"},
    {"name": "Market Analyst", "desc": "Used the Stock Analyzer tool 5 times.", "icon": "🕵️"},
    {"name": "Portfolio Visionary", "desc": "Calculated 5 'What If' scenarios.", "icon": "💸"},
    {"name": "Knowledge Titan", "desc": "Completed all learning modules!", "icon": "🧠"},
    {"name": "Trading Legend", "desc": "Earned all available badges!", "icon": "👑"},
]

# --- Session State Initialization ---
def init_session_state():
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
    # NEW: Track answered quiz questions (module -> set of (card_index, level))
    if 'module_questions_answered' not in st.session_state:
        st.session_state.module_questions_answered = {module: set() for module in VOCAB.keys()}
    # NEW: Initialize page state for custom navigation
    if 'page' not in st.session_state:
        st.session_state.page = "🏠 Home"

init_session_state()

# --- Helper & Charting Functions ---

@st.cache_data(ttl=600)
def get_stock_data(symbol, period="3y"):
    try:
        return yf.Ticker(symbol).history(period=period, auto_adjust=True)
    except Exception:
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def get_full_history(symbol):
    """Gets the entire price history for a stock to find its first trading day."""
    try:
        return yf.Ticker(symbol).history(period="max", auto_adjust=True)
    except Exception:
        return pd.DataFrame()

def check_and_award_badges():
    """Checks progress and awards badges."""
    if any(v > 0 for v in st.session_state.module_progress.values()):
        st.session_state.badges.add("Wall Street Rookie")
    if st.session_state.charts_viewed >= 10:
        st.session_state.badges.add("Chart Master")
    if st.session_state.facts_read >= 5:
        st.session_state.badges.add("Fact Finder")
    if 'fund_page_visited' in st.session_state and st.session_state.fund_page_visited:
        st.session_state.badges.add("Fund Explorer")
    if st.session_state.analyzer_uses >= 5:
        st.session_state.badges.add("Market Analyst")
    if st.session_state.what_if_uses >= 5:
        st.session_state.badges.add("Portfolio Visionary")

    all_modules_completed = all(st.session_state.module_progress[m] >= len(VOCAB[m]) for m in VOCAB)
    if all_modules_completed:
        st.session_state.badges.add("Knowledge Titan")

    if len(st.session_state.badges) >= len(BADGES) - 1:
        st.session_state.badges.add("Trading Legend")

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
        fig_simple = go.Figure()
        fig_simple.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name='Price', line=dict(color='#00A693', width=2)))

        if concept in ['support', 'resistance', 'breakout']:
            level = data['Close'][-200:].median() if concept == 'support' else data['Close'][-200:].quantile(0.75)
            fig_simple.add_hline(y=level, line_width=2, line_dash="dash", line_color="red" if concept != 'support' else 'lime',
                                 annotation_text=concept.title(), annotation_position="bottom right")
            st.info(f"This simplified chart highlights a key price level. Notice how the price interacts with the {concept} line.")
        elif concept == 'ma':
            data['MA50'] = data['Close'].rolling(window=50).mean()
            fig_simple.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='50-Day MA', line=dict(color='orange', width=1.5)))
            st.info("The orange line is the 50-day moving average. It smooths out price action to show the trend more clearly.")
        elif concept == 'cross':
            data['MA50'] = data['Close'].rolling(window=50).mean()
            data['MA200'] = data['Close'].rolling(window=200).mean()
            fig_simple.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='50-Day MA', line=dict(color='orange', width=1.5)))
            fig_simple.add_trace(go.Scatter(x=data.index, y=data['MA200'], mode='lines', name='200-Day MA', line=dict(color='purple', width=1.5)))
            st.info("This chart shows the 50-day (orange) and 200-day (purple) moving averages. A 'Golden Cross' (orange over purple) is bullish.")

        fig_simple.update_layout(title=f"Simplified View: {symbol}", template="plotly_dark", height=400)
        st.plotly_chart(fig_simple, use_container_width=True)

    with analytical_tab:
        st.markdown("**Real-World Chart with Technical Indicators**")
        fig_analytical = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05,
                                       subplot_titles=(f'{symbol.upper()} Price Action', 'Volume'), row_heights=[0.7, 0.3])
        fig_analytical.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'), row=1, col=1)
        fig_analytical.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume', marker_color='rgba(0, 166, 147, 0.5)'), row=2, col=1)
    
        data['MA50'] = data['Close'].rolling(window=50).mean()
        data['MA200'] = data['Close'].rolling(window=200).mean()
        fig_analytical.add_trace(go.Scatter(x=data.index, y=data['MA50'], mode='lines', name='50-Day MA', line=dict(color='orange', width=1)), row=1, col=1)
        fig_analytical.add_trace(go.Scatter(x=data.index, y=data['MA200'], mode='lines', name='200-Day MA', line=dict(color='purple', width=1)), row=1, col=1)

        fig_analytical.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False, legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_analytical, use_container_width=True)

# --- Safe last price helper for robust analyzer fallback ---
def safe_last_close(symbol: str):
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

# --- UI Pages ---

def page_home():
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

    # --- New Interactive Shield Mastery Visualization ---
    st.subheader("🛡️ Module Mastery Shields")
    st.markdown("Visualize your mastery for each learning module. Each shield fills from the bottom up as you complete concepts.")

    modules = list(VOCAB.keys())
    cols_per_row = 3
    rows = [modules[i:i+cols_per_row] for i in range(0, len(modules), cols_per_row)]

    for row in rows:
        cols = st.columns(len(row))
        for i, module_name in enumerate(row):
            with cols[i]:
                prog = st.session_state.module_progress.get(module_name, 0)
                total = len(VOCAB.get(module_name, [])) or 1
                pct = int((prog / total) * 100)

                # sanitize id for SVG clipPaths
                safe_id = ''.join(ch for ch in module_name if ch.isalnum()) or 'mod'

                svg_height = 115
                fill_h = int((pct / 100.0) * svg_height)
                rect_y = svg_height - fill_h

                # Determine total questions for the module and answered count
                total_questions = sum(len(card.get('quiz', [])) for card in VOCAB.get(module_name, [])) or 0
                answered_questions = len(st.session_state.module_questions_answered.get(module_name, set())) if 'module_questions_answered' in st.session_state else 0

                # Determine shield level and color
                if total_questions > 0:
                    if answered_questions >= total_questions:
                        shield_level = 3
                        shield_color = "#FFD700"  # gold
                        level_text = "Level 3 (Max)"
                    elif answered_questions > (total_questions / 2):
                        shield_level = 2
                        shield_color = "#D9382C"  # red
                        level_text = "Level 2"
                    else:
                        shield_level = 1
                        shield_color = "#00A693"  # default green
                        level_text = "Level 1"
                else:
                    shield_level = 1
                    shield_color = "#00A693"
                    level_text = "Level 1"

                svg = f'''<div style="text-align:center">
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
                  <text x="50" y="64" text-anchor="middle" fill="#FAFAFA" font-size="16" font-weight="600">{pct}%</text>
                </svg>
                </div>'''

                st.markdown(svg, unsafe_allow_html=True)
                st.markdown(f"**{module_name}** — {pct}% mastered ({prog}/{total} concepts)  <br><small style='color:#BDBDBD'>{level_text}</small>", unsafe_allow_html=True)

                # Expandable details for the shield
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

    st.markdown("---")

    st.subheader("🏅 Recently Earned Badges")
    if not st.session_state.badges:
        st.info("Start learning in the 'Learning Modules' to earn your first badge!")
    else:
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

# --- NEW QUIZ FUNCTIONS ---
def display_quiz(card, module_name, card_index):
    """Handles the display and logic of a single quiz question."""
    quiz_info = st.session_state.active_quiz
    level = quiz_info['level']
    quiz_data = card['quiz'][level - 1]

    st.subheader(f"📝 Test Your Knowledge: Level {level}")
    st.markdown(f"#### {quiz_data['q']}")
    st.write("") # Add some space

    # Determine number of columns based on number of options for a clean layout
    num_options = len(quiz_data['options'])
    cols = st.columns(2 if num_options > 2 else num_options)

    for i, option in enumerate(quiz_data['options']):
        with cols[i % 2]:
            # When a button is clicked, update the state and rerun
            if st.button(option['text'], key=f"quiz_{module_name}_{card_index}_{level}_{i}", use_container_width=True):
                st.session_state.active_quiz['user_answer'] = i
                if i == quiz_data['correct']:
                    st.session_state.active_quiz['status'] = 'passed'
                    # Record that this (card, level) question was answered correctly for this module
                    try:
                        st.session_state.module_questions_answered[module_name].add((card_index, level))
                    except Exception:
                        # Fallback in case the session state wasn't initialized as expected
                        st.session_state.module_questions_answered[module_name] = {(card_index, level)}
                else:
                    st.session_state.active_quiz['status'] = 'failed'
                st.rerun()

def page_learning_modules():
    st.title("📚 Learning Modules")
    st.sidebar.title("Modules")

    # Use a custom key for the module selector to avoid conflicts
    current_selection = st.sidebar.radio("Select a learning module:", list(VOCAB.keys()), key="module_selector_radio", label_visibility="collapsed")
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
        quiz_status = st.session_state.active_quiz.get('status')
        quiz_level = st.session_state.active_quiz['level']
        quiz_data = card['quiz'][quiz_level - 1]

        # State 1: Quiz is waiting for an answer
        if quiz_status == 'pending':
            display_quiz(card, module_name, card_index)

        # State 2: Quiz was answered correctly, show feedback and next steps
        elif quiz_status == 'passed':
            correct_index = quiz_data['correct']
            st.success(f"### Correct! 🎉")
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

        # State 3: Quiz was answered incorrectly, show feedback and try again
        elif quiz_status == 'failed':
            user_answer_index = st.session_state.active_quiz['user_answer']
            st.error("### Not quite...")
            st.warning(f"**Here's a common point of confusion:** {quiz_data['options'][user_answer_index]['reasoning']}")
        
            st.markdown("---")
            if st.button("Try Again", use_container_width=True, type="primary"):
                st.session_state.active_quiz['status'] = 'pending'
                st.session_state.active_quiz.pop('user_answer', None)
                st.rerun()

    # Default view: Show the flashcard content
    else:
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

        # Show "Test My Understanding" button if not yet completed, or "Review Quiz" if completed
        if card_index >= st.session_state.module_progress.get(module_name, 0):
            if st.button("Test My Understanding", key=f"test_{card_index}", type="primary", use_container_width=True):
                st.session_state.active_quiz = {'module': module_name, 'card_index': card_index, 'level': 1, 'status': 'pending'}
                st.rerun()
        else:
            st.success("✅ You've mastered this topic. Feel free to review or move on.")
            # PATCH START: quick review
            with st.expander("Quick Review (Key Points)"):
                st.markdown(f"- Term: {card['term']}")
                st.markdown(f"- Definition (one-liner): {card['definition'][:180]}{'...' if len(card['definition'])>180 else ''}")
                if card.get("example"):
                    st.markdown(f"- Example: {card['example'][:180]}{'...' if len(card['example'])>180 else ''}")
            # PATCH END
            if st.button("Review Quiz", key=f"review_{card_index}", use_container_width=True):
                st.session_state.active_quiz = {'module': module_name, 'card_index': card_index, 'level': 1, 'status': 'pending'}
                st.rerun()

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
            if card_index < st.session_state.module_progress.get(module_name, 0) and card_index < len(module_vocab) - 1:
                if st.button("Next →"):
                    st.session_state.card_indices[module_name] += 1
                    st.session_state.active_quiz = None
                    st.rerun()

def page_stock_analyzer():
    st.title("🕵️ Stock Analyzer")
    st.markdown("Get a complete snapshot of any stock or crypto. View charts, key data, and news all in one place.")

    symbol = st.text_input("Enter a US Stock or Crypto Symbol (e.g., AAPL, TSLA, BTC-USD)", value="AAPL").upper()

    if st.button("Analyze"):
        st.session_state.analyzer_uses += 1
        check_and_award_badges()
    
        ticker = yf.Ticker(symbol)
        try:
            info = ticker.info
        except Exception:
            info = {}
        # Fallback when info missing/crypto
        price = None
        try:
            price = info.get('regularMarketPrice')
        except Exception:
            pass
        if price is None:
            price = safe_last_close(symbol)
        if not price:
            st.error(f"Could not find data for '{symbol}'. Please enter a valid symbol.")
            return

        st.header(f"{info.get('longName', symbol) or symbol} ({symbol})")
        prev_close = info.get('previousClose')
        if prev_close is None:
            try:
                d2 = yf.download(symbol, period="2d", interval="1d", progress=False, auto_adjust=True)
                prev_close = float(d2["Close"].dropna().iloc[-2]) if len(d2["Close"].dropna()) >= 2 else price
            except Exception:
                prev_close = price
        change = price - prev_close if prev_close else 0
        change_pct = (change / prev_close) * 100 if prev_close else 0

        cols = st.columns(3)
        cols[0].metric("Current Price", f"${price:,.2f}", f"{change:,.2f} ({change_pct:.2f}%)")
        cols[1].metric("Market Cap", f"${info.get('marketCap', 0):,}" if info.get('marketCap') else "N/A")
        pe_ratio = info.get('trailingPE')
        cols[2].metric("P/E Ratio", f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A")

        st.subheader("Interactive Chart")
        show_dual_charts(symbol, 'price')

        cols = st.columns(2)
        with cols[0]:
            st.subheader("Company Profile")
            st.markdown(f"**Sector:** {info.get('sector', 'N/A')}")
            st.markdown(f"**Industry:** {info.get('industry', 'N/A')}")
            st.markdown(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', 'N/A')})")
            with st.expander("Business Summary"):
                st.write(info.get('longBusinessSummary', 'No summary available.'))

        with cols[1]:
            st.subheader("Recent News")
            try:
                news = ticker.news
                if not news:
                    st.write("No recent news found.")
                for item in news[:5]:
                    title = item.get('title', 'No Title')
                    link = item.get('link', '#')
                    publisher = item.get('publisher', 'No Publisher')
                    st.markdown(f"**[{title}]({link})** - *{publisher}*")
            except Exception as e:
                st.warning(f"Could not retrieve news. Error: {e}")

def page_what_if_calculator():
    st.title("💸 The 'What If' Time Machine")
    st.markdown("Ever wonder how much you'd have if you invested in a company years ago? Let's find out!")

    fact = random.choice(FUN_FACTS)
    if st.button("Try this fun fact!"):
        st.session_state.what_if_symbol = fact['symbol']
        st.session_state.what_if_start_date = datetime.datetime.strptime(fact['start'], "%Y-%m-%d").date()
        st.session_state.what_if_amount = 1000
        st.rerun()
    st.info(f"💡 **Fun Fact:** {fact['fact']}")

    # Get the symbol from session state to pre-fetch data for validation
    symbol_for_validation = st.session_state.what_if_symbol.upper()
    history_data = get_full_history(symbol_for_validation)

    first_trading_day = None
    last_trading_day = None

    if not history_data.empty:
        first_trading_day = history_data.index[0].date()
        last_trading_day = history_data.index[-1].date()

    with st.form(key='what_if_form'):
        cols = st.columns([2, 1, 1])
        symbol = cols[0].text_input("Stock/Crypto Symbol", value=st.session_state.what_if_symbol).upper()
    
        # Use the dynamic dates for the date picker
        start_date = cols[1].date_input(
            "Investment Date", 
            value=st.session_state.what_if_start_date,
            min_value=first_trading_day,
            max_value=last_trading_day
        )
        amount = cols[2].number_input("Investment Amount ($)", min_value=1, value=st.session_state.what_if_amount)
        submit_button = st.form_submit_button(label='Calculate My Fortune!')

    if submit_button:
        st.session_state.what_if_symbol = symbol
        st.session_state.what_if_start_date = start_date
        st.session_state.what_if_amount = amount
        st.session_state.what_if_uses += 1
        check_and_award_badges()
    
        # Re-check history in case the symbol was changed inside the form
        if symbol != symbol_for_validation:
            history_data = get_full_history(symbol)
            if not history_data.empty:
                first_trading_day = history_data.index[0].date()
    
        if history_data.empty:
            st.error(f"Invalid symbol '{symbol}'. Please enter a valid stock or crypto symbol.")
            return
    
        # Final validation check before running the calculation
        if start_date < first_trading_day:
            st.error(f"Error: This stock did not exist on the selected date. Please pick a date after {first_trading_day.strftime('%Y-%m-%d')}.")
            return

        end_date = datetime.date.today()
        try:
            data = yf.download(symbol, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'), progress=False)
            if data.empty:
                st.error(f"No data found for '{symbol}' in the specified date range. It may not have been trading yet.")
                return
        
            start_price = float(data.iloc[0]['Close'])
            end_price = float(data.iloc[-1]['Close'])
            amount_float = float(amount)
        
            shares = amount_float / start_price
            final_value = shares * end_price
        
            st.success(f"An investment of **${amount_float:,.2f}** in **{symbol}** on **{start_date}** would be worth...")
            st.header(f"💰 **${final_value:,.2f}** today!")
        
            roi = ((final_value - amount_float) / amount_float) * 100
            st.metric("Total Return on Investment", f"{roi:,.2f}%")

            data['Investment Value'] = (shares * data['Close'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data.index, y=data['Investment Value'], mode='lines', name='Investment Growth', fill='tozeroy', line_color='#00A693'))
            fig.update_layout(title=f'Growth of ${amount_float:,.2f} in {symbol}', yaxis_title='Value (USD)', template='plotly_dark')
            st.plotly_chart(fig, use_container_width=True)
            st.session_state.charts_viewed += 1

        except Exception as e:
            st.error(f"An error occurred. Please check the symbol and date. Error: {e}")

def page_funds_explorer():
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
    st.title("🏅 Your Achievements")
    st.markdown("Track your progress and celebrate your learning milestones!")
    check_and_award_badges()

    if not st.session_state.badges:
        st.info("No badges yet. Complete learning modules and use the app's tools to start earning them!")
        return

    st.subheader("Earned Badges")
    earned_badges = [b for b in BADGES if b['name'] in st.session_state.badges]
    num_columns = min(len(earned_badges), 4)
    cols = st.columns(num_columns or 1)
    for i, badge in enumerate(earned_badges):
        with cols[i % num_columns]:
            st.markdown(f"""
            <div class="badge">
                <h4>{badge['icon']} {badge['name']}</h4>
                <p>{badge['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Badges to Unlock")
    unlocked_badges = [b for b in BADGES if b['name'] not in st.session_state.badges]
    if not unlocked_badges:
        st.success("👑 You are a Trading Legend! You've collected all the badges!")
    else:
        for badge in unlocked_badges:
            st.write(f"**{badge['icon']} {badge['name']}:** *{badge['desc']}*")

# --- Main App Logic & Sidebar Navigation (MODERNIZED) ---

# Define pages and their corresponding functions in a dictionary
PAGES = {
    "🏠 Home": page_home,
    "📚 Learning Modules": page_learning_modules,
    "🕵️ Stock Analyzer": page_stock_analyzer,
    "💸 'What If' Calculator": page_what_if_calculator,
    "🧭 Funds Explorer": page_funds_explorer,
    "🏅 Achievements": page_achievements
}

st.sidebar.title("Wall Street 101")
st.sidebar.markdown("---")

# Display custom navigation menu
for page_name in PAGES.keys():
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

st.sidebar.markdown("---")
st.sidebar.info("This is an educational tool. All data is for informational purposes only. Not financial advice.")

# PATCH START: learner reset
if st.sidebar.button("Reset Session State"):
    keys = list(st.session_state.keys())
    for k in keys:
        del st.session_state[k]
    st.experimental_rerun()
# PATCH END

# Call the function for the selected page to display its content
PAGES[st.session_state.page]()

