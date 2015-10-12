'''
Created on Dec 3, 2011

@author: ppa
'''
import sys
import traceback
import logging
import logging.config

from pyStock.models import Account

from analyzer.backtest.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.backtest.index_helper import IndexHelper
from analyzer.backtest.history import History
from analyzer.backtest.constant import (
    CONF_ANALYZER_SECTION,
    CONF_TRADE_TYPE,
    CONF_START_TRADE_DATE,
    CONF_STRATEGY_NAME
)
# from analyzer.backtest.metric import BasicMetric


LOG = logging.getLogger(__name__)


class BackTester(object):
    ''' back testing '''

    def __init__(self, config, pubsub, session, account, securities, start_tick_date=0, start_trade_date=0, end_trade_date=None):
        self.config = config
        self.pubsub = pubsub
        self.pubsub = pubsub
        self.session = session

        self.account = account
        self.securities = securities
        self.start_tick_date = start_tick_date
        self.end_trade_date = end_trade_date
        self.metric_calculator = None

        LOG.debug(self.securities)

    @property
    def trade_type(self):
        return self.config.get(CONF_ANALYZER_SECTION, CONF_TRADE_TYPE)

    def _run_one_test(self, security):
        ''' run one test '''
        LOG.debug("Running backtest for %s" % security)
        runner = TestRunner(
                self.config,
                self.pubsub,
                self.session,
                self.metric_calculator,
                [security],
                self.start_tick_date,
                self.end_trade_date,
                self.account,
                self.trade_type)
        runner.run_test()

    def run_tests(self):
        ''' run tests '''
        for security in self.securities:
            try:
                self._run_one_test(security)
            except KeyboardInterrupt:
                LOG.error("User Interrupted")
                sys.exit("User Interrupted")
            except BaseException as excp:
                LOG.error("Unexpected error when backtesting %s -- except %s, traceback %s"
                          % (self.securities, excp, traceback.format_exc(8)))

    def getMetrics(self):
        ''' get all metrics '''
        return self.__mCalculator.getMetrics()

    def printMetrics(self):
        ''' print metrics '''
        LOG.info(self.getMetrics())


class TestRunner(object):
    ''' back testing '''
    def __init__(self, config, pubsub, session, metric_manager, securities, start_tick_date, end_trade_date, account, trade_type):
        self.config = config
        self.trade_type = trade_type
        self.account = account
        self.start_tick_date = start_tick_date
        self.end_trade_date = end_trade_date
        self.index_helper = IndexHelper()
        self.history = History()
        self.securities = securities
        self.metric_manager = metric_manager

        # wire things together
        self._setup_strategy()
        self.trading_engine.tickProxy = self.tick_feeder

    def _setup_strategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.create_strategy(
                self.config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
                self.securities,
                self.config)

        # register on trading engine
        # import ipdb; ipdb.set_trace()
        self.trading_engine.register(strategy)

    def _execute(self):
        ''' run backtest '''
        LOG.info("Running backtest for %s" % self.securities)
        # start trading engine
#        thread = Thread(target=self.trading_engine.runListener, args=())
#        thread.setDaemon(False)
#        thread.start()

        # start tickFeeder
        # share a queue and this should be another thread
        timePositions = self.account.positions
        start_trade_date = self.config.get(CONF_ANALYZER_SECTION, CONF_START_TRADE_DATE)
        if start_trade_date:
            start_trade_date = int(start_trade_date)
            timePositions = [tp for tp in timePositions if tp[0] >= start_trade_date]

        # get and save metrics
        # result = self.__metric_manager.calculate(self.securities, timePositions, self.tick_feeder.iTimePositionDict)
        # self.__saver.writeMetrics(result[BasicMetric.START_TIME],
        #                          result[BasicMetric.END_TIME],
        #                          result[BasicMetric.MIN_TIME_VALUE][1],
        #                          result[BasicMetric.MAX_TIME_VALUE][1],
        #                          result[BasicMetric.SRATIO],
        #                          result[BasicMetric.MAX_DRAW_DOWN][1],
        #                          result[BasicMetric.R_SQUARED],
        #                          self.account.total,
        #                          self.account.holdings)

    def _printResult(self):
        ''' print result'''
        LOG.info("account %s" % self.account)
        LOG.debug([str(order) for order in self.account.orders])
        LOG.debug("account position %s" % self.account.positions)

    def run_test(self):
        ''' run one test '''
        self._execute()
        self._printResult()


# ###########Util function################################
def getBackTestResultDbName(securities, strategyName, start_tick_date, end_trade_date):
    ''' get table name for back test result'''
    return "%s__%s__%s__%s" % ('_'.join(securities) if len(securities) <= 1 else len(securities), strategyName, start_tick_date, end_trade_date if end_trade_date else "Now")

if __name__ == "__main__":
    account = Account()
    account.deposit(1000)
    backtester = BackTester(
            "backtest_zscoreMomentumPortfolio.ini",
            account=account,
            start_tick_date=19901010,
            start_trade_date=19901010,
            end_trade_date=20131010)
    backtester.setup()
    backtester.runTests()
    backtester.printMetrics()
