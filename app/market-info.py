import os
import json
from pprint import pprint
from datetime import datetime

import requests
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", default="US")
LANGUAGE = os.getenv("LANGUAGE", default="en")

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"

querystring = {"region":COUNTRY_CODE,"lang":LANGUAGE,"symbol":"AMZN","interval":"1d","range":"5d"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': RAPID_API_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

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