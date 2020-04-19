from datetime import datetime, timedelta


class Stock:
    def __init__(self, name, watch_price):
        self.name = name
        self.watch_price = watch_price
        self.notified = [False]

    def set_notified(self):
        self.notified = [True, datetime.now() + timedelta(hours=2)]

    def can_notify(self) -> bool:
        if not self.notified[0]:
            return True
        elif datetime.now() < self.notified[1]:
            return False
        else:
            self.notified = [False]
            return True


class WatchList:
    def __init__(self, stocks={}):
        self.stocks = {name: Stock(name, price)
                       for name, price in stocks.items()}

    @staticmethod
    def add_stock(self, stock='', price=''):
        if stock in self.stocks:
            self.stocks[stock].watch_price = price
        else:
            self.stocks[stock] = Stock(stock, price)
        return True

    @staticmethod
    def remove_stock(self, stock=''):
        if not stock in self.stocks:
            return False
        else:
            del self.stocks[stock]
