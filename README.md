# Finance: Full Stack Web App using Flask and SQLite
### Homework from [Harvard's Introduction to Computer Science CS50 hosted on eDX](https://www.edx.org/course/cs50s-introduction-to-computer-science)
### 🎓 [Web Track](https://cs50.harvard.edu/x/2020/tracks/web/)
- [Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/): Web application via which you can manage portfolios of stocks. This tool allows you to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying [IEX](iexcloud.io/) for stocks’ prices.
- I wrote all the code in the templates directory. I wrote most of the code in application.py. The remaining files were provided by the instructor.

## Table of Contents
-	[Technologies](#technologies)
-	[Features](#features)
- [Lessons Learned](#lessons-learned)
-	[Project Status](#project-status)
-	[Getting Started](#getting-started)
-	[Tests](#tests)
-	[Acknowledgments](#acknowledgments)
-	[License](#license)

## 🛠 Technologies
|Graphic Design|Front-End|Back-End|Database|Deployment|Testing|
|------------- | ------- | ------ | ------ | -------- | -------|
|Adobe XD	    |HTML5	  |Python3  |SQLite  |Heroku	   |Jasmine|
|.			        |CSS3		  |[Flask](https://flask.palletsprojects.com/en/1.1.x/)   |[SQL Alchemy](https://www.sqlalchemy.org/)|.      |Lighthouse|
|.			        |Bootstrap 4|[Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)	|[Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)	  |Git		   |.|
|.			        |[Jinja](https://jinja.palletsprojects.com/en/2.11.x/)    |.		   |.		    |.		     |.|

## ⚙️ Features
-	Login, sign-up
-	REST API (create, read, update) for stocks
- Security to prevent certain transactions. Look out for the angry cat!
-	[IEX API](iexcloud.io/)

## 💡Lessons Learned
- Database design and Create, Read, Update in SQL
- Rewrote the entire application to use Flask SQL Alchemy
- Using Flask as a server-side framework
- Python Class/Models and Schemas
- Jinja templating
- Password hashing using Werkzeug
- Parsing data from API
- Parsing data from SQL queries
- Calculations using data from API and database

## ✅ Project Status
-	Add tests

## 🚀 Getting Started
To run this project locally:
- In your terminal, navigate to the root project directory and run the following commands
- To install the dependencies
```
$ pipenv install
```
- You'll need to register for an API key in order to be able to query IEX’s data
- [Register](iexcloud.io/cloud-login#/register/) for an account
- Enter your email address and a password, and click “Create account”
- On the next page, scroll down to choose the Start (free) plan
- Once you’ve confirmed your account via a confirmation email, sign in to iexcloud.io
- Click API Tokens
- Copy the key that appears under the Token column (it should begin with pk_)
```
$ export API_KEY=value
```
- To start the web server, execute (without debugging):
```
$ python application.py 
```
- Alternatively, execute (without debugging):
```
$ export FLASK_APP=application.py
$ flask run
```
## 📐 Tests


## 🔒 License
Copyright Notice and Statement: currently not offering any license. Permission only to view and download.