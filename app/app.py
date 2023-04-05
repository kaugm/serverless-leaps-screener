#/opt/homebrew/bin/python3

import os
import json
import boto3
from datetime import datetime

from bs4 import BeautifulSoup
import requests


# Screener Options: Big companies expected to grow that have recently corrected
# Descriptive: Over 2b market cap, IPO > 5 years ago, and optionable
# Fundamental: Positive EPS growth over next 5 yeares, Price/FCF under 50, Positive ROI, Positive EPS growth this year, and Expected positive EPS growth next year
# Technical: Current price above SMA200, but down today
SNS_TOPIC = os.environ['snsTopic']
URL = os.environ['URL']

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

TIMESTAMP = datetime.now().strftime('%B %d %H:%M')

def lambda_handler(event, context):

    # Initiate SNS Client
    sns = boto3.client('sns')

    # Scrape Finviz webpage
    screen = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(screen.text, features='html.parser')
    trs = soup.findAll('tr', {"valign": "top"})

    # Extract Data
    TICKERS = []
    for tr in trs:
        tds = tr.findAll('td', {"class": "screener-body-table-nw"})

        _count = tds[0].text
        _ticker = tds[1].text
        _industry = f"{tds[3].text}: {tds[4].text}"
        _price = tds[8].text
        _change= tds[9].text

        TICKERS.append({
            "Ticker": _ticker,
            "Industry": _industry,
            "Price": _price,
            "Change": _change
        })

    # Sort Output
    TOP_TICKERS = sorted(TICKERS, key=lambda x: x['Change'], reverse=True)
    MESSAGE = f"Recent Stock Corrections\n\n"

    MESSAGE += f"{str('Ticker'):<12}{str('Industry'):<60}{str('Down')}\n"

    for item in TOP_TICKERS[:10]:
        MESSAGE += f"{item['Ticker']:<12}{item['Industry']:<60}{item['Change']}\n"

    response = sns.publish(TargetArn=SNS_TOPIC, Message=MESSAGE, Subject=f"{TIMESTAMP}: Potential LEAPS Options")

    return {
        'statusCode': 200,
        'body': json.dumps(f"Hello from Lambda! {response}")
    }