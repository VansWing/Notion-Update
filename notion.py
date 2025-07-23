import requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup

#Notion Setup
notion_token = "ntn_I7307255014blHrKWbHcI0j2KJKdKr6L8EaY6dhebWL0hN"
database_id_stock = "2241b38bdce681c99ef2cc1f47ee1538"

notion_headers = {
    "Authorization": "Bearer " + notion_token,
    "Content-Type": "application/json",
    "Notion-Version":"2022-06-28",
}


#AAstock Setup
stock_url = "https://www.aastocks.com/en/stocks/quote/detail-quote.aspx"
aastock_header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Referer": "http://www.aastocks.com/en/stocks/quote/detail-quote.aspx"
}


def get_all_values_by_key(json_data, target_key):
    values = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key == target_key:
                values.append(value)
            values.extend(get_all_values_by_key(value, target_key))
    elif isinstance(json_data, list):
        for item in json_data:
            values.extend(get_all_values_by_key(item, target_key))
    return values


def get_pages() -> list:
    notion_url = f"https://api.notion.com/v1/databases/{database_id_stock}/query"

    payload = {"page_size": 100}
    response = requests.post(notion_url, json=payload, headers=notion_headers)

    data = response.json()


    temp = data["results"]
    all_tickers = get_all_values_by_key(temp, "Ticker ")
    result = get_all_values_by_key(all_tickers, "plain_text")

    return result

def get_stock_price(ticker_no):
    url = "http://www.aastocks.com/en/stocks/quote/detail-quote.aspx?symbol={}".format(ticker_no)
    sess = requests.session()
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    "Referer": "http://www.aastocks.com/en/stocks/quote/detail-quote.aspx"
    }
    req = sess.get(url, headers = headers)
    soup = BeautifulSoup(req.text)
    return soup.select(".content #labelLast span")[0].text.strip(" \xa0")

tickers = get_pages()
price = {}

for ticker in tickers:
    str = ticker[0]
    if ord(str) <= 57:
        print(f"The stock no. is {ticker} now in $",get_stock_price(ticker))
    else:
        print(f"The stock no. is {ticker} in US stock")
    #price.update()
