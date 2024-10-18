from flask import Flask, request, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required
from datetime import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
import requests

def lookup(symbol):
    # Example API call to fetch stock data
    # Replace this with your actual API key and URL
    api_key = "c76d1baad138431cb3b5b1989c0c0cfe"
    url = f"https://api.example.com/lookup?symbol={symbol}&apikey={'c76d1baad138431cb3b5b1989c0c0cfe'}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        # Return relevant stock information
        return {
            "symbol": data["symbol"],
            "price": data["latestPrice"],  # Adjust based on your API response structure
            "name": data["companyName"]      # Adjust based on your API response structure
        }
    except Exception as e:
        print(f"Error fetching data for {symbol}: {e}")
        return None

# Step 1: Initialize the application and database
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'  # Update with your actual database URI
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(application)

# Step 2: Define your database models
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cash = db.Column(db.Float, nullable=False)
    # Add other user fields here

class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    current_shares = db.Column(db.Integer, nullable=False)

class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    symbol = db.Column(db.String(10), nullable=False)
    shares_sold = db.Column(db.Integer, nullable=False)
    price_sold = db.Column(db.Float, nullable=False)

# Step 3: Define the sell route
@application.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Obtain user id
    user = session["user_id"]

    if request.method == "GET":
        # Obtain stock symbols that the user possesses
        symbol_list = Portfolio.query.filter_by(user_id=user).all()

        # If user never bought anything, return empty values
        if not symbol_list:
            return render_template("sell.html", symbol_list_length=0)

        # Else display stock symbols in drop-down menu
        symbol_list_length = len(symbol_list)
        return render_template("sell.html", symbol_list=symbol_list, symbol_list_length=symbol_list_length)

    else:
        # Obtain stock symbol and shares from user
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Error handling: Check user entered valid input
        if not symbol:
            return errorPage(title="No Data", info="Please select a stock to sell", file="no-data.svg")
        if shares <= 0:
            return errorPage(title="Invalid Data", info="Number of shares must be a positive integer", file="animated-400.svg")

        # Query portfolio to check how many shares the user holds for the selected stock
        portfolio_entry = Portfolio.query.filter_by(user_id=user, symbol=symbol).first()

        # Check if the user owns the stock
        if not portfolio_entry:
            return errorPage(title="Forbidden", info="You don't own this stock", file="animated-403.svg")

        # Check if user has enough shares to sell
        if portfolio_entry.current_shares < shares:
            return errorPage(title="Forbidden", info="You don't have enough shares to sell", file="animated-403.svg")

        # Get current price of the stock using lookup() API
        stock_price = lookup(symbol).get('price')
        total_sale_value = stock_price * shares

        # Update portfolio: Subtract shares sold
        portfolio_entry.current_shares -= shares
        if portfolio_entry.current_shares == 0:
            # Remove the entry if all shares are sold
            db.session.delete(portfolio_entry)
        db.session.commit()

        # Update user's cash balance
        user_data = Users.query.filter_by(id=user).first()
        user_data.cash += total_sale_value
        db.session.commit()

        # Log the sale in the Sold table
        now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        sale_log = Sold(seller_id=user, time=now, symbol=symbol, shares_sold=shares, price_sold=stock_price)
        db.session.add(sale_log)
        db.session.commit()

        return render_template("sold.html", symbol=symbol, shares=shares, total=usd(total_sale_value))

def errorPage(title, info, file):
    return render_template("error.html", title=title, info=info, file=file)

# Step 4: Error handling (optional)
@application.errorhandler(Exception)
def handle_exception(e):
    # Handle specific HTTPException errors with Flask's default error pages
    if isinstance(e, HTTPException):
        return errorPage(title=f"Error {e.code}", info=e.description, file=f"animated-{e.code}.svg")

    # Otherwise handle as an internal server error
    return errorPage(title="Internal Server Error", info="An unexpected error occurred", file="animated-500.svg")

def usd(value):
    """Format value as USD."""
    if value is None:
        return None  # Handle None value appropriately
    return f"${value:,.2f}"  # Format as currency

# Step 5: Run the application
if __name__ == "__main__":
    application.run(debug=True)
