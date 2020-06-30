import os
import json
from pprint import pprint
from datetime import datetime

import requests
from dotenv import load_dotenv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import rcParams
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format #suppress scientific notation

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", default="US")
LANGUAGE = os.getenv("LANGUAGE", default="en")


def getStockData(symbol, interval="1d", range="1mo"):
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
    timestamplist.extend(inputdata["chart"]["result"][0]["timestamp"])
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
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["high"])
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["low"])
    valueList.extend(inputdata["chart"]["result"][0]["indicators"]["quote"][0]["volume"])
    return valueList

def attachEvents(inputdata):
    eventlist=[]
    
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("open")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("close")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("high")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("low")
    for i in range(0, len(inputdata["chart"]["result"][0]["timestamp"])):
        eventlist.append("volume")
    
    return eventlist

def combineData(inputdata):
    stock_info={}
    stock_info["Date"]=parseTimestamp(inputdata)
    stock_info["Values"]=parseValues(inputdata)
    stock_info["Events"]=attachEvents(inputdata)
    df = pd.DataFrame(stock_info)
    return df

def LinePlot(df_plot, symbol):
    sns.set(style="darkgrid")
    rcParams['figure.figsize']=13,5
    rcParams['figure.subplot.bottom'] = 0.2
      
    ax = sns.lineplot(x="Date", y="Values", hue="Events",dashes=False, markers=True, 
                   data=df_plot, sort=False)
    ax.set_title('Symbol: ' + symbol)
      
    plt.xticks(
        rotation=45, 
        horizontalalignment='right',
        fontweight='light',
        fontsize='xx-small'  
    )
    plt.show()


if __name__ == "__main__":
    symbol = input("Enter the stock symbol: ")
    inputdata = getStockData(symbol = symbol)
    df = combineData(inputdata)
    df_plot = df[(df.Events=="open")|(df.Events=="close")]
    print(df)
    print(df_plot)
    LinePlot(df_plot, symbol)
