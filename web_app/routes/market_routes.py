from flask import Blueprint, render_template, request

from app.get_stock_info import process_stock_info, LinePlot

market_routes = Blueprint("market_routes", __name__)

@market_routes.route("/")
def market_form():
    print("VISITED THE MARKET FORM...")
    return render_template("market_form.html")

@market_routes.route("/report", methods=["GET", "POST"])
def market_report():
    print("GENERATING A STOCK REPORT...")

    if request.method == "POST":
        print("FORM DATA:", dict(request.form))
        symbol = request.form["symbol"]
    elif request.method == "GET":
        print("URL PARAMS:", dict(request.args))
        symbol = request.args["symbol"] #> {'symbol': 'AMZN'}

    stock_info = process_stock_info(symbol)
    last_trading_date = stock_info["Date"].max() # get last trading date
    stock_info_last_date = stock_info[stock_info.Date==last_trading_date] # filter only info from the last trading date
    stock_info_plot = stock_info[(stock_info.Events=="open") | (stock_info.Events=="close")] # filter open and close price
    LinePlot(stock_info_plot, symbol)

    return render_template("market_report.html", symbol=symbol, results=stock_info_last_date, date=last_trading_date)