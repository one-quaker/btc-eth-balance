import os
import random
import sys
import argparse
import time

from bs4 import BeautifulSoup
import requests


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'


parser = argparse.ArgumentParser()
parser.add_argument('-U', '--user-agent', type=str, default=DEFAULT_USER_AGENT)
parser.add_argument('-w', '--wallet', type=str, required=True)
parser.add_argument('-d', '--debug', action='store_true')


ARG = parser.parse_args()


headers = {
    'user-agent': ARG.user_agent,
}


def get_soup(url):
    doc = requests.get(url, headers=headers)
    soup = BeautifulSoup(doc.text, 'html.parser')
    return soup


def get_currency(wallet):
    currency = 'unknown'
    if all([wallet.startswith('0x'), len(wallet) == 42]):
        currency = 'eth'
    elif len(wallet) == 34:
        currency = 'btc'
    if ARG.debug: print('{} wallet detected'.format(currency.upper()))
    return currency


def get_balance(wallet):
    currency = get_currency(wallet)
    balance = -1
    if currency == 'btc':
        selector = 'div.panel-body .abstract-section dl dd'
        url = f'https://btc.com/{wallet}'
        soup = get_soup(url)
        balance = soup.select(selector)[1].text.strip().split(' ')[0]
    elif currency == 'eth':
        selector = 'div.card-body .align-items-center div.col-md-8'
        url = f'https://etherscan.io/address/{wallet}'
        soup = get_soup(url)
        balance = soup.select_one(selector).text.replace(',', '').split()[0]
    return dict(
        currency=currency,
        balance=float(balance),
    )


balance = get_balance(ARG.wallet)
print(balance)
