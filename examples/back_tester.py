'''
Created on Dec 3, 2011

@author: ppa
'''
from datetime import datetime
from datetime import timedelta
from redis import StrictRedis
from arctic import Arctic
from Quandl import Quandl

from analyzer import init_logging
from analyzer.runtime import (
    BackTesterThread,
    #     TradingCenterThread,
)
from analyzer.backtest.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.backtest.constant import (
    CONF_ANALYZER_SECTION,
    CONF_STRATEGY_NAME,
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
    init_logging('debug')
    store = Arctic('localhost')

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
    strategy = StrategyFactory.create_strategy(
            config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
            account,
            config.getSection(CONF_ANALYZER_SECTION),
            config,
            store)
    securities = [stock_ebay]
    store.initialize_library(nasdaq.name)

    library = store[nasdaq.name]

    api_key= 'iDQ6AjPzsi2G6Lxc3Xuw'
    ebay = Quandl.get("GOOG/NASDAQ_EBAY", authtoken=api_key)
    library.write(stock_ebay.symbol, ebay, metadata={'source': 'Quandl'})

    start = datetime.now()
    end = datetime.now() - timedelta(days=30)
    th_backtest = BackTesterThread(store, redis_conn, securities=securities, start=start, end=end)

    th_backtest.start()
    Session.remove()
