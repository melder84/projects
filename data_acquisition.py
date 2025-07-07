import requests

API_KEY = 'YOUR_API_KEY'

def fetch_news_data(api_key, query):
    url = f'https://newsapi.org/v2/everything?q={query}&apiKey={api_key}'
    response = requests.get(url)
    data = response.json()
    return data['articles']

def fetch_stock_data(symbol, function='TIME_SERIES_DAILY'):
    params = {
        'function': function,
        'symbol': symbol,
        'apikey': API_KEY
    }
    response = requests.get(f'https://www.alphavantage.co/query', params=params)
    data = response.json()
    return data

def fetch_previous_day_close(symbol):
    data = fetch_stock_data(symbol)
    last_close = float(list(data['Time Series (Daily)'].values())[0]['4. close'])
    return last_close

def fetch_premarket_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    response = requests.get(f'https://www.alphavantage.co/query', params=params)
    data = response.json()
    return data
