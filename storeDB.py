from urllib.request import Request, urlopen
from datetime import datetime
import bs4 as bs
import pymysql
import mysql.connector

"""FOR GOLD"""
#Web Scraping from the given URL
req = Request('https://www.investing.com/commodities/gold-historical-data', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = bs.BeautifulSoup(webpage,'lxml')
table = soup.find('div',id="results_box")
rows = table.find_all('tr')

#Extracting the Dates and Price from the scraped data
labels = rows[0].text
Dates = []
GoldPrices = []
SilverPrices = []
for row in rows[1:len(rows)-1]:
    splitted = row.text.splitlines()
    #Sanitizing the input and converting it into desired format
    date = splitted[1].replace(",","")
    price = splitted[2].replace(",","")
    datetime_object = datetime.strptime(date, '%b %d %Y')
    Dates.append(datetime_object.date().isoformat())
    GoldPrices.append(float(price))

"""FOR SILVER"""
#Web Scraping from the given URL
req = Request('https://www.investing.com/commodities/silver-historical-data', headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = bs.BeautifulSoup(webpage,'lxml')
table = soup.find('div',id="results_box")
rows = table.find_all('tr')

for row in rows[1:len(rows)-1]:
    splitted = row.text.splitlines()
    #Sanitizing the input and converting it into desired format
    price = splitted[2].replace(",","")
    SilverPrices.append(float(price))

#Storing data into a table in a MySQL DB.
"""
conn = pymysql.connect(host='db',port=3306 ,user='root',password='root')
"""
config = {
    'user': 'root',
    'password': 'yourpasswd',
    'host': 'mysql',
    'port': '3306'
}
conn = mysql.connector.connect(**config)
a = conn.cursor()
sql = 'CREATE DATABASE IF NOT EXISTS bigdatafed;'
a.execute(sql)
conn.commit()
sql = 'USE bigdatafed;'
a.execute(sql)
conn.commit()
sql = 'CREATE TABLE IF NOT EXISTS commodity_pricing (date VARCHAR(20), gold_pricing DOUBLE(10,2), silver_pricing DOUBLE(10,2));'
a.execute(sql)
conn.commit()
sql = "INSERT INTO commodity_pricing (date, gold_pricing, silver_pricing) VALUES (%s, %s, %s)"
for idx in range(len(Dates)):
    val = (Dates[idx],GoldPrices[idx],SilverPrices[idx])
    a.execute(sql,val)
conn.commit()
a.close()
conn.close()
print("Data successfully stored in DB")

