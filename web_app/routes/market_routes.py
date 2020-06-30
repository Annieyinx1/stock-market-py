from flask import Blueprint, render_template, request

from app.get_stock_info import process_stock_info

market_routes = Blueprint("market_routes", __name__)

@market_routes.route("/form")
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

    results = process_stock_info(symbol)
    print(results.keys())
    return render_template("market_report.html", symbol=symbol, results=results)