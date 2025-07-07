import requests
import pandas as pd
import schedule
import time
import datetime

# Function to get data from Coinbase
def get_coinbase_data():
    try:
        url = "https://api.coinbase.com/v2/prices/"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data from Coinbase: {e}")
        return []

# Function to get data from Kraken
def get_kraken_data():
    try:
        url = "https://api.kraken.com/0/public/Ticker"
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data from Kraken: {e}")
        return []

# Calculate 20-day average volume
def calculate_20_day_average(symbol, historical_data):
    try:
        df = pd.DataFrame(historical_data)
        df['volume_avg'] = df['volume'].rolling(window=20).mean()
        return df
    except Exception as e:
        print(f"Error calculating 20-day average volume for {symbol}: {e}")
        return pd.DataFrame()

# Filter cryptocurrencies based on volume and price criteria
def filter_cryptos(df):
    try:
        significant_volume = df['volume'] > 1.2 * df['volume_avg']
        price_increase = df['close'] > 1.05 * df['close'].shift(1)
        return df[significant_volume & price_increase]
    except Exception as e:
        print(f"Error filtering cryptocurrencies: {e}")
        return pd.DataFrame()

# Scan for qualifying cryptocurrencies
def scan_cryptos():
    start_time = datetime.datetime.now()
    print(f"Starting scan at {start_time}")
    
    coinbase_data = get_coinbase_data()
    kraken_data = get_kraken_data()
    
    # Combine and analyze data (example structure)
    combined_data = coinbase_data + kraken_data
    if not combined_data:
        print("No data to process.")
        return
    
    df = pd.DataFrame(combined_data)
    
    # Add some debug prints to check data structure
    print(f"Combined data sample: {df.head()}")
    
    # Calculate 20-day averages and apply filters
    df = calculate_20_day_average('symbol', df)
    filtered_df = filter_cryptos(df)
    
    # Display results
    if not filtered_df.empty:
        print(filtered_df[['symbol', 'volume', 'price']])
    else:
        print("No cryptocurrencies met the criteria.")
    
    end_time = datetime.datetime.now()
    duration = end_time - start_time
    print(f"Scan completed in {duration.total_seconds()} seconds")

# Schedule the scan every 5 minutes
schedule.every(5).minutes.do(scan_cryptos)

while True:
    schedule.run_pending()
    time.sleep(1)
