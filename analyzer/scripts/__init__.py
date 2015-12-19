from redis import StrictRedis
from arctic import Arctic

from analyzer.constant import (
    CONF_ANALYZER_SECTION,
    CONF_STRATEGY_NAME,
)


from analyzer.ufConfig.pyConfig import PyConfig
from analyzer.tick_subscriber.strategies.strategy_factory import StrategyFactory

from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

from pystock.models import (
    Stock,
    Exchange,
)
from pystock.models.account import (
    Broker,
    Account,
    Owner
)

from pystock.models.money import Currency

from pystock.models import Base


def initialize_config():
    config_file = "realtime_sma_cex.ini"
    return PyConfig(config_file)


def initialize_redis(config):
    redis_config = {
        'host': config.get(CONF_ANALYZER_SECTION, 'redis_host'),
        'port': config.get(CONF_ANALYZER_SECTION, 'redis_port'),
        'db': config.get(CONF_ANALYZER_SECTION, 'db'),
    }
    return StrictRedis(**redis_config)


def initialize_store(config):
    return Arctic(config.get(CONF_ANALYZER_SECTION, 'arctic'))
#    store.initialize_library('CEX')


def initialize_database(config):
    engine = create_engine(config.get(CONF_ANALYZER_SECTION, 'database'), echo=True)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    return session


def initialize_strategy(store, config, account):
    return StrategyFactory.create_strategy(
            config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
            account,
            config,
            library=store)


def populate_db(session, engine):
    Base.metadata.create_all(engine)

    usd = Currency(name='Dollar', code='USD')
    cex = Exchange(name='CEX', currency=usd)
    bitcoin = Stock(symbol='BTC', exchange=cex, ISIN='BTC', description='Bitcoin')
    session.add(bitcoin)
    session.commit()

    owner = Owner(name='Lucky')
    broker = Broker(name='Cex.io')
    Account(owner=owner, broker=broker)
