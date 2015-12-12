import sys
import argparse

from analyzer.trading_engine import TradingEngine
from . import (
    initialize_config,
    initialize_redis,
    initialize_strategy,
    initialize_store,
)


def execute(redis, strategy, securities):
    trading_engine = TradingEngine(redis, strategy)
    for security in securities:
        trading_engine.listen(security)

    while True:
        trading_engine.consume()


def parse_args():
    parser = argparse.ArgumentParser(description='Desc')
    parser.add_argument('-s', '--symbols', nargs='+', dest='symbols',
                    help='<Required> Set flag', required=True)

    parser.add_argument('-a', '--account', dest='account',
                    help='')

    parser.add_argument('-c', '--config', dest='config',
                    help='Configuration file')

    return parser.parse_args(sys.argv[1:])


def main():
    import ipdb
    ipdb.set_trace()
    parsed_args = parse_args()

    config = initialize_config()
    redis_conn = initialize_redis(config)
    store = initialize_store(config)
    securities = []
    account = None
    strategy = initialize_strategy(store, config, account)
    execute(redis_conn, strategy, securities)
