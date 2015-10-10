'''
Created on Dec 3, 2011

@author: ppa
'''
from analyzer.module.backtester import BackTester
from pyStock.models import (
    Account,
    Owner,
    Broker,
    Stock,
    Exchange,
)
from pyStock.models.money import Money, Currency
from sqlalchemy.orm.session import Session

from sqlalchemy.engine import create_engine
from pyStock.models import Base

if __name__ == "__main__":
    engine = create_engine('sqlite://')
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.create_all(connection)

    session = Session(connection)
    usd = Currency(name='Dollar', code='USD')
    nasdaq = Exchange(name='NASDAQ', currency=usd)
    stock_ebay = Stock(symbol='EBAY', exchange=nasdaq, ISIN='US2786421030', description='')
    session.add(stock_ebay)
    session.commit()

    owner = Owner(name='Lucky')
    broker = Broker(name='Cheap Broker')
    account = Account(owner=owner, broker=broker)
    pesos = Currency(name='Pesos', code='ARG')
    account.deposit(Money(amount=1000, currency=pesos))
    back_tester=BackTester("backtest_smaPortfolio.ini", session, startTickDate=20101010, startTradeDate=20111220, account=account)
    back_tester.runTests()
    back_tester.printMetrics()
