from unittest import TestCase
from analyzer.ufConfig.pyConfig import PyConfig

from analyzer.backtest.constant import (
    CONF_ANALYZER_SECTION,
    CONF_STRATEGY_NAME
)
from analyzer.backtest.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.backtest.trading_engine import TradingEngine

from mockredis import MockRedis


class TestTradingEngine(TestCase):
    def setUp(self):
        self.pubsub = MockRedis()
        self.config = PyConfig("test_config.ini")
        self.symbols = ['GOOG']
        self.strategy = StrategyFactory.create_strategy(
                self.config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
                self.symbols,
                self.config)

        self.strategy2 = StrategyFactory.create_strategy(
                self.config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
                self.symbols,
                self.config.getSection(CONF_ANALYZER_SECTION))

    def tearDown(self):
        pass

    def test_register_strategy(self):
        trading_engine = TradingEngine(self.pubsub)
        trading_engine.register(self.strategy)

        # lets check that the trading engine was setup correctly
        for key in trading_engine.strategies:
            event = trading_engine.strategies[key]
            for strategy in event.keys():
                self.assertEquals(self.strategy, strategy)
                self.assertEquals(self.symbols, event[strategy]['symbols'])
                self.assertEquals(0, event[strategy]['fail'])

    def test_unregister_strategy(self):
        trading_engine = TradingEngine(self.pubsub)
        trading_engine.register(self.strategy)

        self.assertEquals(len(trading_engine.strategies), 1)
        trading_engine.unregister(self.strategy)
        # since this was the only strategy check if events is empty
        self.assertEquals(len(trading_engine.strategies), 0)
        trading_engine.register(self.strategy)
        trading_engine.register(self.strategy2)
        self.assertEquals(len(trading_engine.strategies), 2)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.strategies.values())[0]), 2)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.strategies.values())[1]), 2)
        trading_engine.unregister(self.strategy)
        self.assertEquals(len(trading_engine.strategies.keys()), 2)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.strategies.values())[0]), 1)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.strategies.values())[1]), 1)

    def test_consume_ticks(self):
        pass

    def test_consume_executed_order(self):
        pass

    def test_place_order(self):
        pass
