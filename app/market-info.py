import os
import json
from pprint import pprint

import requests
from dotenv import load_dotenv

load_dotenv()

RAPID_API_KEY = os.getenv("RAPID_API_KEY")
COUNTRY_CODE = os.getenv("COUNTRY_CODE", default="US")
LANGUAGE = os.getenv("LANGUAGE", default="en")

url = "https://apidojo-yahoo-finance-v1.p.rapidapi.com/market/get-charts"

querystring = {"region":COUNTRY_CODE,"lang":LANGUAGE,"symbol":"AMZN","interval":"5m","range":"1d"}

headers = {
    'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com",
    'x-rapidapi-key': RAPID_API_KEY
    }

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)