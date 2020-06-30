# app/daily_market_briefing.py

import os
from dotenv import load_dotenv
from datetime import date
#from pprint import pprint

from app import APP_ENV
from app.get_stock_info import process_stock_info, LinePlot
from app.email_service import send_email

load_dotenv()

MY_NAME = os.getenv("MY_NAME", default="User 1")

# function to convert to USD
def to_usd(stock_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.

    Param: stock_price (int or float) like 4000.444444

    Example: to_usd(4000.444444)

    Returns: $4,000.44
    """
    return f"${stock_price:,.2f}"

def to_numeric(number):
    """
    Converts a numeric value to string with comma thousand separator and no decimals.

    Param: number (int or float) like 4000.00

    Example: to_numeric(4000.00)

    Returns: 4,000
    """
    return f"{number:,.0f}"

if __name__ == "__main__":

    if APP_ENV == "development":
        symbol = input("PLEASE INPUT A STOCK SYMBOL (e.g. AMZN): ")
        stock_info = process_stock_info(symbol = symbol) # invoke with custom params
    else:
        stock_info = process_stock_info() # invoke with default params

    last_trading_date = stock_info["Date"].max() # get last trading date
    stock_info_last_date = stock_info[stock_info.Date==last_trading_date] # filter only info from the last trading date
    stock_info_plot = stock_info[(stock_info.Events=="open") | (stock_info.Events=="close")] # filter open and close price
    LinePlot(stock_info_plot, symbol)

    html = ""
    html += f"<h3>Good Afternoon, {MY_NAME}!</h3>"

    html += "<h4>Today's Date</h4>"
    html += f"<p>{date.today().strftime('%A, %B %d, %Y')}</p>"

    html += f"<h4>Stock Information for {symbol} on {last_trading_date}</h4>"
    html += "<ul>"
    for index, row in stock_info_last_date.iterrows():
        if row['Events'] == "volume":
            html += f"<li>{row['Events']} : {to_numeric(row['Values'])} </li>"
        else:
            html += f"<li>{row['Events']} : {to_usd(row['Values'])} </li>"
    html += "</ul>"
    html += "<img src = 'historic_trend.png'>"

    send_email(subject="[Daily Briefing] My Market Report", html=html)
