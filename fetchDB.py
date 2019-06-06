from flask import Flask,request
import pandas as pd
import mysql.connector
import json

app = Flask(__name__)

@app.route('/commodity')
def filter():
    #Extracting parameters from get request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    commodity_type = request.args.get('commodity_type')

    #Preparing JSON object
    json_dict = fetchFromDB(start_date,end_date,commodity_type)
    json_data = json.dumps(json_dict)
    print(json_data)
    return json_data

def fetchFromDB(start_date,end_date,commodity_type):
    #Fetching data from MySQL DB
    config = {
    'user': 'root',
    'password': 'yourpasswd',
    'host': 'mysql',
    'port': '3306',
    'database': 'bigdatafed'
    }
    conn = mysql.connector.connect(**config)
    df = pd.read_sql('SELECT * FROM commodity_pricing', con=conn)
    conn.close()
    #Applying the date range on the data 
    mask = (df['date'] > start_date) & (df['date'] <= end_date)
    df = df.loc[mask]
    if df.empty:
        return {"data": {}, "mean": "0.0", "variance": "0.0"}

    dates = list(df['date'])
    if commodity_type == "gold":
        prices = list(df['gold_pricing'])
    else:
        prices = list(df['silver_pricing'])
    
    #Generating mean and variance
    data_dict = {}
    for idx in range(len(dates)):
        data_dict[dates[idx]] = prices[idx]
    mean = sum(prices)/len(prices)
    vSum = 0
    for each in prices:
        vSum+=pow(each-mean,2)
    variance = vSum/len(prices)
    variance = format(variance,'.2f')
    mean = format(mean,'.2f')

    json_dict = {"data":data_dict,"mean":mean,"variance":variance}

    return json_dict


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=8080)