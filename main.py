from config import *
import requests
from twilio.rest import Client
from datetime import date, timedelta

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
TIME_SERIES = "TIME_SERIES_DAILY"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_params = {
    "function": TIME_SERIES,
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

news_response = requests.get(STOCK_ENDPOINT, stock_params)
news_response.raise_for_status()
today = date.today() - timedelta(days=3)
print(f"HTTP Status Code: {news_response.status_code}")
print(today)

stock_data = news_response.json()

closing_price = [
    stock_data["Time Series (Daily)"]["{0}".format(today)]["4. close"]]
day_before_closing_price = [
    stock_data["Time Series (Daily)"]["{0}".format(today-timedelta(days=1))]["4. close"]]

closing = float("".join(closing_price))
closing_day_before = float("".join(day_before_closing_price))
print(closing)
print(closing_day_before)

difference = closing - closing_day_before

up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

diff_percent = round((difference / closing) * 100)
print(diff_percent)

if abs(diff_percent) > 5:
    news_params = {
        "qInTitle": COMPANY_NAME,
        "apiKey": NEWS_API_KEY
    }

    news_response = requests.get(NEWS_ENDPOINT, news_params)
    news_response.raise_for_status()

    print(f"HTTP Status Code: {news_response.status_code}")

    articles = news_response.json()["articles"]

    three_articles = articles[:3]
    print(three_articles)

    formatted_articles = [
        f"{STOCK_NAME}: {up_down}{diff_percent}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in three_articles]
    print("".join(formatted_articles))

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER
        )
        print(message.status)