import yfinance as yf
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Parameters
volume_threshold = 1.2  # 20% increase
price_increase_threshold = 1.05  # 5% increase
update_interval = 300  # 5 minutes in seconds

# Stock list (for example, top 100 NYSE stocks)
stocks = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'FB']  # Add more tickers as needed

def get_stock_data(ticker):
    stock = yf.Ticker(ticker)
    hist = stock.history(period="5d")
    return hist

def check_volume_and_price(hist):
    if len(hist) < 21:
        return False
    
    avg_volume = hist['Volume'][:-1].mean()
    latest_volume = hist['Volume'].iloc[-1]
    previous_close = hist['Close'].iloc[-2]
    latest_close = hist['Close'].iloc[-1]

    volume_surge = latest_volume / avg_volume
    price_increase = latest_close / previous_close

    return volume_surge >= volume_threshold and price_increase >= price_increase_threshold

def scan_market():
    result = []
    for ticker in stocks:
        try:
            hist = get_stock_data(ticker)
            if check_volume_and_price(hist):
                result.append(ticker)
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    return result

if __name__ == "__main__":
    while True:
        print(f"Scanning market at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        tickers = scan_market()
        print("Stocks meeting criteria:", tickers)
        time.sleep(update_interval)
