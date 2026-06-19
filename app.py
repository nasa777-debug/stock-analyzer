import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
from decimal import Decimal
from database import db, User, Transaction, Holding
from simulator import simulator

app = Flask(__name__)

# Flask Configurations
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'stock_analyzer_secret_key_998877')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///stock_analyzer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB with App
db.init_app(app)
with app.app_context():
    db.create_all()

# Helper function to get current logged-in user
def get_current_user():
    if 'user_id' not in session:
        return None
    return db.session.get(User, session['user_id'])

# --- Web Page Routes ---

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
        
    if request.method == 'POST':
        action = request.form.get('action') # 'login' or 'register'
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            flash('Username and password are required.', 'error')
            return render_template('login.html')
            
        if action == 'register':
            # Handle Registration
            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash('Username already exists. Please choose a different one.', 'error')
                return render_template('login.html')
            
            new_user = User(username=username)
            new_user.set_password(password)
            new_user.cash_balance = Decimal('100000.00') # Default cash balance
            
            try:
                db.session.add(new_user)
                db.session.commit()
                session['user_id'] = new_user.id
                session['username'] = new_user.username
                flash('Registration successful! Welcome to Stock Analyzer.', 'success')
                return redirect(url_for('dashboard'))
            except Exception as e:
                db.session.rollback()
                flash('An error occurred during registration. Please try again.', 'error')
                
        else:
            # Handle Login
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash('Successfully logged in!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Invalid username or password.', 'error')
                
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Successfully logged out.', 'info')
    return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    user = get_current_user()
    if not user:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login_page'))
    return render_template('dashboard.html', username=user.username)

@app.route('/market')
def market():
    user = get_current_user()
    if not user:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login_page'))
    return render_template('market.html', username=user.username)

@app.route('/transactions')
def transactions():
    user = get_current_user()
    if not user:
        flash('Please login to access this page.', 'error')
        return redirect(url_for('login_page'))
    return render_template('transactions.html', username=user.username)

# --- API Endpoints ---

@app.route('/api/stocks', methods=['GET'])
def get_stocks():
    """Get all stocks with prices and 24h changes."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    return jsonify(simulator.get_market_summary())

@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_detail(ticker):
    """Get historical charts and technical indicators for a specific stock."""
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    details = simulator.get_stock_details(ticker.upper())
    if not details:
        return jsonify({'error': 'Stock not found'}), 404
        
    return jsonify(details)

@app.route('/api/portfolio', methods=['GET'])
def get_portfolio():
    """Calculate portfolio net worth, P/L, and holding statistics."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    holdings_data = []
    total_holdings_value = Decimal('0.00')
    total_cost_basis = Decimal('0.00')
    
    simulator.update_prices()
    
    for holding in user.holdings:
        ticker = holding.ticker
        current_price = Decimal(str(simulator.prices.get(ticker, 0.0)))
        shares = holding.shares
        avg_price = holding.average_price
        
        value = shares * current_price
        cost = shares * avg_price
        pl = value - cost
        pl_pct = (pl / cost * 100) if cost > 0 else Decimal('0.00')
        
        total_holdings_value += value
        total_cost_basis += cost
        
        holdings_data.append({
            'ticker': ticker,
            'name': simulator.stocks_info.get(ticker, {}).get('name', ''),
            'shares': float(shares),
            'average_price': float(avg_price),
            'current_price': float(current_price),
            'total_cost': float(cost),
            'current_value': float(value),
            'profit_loss': float(pl),
            'profit_loss_pct': float(pl_pct)
        })
        
    cash = user.cash_balance
    net_worth = cash + total_holdings_value
    total_pl = net_worth - Decimal('100000.00') # Profit relative to starting capital
    total_pl_pct = (total_pl / Decimal('100000.00')) * 100
    
    # Calculate asset allocation percentages
    allocation = []
    if net_worth > 0:
        allocation.append({
            'asset': 'Cash',
            'value': float(cash),
            'percentage': round(float(cash / net_worth * 100), 2)
        })
        for item in holdings_data:
            allocation.append({
                'asset': item['ticker'],
                'value': item['current_value'],
                'percentage': round(float(Decimal(str(item['current_value'])) / net_worth * 100), 2)
            })

    return jsonify({
        'cash_balance': float(cash),
        'total_holdings_value': float(total_holdings_value),
        'net_worth': float(net_worth),
        'total_profit_loss': float(total_pl),
        'total_profit_loss_pct': float(total_pl_pct),
        'holdings': holdings_data,
        'allocation': allocation
    })

@app.route('/api/buy', methods=['POST'])
def buy_stock():
    """Buy shares of a stock using virtual cash."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or {}
    ticker = data.get('ticker', '').upper().strip()
    shares_raw = data.get('shares')
    
    if not ticker or ticker not in simulator.stocks_info:
        return jsonify({'error': 'Invalid ticker symbol.'}), 400
        
    try:
        shares = Decimal(str(shares_raw))
        if shares <= 0:
            raise ValueError()
    except (TypeError, ValueError, ArithmeticError):
        return jsonify({'error': 'Shares must be a positive number.'}), 400
        
    # Get current price
    simulator.update_prices()
    price = Decimal(str(simulator.prices[ticker]))
    total_cost = shares * price
    
    if user.cash_balance < total_cost:
        return jsonify({'error': f'Insufficient cash. Required: ${total_cost:,.2f}, Available: ${user.cash_balance:,.2f}'}), 400
        
    try:
        # Deduct cash
        user.cash_balance -= total_cost
        
        # Check if holding already exists
        holding = Holding.query.filter_by(user_id=user.id, ticker=ticker).first()
        if holding:
            new_shares = holding.shares + shares
            # Calculate new weighted average cost
            new_avg_price = ((holding.shares * holding.average_price) + (shares * price)) / new_shares
            holding.shares = new_shares
            holding.average_price = new_avg_price
        else:
            holding = Holding(user_id=user.id, ticker=ticker, shares=shares, average_price=price)
            db.session.add(holding)
            
        # Record transaction
        tx = Transaction(user_id=user.id, ticker=ticker, action='BUY', shares=shares, price=price)
        db.session.add(tx)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Successfully bought {float(shares)} shares of {ticker} at ${float(price):,.2f}',
            'cash_balance': float(user.cash_balance)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Transaction failed. Please try again.'}), 500

@app.route('/api/sell', methods=['POST'])
def sell_stock():
    """Sell holdings of a stock for virtual cash."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    data = request.get_json() or {}
    ticker = data.get('ticker', '').upper().strip()
    shares_raw = data.get('shares')
    
    if not ticker or ticker not in simulator.stocks_info:
        return jsonify({'error': 'Invalid ticker symbol.'}), 400
        
    try:
        shares = Decimal(str(shares_raw))
        if shares <= 0:
            raise ValueError()
    except (TypeError, ValueError, ArithmeticError):
        return jsonify({'error': 'Shares must be a positive number.'}), 400
        
    # Get user's holding
    holding = Holding.query.filter_by(user_id=user.id, ticker=ticker).first()
    if not holding or holding.shares < shares:
        available = float(holding.shares) if holding else 0.0
        return jsonify({'error': f'Insufficient shares to sell. Available: {available}'}), 400
        
    # Get current price
    simulator.update_prices()
    price = Decimal(str(simulator.prices[ticker]))
    revenue = shares * price
    
    try:
        # Add cash
        user.cash_balance += revenue
        
        # Deduct shares
        holding.shares -= shares
        if holding.shares == 0:
            db.session.delete(holding)
            
        # Record transaction
        tx = Transaction(user_id=user.id, ticker=ticker, action='SELL', shares=shares, price=price)
        db.session.add(tx)
        
        db.session.commit()
        return jsonify({
            'success': True,
            'message': f'Successfully sold {float(shares)} shares of {ticker} at ${float(price):,.2f}',
            'cash_balance': float(user.cash_balance)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Transaction failed. Please try again.'}), 500

@app.route('/api/transactions_list', methods=['GET'])
def get_transactions():
    """Get transaction history for the logged-in user."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Unauthorized'}), 401
        
    txs = Transaction.query.filter_by(user_id=user.id).order_by(Transaction.timestamp.desc()).all()
    return jsonify([tx.to_dict() for tx in txs])

# Database tables creation & app runner
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
