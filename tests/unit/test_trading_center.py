'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

from analyzer.backtest.trading_center import TradingCenter
from pyStock import Base
from pyStock.models.money import Currency, Money
from pyStock.models import (
    Stock,
    BuyOrder,
    CancelOrderStage,
    Account,
    Broker,
    Owner,
    Exchange,
)

from mockredis import MockRedis


# Connect to the database and create the schema within a transaction
engine = create_engine('sqlite://')
connection = engine.connect()
transaction = connection.begin()
Base.metadata.create_all(connection)


class testTradingCenter(unittest.TestCase):

    def setUp(self):
        self.pubsub = MockRedis()
        self.trans = connection.begin()
        self.session = Session(connection)

        currency = Currency(name='Pesos', code='ARG')
        self.exchange = Exchange(name='Merval', code='MERV', currency=currency)
        self.owner = Owner(name='poor owner')
        self.broker = Broker(name='broker1')
        self.account = Account(owner=self.owner, broker=self.broker)
        self.account.deposit(Money(amount=10000, currency=currency))

    def tearDown(self):
        self.trans.rollback()
        self.session.close()

    def test_retrievet_open_orders(self):

        stock=Stock(symbol='symbol', description='a stock', ISIN='US123456789', exchange=self.exchange)
        order1=BuyOrder(account=self.account, security=stock, price=13.2, share=10)
        order2=BuyOrder(account=self.account, security=stock, price=13.25, share=10)
        self.session.add(order1)
        self.session.add(order2)
        self.session.commit()

        tc=TradingCenter(self.session, self.pubsub)
        orders=tc.open_orders(stock)
        self.assertEquals([order1, order2], list(orders))

    def testCancelOrder(self):

        stock=Stock(symbol='symbol', description='a stock', ISIN='US123456789', exchange=self.exchange)
        order1=BuyOrder(account=self.account, security=stock, price=13.2, share=10)
        order2=BuyOrder(account=self.account, security=stock, price=13.25, share=10)

        self.session.add(order1)
        self.session.add(order2)
        self.session.commit()

        tc=TradingCenter(self.session, self.pubsub)

        order1.cancel()
        self.assertEquals([order2], tc.open_orders(stock))
        # cancel open orders
        self.assertEquals([order2], tc.cancel_orders())
        self.assertEquals(CancelOrderStage, type(order1.current_stage))
        self.assertEquals([], tc.open_orders(stock))

    def testCancelAllOpenOrders(self):
        security=Stock(symbol='symbol', description='a stock', ISIN='US123456789', exchange=self.exchange)
        order1=BuyOrder(account=self.account, security=security, price=13.2, share=10)
        order2=BuyOrder(account=self.account, security=security, price=13.25, share=10)

        self.session.add(order1)
        self.session.add(order2)
        self.session.commit()

        tc=TradingCenter(self.session, self.pubsub)

        tc.cancel_orders()

        self.assertEquals([], tc.open_orders(security))

    def testConsume(self):
        pass

    def testPostConsume(self):
        pass

    def testCreateAccountWithMetrix(self):
        pass
