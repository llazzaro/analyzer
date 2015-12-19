'''
Created on Dec 3, 2011

@author: ppa
'''
import logging
from datetime import datetime
from datetime import timedelta
from redis import StrictRedis
from arctic import Arctic
from Quandl import Quandl

from analyzer import init_logging
from analyzer.runtime import (
    BackTesterThread,
    TradingCenterThread,
)
from analyzer.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.constant import (
    CONF_ANALYZER_SECTION,
    CONF_STRATEGY_NAME,
)
from analyzer.ufConfig.pyConfig import PyConfig
from pystock.models import (
    Account,
    Owner,
    Broker,
    Stock,
    Exchange,
)

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from pystock.models.money import Money, Currency

from sqlalchemy.engine import create_engine
from pystock.models import Base

if __name__ == "__main__":
    logger = logging.getLogger('analyzer')
    logger = logging.getLogger('analyzerstrategies')
    init_logging(logger, 'debug')
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
    nasdaq = Exchange(name='NASDAQ', currency=usd, code='NASDAQ4')
    stock_ebay = Stock(symbol='EBAY', exchange=nasdaq, ISIN='US2786421030', description='')

    owner = Owner(name='Lucky')
    broker = Broker(name='Cheap Broker')
    account = Account(owner=owner, broker=broker)
    pesos = Currency(name='Pesos', code='ARG')
    account.deposit(Money(amount=1000, currency=pesos))
    config_file = "backtest_smaPortfolio.ini"
    config = PyConfig(config_file)
    store.initialize_library(nasdaq.code)
    library = store[nasdaq.code]
    strategy = StrategyFactory.create_strategy(
            config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
            account,
            config,
            library)
    securities = [stock_ebay]


    api_key= 'iDQ6AjPzsi2G6Lxc3Xuw'
    ebay = Quandl.get("GOOG/NASDAQ_EBAY", authtoken=api_key)
    library.write(stock_ebay.symbol, ebay, metadata={'source': 'Quandl'})
    th_center = TradingCenterThread(session, redis_conn.pubsub())
    th_center.start()

    start = datetime.now() - timedelta(days=30)
    end = datetime.now()
    for security in securities:
        th_backtest = BackTesterThread(session, store, redis_conn, security=security, strategy=strategy, start=start, end=end)
        th_backtest.start()
    Session.remove()
