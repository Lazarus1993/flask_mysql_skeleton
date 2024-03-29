from urllib.request import Request, urlopen
from datetime import datetime
import bs4 as bs
import mysql.connector
import requests
import os



def source_website_health_gold():
    response = requests.get(f'https://www.investing.com/commodities/gold-historical-data')
    if response.ok:
        return response.text
    else:
        return 'Bad Response'

def source_website_health_silver():
    response = requests.get(f'https://www.investing.com/commodities/silver-historical-data')
    if response.ok:
        return response.text
    else:
        return 'Bad Response'

def webScraping(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = bs.BeautifulSoup(webpage,'lxml')
    table = soup.find('div',id="results_box")
    rows = table.find_all('tr')
    return rows

Dates = []
GoldPrices = []
SilverPrices = []

"""FOR GOLD"""
rows = webScraping('https://www.investing.com/commodities/gold-historical-data')

#Extracting the Dates and Price from the scraped data
labels = rows[0].text
for row in rows[1:len(rows)-1]:
    splitted = row.text.splitlines()
    #Sanitizing the input and converting it into desired format
    date = splitted[1].replace(",","")
    price = splitted[2].replace(",","")
    datetime_object = datetime.strptime(date, '%b %d %Y')
    Dates.append(datetime_object.date().isoformat())
    GoldPrices.append(float(price))

"""FOR SILVER"""
rows = webScraping('https://www.investing.com/commodities/silver-historical-data')

for row in rows[1:len(rows)-1]:
    splitted = row.text.splitlines()
    #Sanitizing the input and converting it into desired format
    price = splitted[2].replace(",","")
    SilverPrices.append(float(price))

#Storing data into a table in a MySQL DB.
config = {
    'user': 'root',
    'password': os.environ['MYSQL_ROOT_PASSWORD'],
    'host': os.environ['MYSQL_HOST'],
    'port': os.environ['MYSQL_PORT'],
    'database': os.environ['MYSQL_DATABASE']
    }
conn = mysql.connector.connect(**config)
a = conn.cursor()
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