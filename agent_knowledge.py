# agent_knowledge.py
# Stock Analyzer - Educational Knowledge Base

KNOWLEDGE = {

    # =========================
    # STOCK MARKET BASICS
    # =========================

    "stock": {
        "keywords": ["stock", "stocks", "share", "shares"],
        "answer": """A **stock** represents ownership in a company.

When you buy a company's stock, you own a small portion of that company.

For example, if a company has 1,000 shares and you own 10 shares, you own 1% of the company.

The price of a stock changes because buyers and sellers continuously interact in the market.

Stocks can potentially provide returns through:
• Price appreciation
• Dividends

Related concepts: shares, stock exchange, market capitalization, dividend"""
    },

    "stock_market": {
        "keywords": ["stock market", "market", "share market"],
        "answer": """The **stock market** is a marketplace where shares of publicly listed companies are bought and sold.

In India, two major stock exchanges are:

• **NSE** — National Stock Exchange
• **BSE** — Bombay Stock Exchange

Investors and traders use these exchanges to buy and sell securities.

The stock market also reflects expectations about companies, industries and the economy."""
    },

    "nse": {
        "keywords": ["nse", "national stock exchange"],
        "answer": """**NSE** stands for National Stock Exchange of India.

It is one of India's major stock exchanges.

NSE is widely known for its electronic trading system and for indices such as the **NIFTY 50**.

Related concepts: BSE, NIFTY 50, stock exchange"""
    },

    "bse": {
        "keywords": ["bse", "bombay stock exchange"],
        "answer": """**BSE** stands for Bombay Stock Exchange.

It is one of India's major stock exchanges and is one of the world's oldest stock exchanges.

Its major benchmark index is the **SENSEX**.

Related concepts: NSE, SENSEX, stock exchange"""
    },

    "ipo": {
        "keywords": ["ipo", "initial public offering"],
        "answer": """An **IPO (Initial Public Offering)** is when a private company offers its shares to the public for the first time.

Before an IPO, ownership is generally held by founders, employees and private investors.

After listing, the company's shares can be traded on a stock exchange.

Related concepts: listing, shares, stock exchange"""
    },

    "market_cap": {
        "keywords": [
            "market cap",
            "market capitalization",
            "market capitalisation"
        ],
        "answer": """**Market capitalization** represents the total market value of a company's outstanding shares.

Formula:

**Market Cap = Share Price × Shares Outstanding**

Example:

If a company has 10 crore shares and each share costs ₹100:

Market Cap = 10 crore × ₹100 = ₹1,000 crore.

Market capitalization is commonly used to classify companies as large-cap, mid-cap or small-cap."""
    },


    # =========================
    # COMPANY FINANCIALS
    # =========================

    "revenue": {
        "keywords": ["revenue", "sales", "turnover"],
        "answer": """**Revenue** is the money a company generates from its business activities before subtracting expenses.

For example, if a company sells products worth ₹10 crore during a year, its revenue is ₹10 crore.

Revenue is sometimes called **sales** or **turnover**.

Revenue is different from profit because a company still has to pay expenses before determining its profit."""
    },

    "profit": {
        "keywords": [
            "profit",
            "net profit",
            "earnings",
            "net income"
        ],
        "answer": """**Profit** is the amount left after a company subtracts its expenses from its revenue.

Simplified:

**Profit = Revenue − Expenses**

For example:

Revenue = ₹100 crore
Expenses = ₹75 crore

Profit = ₹25 crore

Investors often examine whether a company's profit is growing consistently."""
    },

    "eps": {
        "keywords": [
            "eps",
            "earnings per share"
        ],
        "answer": """**EPS (Earnings Per Share)** represents the portion of a company's profit attributable to each outstanding share.

Simplified formula:

**EPS = Net Profit ÷ Outstanding Shares**

Example:

Net profit = ₹100 crore
Shares = 20 crore

EPS = ₹5

EPS is particularly important because the **P/E ratio** uses earnings per share.

Related concepts: profit, P/E ratio, shares outstanding"""
    },

    "pe": {
        "keywords": [
            "pe",
            "p/e",
            "pe ratio",
            "price earnings",
            "price to earnings"
        ],
        "answer": """The **P/E (Price-to-Earnings) ratio** compares a company's share price with its earnings per share.

Formula:

**P/E = Share Price ÷ EPS**

Example:

Share price = ₹200
EPS = ₹10

P/E = 20

A higher P/E can indicate that investors are paying more for each unit of current earnings, while a lower P/E means a lower price relative to earnings.

However, a low P/E is **not automatically better**. Growth expectations, industry characteristics, profitability and future earnings all matter.

Related concepts: EPS, valuation, earnings growth"""
    },

    "pb": {
        "keywords": [
            "pb",
            "p/b",
            "pb ratio",
            "price to book",
            "price book"
        ],
        "answer": """The **P/B (Price-to-Book) ratio** compares a company's market value with its book value.

Simplified:

**P/B = Market Price per Share ÷ Book Value per Share**

It is often useful when comparing companies where the value of physical or financial assets is important.

P/B should generally be interpreted together with profitability metrics such as ROE."""
    },

    "roe": {
        "keywords": [
            "roe",
            "return on equity"
        ],
        "answer": """**ROE (Return on Equity)** measures how effectively a company generates profit from shareholders' equity.

Simplified:

**ROE = Net Income ÷ Shareholders' Equity × 100**

For example, an ROE of 15% means the company generated ₹15 of profit for every ₹100 of equity, using the simplified interpretation.

ROE is most useful when compared across similar companies and across multiple years."""
    },

    "roce": {
        "keywords": [
            "roce",
            "return on capital employed"
        ],
        "answer": """**ROCE (Return on Capital Employed)** measures how efficiently a company generates operating returns from the capital employed in its business.

It is commonly used when analyzing capital-intensive businesses.

A consistently strong ROCE can indicate efficient use of capital, but it should be compared with industry peers and historical values."""
    },

    "debt": {
        "keywords": [
            "debt",
            "debt equity",
            "debt to equity",
            "debt-to-equity"
        ],
        "answer": """**Debt** is money borrowed by a company.

One commonly used measure is the **Debt-to-Equity ratio**.

Simplified:

**Debt-to-Equity = Total Debt ÷ Shareholders' Equity**

Debt can help a company expand, but excessive debt can increase financial risk because interest and repayments still have to be made.

Debt should therefore be evaluated together with cash flow, profitability and the company's industry."""
    },

    "dividend": {
        "keywords": [
            "dividend",
            "dividends",
            "dividend yield"
        ],
        "answer": """A **dividend** is a distribution of part of a company's profits to shareholders.

For example, if a company declares ₹5 per share and you own 100 shares:

Dividend received = ₹500.

**Dividend Yield** compares annual dividend with the share price.

Simplified:

**Dividend Yield = Annual Dividend per Share ÷ Share Price × 100**

Companies do not have to pay dividends; they may instead retain profits for growth."""
    },


    # =========================
    # FUNDAMENTAL ANALYSIS
    # =========================

    "fundamental_analysis": {
        "keywords": [
            "fundamental analysis",
            "fundamentals",
            "fundamental"
        ],
        "answer": """**Fundamental analysis** evaluates a company using its business, financial statements, competitive position and valuation.

Common areas include:

• Revenue growth
• Profit growth
• EPS
• P/E
• ROE
• ROCE
• Debt
• Cash flow
• Competitive advantages
• Industry conditions
• Valuation

The goal is to understand the underlying business rather than focusing only on short-term price movements."""
    },

    "technical_analysis": {
        "keywords": [
            "technical analysis",
            "technical",
            "chart analysis"
        ],
        "answer": """**Technical analysis** studies price and trading-volume data to identify patterns and potential market behavior.

Common concepts include:

• Candlesticks
• Support
• Resistance
• Trend
• Volume
• Moving averages
• RSI
• MACD

Technical analysis focuses primarily on market data rather than a company's financial statements."""
    },

    "intrinsic_value": {
        "keywords": [
            "intrinsic value",
            "fair value",
            "fair price"
        ],
        "answer": """**Intrinsic value** is an estimate of what an asset or company may be worth based on underlying economic factors.

Different valuation methods can produce different estimates.

For example, analysts may use:

• Discounted Cash Flow (DCF)
• Comparable company valuation
• Dividend-based models

Intrinsic value is an estimate, not a guaranteed future price."""
    },


    # =========================
    # TECHNICAL ANALYSIS
    # =========================

    "candlestick": {
        "keywords": [
            "candlestick",
            "candle",
            "candlestick chart"
        ],
        "answer": """A **candlestick** represents price movement during a specific period.

A candle generally contains:

• Open price
• High price
• Low price
• Close price

The body represents the relationship between opening and closing prices, while the wicks show the high and low.

Candlesticks are commonly used to study price patterns and market behavior."""
    },

    "support": {
        "keywords": [
            "support",
            "support level"
        ],
        "answer": """**Support** is a price area where buying interest has historically been strong enough to slow or reverse a decline.

For example, if a stock repeatedly finds buying interest around ₹100, traders may identify ₹100 as a potential support area.

Support is not a guaranteed floor. Price can move below it."""
    },

    "resistance": {
        "keywords": [
            "resistance",
            "resistance level"
        ],
        "answer": """**Resistance** is a price area where selling pressure has historically been strong enough to slow or reverse a rise.

For example, if a stock repeatedly struggles around ₹200, traders may identify ₹200 as a potential resistance area.

Resistance is not a guaranteed ceiling."""
    },

    "volume": {
        "keywords": [
            "volume",
            "trading volume"
        ],
        "answer": """**Trading volume** represents the number of shares traded during a particular period.

Volume can help provide context for price movements.

For example, a price movement accompanied by unusually high volume may indicate stronger market participation.

Volume should be interpreted together with price and other information."""
    },

    "moving_average": {
        "keywords": [
            "moving average",
            "moving averages",
            "sma",
            "ema"
        ],
        "answer": """A **moving average** smooths price data over a specified period.

Two common types are:

**SMA — Simple Moving Average**

Calculates the average price over a period.

**EMA — Exponential Moving Average**

Gives greater weight to more recent prices.

Moving averages are commonly used to study trends and price momentum."""
    },

    "rsi": {
        "keywords": [
            "rsi",
            "relative strength index"
        ],
        "answer": """**RSI (Relative Strength Index)** is a momentum indicator commonly displayed on a scale from 0 to 100.

Traditional interpretations often use:

Below 30 → potentially oversold
Above 70 → potentially overbought

These levels are not guaranteed buy or sell signals. RSI should be interpreted with the broader market context."""
    },

    "macd": {
        "keywords": [
            "macd",
            "moving average convergence divergence"
        ],
        "answer": """**MACD (Moving Average Convergence Divergence)** is a momentum and trend-following indicator.

It is based on relationships between exponential moving averages.

Traders commonly examine:

• MACD line
• Signal line
• Histogram

MACD can help analyze momentum and potential trend changes."""
    },


    # =========================
    # INVESTING
    # =========================

    "mutual_fund": {
        "keywords": [
            "mutual fund",
            "mutual funds"
        ],
        "answer": """A **mutual fund** pools money from many investors and invests it according to a defined strategy.

The portfolio may contain:

• Stocks
• Bonds
• Money-market instruments
• Other securities

A professional fund manager generally manages the portfolio according to the fund's objectives.

Mutual funds can provide diversification, but they also carry investment risk."""
    },

    "etf": {
        "keywords": [
            "etf",
            "exchange traded fund",
            "exchange-traded fund"
        ],
        "answer": """An **ETF (Exchange-Traded Fund)** is a fund whose units trade on a stock exchange.

An ETF may track:

• A stock index
• A sector
• Bonds
• Commodities
• Other assets

For example, an index ETF may attempt to track the performance of a particular index.

ETFs combine characteristics of funds with exchange-based trading."""
    },

    "sip": {
        "keywords": [
            "sip",
            "systematic investment plan"
        ],
        "answer": """**SIP (Systematic Investment Plan)** is a method of investing a fixed amount into a mutual fund at regular intervals.

For example, an investor could invest ₹2,000 every month.

SIP is a method of investing, not a separate investment product.

The value of investments can rise or fall with the underlying assets."""
    },

    "diversification": {
        "keywords": [
            "diversification",
            "diversify",
            "diversified portfolio"
        ],
        "answer": """**Diversification** means spreading investments across different assets, companies, sectors or other categories.

The basic idea is that poor performance from one investment may have a smaller effect on the overall portfolio when exposure is spread across multiple investments.

Diversification does not eliminate investment risk."""
    },


    # =========================
    # TRADING
    # =========================

    "market_order": {
        "keywords": [
            "market order",
            "market orders"
        ],
        "answer": """A **market order** instructs a broker or trading system to execute an order immediately at the best available price.

The exact execution price may differ from the price you saw when placing the order, especially in a rapidly moving or less liquid market."""
    },

    "limit_order": {
        "keywords": [
            "limit order",
            "limit orders"
        ],
        "answer": """A **limit order** specifies the maximum price you are willing to pay when buying or the minimum price you are willing to accept when selling.

The order may remain unexecuted if the market does not reach the specified price."""
    },

    "stop_loss": {
        "keywords": [
            "stop loss",
            "stop-loss",
            "stoploss"
        ],
        "answer": """A **stop-loss** is an order mechanism used to limit potential losses by triggering an order when the price reaches a specified level.

For example, a trader buying at ₹100 might set a stop level below ₹100.

A stop-loss does not guarantee execution at exactly the specified price because market conditions can change quickly."""
    },

    "volatility": {
        "keywords": [
            "volatility",
            "volatile",
            "volatility meaning"
        ],
        "answer": """**Volatility** describes how much and how quickly an asset's price changes.

Higher volatility means larger price fluctuations.

Lower volatility generally means smaller price fluctuations.

Volatility is not the same thing as direction. A stock can be highly volatile while moving either upward or downward."""
    },

    "short_selling": {
        "keywords": [
            "short selling",
            "short sell",
            "short selling meaning"
        ],
        "answer": """**Short selling** is a trading strategy where a trader attempts to benefit from a decline in an asset's price.

In a simplified example:

1. Shares are borrowed.
2. They are sold.
3. The trader later buys shares to return them.

If the price falls, the difference may represent a gain before costs.

Short selling can involve significant risk because losses can become very large if the price rises."""
    },


    # =========================
    # RISK
    # =========================

    "risk": {
        "keywords": [
            "risk",
            "investment risk",
            "stock risk"
        ],
        "answer": """**Investment risk** is the possibility that an investment's actual outcome differs from what you expected.

Common types include:

• Market risk
• Business risk
• Credit risk
• Liquidity risk
• Interest-rate risk
• Currency risk

Risk cannot be completely eliminated. Investors generally manage it through research, diversification, position sizing and understanding the investment."""
    },

    "compounding": {
        "keywords": [
            "compounding",
            "compound interest",
            "compounding returns"
        ],
        "answer": """**Compounding** occurs when returns generated by an investment remain invested and can themselves generate future returns.

For example, if ₹10,000 grows by 10%, it becomes ₹11,000.

If another 10% return occurs on ₹11,000, the value becomes ₹12,100.

Over long periods, this effect can become significant."""
    }
}


# ==========================================
# QUESTION MATCHING
# ==========================================

def find_concept(question):
    """
    Find the most relevant concept from the knowledge base.
    """

    question = question.lower().strip()

    best_match = None
    best_score = 0

    for concept, data in KNOWLEDGE.items():

        score = 0

        for keyword in data["keywords"]:

            if keyword in question:

                # Longer phrases are stronger matches
                score += len(keyword.split()) * 2

        if score > best_score:

            best_score = score
            best_match = concept

    return best_match


def answer_question(question):
    """
    Return an educational answer and related concepts.
    """

    concept = find_concept(question)

    if not concept:

        return {
            "answer": """I don't have a dedicated explanation for that question yet.

Try asking me about:

• Stocks
• IPOs
• NSE / BSE
• Market capitalization
• Revenue and profit
• EPS
• P/E ratio
• ROE / ROCE
• Fundamental analysis
• Technical analysis
• Candlesticks
• Support and resistance
• RSI / MACD
• Mutual funds
• ETFs
• SIP
• Diversification
• Market orders
• Limit orders
• Stop-loss
• Risk
• Compounding

You can also ask a follow-up question about any concept I explain.""",

            "related": [
                "What is a stock?",
                "What is P/E ratio?",
                "What is fundamental analysis?",
                "What is technical analysis?"
            ]
        }

    answer = KNOWLEDGE[concept]["answer"]

    related_map = {

        "stock": [
            "What is market capitalization?",
            "Why do stock prices change?",
            "What is a dividend?"
        ],

        "eps": [
            "What is P/E ratio?",
            "What is profit?",
            "What is revenue?"
        ],

        "pe": [
            "What is EPS?",
            "What is valuation?",
            "Is a low P/E always better?"
        ],

        "fundamental_analysis": [
            "What is EPS?",
            "What is ROE?",
            "What is P/E ratio?"
        ],

        "technical_analysis": [
            "What is a candlestick?",
            "What is RSI?",
            "What is MACD?"
        ],

        "rsi": [
            "What is technical analysis?",
            "What is volume?",
            "What is MACD?"
        ],

        "mutual_fund": [
            "What is an ETF?",
            "What is SIP?",
            "What is diversification?"
        ],

        "etf": [
            "What is a mutual fund?",
            "What is diversification?",
            "What is an index?"
        ],

        "risk": [
            "What is diversification?",
            "What is volatility?",
            "What is stop-loss?"
        ]

    }

    return {
        "answer": answer,
        "related": related_map.get(
            concept,
            [
                "Explain this with an example",
                "Why is this important?",
                "What should I learn next?"
            ]
        )
    }
