from urllib.request import Request, urlopen
from datetime import datetime
import bs4 as bs
import csv
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
    date = splitted[1].replace(",","")
    price = splitted[2].replace(",","")
    datetime_object = datetime.strptime(date, '%b %d %Y')
    SilverPrices.append(float(price))
Dates.insert(0,"Date")
GoldPrices.insert(0,"Gold")
SilverPrices.insert(0,"Silver")
#Storing the data in a CSV file
with open('data.csv','w') as f:
    writer = csv.writer(f)
    writer.writerows(zip(Dates,GoldPrices,SilverPrices))