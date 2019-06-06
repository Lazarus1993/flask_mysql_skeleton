from flask import Flask,request
import pandas as pd
import json

app = Flask(__name__)

@app.route('/commodity')
def filter():
    #Extracting parameters from get request
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    commodity_type = request.args.get('commodity_type')

    #Fetching data from CSV file
    df = pd.read_csv('data.csv')
    mask = (df['Date'] > start_date) & (df['Date'] <= end_date)
    df = df.loc[mask]
    dates = list(df['Date'])
    if commodity_type == "gold":
        prices = list(df['Gold'])
    else:
        prices = list(df['Silver'])
    
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

    #Preparing JSON object

    json_dict = {"data":data_dict,"mean":mean,"variance":variance}
    json_data = json.dumps(json_dict)
    print(json_data)
    return json_data

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port=8080)