from yahoo_fin import stock_info as si
from yahoo_fin import options as op
import json

from mailer import Mailer
from watch_list import WatchList

from datetime import datetime, time
from termcolor import colored

from time import sleep

import os


def parse():
    stocks = {}
    with open('stocks.txt') as f:
        data = f.read()
        lines = data.split('\n')

        for entry in lines:
            prop = entry.split(' ')
            stocks[prop[0]] = float(prop[1])
    return data, WatchList(stocks)


def check_cache():
    with open('stocks.txt') as f:
        data = f.read
    return True if data != cache else False


def single():
    prices = {}
    for stock in watch_list.stocks.values():
        try:
            curr_price = round(si.get_live_price(stock.name), 2)

        except Exception as e:
            print(datetime.now(), colored(f'[ERROR] Could not get stock price for {stock.name}.', 'red'), colored(
                'Error Message:' + str(e), 'yellow'))
            continue

        if curr_price < stock.watch_price and stock.can_notify():
            print(datetime.now(),
                  f' [INFO] Sending alert for stock {stock.name}')
            stock.set_notified()
            mailer.create_message_stock(stock.name.split(
                '.', 1)[0], stock.watch_price, curr_price)
        prices[stock.name] = curr_price


def EOD():
    stock_close = []

    for name, stock in sorted(watch_list.stocks.items()):
        curr_price = round(si.get_live_price(name), 2)
        stock_close.append(
            [name.split('.', 1)[0], curr_price, stock.watch_price])

    print(datetime.now(), "Sending end of day report.")
    mailer.create_message_EOD(stock_close)


cache, watch_list = parse()
mailer = Mailer()

if __name__ == "__main__":

    # setup

    os.environ['SENDER_EMAIL'] = input(
        'What is the email you want to send notifications from: ')
    os.environ['SENDER_PASSWORD'] = input(
        'What is the password for that email (Note: you might have to set up a third party access key if you have 2FA enabled): ')
    os.environ['SMTP_SERVER'] = input(
        'What is the email smtp server the sender email is hosted on (Default is Gmail (smtp.gmail.com)): ')
    os.environ["SMTP_PORT"] = input(
        'What is the TLS port on that smtp server (Default is gmail\'s port (587)) :')
    os.environ['RECIEVER_PASSWORD'] = input(
        'What is the email you want to recieve email notifications from: ')
    os.environ['RECIEVER_PHONE_MAILBOX'] = input(
        'What is the phone mailbox that you want to receive text notifications from (i.e xxxxxxxxxx@txt.att.net): ')

    # program
    while True:
        if datetime.now().time() > time(9, 45, 00) and datetime.now().time() < time(16, 00):
            if check_cache():
                cache, watch_list = parse()
            single()
            sleep(300)  # 5 mins
        elif datetime.now().time() > time(16, 00) and datetime.today().weekday() < 4:
            eod()
            sleep(63960)  # until next open (17 hours 46 mins)
        else:  # friday
            eod()
            sleep(236760)  # until next open (2 days (48 hours) + 17 hours 46 mins)
