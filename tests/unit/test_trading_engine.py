import unittest

from analyzer.ufConfig.pyConfig import PyConfig

from analyzer.backtest.constant import (
    CONF_ULTRAFINANCE_SECTION,
    CONF_STRATEGY_NAME
)
from analyzer.backtest.tickSubscriber.strategies.strategyFactory import StrategyFactory
from analyzer.backtest.trading_engine import TradingEngine


class testTradingEngine(unittest.TestCase):
    def setUp(self):
        self.config = PyConfig()
        self.config.setSource("test_config.ini")
        self.strategy = StrategyFactory.createStrategy(self.config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_STRATEGY_NAME),
                                                  self.config.getSection(CONF_ULTRAFINANCE_SECTION))
        self.symbols = ['GOOG']
        self.strategy.setSymbols(self.symbols)

        self.strategy2 = StrategyFactory.createStrategy(self.config.getOption(CONF_ULTRAFINANCE_SECTION, CONF_STRATEGY_NAME),
                                                  self.config.getSection(CONF_ULTRAFINANCE_SECTION))
        self.symbols = ['GOOG']
        self.strategy2.setSymbols(self.symbols)

    def tearDown(self):
        pass

    def test_stop(self):
        trading_engine = TradingEngine()
        self.assertFalse(trading_engine._stop)
        trading_engine.stop()

        self.assertTrue(trading_engine._stop)

    def test_register_strategy(self):
        trading_engine = TradingEngine()
        trading_engine.register(self.strategy)

        # lets check that the trading engine was setup correctly
        for key in trading_engine.subs.keys():
            event = trading_engine.subs[key]
            for strategy in event.keys():
                self.assertEquals(self.strategy, strategy)
                self.assertEquals(self.symbols, event[strategy]['symbols'])
                self.assertEquals(0, event[strategy]['fail'])

    def test_unregister_strategy(self):
        trading_engine = TradingEngine()
        trading_engine.register(self.strategy)

        self.assertEquals(len(trading_engine.subs.keys()), 2)
        trading_engine.unregister(self.strategy)
        # since this was the only strategy check if events is empty
        self.assertEquals(len(trading_engine.subs.keys()), 0)
        trading_engine.register(self.strategy)
        trading_engine.register(self.strategy2)
        self.assertEquals(len(trading_engine.subs.keys()), 2)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.subs.values())[0]), 2)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.subs.values())[1]), 2)
        trading_engine.unregister(self.strategy)
        self.assertEquals(len(trading_engine.subs.keys()), 2)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.subs.values())[0]), 1)
        self.assertEquals(len(map(lambda vdict: vdict.keys(), trading_engine.subs.values())[1]), 1)


    def test_consume_ticks(self):
        pass

    def test_consume_executed_order(self):
        pass

    def test_place_order(self):
        pass
