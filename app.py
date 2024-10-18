from flask import Flask, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import requests
import pandas as pd

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'your_secret_key'

# Configure the database URI (use SQLite for this example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)

# Define the Users model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    cash = db.Column(db.Float, default=10000)

# Define the Portfolio model
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    current_shares = db.Column(db.Integer, nullable=False)

# Define the Sold model
class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares_sold = db.Column(db.Integer, nullable=False)
    price_sold = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(20), nullable=False)

# Define the Bought model
class Bought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares_bought = db.Column(db.Integer, nullable=False)
    price_bought = db.Column(db.Float, nullable=False)
    time = db.Column(db.String(20), nullable=False)

# Alpha Vantage API function to get stock data
API_KEY = 'your_alpha_vantage_api_key'

def lookup(symbol):
    """Look up stock price for a given symbol using Alpha Vantage API."""
    base_url = 'https://www.alphavantage.co/query'
    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'apikey': API_KEY,
        'outputsize': 'compact'
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    # Handle missing data case
    if 'Time Series (Daily)' not in data:
        return None

    # Extract stock price data
    time_series = data['Time Series (Daily)']
    latest_day = list(time_series.keys())[0]
    stock_price = float(time_series[latest_day]['4. close'])
    return {'symbol': symbol, 'price': stock_price}

def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

# Route to sell stocks
@app.route("/sell", methods=["GET", "POST"])
def sell():
    user = session.get("user_id")

    if request.method == "GET":
        symbol_list = Portfolio.query.filter_by(user_id=user).all()
        if not symbol_list:
            return render_template("sell.html", symbol_list_length=0)
        return render_template("sell.html", symbol_list=symbol_list, symbol_list_length=len(symbol_list))

    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        if not symbol or shares <= 0:
            return errorPage("Invalid Data", "Please enter valid stock and shares.", "400.svg")

        portfolio_entry = Portfolio.query.filter_by(user_id=user, symbol=symbol).first()
        if not portfolio_entry or portfolio_entry.current_shares < shares:
            return errorPage("Forbidden", "You don't own enough shares.", "403.svg")

        stock_price = lookup(symbol).get('price')
        total_sale_value = stock_price * shares
        portfolio_entry.current_shares -= shares
        if portfolio_entry.current_shares == 0:
            db.session.delete(portfolio_entry)
        db.session.commit()

        user_data = Users.query.filter_by(id=user).first()
        user_data.cash += total_sale_value
        db.session.commit()

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sale_log = Sold(seller_id=user, time=now, symbol=symbol, shares_sold=shares, price_sold=stock_price)
        db.session.add(sale_log)
        db.session.commit()

        return render_template("sold.html", symbol=symbol, shares=shares, total=usd(total_sale_value))

# Route to buy stocks
@app.route("/buy", methods=["GET", "POST"])
def buy():
    if request.method == "GET":
        return render_template("buy.html")

    try:
        symbol = request.form.get("symbol").upper()
        shares = int(request.form.get("shares"))

        if not symbol or shares <= 0:
            return errorPage("Invalid Data", "Invalid stock symbol or shares.", "400.svg")

        stock = lookup(symbol)
        if not stock:
            return errorPage("Invalid Stock", "Please enter a valid stock symbol.", "400.svg")

        price = stock.get('price')
        user_id = session["user_id"]
        user_data = Users.query.filter_by(id=user_id).first()
        total_cost = price * shares
        if user_data.cash < total_cost:
            return errorPage("Insufficient Funds", "Not enough funds for this purchase.", "403.svg")

        user_data.cash -= total_cost
        portfolio_entry = Portfolio.query.filter_by(user_id=user_id, symbol=symbol).first()

        if not portfolio_entry:
            portfolio_entry = Portfolio(user_id=user_id, symbol=symbol, current_shares=shares)
            db.session.add(portfolio_entry)
        else:
            portfolio_entry.current_shares += shares
        db.session.commit()

        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        log = Bought(buyer_id=user_id, time=now, symbol=symbol, shares_bought=shares, price_bought=price)
        db.session.add(log)
        db.session.commit()

        return render_template("bought.html", symbol=symbol, shares=shares, total=usd(total_cost))

    except Exception as e:
        db.session.rollback()
        return errorPage("Transaction Failed", str(e), "500.svg")

# Error handling function
def errorPage(title, info, file):
    return render_template("error.html", title=title, info=info, file=file)

if __name__ == "__main__":
    app.run(debug=True)
