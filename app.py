import os
from agent_knowledge import answer_question
from decimal import Decimal
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from database import db, User, Transaction, Holding
from simulator import simulator

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'stock_analyzer_secret_key_998877')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///stock_analyzer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
with app.app_context():
    db.create_all()

# -----------------------------------------------------------------------------
# Educational knowledge base. This intentionally stays deterministic so the
# public demo does not need an LLM key. It can later be connected to an LLM.
# -----------------------------------------------------------------------------
STOCK_KNOWLEDGE = {
    'AAPL': {'sector': 'Technology', 'about': 'Apple designs consumer electronics, software and services. Its ecosystem spans iPhone, Mac, iPad, wearables and subscription services.', 'watch': 'Hardware demand, services growth, margins and ecosystem strength.'},
    'MSFT': {'sector': 'Technology', 'about': 'Microsoft develops software, cloud infrastructure and productivity products including Azure, Microsoft 365 and Windows.', 'watch': 'Cloud growth, enterprise spending, recurring revenue and AI investment.'},
    'GOOGL': {'sector': 'Communication Services', 'about': 'Alphabet operates Google Search, YouTube, Android and Google Cloud, with advertising as a major business.', 'watch': 'Advertising demand, cloud growth, AI products and regulatory developments.'},
    'AMZN': {'sector': 'Consumer Cyclical', 'about': 'Amazon combines e-commerce, logistics, cloud computing through AWS and advertising services.', 'watch': 'AWS growth, retail margins, consumer demand and operating efficiency.'},
    'TSLA': {'sector': 'Consumer Cyclical', 'about': 'Tesla focuses on electric vehicles, energy storage and related software and services.', 'watch': 'Vehicle deliveries, margins, pricing, energy growth and competition.'},
    'NVDA': {'sector': 'Technology', 'about': 'NVIDIA develops GPUs and accelerated computing platforms used heavily in AI, data centers and graphics.', 'watch': 'Data-center demand, AI infrastructure spending, margins and competition.'},
    'NFLX': {'sector': 'Communication Services', 'about': 'Netflix provides subscription and advertising-supported video streaming globally.', 'watch': 'Subscriber engagement, revenue growth, content spending and advertising.'},
    'META': {'sector': 'Communication Services', 'about': 'Meta operates social and messaging platforms including Facebook, Instagram and WhatsApp, plus Reality Labs.', 'watch': 'Advertising demand, user engagement, AI investment and operating costs.'},
}

LEARN_TOPICS = [
    {'term':'Stock','category':'Basics','level':'Beginner','summary':'A small ownership claim in a company.','example':'Owning 1 share means you own a tiny fraction of the company.', 'why':'Stocks let companies raise capital and give investors exposure to business performance.'},
    {'term':'Market Capitalization','category':'Basics','level':'Beginner','summary':'The market value of all outstanding shares.','example':'Share price × shares outstanding = market cap.','why':'It gives a quick sense of company size, not company quality.'},
    {'term':'P/E Ratio','category':'Valuation','level':'Beginner','summary':'Price divided by earnings per share.','example':'₹200 share price ÷ ₹10 EPS = P/E of 20.','why':'It helps compare the price investors pay for each unit of earnings.'},
    {'term':'EPS','category':'Valuation','level':'Beginner','summary':'Earnings per share shows profit attributable to each share.','example':'₹100 crore profit ÷ 10 crore shares = ₹10 EPS.','why':'It is a core input for valuation ratios such as P/E.'},
    {'term':'Dividend','category':'Fundamentals','level':'Beginner','summary':'A distribution of company profits to shareholders.','example':'A ₹5 dividend on one share pays ₹5 per share.','why':'Income-focused investors often track dividend consistency and yield.'},
    {'term':'Volume','category':'Technical Analysis','level':'Beginner','summary':'The number of shares traded during a period.','example':'A volume spike can show unusually high market activity.','why':'Volume can add context to price moves and breakouts.'},
    {'term':'SMA','category':'Technical Analysis','level':'Intermediate','summary':'Simple Moving Average: the average price over a fixed window.','example':'A 20-day SMA averages the latest 20 prices.','why':'It smooths price noise and helps visualize trends.'},
    {'term':'EMA','category':'Technical Analysis','level':'Intermediate','summary':'Exponential Moving Average gives more weight to recent prices.','example':'A 12-day EMA reacts faster than a 12-day SMA.','why':'Traders use it to study trend direction and momentum.'},
    {'term':'RSI','category':'Technical Analysis','level':'Intermediate','summary':'Relative Strength Index measures recent price momentum on a 0–100 scale.','example':'Below 30 is commonly described as oversold; above 70 as overbought.','why':'RSI is a momentum signal, not a guarantee of a reversal.'},
    {'term':'MACD','category':'Technical Analysis','level':'Intermediate','summary':'Moving Average Convergence Divergence compares exponential moving averages.','example':'MACD crossing its signal line can indicate a momentum change.','why':'It helps learners study trend and momentum together.'},
    {'term':'Volatility','category':'Risk','level':'Beginner','summary':'A measure of how much prices fluctuate.','example':'A stock moving sharply up and down has higher volatility.','why':'Higher volatility generally means a wider range of possible outcomes.'},
    {'term':'Diversification','category':'Risk','level':'Beginner','summary':'Spreading exposure across different assets or businesses.','example':'Owning companies from multiple sectors instead of one company.','why':'It can reduce the impact of one holding performing poorly.'},
    {'term':'Support','category':'Technical Analysis','level':'Intermediate','summary':'A price area where buying interest has historically appeared.','example':'A stock repeatedly stabilizing near ₹100 may have a perceived support area.','why':'Support is a chart concept, not a guaranteed floor.'},
    {'term':'Resistance','category':'Technical Analysis','level':'Intermediate','summary':'A price area where selling pressure has historically appeared.','example':'Repeated rejection near ₹150 may form a resistance area.','why':'It helps learners identify important price zones.'},
    {'term':'Bull Market','category':'Market Concepts','level':'Beginner','summary':'A sustained period of broadly rising market prices.','example':'Major indexes rising over an extended period.','why':'Market regime affects sentiment and risk-taking behavior.'},
    {'term':'Bear Market','category':'Market Concepts','level':'Beginner','summary':'A sustained period of broadly falling market prices.','example':'A major index declining substantially from a recent peak.','why':'It reminds investors that markets can experience prolonged declines.'},
]


def get_current_user():
    if 'user_id' not in session:
        return None
    return db.session.get(User, session['user_id'])


def login_required_page():
    user = get_current_user()
    if not user:
        flash('Please login to access this page.', 'error')
    return user


@app.route('/')
def index():
    return redirect(url_for('dashboard' if session.get('user_id') else 'login_page'))


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if session.get('user_id'):
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        action = request.form.get('action', 'login')
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
        if action == 'register':
            if User.query.filter_by(username=username).first():
                flash('Username already exists. Choose another one.', 'error')
                return render_template('login.html')
            user = User(username=username)
            user.set_password(password)
            user.cash_balance = Decimal('100000.00')
            try:
                db.session.add(user)
                db.session.commit()
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Account created. Your $100,000 learning portfolio is ready.', 'success')
                return redirect(url_for('dashboard'))
            except Exception:
                db.session.rollback()
                flash('Could not create the account. Please try again.', 'error')
        else:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Welcome back.', 'success')
                return redirect(url_for('dashboard'))
            flash('Invalid username or password.', 'error')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))


@app.route('/dashboard')
def dashboard():
    user = login_required_page()
    if not user:
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', username=user.username)


@app.route('/market')
def market():
    user = login_required_page()
    if not user:
        return redirect(url_for('login_page'))
    return render_template('market.html', username=user.username)


@app.route('/learn')
def learn():
    user = login_required_page()
    if not user:
        return redirect(url_for('login_page'))
    return render_template('learn.html', username=user.username, topics=LEARN_TOPICS)


@app.route('/agent')
def agent():
    user = login_required_page()
    if not user:
        return redirect(url_for('login_page'))
    return render_template('agent.html', username=user.username)


@app.route('/transactions')
def transactions():
    user = login_required_page()
    if not user:
        return redirect(url_for('login_page'))
    return render_template('transactions.html', username=user.username)


@app.route('/api/stocks')
def get_stocks():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(simulator.get_market_summary())


@app.route('/api/stock/<ticker>')
def get_stock_detail(ticker):
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    ticker = ticker.upper()
    details = simulator.get_stock_details(ticker)
    if not details:
        return jsonify({'error': 'Stock not found'}), 404
    profile = STOCK_KNOWLEDGE.get(ticker, {})
    details['sector'] = profile.get('sector', 'Market')
    details['about'] = profile.get('about', 'Educational simulated market profile.')
    details['watch'] = profile.get('watch', 'Review the chart and indicators carefully.')
    return jsonify(details)


@app.route('/api/learn')
def api_learn():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(LEARN_TOPICS)


@app.route('/api/agent', methods=['POST'])
def agent_chat():
    if not session.get('user_id'):
        return jsonify({'error': 'Unauthorized'}), 401
    question = (request.get_json() or {}).get('question', '').strip()
    if not question:
        return jsonify({'answer': 'Ask me something about stocks, investing concepts or technical indicators.'})

    q = question.lower()
    # Stock-aware answers first.
    for ticker, profile in STOCK_KNOWLEDGE.items():
        if ticker.lower() in q or simulator.stocks_info.get(ticker, {}).get('name', '').lower().split()[0] in q:
            details = simulator.get_stock_details(ticker)
            answer = (
                f"**{ticker} — {details['name']}**\n\n"
                f"{profile['about']}\n\n"
                f"Current simulated price: **${details['current_price']:,.2f}**. "
                f"RSI is **{details['latest_rsi']:.2f}** and MACD is **{details['latest_macd']:.2f}**.\n\n"
                f"**What to learn:** {profile['watch']}\n\n"
                "These numbers come from the educational simulator and are not real-time market data or financial advice."
            )
            return jsonify({'answer': answer, 'ticker': ticker})

    # Topic matching.
    ranked = []
    for topic in LEARN_TOPICS:
        words = [topic['term'].lower()] + topic['summary'].lower().split()
        score = sum(1 for word in words if word in q)
        if topic['term'].lower() in q:
            score += 5
        if score:
            ranked.append((score, topic))
    if ranked:
        topic = sorted(ranked, key=lambda x: x[0], reverse=True)[0][1]
        answer = (
            f"**{topic['term']}**\n\n{topic['summary']}\n\n"
            f"**Example:** {topic['example']}\n\n"
            f"**Why it matters:** {topic['why']}\n\n"
            "Want to go one level deeper? Ask me for a simple explanation, an example, or how it relates to a stock chart."
        )
        return jsonify({'answer': answer})

    if any(word in q for word in ['portfolio', 'holdings', 'my investments']):
        user = get_current_user()
        total = sum((Decimal(str(simulator.prices.get(h.ticker, 0))) * h.shares for h in user.holdings), Decimal('0'))
        return jsonify({'answer': f"Your simulated account currently has **${user.cash_balance:,.2f}** in cash and approximately **${total:,.2f}** in market holdings. I can explain how diversification, cost basis and unrealized P/L work."})

    return jsonify({'answer': "I’m your Stock Learning Agent. Try questions such as **What is P/E?**, **Explain RSI**, **What does MACD mean?**, **Tell me about NVDA**, or **Explain diversification**."})


@app.route('/api/portfolio')
def get_portfolio():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
    simulator.update_prices()
    holdings_data, total_holdings_value = [], Decimal('0.00')
    for holding in user.holdings:
        price = Decimal(str(simulator.prices.get(holding.ticker, 0.0)))
        shares, avg = holding.shares, holding.average_price
        value, cost = shares * price, shares * avg
        pl = value - cost
        pl_pct = (pl / cost * 100) if cost > 0 else Decimal('0.00')
        total_holdings_value += value
        holdings_data.append({'ticker': holding.ticker, 'name': simulator.stocks_info.get(holding.ticker, {}).get('name',''), 'shares': float(shares), 'average_price': float(avg), 'current_price': float(price), 'total_cost': float(cost), 'current_value': float(value), 'profit_loss': float(pl), 'profit_loss_pct': float(pl_pct)})
    cash = user.cash_balance
    net_worth = cash + total_holdings_value
    total_pl = net_worth - Decimal('100000.00')
    total_pl_pct = total_pl / Decimal('100000.00') * 100
    allocation = [{'asset':'Cash','value':float(cash),'percentage':round(float(cash/net_worth*100),2) if net_worth else 0}]
    for item in holdings_data:
        allocation.append({'asset':item['ticker'],'value':item['current_value'],'percentage':round(item['current_value']/float(net_worth)*100,2) if net_worth else 0})
    return jsonify({'cash_balance':float(cash),'total_holdings_value':float(total_holdings_value),'net_worth':float(net_worth),'total_profit_loss':float(total_pl),'total_profit_loss_pct':float(total_pl_pct),'holdings':holdings_data,'allocation':allocation})


@app.route('/api/buy', methods=['POST'])
def buy_stock():
    user = get_current_user()
    if not user: return jsonify({'error':'Unauthorized'}), 401
    data = request.get_json() or {}
    ticker = str(data.get('ticker','')).upper().strip()
    try: shares = Decimal(str(data.get('shares')))
    except Exception: shares = Decimal('0')
    if ticker not in simulator.stocks_info or shares <= 0: return jsonify({'error':'Enter a valid stock and positive share quantity.'}), 400
    simulator.update_prices(); price = Decimal(str(simulator.prices[ticker])); total = shares * price
    if user.cash_balance < total: return jsonify({'error':f'Insufficient cash. Required ${total:,.2f}.'}), 400
    try:
        user.cash_balance -= total
        holding = Holding.query.filter_by(user_id=user.id, ticker=ticker).first()
        if holding:
            new_shares = holding.shares + shares
            holding.average_price = ((holding.shares*holding.average_price)+(shares*price))/new_shares
            holding.shares = new_shares
        else:
            db.session.add(Holding(user_id=user.id,ticker=ticker,shares=shares,average_price=price))
        db.session.add(Transaction(user_id=user.id,ticker=ticker,action='BUY',shares=shares,price=price))
        db.session.commit()
        return jsonify({'success':True,'message':f'Bought {float(shares):g} {ticker} at ${price:,.2f}.','cash_balance':float(user.cash_balance)})
    except Exception:
        db.session.rollback(); return jsonify({'error':'Transaction failed. Please try again.'}),500


@app.route('/api/sell', methods=['POST'])
def sell_stock():
    user = get_current_user()
    if not user: return jsonify({'error':'Unauthorized'}),401
    data = request.get_json() or {}; ticker = str(data.get('ticker','')).upper().strip()
    try: shares = Decimal(str(data.get('shares')))
    except Exception: shares = Decimal('0')
    holding = Holding.query.filter_by(user_id=user.id,ticker=ticker).first()
    if ticker not in simulator.stocks_info or shares <= 0: return jsonify({'error':'Enter a valid stock and positive share quantity.'}),400
    if not holding or holding.shares < shares: return jsonify({'error':f'Insufficient shares. Available: {float(holding.shares) if holding else 0:g}.'}),400
    simulator.update_prices(); price=Decimal(str(simulator.prices[ticker])); revenue=shares*price
    try:
        user.cash_balance += revenue; holding.shares -= shares
        if holding.shares == 0: db.session.delete(holding)
        db.session.add(Transaction(user_id=user.id,ticker=ticker,action='SELL',shares=shares,price=price)); db.session.commit()
        return jsonify({'success':True,'message':f'Sold {float(shares):g} {ticker} at ${price:,.2f}.','cash_balance':float(user.cash_balance)})
    except Exception:
        db.session.rollback(); return jsonify({'error':'Transaction failed. Please try again.'}),500


@app.route('/api/transactions_list')
def get_transactions():
    user = get_current_user()
    if not user: return jsonify({'error':'Unauthorized'}),401
    return jsonify([tx.to_dict() for tx in Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()])

@app.route("/api/agent", methods=["POST"])
def agent_api():
    if "user_id" not in session:
        return jsonify({"error": "Please log in to use the learning agent."}), 401

    data = request.get_json(silent=True) or {}

    question = str(data.get("question", "")).strip()

    if not question:
        return jsonify({
            "error": "Please enter a question."
        }), 400

    if len(question) > 1000:
        return jsonify({
            "error": "Please keep your question under 1000 characters."
        }), 400

    try:
        result = answer_question(question)

        return jsonify({
            "answer": result.get("answer", ""),
            "related": result.get("related", [])
        })

    except Exception as e:
        print("Agent error:", e)

        return jsonify({
            "error": "The learning agent encountered an error. Please try again."
        }), 500
        
@app.route("/trade")
def trade():
    if "user_id" not in session:
        return redirect(url_for("login"))

    return render_template("trade.html")
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
