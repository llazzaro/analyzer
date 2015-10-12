import unittest
from analyzer.backtest.metric import MetricManager
from analyzer.module.backtester import TestRunner
from analyzer.backtest.trading_engine import TradingEngine
from analyzer.ufConfig.pyConfig import PyConfig
from analyzer.backtest.constant import (
    CONF_ANALYZER_SECTION,
    CONF_TRADE_TYPE
)
from mockredis import MockRedis


class TestTestRunner(unittest.TestCase):
    def setUp(self):
        self.config = PyConfig("test_config.ini")
        self.pubsub = MockRedis()

    def test_runner(self):
        trading_engine = TradingEngine(self.pubsub)
        m_calculator = MetricManager()
        start_tick_date=20101010
        end_trade_date=None
        accounts = []
        cash=150000
        trade_type = self.config.get(CONF_ANALYZER_SECTION, CONF_TRADE_TYPE)
        symbols = ['GOOG']
        TestRunner(self.config,
                    self.pubsub,
                            m_calculator,
                            accounts,
                            symbols,
                            start_tick_date,
                            end_trade_date,
                            cash,
                            trade_type,
                            trading_engine)


if __name__ == '__main__':
    unittest.main()
