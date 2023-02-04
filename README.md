<div align="center">
  <img width="200" src="static/favicon/android-chrome-512x512.png" alt="Wall Street Trader logo">

# [Finance: Full Stack Web App using Flask and SQL](http://wallstreettrader.app/)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://flask-env.eba-z6mwdiua.us-west-2.elasticbeanstalk.com/)
![Security Headers](https://img.shields.io/security-headers?url=http%3A%2F%2Fflask-env.eba-z6mwdiua.us-west-2.elasticbeanstalk.com%2F)
[![Build Status](https://travis-ci.org/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL.svg?branch=master)](https://travis-ci.org/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/323b83dec4c44b78bde6a4b2aa3477ec)](https://www.codacy.com/gh/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL&amp;utm_campaign=Badge_Grade)
[![Updates](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/shield.svg)](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/)
[![Python 3](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/python-3-shield.svg)](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/)
</div>

## Homework from [Harvard's Introduction to Computer Science CS50 hosted on eDX](https://www.edx.org/course/cs50s-introduction-to-computer-science) 🎓 [Web Track](https://cs50.harvard.edu/x/2020/tracks/web/) - [Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/)


## 🚀 Getting Started
### To run this project on your system:
-   Ensure that `python3` and `python3-pip` are installed on your system
-   In your terminal, navigate to the root project directory and run the following commands
-   Activate the virtual environment
```
$ pipenv shell
```
-   Install the dependencies
```
$ pipenv install -r requirements.txt
```
-   You'll need to register for an API key in order to be able to query IEX’s data
	-   [Register](iexcloud.io/cloud-login#/register/) for an account
	-   Enter your email address and a password, and click “Create account”
	-   On the next page, scroll down to choose the Start (free) plan
	-   Once you’ve confirmed your account via a confirmation email, sign in to iexcloud.io
	-   Click API Tokens
	-   Copy the key that appears under the Token column (it should begin with pk_) into the `<value>` in the next step
-   Create a .env file and paste the following into it: `API_KEY=<value>`
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
-   To initialize the SQL database within application.py, add `db.create_all()` below `Initialize Schemas`. Once the code runs and the you've verified the database exists, remove `db.create_all()`
-   To initialize the SQL database in the python shell, execute:
```
$ python
$ from application import db
$ db.create_all()
```
-   To initialize the database with SQL command-line arguemnts (using MySQL syntax) run each `CREATE TABLE` command (one at a time):
```
CREATE TABLE users (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	username VARCHAR(50) UNIQUE, 
	hash VARCHAR(200) NOT NULL, 
	cash INTEGER
);
CREATE TABLE portfolio (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	user_id INTEGER, 
	symbol VARCHAR(5), 
	current_shares INTEGER
);
CREATE TABLE bought (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	buyer_id INTEGER, 
	time VARCHAR(100), 
	symbol VARCHAR(5), 
	shares_bought INTEGER, 
	price_bought FLOAT
);
CREATE TABLE sold (
	id INTEGER PRIMARY KEY AUTO_INCREMENT,
	seller_id INTEGER, 
	time VARCHAR(100), 
	symbol VARCHAR(5), 
	shares_sold INTEGER, 
	price_sold FLOAT
);
```

## 📣 Attribution
-   Stock prices pulled from [IEX Stock Quote API](https://iexcloud.io/docs/api/#quote)
-   Hat icon made by [Alice Noir](https://thenounproject.com/AliceNoir/) from [the Noun Project](https://thenounproject.com/icon/pirate-hat-4121754/)
-   Feather icon made by [Jacopo Mencacci](https://thenounproject.com/jacopoPaper/) from [the Noun Project](https://thenounproject.com/icon/feather-10683/)
-   Illustrations by [Freepik Storyset](https://storyset.com/people/rafiki)

## 🔒 License
Copyright Notice and Statement: currently not offering any license. Permission only to view and download. Refer to [choose a license](https://choosealicense.com/no-permission/) for more info.
