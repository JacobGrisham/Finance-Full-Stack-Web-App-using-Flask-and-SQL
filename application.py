import os
import redis
from datetime import datetime
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import errorPage, login_required, lookup, usd
from dotenv import load_dotenv


load_dotenv()
os.environ["API_KEY"] = "f8c4f7effd7c4ad3aa15ca14e35523d4"
API_KEY="f8c4f7effd7c4ad3aa15ca14e35523d4"

application = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


application.config["TEMPLATES_AUTO_RELOAD"] = True


@application.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


application.jinja_env.filters["usd"] = usd


application.secret_key = 'BAD_SECRET_KEY'
application.config['SESSION_TYPE'] = 'redis'
application.config['SESSION_PERMANENT'] = False
application.config['SESSION_USE_SIGNER'] = True
application.config['SESSION_REDIS'] = redis.from_url('redis://localhost:6379')

server_session = Session(application)


application.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'finances.db')
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(application)


ma = Marshmallow(application)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(length=50))
    hash = db.Column(db.String(length=200))
    cash = db.Column(db.Integer)
    
    def __init__(self, username, hash, cash):
        self.username = username
        self.hash = hash
        self.cash = cash
class Portfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    symbol = db.Column(db.String(length=5))
    current_shares = db.Column(db.Integer)
    
    def __init__(self, user_id, symbol, current_shares):
        self.user_id = user_id
        self.symbol = symbol
        self.current_shares = current_shares
class Bought(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer_id = db.Column(db.Integer)
    time = db.Column(db.String(length=100))
    symbol = db.Column(db.String(length=5))
    shares_bought = db.Column(db.Integer)
    price_bought = db.Column(db.Float)
    
    def __init__(self, buyer_id, time, symbol, shares_bought, price_bought):
        self.buyer_id = buyer_id
        self.time = time
        self.symbol = symbol
        self.shares_bought = shares_bought
        self.price_bought = price_bought
class Sold(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer)
    time = db.Column(db.String(length=100))
    symbol = db.Column(db.String(length=5))
    shares_sold = db.Column(db.Integer)
    price_sold = db.Column(db.Float)
    
    def __init__(self, seller_id, time, symbol, shares_sold, price_sold):
        self.seller_id = seller_id
        self.time = time
        self.symbol = symbol
        self.shares_sold = shares_sold
        self.price_sold = price_sold


class UsersSchema(ma.Schema):
    class Meta:
        fields = ('username', 'cash')
class PortfolioSchema(ma.Schema):
    class Meta:
        fields = ('symbol', 'current_shares')
class BoughtSchema(ma.Schema):
    class Meta:
        fields = ('time', 'symbol', 'shares_bought', 'price_bought')
class SoldSchema(ma.Schema):
    class Meta:
        fields = ('time', 'symbol', 'shares_sold', 'price_sold')
        

users_schema = UsersSchema
portfolio_schema = PortfolioSchema(many=True)
bought_schema = BoughtSchema(many=True)
sold_schema = SoldSchema(many=True)


os.environ.get("API_KEY")

def new_func():
    raise RuntimeError("API_KEY not set")

if not os.environ.get("API_KEY"):
    new_func()

@application.route("/")
def landing():
    return render_template("landing.html")

@application.route("/home")
@login_required
def index():
    
    user = session["user_id"]
    print("user: ", user)

    
    available = (Users.query.filter_by(id = user).first()).cash
    print("available: ", available)

    
    symbol_list = Portfolio.query.filter_by(user_id = user).all()
    print("symbol list: ", symbol_list)

    
    if symbol_list == []:
        return render_template("index.html", available = usd(available), grand_total = usd(available),  total = [], shares = [], price = [], symbols = [], symbol_list_length = 0)
   
    else:
        
        symbol_list_length = len(symbol_list)
        print("symbol_list_length: ", symbol_list_length)

        
        symbols = []
        price = []
        shares = []
        total = []
        
        for i in range(len(symbol_list)):
            symbol_index = symbol_list[i].symbol
            print("symbol_index:", symbol_index)
            symbols.append(symbol_index)
            
            price_index = float(lookup(symbol_index).get('price'))
            print("price_index:", price_index)
            price.append(price_index)
           
            shares_list = Portfolio.query.filter_by(user_id = user, symbol = symbol_index).all()
            print("shares_list:", shares_list)
            
            for i in range(len(shares_list)):
                share_index = shares_list[i].current_shares
                print("share_index:", share_index)
                shares.append(share_index)
           
            calc = share_index * price_index
            print("calc:", calc)
            total.append(calc)
        print("symbols:", symbols)
        print("price:", price)
        print("shares:", shares)
        print("total:", total)
        
        grand_total = sum(total) + available

        
        return render_template("index.html", symbol_list = symbol_list, symbol_list_length = symbol_list_length, shares = shares, price = price, total = total, available = usd(available), grand_total = usd(grand_total))


@application.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    if request.method == "GET":
        return render_template("buy.html")
    else:
        symbol = request.form.get("symbol").upper()

        
        if not symbol:
            return errorPage(title="No Data", info = "Please enter a stock symbol, i.e. AMZN", file = "no-data.svg")
        result = lookup(symbol)
        if result == None:
             return errorPage(title = "Bad Request", info = "Please enter a valid stock symbol", file="animated-400.svg")
        shares = int(request.form.get("shares"))
        if symbol == None:
            return errorPage(title="No Data", info = "Please enter number of shares", file = "no-data.svg")
        if shares < 0:
             return errorPage(title = "Bad Request", info = "Please enter a positive number", file="animated-400.svg")
        if shares == 0:
             return errorPage(title="No Data", info = "Transaction will not proceed", file = "no-data.svg")

        
        user = session["user_id"]
        print("user:", user)

        
        available = (Users.query.filter_by(id = user).first()).cash
        print("available:", available)

        
        price = lookup(symbol).get('price')
        print("price:", price)

        
        total = shares * price
        
       
        if available < total:
             return errorPage(title="Forbidden", info = "Insufficient funds to complete transaction", file="animated-403.svg")
        
       
        remaining = available - total

       
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")

        
        update_cash = Users.query.filter_by(id = user).first()
        update_cash.cash = remaining
        db.session.commit()
       
       
        log_purchase = Bought(user, time, symbol, shares, price)
        db.session.add(log_purchase)
        db.session.commit()
        

        
        portfolio = Portfolio.query.filter(Portfolio.user_id == user, Portfolio.symbol == symbol).first()
        print("portfolio", portfolio)

       
        if portfolio == None:
            db.session.add(Portfolio(user, symbol, shares))
            db.session.commit()
            
        else:
            stock_owned = portfolio.symbol
            print("stock_owned", stock_owned)
            
            current_shares = portfolio.current_shares
            print("current shares", current_shares)
            

    
            new_shares = shares + current_shares
            print("Total shares now:", new_shares)

            
            portfolio.current_shares = new_shares
            print("Update db with new total:", portfolio.current_shares)
            db.session.commit()
            

        return render_template("bought.html", symbol = symbol, shares = shares, total = usd(total))


@application.route("/history")
@login_required
def history():
    
    user = session["user_id"]

    
    bought_list = Bought.query.filter_by(buyer_id = user).all()
    print("bought_list:", bought_list)
    

    
    if bought_list == []:
        
        return render_template("history.html", bought_list_length = 0, bought_list = [], sold_list_length = 0, sold_list = [])
        
    
    else:
    
        sold_list = Sold.query.filter_by(seller_id = user).all()
        print("sold_list:", sold_list)
       

       
        bought_list_length = len(bought_list)
        sold_list_length = len(sold_list)

        return render_template("history.html", bought_list = bought_list, sold_list = sold_list, bought_list_length = bought_list_length, sold_list_length = sold_list_length)


@application.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    
    session.clear()

    
    if request.method == "POST":

        
        if not request.form.get("username"):
            return errorPage(title="No Data", info = "Must provide username", file = "no-data.svg")

        
        elif not request.form.get("password"):
            return errorPage(title="No Data", info = "Must provide password", file = "no-data.svg")

        
        rows = Users.query.filter_by(username=request.form.get("username")).first()
        

        
        try:
            rows.username

        
        except AttributeError:
             return errorPage(title="No Data", info = "User doesn't exist", file = "no-data.svg")

        
        else:
            
            if rows.username != request.form.get("username") or not check_password_hash(rows.hash, request.form.get("password")):
                return errorPage(title = "Unauthorized", info = "invalid username and/or password", file="animated-401.svg")

            
            session["user_id"] = rows.id

            
            return redirect("/home")

    
    else:
        return render_template("login.html")


@application.route("/logout")
def logout():
    """Log user out"""

    
    session.clear()

    
    return redirect("/")


@application.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "GET":
        return render_template("quote.html")
    else:
        symbol = request.form.get("symbol")
        data = lookup(symbol)
        
        if not symbol:
            return errorPage(title="No Data", info = "Please enter a stock symbol, i.e. AMZN", file = "no-data.svg")
        if data == None:
            return errorPage(title = "Bad Request", info = "Please enter a valid stock symbol", file="animated-400.svg")
        return render_template("quoted.html", data = data)


@application.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        
        username = request.form.get("username")

        
        if not username:
            return errorPage(title="No Data", info = "Please enter a username", file = "no-data.svg")

        existing = Users.query.filter_by(username=username)
        print("EXISTING USER: ", existing)
        
        if existing == username:
            print("EXISTING USER ALREADY!: ", existing)
            return errorPage(title="Forbidden", info = "Username already taken", file="animated-403.svg")
        password = request.form.get("password")
        if not password:
            return errorPage(title="No Data", info = "Please enter a password", file = "no-data.svg")
        confirmation = request.form.get("confirmation")
        if password != confirmation:
            return errorPage(title = "Unauthorized", info = "Passwords do not match", file="animated-401.svg")
        hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=8)

        
        cash = 10000

        
        db.session.add(Users(username, hashed, cash))
        db.session.commit()
        

        
        rows = Users.query.filter_by(username=request.form.get("username")).first()
        session["user_id"] = rows.id

        
        return redirect("/home")


@application.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    
    user = session["user_id"]

    if request.method == "GET":
        
        symbol_list = Portfolio.query.filter_by(user_id = user).all()
        

        
        if symbol_list == []:
            return render_template("sell.html", symbol_list_length = 0)
        
        else:
            symbol_list_length = len(symbol_list)
            
            return render_template("sell.html", symbol_list = symbol_list, symbol_list_length = symbol_list_length)
    else:
        
        symbol = request.form.get("symbol")

        
        if symbol == '':
            return errorPage(title="Forbidden", info = "Must own stock before selling", file="animated-403.svg")

        
        shares = int(request.form.get("shares"))

        
        if not shares:
             return errorPage(title="No Data", info = "Please enter number of shares", file = "no-data.svg")
        if shares < 0:
             return errorPage(title = "Bad Request", info = "Please enter a positive number", file="animated-400.svg")
        if shares == 0:
             return errorPage(title="No Data", info = "Transaction will not proceed", file = "no-data.svg")

        
        shares_held_list = Portfolio.query.filter(Portfolio.user_id == user, Portfolio.symbol == symbol).first()
        
        print("shares_held_list:", shares_held_list)

        
        shares_held = shares_held_list.current_shares
        print("shares_held:", shares_held)

        
        if shares > shares_held:
            return errorPage(title="Forbidden", info = "Unable to sell more than you have", file="animated-403.svg")

        
        available = (Users.query.filter_by(id = user).first()).cash
       

        
        price = lookup(symbol).get('price')

       
        updated_shares = shares_held - shares

        
        portfolio = Portfolio.query.filter(Portfolio.user_id == user, Portfolio.symbol == symbol).first()
        print("portfolio", portfolio)
        portfolio.current_shares = updated_shares
        print("Update db with new total:", portfolio.current_shares)
        db.session.commit()
        

       
        total = available + (price * shares)

       
        update_cash = Users.query.filter_by(id = user).first()
        update_cash.cash = total
        db.session.commit()
        
        now = datetime.now()
        time = now.strftime("%d/%m/%Y %H:%M:%S")

    
        log_sale = Sold(user, time, symbol, shares, price)
        db.session.add(log_sale)
        db.session.commit()
        
        return render_template("sold.html", shares = shares, symbol = symbol.upper())

@application.errorhandler(404)
def page_not_found(e):

    return render_template('404.html'), 404


if __name__ == '__main__':
    application.run(host='0.0.0.0')
