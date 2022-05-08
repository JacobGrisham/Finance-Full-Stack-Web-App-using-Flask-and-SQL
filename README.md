<div align="center">
  <img width="200" src="static/favicon/android-chrome-512x512.png" alt="Robynhood logo">

# [Finance: Full Stack Web App using Flask and SQL](http://robynhood.app/)
[![Website shields.io](https://img.shields.io/website-up-down-green-red/http/shields.io.svg)](http://flask-env.eba-z6mwdiua.us-west-2.elasticbeanstalk.com/)
![Security Headers](https://img.shields.io/security-headers?url=http%3A%2F%2Fflask-env.eba-z6mwdiua.us-west-2.elasticbeanstalk.com%2F)
[![Build Status](https://travis-ci.org/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL.svg?branch=master)](https://travis-ci.org/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/323b83dec4c44b78bde6a4b2aa3477ec)](https://www.codacy.com/gh/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL&amp;utm_campaign=Badge_Grade)
[![Updates](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/shield.svg)](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/)
[![Python 3](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/python-3-shield.svg)](https://pyup.io/repos/github/JacobGrisham/Finance-Full-Stack-Web-App-using-Flask-and-SQL/)
</div>

## Homework from [Harvard's Introduction to Computer Science CS50 hosted on eDX](https://www.edx.org/course/cs50s-introduction-to-computer-science)
## 🎓 [Web Track](https://cs50.harvard.edu/x/2020/tracks/web/)
-   [Finance](https://cs50.harvard.edu/x/2020/tracks/web/finance/): Web application via which you can manage portfolios of stocks. This tool allows you to check real stocks’ actual prices and portfolios’ values, it will also let you buy (okay, “buy”) and sell (okay, “sell”) stocks by querying [IEX Stock Quote API](https://iexcloud.io/docs/api/#quote) for stocks’ prices.
-   I wrote all the code in the templates directory. I wrote most of the code in application.py. Some of the code in helpers.py was provided by instructor
-   I styled the application myself, with illustrations provided by [Freepik](http://www.freepik.com/).

![Finance Program Demo](img/demo.gif)

## 💡Lessons Learned
-   Database design and Create, Read, Update in SQL
-   Rewrote the entire application to use [Flask SQL Alchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/), an extension of [SQL Alchemy](https://www.sqlalchemy.org/)
-   Developed MVP of application with [SQLite](https://www.sqlite.org/index.html) locally and Deployed with [MySQL](https://www.mysql.com/)
-   Using [Flask](https://flask.palletsprojects.com/en/1.1.x/) as a server-side micro-framework
-   Python Class/Models and Schemas
-   [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) templating
-   Password hashing using [Werkzeug](https://werkzeug.palletsprojects.com/en/1.0.x/)
-   Caching user sessions with [Redis](https://redis.io/) and [Flask-sessions](https://flask-session.readthedocs.io/en/latest/)
-   Parsing data from API with python
-   Parsing data from SQL queries with python
-   Calculations using data from API and database
-   Hosting application on AWS with an [EC2](https://aws.amazon.com/ec2/) instance with an [Ubuntu](https://ubuntu.com/) operating system, [Gunicorn](https://gunicorn.org/) WSGI HTTP server, and [Nginx](https://www.nginx.com/) front-end reverse proxy
-   Using [Ubuntu](https://ubuntu.com/) as an operating system
-   [Gunicorn](https://gunicorn.org/) configuration and error-logging
-   [Nginx](https://www.nginx.com/) configuration and server security/performance optimization
-   Hosting MySQL database on AWS with a [RDS](https://aws.amazon.com/rds/) instance
-   Hosting Redis cache on AWS with an [Elasticache](https://aws.amazon.com/elasticache/) instance
-   Using AWS Cloudfront as a Content Delivery Network (CDN) and connecting Google Domains custom domain to AWS CDN
-   Error logging with [Sentry](https://sentry.io/welcome/) for hosted application in production
-   Continous integration and continuous deployment with [Travis CI](https://travis-ci.org/) and AWS CodeDeploy
-   (Deprecated) Hosting application on AWS with an [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) instance and MySQL database on AWS with a [RDS](https://aws.amazon.com/rds/) instance

## 🛠 Technologies
|Graphic Design |Front-End			|Back-End				|Database				|Deployment			|Testing 				|
| ------------- | ------------- | ------------- | ------------- | ------------- | --------------|
|Inkscape				|HTML5	 				|Python3  			|MySQL  				|AWS EC2   			|Pytest					|
|Freepik				|CSS3	 					|Flask					|SQL Alchemy		|Ubuntu      		|Lighthouse			|
|.							|Bootstrap 4		|Werkzeug				|Flask SQL Alchemy|Gunicorn			|.							|
|.							|Jinja					|.							|Redis					|Nginx 					|.							|
|.							|.							|.							|.							|Sentry					|.							|
|.							|.							|.	  					|.	   					|AWS RDS				|.       				|
|.							|.							|.							|.							|AWS Elasticache|.							|
|.							|.							|.							|.							|AWS Cloudfront	|.							|
|.							|.							|.							|.							|Travis CI			|.							|
|.							|.							|.							|.							|AWS CodeDeploy	|.							|

## ⚖️ Methodology
-   Initially hosted application on AWS [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) for a gradual introduction to AWS. Previously only used Heroku to host full-stack web applications, so I chose a similar IaaS offered by AWS. After numerous Elastic Beanstalk policy changes and disconnections, decided to go to the next level down in AWS, which is hosting this application on an EC2 instance. This offered a lot of experience and opportunities for learning about web servers.
-   Ubuntu as OS since it's the most popular operating system for web servers. Gunicorn as the WSGI since it's fast. Nginx as the reverse proxy since it was made with this optimization in mind.
-   Initially stored user sessions in a tmp folder with [`mkdtemp`](https://docs.python.org/3/library/tempfile.html), however Nginx had trouble accessing it in production. Therefore refactored application to store user sessions in a Redis database and hosted the Redis database on AWS [Elasticache](https://aws.amazon.com/elasticache/).

## ⚙️ Features
-   Login, sign-up
-   Security to prevent certain transactions using error codes 400-404
-   Create, Read, and Update for stocks

## 📐 Tests

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
