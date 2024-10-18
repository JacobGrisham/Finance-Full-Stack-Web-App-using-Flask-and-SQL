from flask import Flask, render_template, request, session
import requests
import pandas as pd
import numpy as np
import alpaca_trade_api as tradeapi
import backtrader as bt
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_KEY_ALPHA_VANTAGE = 'your_alpha_vantage_api_key'
ALPACA_API_KEY = 'your_alpaca_api_key'
ALPACA_API_SECRET = 'your_alpaca_secret_key'
ALPACA_BASE_URL = 'https://paper-api.alpaca.markets'

# Alpaca API for trade execution
alpaca_api = tradeapi.REST(ALPACA_API_KEY, ALPACA_API_SECRET, ALPACA_BASE_URL, api_version='v2')

# Function to get stock data from Alpha Vantage
def get_stock_data(symbol, interval='1min', outputsize='compact'):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={API_KEY_ALPHA_VANTAGE}&outputsize={outputsize}'
    response = requests.get(url)
    data = response.json()
    df = pd.DataFrame.from_dict(data['Time Series (1min)'], orient='index')
    df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df.astype(float)
    return df

# Simple Moving Average (SMA) Strategy
def sma_strategy(df, short_window=50, long_window=200):
    df['short_mavg'] = df['Close'].rolling(window=short_window, min_periods=1).mean()
    df['long_mavg'] = df['Close'].rolling(window=long_window, min_periods=1).mean()
    df['signal'] = 0
    df['signal'][short_window:] = np.where(df['short_mavg'][short_window:] > df['long_mavg'][short_window:], 1, 0)
    df['positions'] = df['signal'].diff()
    return df

# Route for stock trading strategy
@app.route("/quantitative_trading", methods=["GET", "POST"])
def quantitative_trading():
    if request.method == "POST":
        symbol = request.form.get("symbol").upper()
        short_window = int(request.form.get("short_window", 50))
        long_window = int(request.form.get("long_window", 200))

        # Get stock data
        df = get_stock_data(symbol)
        df = sma_strategy(df, short_window, long_window)

        # Display the trading signals (buy/sell points)
        return render_template("trading_result.html", df=df.to_html(), symbol=symbol)

    return render_template("quantitative_trading.html")

# Route to execute a trade using Alpaca API
@app.route("/trade", methods=["POST"])
def trade():
    symbol = request.form.get("symbol").upper()
    qty = int(request.form.get("qty"))
    side = request.form.get("side")  # "buy" or "sell"
    
    try:
        alpaca_api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        return f"Successfully placed a {side} order for {qty} shares of {symbol}"
    except Exception as e:
        return f"Error placing order: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
