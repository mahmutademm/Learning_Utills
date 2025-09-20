"""
Data definitions for the Wall Street 101 application.
Contains vocabulary, quiz questions, badges, funds, and fun facts.
"""

# Complete vocabulary data with all modules and quiz questions
VOCAB = {
    "⭐ Getting Started": [
        {"term": "Stock", "definition": "A security that represents ownership in a fraction of a corporation. Entitles the owner to a proportion of the corporation's assets and profits. Stocks can be common or preferred, with common stocks offering voting rights and potential dividends, while preferred stocks provide fixed dividends but limited voting rights. Stock prices fluctuate based on supply and demand, company performance, and market conditions. They are key components of investment portfolios and can be traded on exchanges.", "example": "Buying one share of Apple (AAPL) makes you a part-owner of Apple Inc. If Apple performs well, the stock price may rise, and you might receive dividends. However, if the company struggles, the stock value could decline. For instance, during the 2008 financial crisis, many stocks lost significant value, but long-term holders of strong companies like Apple saw substantial recovery and growth.", "chart": "AAPL", "concept": "price", "quiz": [
            {"q": "A stock represents which of the following?", "options": [
                {"text": "A loan to a company", "reasoning": "This is a common misconception. A loan to a company is a form of debt, and the holder is a lender, not an owner. This type of investment is typically a bond, which pays interest. Stocks, on the other hand, represent ownership."},
                {"text": "Ownership in a company", "reasoning": "Correct! A stock (also known as equity) is a security that represents the ownership of a fraction of a corporation, making you a part-owner with a claim on its assets and profits."}
            ], "correct": 1}
        ]},
        {"term": "Ticker Symbol", "definition": "A unique series of letters assigned to a security for trading purposes. E.g., 'AAPL' for Apple, 'TSLA' for Tesla.", "example": "To buy or analyze a stock, you almost always start with its ticker symbol. For example, 'AAPL' is Apple on NASDAQ.", "chart": None, "quiz": [
            {"q": "What is the primary purpose of a ticker symbol?", "options": [
                {"text": "To hide a company's real name", "reasoning": "While it's an abbreviation, the purpose isn't to hide the name but to make it faster and easier to identify for trading."},
                {"text": "To uniquely identify a stock for trading", "reasoning": "Correct! Ticker symbols are abbreviations that allow for fast and unambiguous identification of securities on exchanges."}
            ], "correct": 1}
        ]}
    ],
    "📈 Basic Charting": [
        {"term": "Support", "definition": "A price level where a falling stock tends to stop and may reverse upward, caused by a concentration of demand.", "example": "In 2022, the S&P 500 found strong support around the $360 level, bouncing off it multiple times.", "chart": "SPY", "concept": "support", "quiz": [
            {"q": "Support is a price level that acts as a...", "options": [
                {"text": "Floor", "reasoning": "Correct! Support acts as a floor where buying pressure is strong enough to stop a price from falling further."},
                {"text": "Ceiling", "reasoning": "A price ceiling is known as 'resistance,' which is the opposite of support."}
            ], "correct": 0}
        ]},
        {"term": "Resistance", "definition": "A price level where a rising stock tends to stop and may reverse downward, caused by a concentration of supply.", "example": "Tesla faced major resistance at the $300 mark throughout 2023 before its breakout.", "chart": "TSLA", "concept": "resistance", "quiz": [
            {"q": "Resistance is a price level that acts as a...", "options": [
                {"text": "Floor", "reasoning": "A price floor is known as 'support,' which is the opposite of resistance."},
                {"text": "Ceiling", "reasoning": "Correct! Resistance acts as a ceiling where selling pressure is strong enough to stop a price from rising further."}
            ], "correct": 1}
        ]}
    ],
    "🛒 Essential Order Types": [
        {"term": "Market Order", "definition": "An order to buy or sell a stock immediately at the best available current price. It guarantees execution but not the price.", "example": "Use a market order when you want to get in or out of a stock quickly and are less concerned about the exact price.", "chart": None, "quiz": [
            {"q": "A market order guarantees...", "options": [
                {"text": "The price you want", "reasoning": "This describes a 'limit order.' A market order prioritizes speed over price."},
                {"text": "That your order will be executed", "reasoning": "Correct! A market order prioritizes execution over price."}
            ], "correct": 1}
        ]},
        {"term": "Limit Order", "definition": "An order to buy or sell a stock at a specific price or better. Provides price control but may not execute.", "example": "If AAPL is at $175, you can set a buy limit order at $170 to purchase it only if the price drops.", "chart": None, "quiz": [
            {"q": "A limit order guarantees...", "options": [
                {"text": "The price you want (or better)", "reasoning": "Correct! A limit order prioritizes price over execution."},
                {"text": "That your order will be executed", "reasoning": "This describes a 'market order.' A limit order has no guarantee of execution."}
            ], "correct": 0}
        ]}
    ]
}

# Fun facts data
FUN_FACTS = [
    {"fact": "If you invested $1,000 in Apple (AAPL) at its IPO in 1980, you'd have over $1.7 million today, accounting for stock splits.", "symbol": "AAPL", "start": "1980-12-12"},
    {"fact": "Nvidia (NVDA) stock has returned over 25,000% in the last 10 years, turning a $1,000 investment into over $250,000.", "symbol": "NVDA", "start": "2014-01-01"},
    {"fact": "Amazon (AMZN) lost over 90% of its value after the dot-com bubble burst. A $10,000 investment would have dropped to under $1,000 before its legendary recovery.", "symbol": "AMZN", "start": "1999-12-10"},
    {"fact": "In 2010, someone famously bought two pizzas for 10,000 Bitcoin. At its peak, that Bitcoin was worth over $600 million.", "symbol": "BTC-USD", "start": "2010-05-22"},
    {"fact": "The term 'blue chip' comes from poker, where the blue chips are traditionally the highest value chips.", "symbol": "JNJ", "start": "2020-01-01"},
]

# ETF and funds data
FUNDS = [
    {"name": "S&P 500 Index Fund (e.g., VOO, SPY)", "type": "Index ETF", "avg_return": "~10% annually", "description": "Tracks the 500 largest U.S. companies. The bedrock of many portfolios, offering broad market exposure and diversification.", "symbol": "VOO"},
    {"name": "Nasdaq 100 Index Fund (e.g., QQQ)", "type": "Index ETF", "avg_return": "~13% annually (higher volatility)", "description": "Tracks the 100 largest non-financial companies on the Nasdaq. Heavily weighted towards technology and growth.", "symbol": "QQQ"},
    {"name": "Vanguard Total Stock Market ETF (VTI)", "type": "Index ETF", "avg_return": "~9.8% annually", "description": "Own a piece of the entire U.S. stock market (over 3,000 stocks), including large, mid, and small-cap companies.", "symbol": "VTI"},
    {"name": "ARK Innovation ETF (ARKK)", "type": "Actively Managed ETF", "avg_return": "Highly volatile", "description": "Invests in companies poised to benefit from 'disruptive innovation' like AI, robotics, and genomics. High risk, high potential reward.", "symbol": "ARKK"},
    {"name": "Schwab U.S. Dividend Equity ETF (SCHD)", "type": "Dividend ETF", "avg_return": "~12% annually (with dividends)", "description": "Focuses on high-quality, dividend-paying U.S. stocks with a track record of financial strength.", "symbol": "SCHD"},
]

# Badge definitions
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