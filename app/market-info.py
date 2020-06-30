import os
import json
from pprint import pprint
from datetime import datetime
import panda as pd

import requests
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", default="US")
LANGUAGE = os.getenv("LANGUAGE", default="en")

stock_info = {}

def getStockData(symbol, interval="1d", range="3m"):
    url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"

    querystring = {"region":COUNTRY_CODE,"lang":LANGUAGE,"symbol":symbol,"interval":interval,"range":range}

    headers = {
        'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
        'x-rapidapi-key': RAPID_API_KEY
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    if(response["chart"]["result"] is None):
        print("Symbol Not Found")
        quit()
    else:
        return response

def parseTimestamp(inputdata):
    timestamplist=[]
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])

    calendertime=[]

    for ts in timestamplist:
        dt=datetime.fromtimestamp(ts)
        calendertime.append(dt.strftime("%m/%d/%Y"))
    
    return calendertime

def parseValues(inputdata):
    valueList=[]
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["open"])
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["close"])

    return valueList

def attachEvents(inputdata):
    eventlist=[]
    
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")

    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")
    
    return eventlist

if if __name__ == "__main__":
    symbol = input("Enter the stock symbol: ")
    inputdata = getStockData(symbol = symbol)

    if(None != stock_info):
        stock_info["Timestamp"]=parseTimestamp(inputdata)
        stock_info["Values"]=parseValues(inputdata)
        stock_info["Events"]=attachEvents(inputdata)
        df = pd.DataFrame(stock_info)
