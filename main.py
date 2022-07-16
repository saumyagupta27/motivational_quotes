from bs4 import BeautifulSoup
import requests
from random import choice
import os
from twilio.rest import Client
import schedule
import time

URL = "https://www.goodreads.com/quotes/tag/inspirational"
account_sid = os.environ.get("TW_ACCOUNT_SID")
auth_token = os.environ.get("TW_AUTH_TOKEN")
my_phone = os.environ.get("MY_PHONE")


def get_quote(quotes_list):
    """This method will return a random quote from the list of quotes passed"""
    quote = choice(quotes_list).getText().strip()
    quote_text = quote.split('―')[0].strip()
    quote_author = quote.split('―')[1].strip()
    return f"{quote_text}\n\n~ {quote_author}"


def send_quote():
    """This method will send a random quote"""
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "lxml")

    all_quotes = soup.find_all("div", class_="quoteText")
    quote_to_send = get_quote(all_quotes)

    client = Client(account_sid, auth_token)

    client.messages.create(
                         body=quote_to_send,
                         from_='+19894673922',
                         to=my_phone
                     )


schedule.every().day.at("08:00").do(send_quote)
while True:
    schedule.run_pending()
    time.sleep(1)
