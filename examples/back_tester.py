'''
Created on Dec 3, 2011

@author: ppa
'''
# from datetime import datetime
from redis import StrictRedis
# from analyzer.module.backtester import BackTester
from analyzer.runtime import (
    TickFeederThread,
    #     TradingCenterThread,
    #    TradingEngineThread,
)
from analyzer.ufConfig.pyConfig import PyConfig
from pyStock.models import (
    Account,
    Owner,
    Broker,
    Stock,
    Exchange,
)

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from pyStock.models.money import Money, Currency

from sqlalchemy.engine import create_engine
from pyStock.models import Base

if __name__ == "__main__":
    config = {
        'host': 'localhost',
        'port': 6379,
        'db': 0,
    }
    redis_conn = StrictRedis(**config)
    engine = create_engine('sqlite://')
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()

    Base.metadata.create_all(engine)
    usd = Currency(name='Dollar', code='USD')
    nasdaq = Exchange(name='NASDAQ', currency=usd)
    stock_ebay = Stock(symbol='EBAY', exchange=nasdaq, ISIN='US2786421030', description='')

    owner = Owner(name='Lucky')
    broker = Broker(name='Cheap Broker')
    account = Account(owner=owner, broker=broker)
    pesos = Currency(name='Pesos', code='ARG')
    account.deposit(Money(amount=1000, currency=pesos))
    config_file = "backtest_smaPortfolio.ini"
    config = PyConfig(config_file)

    th_tick_feeder = TickFeederThread(config, redis_conn, securities=[stock_ebay])
    th_tick_feeder.start()

#    start = datetime.now()
#    end = datetime.now() - datetime.timedelta(days=30)
#    back_tester=BackTester(config, redis_conn, session, start=start, end=end, account=account)
#    back_tester.run_tests()
#    back_tester.printMetrics()
    Session.remove()
