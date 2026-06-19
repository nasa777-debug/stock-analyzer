import random
import time
import math

class StockSimulator:
    def __init__(self):
        # Ticker configuration with names, base prices, and volatility factors
        self.stocks_info = {
            'AAPL': {'name': 'Apple Inc.', 'base_price': 175.0, 'volatility': 0.0015},
            'MSFT': {'name': 'Microsoft Corp.', 'base_price': 420.0, 'volatility': 0.0012},
            'GOOGL': {'name': 'Alphabet Inc.', 'base_price': 150.0, 'volatility': 0.0018},
            'AMZN': {'name': 'Amazon.com Inc.', 'base_price': 178.0, 'volatility': 0.0016},
            'TSLA': {'name': 'Tesla Inc.', 'base_price': 170.0, 'volatility': 0.0030},
            'NVDA': {'name': 'NVIDIA Corp.', 'base_price': 850.0, 'volatility': 0.0035},
            'NFLX': {'name': 'Netflix Inc.', 'base_price': 610.0, 'volatility': 0.0020},
            'META': {'name': 'Meta Platforms Inc.', 'base_price': 500.0, 'volatility': 0.0022}
        }
        
        self.prices = {}
        self.daily_history = {}
        self.last_update_time = time.time()
        
        self._initialize_market()

    def _initialize_market(self):
        """Initialize starting prices and historical data for all stocks."""
        for ticker, info in self.stocks_info.items():
            base = info['base_price']
            self.prices[ticker] = base
            
            # Generate 30 days of historical data backwards from base price
            history = []
            current_p = base
            # Use random seed based on ticker to make history somewhat repeatable initially
            # but then organic.
            rand = random.Random(hash(ticker))
            for _ in range(50):  # Generate 50 points to have enough data for 26-day EMA / MACD
                change_pct = rand.normalvariate(0.0002, info['volatility'] * 3) # small drift
                current_p = current_p * (1 - change_pct)
                history.insert(0, round(max(current_p, 1.0), 2))
            self.daily_history[ticker] = history

    def update_prices(self):
        """Update live stock prices using Geometric Brownian Motion simulation."""
        now = time.time()
        elapsed = now - self.last_update_time
        self.last_update_time = now
        
        # Limit elapsed time to avoid extreme price jumps if the server has been idle
        elapsed = min(elapsed, 300.0) 
        if elapsed < 0.1:
            return
            
        for ticker, info in self.stocks_info.items():
            vol = info['volatility']
            current = self.prices[ticker]
            
            # Simple random walk scaling with elapsed time
            # Drift is slightly positive (0.0001) to simulate general market uptrend
            drift = 0.00005 * elapsed
            shock = vol * math.sqrt(elapsed) * random.normalvariate(0, 1)
            new_price = current * (1 + drift + shock)
            
            # Ensure price doesn't fall below $1.00
            self.prices[ticker] = round(max(new_price, 1.0), 2)

    def get_market_summary(self):
        """Get the latest prices and 24h percent change for all stocks."""
        self.update_prices()
        summary = []
        for ticker, info in self.stocks_info.items():
            current_price = self.prices[ticker]
            # Yesterday's close is the last element in the historical daily data
            yesterday_price = self.daily_history[ticker][-1]
            change = current_price - yesterday_price
            change_pct = (change / yesterday_price) * 100
            
            summary.append({
                'ticker': ticker,
                'name': info['name'],
                'price': current_price,
                'change': round(change, 2),
                'change_pct': round(change_pct, 2)
            })
        return summary

    def get_stock_details(self, ticker):
        """Get current price, history, and calculated technical indicators for a ticker."""
        self.update_prices()
        if ticker not in self.stocks_info:
            return None
            
        current_price = self.prices[ticker]
        # Copy history and append current price as today's live price
        full_history = self.daily_history[ticker].copy()
        full_history.append(current_price)
        
        # Take the last 30 data points for plotting
        plot_prices = full_history[-30:]
        
        # Calculate technical indicators for the plotted range (using full_history to support lagging indices)
        sma_10 = self._calculate_sma(full_history, 10)[-30:]
        sma_20 = self._calculate_sma(full_history, 20)[-30:]
        ema_12 = self._calculate_ema(full_history, 12)[-30:]
        ema_26 = self._calculate_ema(full_history, 26)[-30:]
        rsi_14 = self._calculate_rsi(full_history, 14)[-30:]
        macd_line, signal_line, macd_hist = self._calculate_macd(full_history)
        macd_line = macd_line[-30:]
        signal_line = signal_line[-30:]
        macd_hist = macd_hist[-30:]

        # Get latest indicator values for summary cards
        latest_rsi = rsi_14[-1] if rsi_14 else 50
        latest_macd = macd_line[-1] if macd_line else 0
        latest_signal = signal_line[-1] if signal_line else 0
        latest_sma10 = sma_10[-1] if sma_10 else current_price
        latest_sma20 = sma_20[-1] if sma_20 else current_price

        # Recommendation logic based on indicators
        recommendation = "HOLD"
        reco_reason = "Indicators are in neutral territory."
        if latest_rsi < 30:
            recommendation = "BUY"
            reco_reason = f"RSI is oversold ({latest_rsi:.1f}). Potential rebound."
        elif latest_rsi > 70:
            recommendation = "SELL"
            reco_reason = f"RSI is overbought ({latest_rsi:.1f}). Potential pullback."
        elif latest_macd > latest_signal and current_price > latest_sma10:
            recommendation = "BUY"
            reco_reason = "Bullish MACD crossover and price above 10-day SMA."
        elif latest_macd < latest_signal and current_price < latest_sma10:
            recommendation = "SELL"
            reco_reason = "Bearish MACD crossover and price below 10-day SMA."

        return {
            'ticker': ticker,
            'name': self.stocks_info[ticker]['name'],
            'current_price': current_price,
            'prices': plot_prices,
            'sma_10': sma_10,
            'sma_20': sma_20,
            'ema_12': ema_12,
            'ema_26': ema_26,
            'rsi_14': rsi_14,
            'macd': macd_line,
            'macd_signal': signal_line,
            'macd_hist': macd_hist,
            'latest_rsi': round(latest_rsi, 2),
            'latest_macd': round(latest_macd, 2),
            'latest_signal': round(latest_signal, 2),
            'recommendation': recommendation,
            'reco_reason': reco_reason
        }

    # --- Technical Indicator Math Helpers ---

    def _calculate_sma(self, data, period):
        """Calculate Simple Moving Average."""
        sma = []
        for i in range(len(data)):
            if i < period - 1:
                sma.append(data[i])  # Fallback to current price if not enough data
            else:
                window = data[i - period + 1 : i + 1]
                sma.append(round(sum(window) / period, 2))
        return sma

    def _calculate_ema(self, data, period):
        """Calculate Exponential Moving Average."""
        ema = []
        alpha = 2 / (period + 1)
        for i in range(len(data)):
            if i == 0:
                ema.append(data[0])
            else:
                val = data[i] * alpha + ema[-1] * (1 - alpha)
                ema.append(round(val, 2))
        return ema

    def _calculate_rsi(self, data, period=14):
        """Calculate Relative Strength Index."""
        rsi = [50] * len(data) # Default neutral RSI for early values
        if len(data) < period + 1:
            return rsi

        # First RSI
        gains = []
        losses = []
        for i in range(1, period + 1):
            diff = data[i] - data[i-1]
            gains.append(diff if diff > 0 else 0)
            losses.append(-diff if diff < 0 else 0)

        avg_gain = sum(gains) / period
        avg_loss = sum(losses) / period
        
        if avg_loss == 0:
            rsi[period] = 100
        else:
            rs = avg_gain / avg_loss
            rsi[period] = round(100 - (100 / (1 + rs)), 2)

        # Subsequent RSIs
        for i in range(period + 1, len(data)):
            diff = data[i] - data[i-1]
            gain = diff if diff > 0 else 0
            loss = -diff if diff < 0 else 0
            
            avg_gain = (avg_gain * (period - 1) + gain) / period
            avg_loss = (avg_loss * (period - 1) + loss) / period
            
            if avg_loss == 0:
                rsi[i] = 100
            else:
                rs = avg_gain / avg_loss
                rsi[i] = round(100 - (100 / (1 + rs)), 2)
        return rsi

    def _calculate_macd(self, data):
        """Calculate MACD Line, Signal Line, and Histogram."""
        ema12 = self._calculate_ema(data, 12)
        ema26 = self._calculate_ema(data, 26)
        
        macd_line = []
        for e12, e26 in zip(ema12, ema26):
            macd_line.append(round(e12 - e26, 2))
            
        # Signal Line (9-period EMA of MACD Line)
        signal_line = self._calculate_ema(macd_line, 9)
        
        # Histogram
        macd_hist = []
        for ml, sl in zip(macd_line, signal_line):
            macd_hist.append(round(ml - sl, 2))
            
        return macd_line, signal_line, macd_hist

# Instantiate global simulator object
simulator = StockSimulator()
