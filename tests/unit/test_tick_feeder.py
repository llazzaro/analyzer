'''
Created on Jan 18, 2011

@author: ppa
'''
import datetime
import unittest
from datetime import timedelta

try:
    from unittest.mock import MagicMock
except ImportError:
    from mock import MagicMock

from mockredis import MockRedis
from analyzer.dam import BaseDAM
from pystock.models.money import Currency
from pystock.models import (
    Exchange,
    Stock,
)

from analyzer.tick_feeder import TickFeeder, QuoteFeeder


class TestTickFeeder(unittest.TestCase):
    def setUp(self):
        self.pubsub = MockRedis()
        self.pesos = Currency(name='Pesos', code='ARG')
        self.exchange = Exchange(name='Merval', currency=self.pesos)
        self.stock_one = Stock(symbol='PBR', description='Petrobras BR', ISIN='US71654V4086', exchange=self.exchange)
        self.stock_two = Stock(symbol='YPF', description='YPF S.A', ISIN='US9842451000', exchange=self.exchange)

    def test_quotes_feeder(self):
        now = datetime.datetime.now()

        start = datetime.datetime.now() - timedelta(days=1)
        end = datetime.datetime.now() + timedelta(days=1)

        dam1 = self._dam_with_quotes(now, self.stock_one)
        dam2 = self._dam_with_quotes(now, self.stock_two)

        tf1 = QuoteFeeder(publisher=self.pubsub, dam=dam1, security=self.stock_one)
        tf2 = QuoteFeeder(publisher=self.pubsub, dam=dam2, security=self.stock_two)

        time_quotes_1 = tf1.load(start, end)
        time_quotes_2 = tf2.load(start, end)

        self.assertEquals(time_quotes_1[0]['open'], 11.1)
        self.assertEquals(time_quotes_2[0]['open'], 11.1)

    def test_tick_feeder(self):
        now = datetime.datetime.now()
        start = datetime.datetime.now() - timedelta(days=1)
        end = datetime.datetime.now() + timedelta(days=1)

        now_2 = datetime.datetime.now()
        dam1 = self._dam_with_ticks(now, self.stock_one)
        dam2 = self._dam_with_ticks(now_2, self.stock_two)

        tf_1 = TickFeeder(publisher=self.pubsub, dam=dam1, security=self.stock_one)
        tf_2 = TickFeeder(publisher=self.pubsub, dam=dam2, security=self.stock_two)

        time_ticks_1 = tf_1.load(start, end)
        time_ticks_2 = tf_2.load(start, end)

        self.assertEquals(time_ticks_1[0]['open'], 11.1)

        self.assertEquals(time_ticks_2[0]['open'], 11.1)

    def _dam_with_quotes(self, now, stock):
        quote_1_dam1 = {'date': now,
                'close': 10,
                'high': 11.5,
                'low': 9.9,
                'open': 11.1,
                'volume': 192863}

        dam1 = BaseDAM()
        dam1.quotes = MagicMock(return_value=[quote_1_dam1])

        return dam1

    def _dam_with_ticks(self, now, stock):
        tick_1_dam1 = {'date': now,
                'close': 10,
                'high': 11.5,
                'low': 9.9,
                'open': 11.1,
                'volume': 192863}

        dam1 = BaseDAM()
        dam1.ticks = MagicMock(return_value=[tick_1_dam1])

        return dam1

    def test_execute(self):
        now = datetime.datetime.now()
        start = datetime.datetime.now() - timedelta(days=1)
        end = datetime.datetime.now() + timedelta(days=1)
        dam1 = self._dam_with_ticks(now, self.stock_one)
        tf_1 = TickFeeder(publisher=self.pubsub, dam=dam1, security=self.stock_one)
        self.pubsub.publish = MagicMock(return_value=None)
        tf_1.execute(start, end)

        self.assertTrue(self.pubsub.publish.called)
        self.assertEquals(self.pubsub.publish.call_count, 1)
        self.pubsub.publish.assert_called_with('PBR', {'volume': 192863, 'high': 11.5, 'low': 9.9, 'date': now, 'close': 10, 'open': 11.1})


if __name__ == '__main__':
    unittest.main()
