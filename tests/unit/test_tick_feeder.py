'''
Created on Jan 18, 2011

@author: ppa
'''
from mox3 import mox
import unittest
from datetime import timedelta
import datetime
from decimal import Decimal


from mockredis import MockRedis
from analyzer.dam import BaseDAM
from pyStock.models.money import Currency
from pyStock.models import (
    Tick,
    Exchange,
    Stock,
    SecurityQuote,
)

from analyzer.tick_feeder import TickFeeder, QuoteFeeder


class TestTickFeeder(unittest.TestCase):
    def setUp(self):
        self.mock = mox.Mox()
        self.pubsub = MockRedis()
        self.pesos = Currency(name='Pesos', code='ARG')
        self.exchange = Exchange(name='Merval', currency=self.pesos)
        self.stock_one = Stock(symbol='PBR', description='Petrobras BR', ISIN='US71654V4086', exchange=self.exchange)
        self.stock_two = Stock(symbol='YPF', description='YPF S.A', ISIN='US9842451000', exchange=self.exchange)

    def test_quotes_feeder(self):
        now = datetime.datetime.now()

        start = datetime.datetime.now() - timedelta(days=1)
        end = datetime.datetime.now() + timedelta(days=1)
        cur_price = 10.4

        quote_1_dam1 = SecurityQuote(date=now, close_price=cur_price, open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.stock_one)
        quote_2_dam1 = SecurityQuote(date=now, close_price=cur_price, open_price=112, high_price=14, low_price=10.5, volume=200, security=self.stock_two)

        now_2 = datetime.datetime.now()
        quote_1_dam2 = SecurityQuote(date=now_2, close_price=cur_price, open_price=10.1, high_price=14, low_price=10.1, volume=10000, security=self.stock_one)
        quote_2_dam2 = SecurityQuote(date=now_2, close_price=cur_price, open_price=12, high_price=15, low_price=10.4, volume=300, security=self.stock_two)

        dam1 = self.mock.CreateMock(BaseDAM)
        dam1.read_quotes(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([quote_1_dam1, quote_2_dam1])

        dam2 = self.mock.CreateMock(BaseDAM)
        dam2.read_quotes(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([quote_1_dam2, quote_2_dam2])

        tf1 = QuoteFeeder(publisher=self.pubsub, dam=dam1)
        tf2 = QuoteFeeder(publisher=self.pubsub, dam=dam2)

        self.mock.ReplayAll()
        time_ticks_1 = tf1.load(start, end)
        time_ticks_2 = tf2.load(start, end)
        self.mock.VerifyAll()

        self.assertEquals(time_ticks_1, [quote_1_dam1, quote_2_dam1])
        self.assertEquals(time_ticks_2, [quote_1_dam2, quote_2_dam2])

    def test_tick_feeder(self):
        now = datetime.datetime.now()
        start = datetime.datetime.now() - timedelta(days=1)
        end = datetime.datetime.now() + timedelta(days=1)
        tick_1_dam1 = Tick(security=self.stock_one, trade_date=now, price=Decimal(19), volume=100)
        tick_2_dam1 = Tick(security=self.stock_one, trade_date=now, price=Decimal(23), volume=100)

        now_2 = datetime.datetime.now()
        tick_1_dam2 = Tick(security=self.stock_two, trade_date=now_2, price=Decimal(8), volume=100)
        tick_2_dam2 = Tick(security=self.stock_two, trade_date=now_2, price=Decimal(12), volume=100)

        dam1 = self.mock.CreateMock(BaseDAM)
        dam1.read_ticks(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([tick_1_dam1, tick_2_dam1])

        dam2 = self.mock.CreateMock(BaseDAM)
        dam2.read_ticks(mox.IgnoreArg(), mox.IgnoreArg(), mox.IgnoreArg()).AndReturn([tick_1_dam2, tick_2_dam2])

        tf_1 = TickFeeder(publisher=self.pubsub, dam=dam1)
        tf_2 = TickFeeder(publisher=self.pubsub, dam=dam2)

        self.mock.ReplayAll()
        time_ticks_1 = tf_1.load(start, end)
        time_ticks_2 = tf_2.load(start, end)
        self.mock.VerifyAll()

        self.assertEquals(time_ticks_1, [tick_1_dam1, tick_2_dam1])
        self.assertEquals(time_ticks_2, [tick_1_dam2, tick_2_dam2])

    def test_execute(self):
        pass


if __name__ == '__main__':
        unittest.main()
