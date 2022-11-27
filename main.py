import requests
import os
from datetime import date
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
'TWILIO_ACCOUNT_SID'


#working out stock change
STOCK_API_Key = "E2AYT039I9WHNQAR"
STOCK_PARAMS = {
    "function" : "TIME_SERIES_WEEKLY",
    "symbol" : STOCK,
    "apikey" : STOCK_API_Key,
}
response = requests.get(STOCK_ENDPOINT, params=STOCK_PARAMS)

STOCKS_DATA = response.json()["Weekly Time Series"]
STOCKS_DATA_list = [value for (key, value) in STOCKS_DATA.items()]


last_week = STOCKS_DATA_list[0]
week_before = STOCKS_DATA_list[1]

stock_diff = float(last_week["4. close"]) - float(week_before["4. close"])
delta = round((abs(stock_diff) / float(last_week["4. close"])) * 100, 2)

sign = ""
if stock_diff > 0:
    sign = "🔺"
else:
    sign = "🔻"

#end of working out stock change


if delta > 1:
    today = date.today()
    NEWS_API_key = "34f36d2990a64f5292a5cb5aee33e6cf"
    NEWS_PARAMS = {
        "qInTitle": COMPANY_NAME,
        "from": today.strftime("%d/%m/%Y"),
        "sortBy": "publishedAt",
        "apiKey": NEWS_API_key
    }
    news_response = requests.get(NEWS_ENDPOINT, params= NEWS_PARAMS)
    NEWS_DATA = news_response.json()["articles"]
    NEWS_DATA_list = NEWS_DATA[:3]
    formatted_article_list = [
        f"{STOCK}: {sign} {delta}%\nHeadline: {article['title']}. \nBrief: {article['description']}" for article in
        NEWS_DATA_list]

    account_sid = "AC29314e34f5a85d736730183bcf796f2f"
    auth_token = "f828755e64a0792cf363ab4312eddfb9"
    client = Client(account_sid, auth_token)

    for article in formatted_article_list:
        message = client.messages \
            .create(
            body=article,
            from_='+14302492617',
            to='+18324257053'
        )

        print(message.sid)
else:
    print(delta)
