import random, time, math

class StockSimulator:
    def __init__(self):
        self.stocks_info = {
            'AAPL': {'name':'Apple Inc.','base_price':175.0,'volatility':0.0015},
            'MSFT': {'name':'Microsoft Corp.','base_price':420.0,'volatility':0.0012},
            'GOOGL': {'name':'Alphabet Inc.','base_price':150.0,'volatility':0.0018},
            'AMZN': {'name':'Amazon.com Inc.','base_price':178.0,'volatility':0.0016},
            'TSLA': {'name':'Tesla Inc.','base_price':170.0,'volatility':0.0030},
            'NVDA': {'name':'NVIDIA Corp.','base_price':850.0,'volatility':0.0035},
            'NFLX': {'name':'Netflix Inc.','base_price':610.0,'volatility':0.0020},
            'META': {'name':'Meta Platforms Inc.','base_price':500.0,'volatility':0.0022},
        }
        self.prices, self.daily_history = {}, {}
        self.last_update_time = time.time()
        self._initialize_market()
    def _initialize_market(self):
        for ticker, info in self.stocks_info.items():
            base=info['base_price']; self.prices[ticker]=base; history=[]; current=base
            rand=random.Random(ticker)
            for _ in range(50):
                change=rand.normalvariate(0.0002, info['volatility']*3)
                current=current*(1-change); history.insert(0, round(max(current,1),2))
            self.daily_history[ticker]=history
    def update_prices(self):
        now=time.time(); elapsed=min(now-self.last_update_time,300.0); self.last_update_time=now
        if elapsed<0.1:return
        for ticker, info in self.stocks_info.items():
            current=self.prices[ticker]; drift=0.00005*elapsed; shock=info['volatility']*math.sqrt(elapsed)*random.normalvariate(0,1)
            self.prices[ticker]=round(max(current*(1+drift+shock),1),2)
    def get_market_summary(self):
        self.update_prices(); out=[]
        for ticker,info in self.stocks_info.items():
            price=self.prices[ticker]; y=self.daily_history[ticker][-1]; change=price-y
            out.append({'ticker':ticker,'name':info['name'],'price':price,'change':round(change,2),'change_pct':round(change/y*100,2)})
        return out
    def _sma(self,data,p): return [data[i] if i<p-1 else round(sum(data[i-p+1:i+1])/p,2) for i in range(len(data))]
    def _ema(self,data,p):
        a=2/(p+1); out=[]
        for i,v in enumerate(data): out.append(v if i==0 else round(v*a+out[-1]*(1-a),2))
        return out
    def _rsi(self,data,p=14):
        out=[50]*len(data)
        if len(data)<p+1:return out
        gains=[]; losses=[]
        for i in range(1,p+1):
            d=data[i]-data[i-1]; gains.append(max(d,0)); losses.append(max(-d,0))
        ag=sum(gains)/p; al=sum(losses)/p; out[p]=100 if al==0 else round(100-100/(1+ag/al),2)
        for i in range(p+1,len(data)):
            d=data[i]-data[i-1]; ag=(ag*(p-1)+max(d,0))/p; al=(al*(p-1)+max(-d,0))/p
            out[i]=100 if al==0 else round(100-100/(1+ag/al),2)
        return out
    def _macd(self,data):
        e12=self._ema(data,12); e26=self._ema(data,26); macd=[round(a-b,2) for a,b in zip(e12,e26)]; sig=self._ema(macd,9); hist=[round(a-b,2) for a,b in zip(macd,sig)]; return macd,sig,hist
    def get_stock_details(self,ticker):
        self.update_prices()
        if ticker not in self.stocks_info:return None
        price=self.prices[ticker]; full=self.daily_history[ticker].copy()+[price]; plot=full[-30:]
        sma10=self._sma(full,10)[-30:]; sma20=self._sma(full,20)[-30:]; ema12=self._ema(full,12)[-30:]; ema26=self._ema(full,26)[-30:]; rsi=self._rsi(full,14)[-30:]; macd,sig,hist=self._macd(full); macd=macd[-30:];sig=sig[-30:];hist=hist[-30:]
        lr=rsi[-1] if rsi else 50; lm=macd[-1] if macd else 0; ls=sig[-1] if sig else 0; lsma=sma10[-1] if sma10 else price
        rec='HOLD'; reason='Indicators are in neutral territory.'
        if lr<30: rec='BUY'; reason=f'RSI is oversold ({lr:.1f}). Potential rebound.'
        elif lr>70: rec='SELL'; reason=f'RSI is overbought ({lr:.1f}). Potential pullback.'
        elif lm>ls and price>lsma: rec='BUY'; reason='Bullish MACD relationship and price above 10-day SMA.'
        elif lm<ls and price<lsma: rec='SELL'; reason='Bearish MACD relationship and price below 10-day SMA.'
        return {'ticker':ticker,'name':self.stocks_info[ticker]['name'],'current_price':price,'prices':plot,'sma_10':sma10,'sma_20':sma20,'ema_12':ema12,'ema_26':ema26,'rsi_14':rsi,'macd':macd,'macd_signal':sig,'macd_hist':hist,'latest_rsi':round(lr,2),'latest_macd':round(lm,2),'latest_signal':round(ls,2),'recommendation':rec,'reco_reason':reason}

simulator=StockSimulator()
