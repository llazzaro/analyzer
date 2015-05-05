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

    def tearDown(self):
        pass

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
