from datetime import datetime, timedelta

from analyzer.tick_feeder import TickFeeder, QuoteFeeder
from analyzerdam.DAMFactory import DAMFactory

from analyzer.constant import CONF_ANALYZER_SECTION

from analyzer import init_logging
from analyzer.scripts import (
    initialize_config,
    initialize_redis,
    initialize_database,
)


def _create_dam(config, symbol):
    dam_name = config.get(CONF_ANALYZER_SECTION, 'dam')
    dam = DAMFactory.createDAM(dam_name, config)
    dam.symbol = symbol

    return dam


def execute(config, pubsub, session, securities):
    """
        This is used to retrieve realtime info
        and broadcast to all trading engines
    """
    if config.get(CONF_ANALYZER_SECTION, 'feed_type') == 'quote':
        klass = QuoteFeeder
    if config.get(CONF_ANALYZER_SECTION, 'feed_type') == 'tick':
        klass = TickFeeder

    tick_feeder = klass(
        publisher=pubsub,
        securities=securities,
        dam=_create_dam(config, ""),  # no need to set symbol because it's batch operation
    )

    last_execution = datetime.now()

    while True:
        last_execution = datetime.now()
        tick_feeder.execute(last_execution, datetime.now() + timedelta(minutes=100))


def main():
    init_logging(logger=None, level='debug')
    config = initialize_config()
    redis_conn = initialize_redis(config)
    session = initialize_database(config)
    securities = []
    execute(config, redis_conn.pubsub(), session, securities)
