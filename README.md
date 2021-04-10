# [Finance: Full Stack Web App using Flask and SQL](http://flask-env.eba-z6mwdiua.us-west-2.elasticbeanstalk.com/)
[![Build Status](https://travis-ci.org/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL.svg?branch=master)](https://travis-ci.org/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/323b83dec4c44b78bde6a4b2aa3477ec)](https://www.codacy.com/gh/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL&amp;utm_campaign=Badge_Grade)
[![Updates](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/shield.svg)](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/)
[![Python 3](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/python-3-shield.svg)](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/)
## Homework from [Harvard's Introduction to Computer Science CS50 hosted on eDX](https://www.edx.org/course/cs50s-introduction-to-computer-science)
## 🎓 [Web Track](https://cs50.harvard.edu/x/2020/tracks/web/)
-   [Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/): Web application via which you can manage portfolios of stocks. This tool allows you to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying [IEX](iexcloud.io/) for stocks’ prices.
-   I wrote all the code in the templates directory. I wrote most of the code in application.py. Some of the code in helpers.py was provided by instructor
-   I styled the application myself, with illustrations provided by [Freepik](http://www.freepik.com/). Landing page and favicon cloned after [Robinhood](https://robinhood.com/us/en/)

![Finance Program Demo](img/demo.gif)

## 🖥 [Live Application](http://flask-env.eba-z6mwdiua.us-west-2.elasticbeanstalk.com/)

## Table of Contents
-   [Technologies](#technologies)
-   [Features](#features)
-   [Lessons Learned](#lessons-learned)
-   [Project Status](#project-status)
-   [Getting Started](#getting-started)
-   [Tests](#tests)
-   [Attribution](#attribution)
-   [License](#license)

## 🛠 Technologies
|Graphic Design|Front-End|Back-End|Database|Deployment|Testing|
|------------- | ------- | ------ | ------ | -------- | -------|
|Inkscape	    |HTML5	  |Python3  |SQLite and MySQL  |[AWS Elastic Beanstalk]()	   |Pytest|
|.			      |CSS3		  |[Flask](https://flask.palletsprojects.com/en/1.1.x/)   |[SQL Alchemy](https://www.sqlalchemy.org/)|[AWS RDS](https://aws.amazon.com/rds/)      |Lighthouse|
|.			        |Bootstrap 4|[Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)	|[Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)	  |Git		   |.|
|.			        |[Jinja](https://jinja.palletsprojects.com/en/2.11.x/)    |.		   |.		    |.		     |.|

## ⚙️ Features
-   Login, sign-up
-	  Create, Read, and Update for stocks
-   Security to prevent certain transactions using error codes 400-404

## 💡Lessons Learned
-   Database design and Create, Read, Update in SQL
-   Rewrote the entire application to use Flask SQL Alchemy
-   Developed MVP of application with SQLite locally and Deployed with MySQL on [RDS](https://aws.amazon.com/rds/) instance
-   Using Flask as a server-side framework
-   Python Class/Models and Schemas
-   Jinja templating
-   Password hashing using Werkzeug
-   Parsing data from API
-   Parsing data from SQL queries
-   Calculations using data from API and database
-   Continous integration and continuous deployment with Travis CI
-   Deploying application to AWS with [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) instance and SQL database to a separate [RDS](https://aws.amazon.com/rds/) instance

## ✅ Project Status
-	  Add tests

## 🚀 Getting Started
To run this project locally:
-   In your terminal, navigate to the root project directory and run the following commands
-   To install the dependencies
```
$ pipenv install -r requirements.txt
```
-   You'll need to register for an API key in order to be able to query IEX’s data
-   [Register](iexcloud.io/cloud-login#/register/) for an account
-   Enter your email address and a password, and click “Create account”
-   On the next page, scroll down to choose the Start (free) plan
-   Once you’ve confirmed your account via a confirmation email, sign in to iexcloud.io
-   Click API Tokens
-   Copy the key that appears under the Token column (it should begin with pk_)
-   Create a .env file and paste the following code into it
```
$ API_KEY=<value>
```
-   To start the web server, execute (without debugging):
```
$ python application.py 
```
-   Alternatively, execute (with debugging):
```
$ export FLASK_APP=application.py
$ flask run
```
-   Lastly, create a SQL database named `finances.db`
-		To initialize the SQL database within application.py, add `db.create_all()` below `Initialize Schemas`. Once the code runs and the you've verified the database exists, remove `db.create_all()`
-   To initialize the SQL database in the python shell, execute:
```
$ python
$ from application import db
$ db.create_all()
```
-   To initialize the database with SQL command-line arguemnts:
```
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	username VARCHAR(50) UNIQUE, 
	hash VARCHAR(200) NOT NULL, 
	cash INTEGER
)
CREATE TABLE portfolio (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	user_id INTEGER, 
	symbol VARCHAR(5), 
	current_shares INTEGER
)
CREATE TABLE bought (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	buyer_id INTEGER, 
	time VARCHAR, 
	symbol VARCHAR(5), 
	shares_bought INTEGER, 
	price_bought FLOAT
)
CREATE TABLE sold (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	seller_id INTEGER, 
	time VARCHAR(100), 
	symbol VARCHAR(5), 
	shares_sold INTEGER, 
	price_sold FLOAT
)
```

## 📐 Tests

## 📣 Attribution
-   Stock prices pulled from [IEX API](iexcloud.io/)
-   Feather icon made by [Freepik](http://www.freepik.com/) from [Flaticon](https://www.flaticon.com/free-icon/feather_105145?term=feather&page=1&position=85&related_item_id=105145)
-   Illustrations by [Freepik Storyset](https://storyset.com/people/rafiki)

## 🔒 License
Copyright Notice and Statement: currently not offering any license. Permission only to view and download.
