from redis import StrictRedis
from arctic import Arctic

from analyzer import init_logging
from analyzer.runtime import (
    TickFeederThread,
    TradingCenterThread,
    TradingEngineThread,
    AlarmThread,
)
from analyzer.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.constant import (
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
from pyStock.models.money import Currency

from sqlalchemy.engine import create_engine
from pyStock.models import Base

if __name__ == "__main__":
    init_logging('debug')
    config_file = "realtime_sma_cex.ini"
    config = PyConfig(config_file)

    redis_config = {
        'host': config.get(CONF_ANALYZER_SECTION, 'redis_host'),
        'port': config.get(CONF_ANALYZER_SECTION, 'redis_port'),
        'db': config.get(CONF_ANALYZER_SECTION, 'db'),
    }
    redis_conn = StrictRedis(**redis_config)
    store = Arctic(config.get(CONF_ANALYZER_SECTION, 'arctic'))
    store.initialize_library('CEX')
    engine = create_engine(config.get(CONF_ANALYZER_SECTION, 'database'), echo=True)
    session_factory = sessionmaker(bind=engine)
    Session = scoped_session(session_factory)
    session = Session()
    Base.metadata.create_all(engine)

    usd = Currency(name='Dollar', code='USD')
    cex = Exchange(name='CEX', currency=usd)
    bitcoin = Stock(symbol='BTC', exchange=cex, ISIN='BTC', description='Bitcoin')
    session.add(bitcoin)
    session.commit()

    owner = Owner(name='Lucky')
    broker = Broker(name='Cex.io')
    account = Account(owner=owner, broker=broker)
    strategy = StrategyFactory.create_strategy(
            config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
            account,
            config,
            library=store['CEX'])

    th_tick_feeder = TickFeederThread(config, redis_conn, securities=[bitcoin])
    th_trading_engine = TradingEngineThread(redis_conn, securities=[bitcoin], strategy=strategy)
    th_trading_center = TradingCenterThread(session, redis_conn.pubsub())
    th_alarm = AlarmThread(redis_conn.pubsub(), config, 'action')

    th_alarm.start()
    th_trading_center.start()
    th_trading_engine.start()
    th_tick_feeder.start()
    Session.remove()
