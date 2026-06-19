import unittest
import json
from decimal import Decimal
from app import app, db, User, Holding, Transaction
from simulator import simulator

class StockAnalyzerTestCase(unittest.TestCase):
    def setUp(self):
        # Configure app for testing
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' # Use in-memory SQLite for testing
        app.config['WTF_CSRF_ENABLED'] = False
        self.app = app.test_client()
        
        with app.app_context():
            db.create_all()
            
            # Seed a test user
            self.test_user = User(username='testuser')
            self.test_user.set_password('password123')
            self.test_user.cash_balance = Decimal('100000.00')
            db.session.add(self.test_user)
            db.session.commit()
            
            self.test_user_id = self.test_user.id

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            action='login',
            username=username,
            password=password
        ), follow_redirects=True)

    def register(self, username, password):
        return self.app.post('/login', data=dict(
            action='register',
            username=username,
            password=password
        ), follow_redirects=True)

    def test_registration_and_login(self):
        """Test user registration and login flows."""
        # 1. Register a new user
        response = self.register('newuser', 'newpass123')
        self.assertIn(b'Welcome back, newuser!', response.data)
        
        # Log out to clear session
        self.app.get('/logout', follow_redirects=True)
        
        # 2. Login as the seeded user
        response = self.login('testuser', 'password123')
        self.assertIn(b'Welcome back, testuser!', response.data)
        
        # Log out to clear session
        self.app.get('/logout', follow_redirects=True)
        
        # 3. Login with invalid credentials
        response = self.login('testuser', 'wrongpass')
        self.assertIn(b'Invalid username or password', response.data)

    def test_stock_api(self):
        """Test stocks listing and specific stock details APIs."""
        # Need to log in first
        self.login('testuser', 'password123')
        
        # 1. Test get all stocks
        response = self.app.get('/api/stocks')
        self.assertEqual(response.status_code, 200)
        stocks = json.loads(response.data)
        self.assertTrue(len(stocks) > 0)
        self.assertIn('ticker', stocks[0])
        self.assertIn('price', stocks[0])
        
        # 2. Test get details of a specific ticker
        response = self.app.get('/api/stock/AAPL')
        self.assertEqual(response.status_code, 200)
        details = json.loads(response.data)
        self.assertEqual(details['ticker'], 'AAPL')
        self.assertIn('prices', details)
        self.assertIn('sma_10', details)
        self.assertIn('rsi_14', details)
        self.assertIn('recommendation', details)

    def test_trading_and_portfolio_apis(self):
        """Test simulated trading and portfolio valuation logic."""
        # Log in
        self.login('testuser', 'password123')
        
        # 1. Verify starting portfolio
        response = self.app.get('/api/portfolio')
        self.assertEqual(response.status_code, 200)
        portfolio = json.loads(response.data)
        self.assertEqual(portfolio['cash_balance'], 100000.0)
        self.assertEqual(portfolio['total_holdings_value'], 0.0)
        self.assertEqual(len(portfolio['holdings']), 0)
        
        # 2. Execute buy transaction: Buy 10 shares of NVDA
        response = self.app.post('/api/buy', 
                                 data=json.dumps({'ticker': 'NVDA', 'shares': 10}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        buy_res = json.loads(response.data)
        self.assertTrue(buy_res['success'])
        
        # Verify cash deducted
        self.assertTrue(buy_res['cash_balance'] < 100000.00)
        
        # 3. Check portfolio details after buy
        response = self.app.get('/api/portfolio')
        portfolio = json.loads(response.data)
        self.assertEqual(len(portfolio['holdings']), 1)
        self.assertEqual(portfolio['holdings'][0]['ticker'], 'NVDA')
        self.assertEqual(portfolio['holdings'][0]['shares'], 10.0)
        
        # 4. Check transaction log
        response = self.app.get('/api/transactions_list')
        txs = json.loads(response.data)
        self.assertEqual(len(txs), 1)
        self.assertEqual(txs[0]['ticker'], 'NVDA')
        self.assertEqual(txs[0]['action'], 'BUY')
        self.assertEqual(txs[0]['shares'], 10.0)
        
        # 5. Sell 4 shares of NVDA
        response = self.app.post('/api/sell', 
                                 data=json.dumps({'ticker': 'NVDA', 'shares': 4}),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        sell_res = json.loads(response.data)
        self.assertTrue(sell_res['success'])
        
        # 6. Verify remaining shares are 6
        response = self.app.get('/api/portfolio')
        portfolio = json.loads(response.data)
        self.assertEqual(portfolio['holdings'][0]['shares'], 6.0)
        
        # Verify transaction log now has 2 items
        response = self.app.get('/api/transactions_list')
        txs = json.loads(response.data)
        self.assertEqual(len(txs), 2)
        self.assertEqual(txs[0]['action'], 'SELL') # Sorted descending, so sell is first
        self.assertEqual(txs[0]['shares'], 4.0)

if __name__ == '__main__':
    unittest.main()
