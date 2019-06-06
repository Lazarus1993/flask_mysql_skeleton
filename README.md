# flask_mysql_skeleton
Skeleton code for a flask-mysql application

Just a bare bones project of a flask and mysql application.

Technologies Used:
Database: MySQL
Backend: Flask(Python3)
Containerization: Docker
Version Control: GitHub

Objective:
The application web scrapes prices of gold and silver from investing.com.
It stores the scraped data in a MySQL database.
The user is expected to provide a range of dates and the price of commodity that he/she wants to see.
The user will then recieve the prices of the commodity requested in betweeen the dates given along with the mean and variance values.


Steps to setup and use:
Install Docker
Run docker-compose up
Use curl or hit url in browser: http://localhost:8080/commodity?start_date=2019-05-10&end_date=2019-05-22&commodity_type=gold
