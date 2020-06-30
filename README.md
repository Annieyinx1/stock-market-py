# Daily Market Briefings Service (Python)

Sends you a customized email every day after trading closes at 4pm, with information of open, close, high, low and volumn of selected stock.

## Setup

Create and activate a new Anaconda virtual environment, perhaps named "market-briefing-env":

```sh
conda create -n market-briefing-env python=3.7
conda activate market-briefing-env
```

Then, from within the virtual environment, install package dependencies:

```sh
pip install -r requirements.txt
```

Obtain API Keys from the [RapidAPI](https://rapidapi.com/apidojo/api/yahoo-finance1/details), and [SendGrid](https://app.sendgrid.com/settings/api_keys) services.

## Usage

From within the virtual environment, ensure you can run each of the following files and see them produce their desired results of: printing today's selected stock performance, and sending an example email, respectively.

```sh
python -m app.get_stock_info # note the module-syntax invocation
#> TODAY'S MARKET INFO ... SAVING PLOT
```

```sh
python -m app.email_service # note the module-syntax invocation
#> SENDING EMAIL TO ...
```

As long as each of those scripts works by itself, you can send the daily briefing email:

```sh
python -m app.daily_market_briefing # note the module-syntax invocation
```

## Web App Usage

Run the app:

```sh
FLASK_APP=web_app flask run
```

## Next Step

The plot is not working for both email and app. The reason might be that the plot is saved in a local path.

Include functionality to sign up/log in as user and add/remove stock symbols. Save user/stock information in a google sheet.

Produce more information and useful analysis for stock recommendation.