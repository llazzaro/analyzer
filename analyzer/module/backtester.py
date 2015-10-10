'''
Created on Dec 3, 2011

@author: ppa
'''
import os
import sys
import traceback
import logging
import logging.config
from threading import Thread

from pyStock.models import Account

from analyzer.backtest.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.ufConfig.pyConfig import PyConfig
from analyzer.backtest.metric import MetricManager
from analyzer.backtest.index_helper import IndexHelper
from analyzer.backtest.history import History
from analyzer.backtest.constant import (
    CONF_ANALYZER_SECTION,
    CONF_INPUT_DB,
    CONF_TRADE_TYPE,
    CONF_INIT_CASH,
    CONF_START_TRADE_DATE,
    CONF_END_TRADE_DATE,
    CONF_SYMBOL_FILE,
    CONF_INDEX,
    CONF_INPUT_DAM,
    CONF_STRATEGY_NAME
)
# from analyzer.backtest.metric import BasicMetric


from pyStock.models import Security

LOG = logging.getLogger()


class BackTester(object):
    ''' back testing '''

    def __init__(self, config_file, pubsub, session, account, start_tick_date=0, startTradeDate=0, endTradeDate=None, securities=None):
        LOG.debug("Loading config from %s" % config_file)
        self.pubsub = pubsub
        self.pubsub = pubsub
        self.session = session

        self.account = account
        self.__mCalculator = MetricManager()
        self.securities = []
        self.start_tick_date = start_tick_date
        self.__startTradeDate = startTradeDate
        self.end_trade_date = endTradeDate
        self.__firstSaver = None

        ''' setup '''
        self.config.override(CONF_ANALYZER_SECTION, CONF_INIT_CASH, self.account.cash)
        self.config.override(CONF_ANALYZER_SECTION, CONF_START_TRADE_DATE, self.__startTradeDate)
        self.config.override(CONF_ANALYZER_SECTION, CONF_END_TRADE_DATE, self.end_trade_date)
        self._setupLog()
        LOG.debug(self.securities)
        if not self.securities:
            self._load_securities(securities)

    @property
    def trade_type(self):
        return self.config.get(CONF_ANALYZER_SECTION, CONF_TRADE_TYPE)

    def _setupLog(self):
        ''' setup logging '''
        if self.config.getSection("loggers"):
            logging.config.fileConfig(self.config.getFullPath())

    def _run_one_test(self, security):
        ''' run one test '''
        LOG.debug("Running backtest for %s" % security)
        runner = TestRunner(
                self.config,
                self.pubsub,
                self.session,
                self.__mCalculator,
                [security],
                self.start_tick_date,
                self.end_trade_date,
                self.account,
                self.trade_type)
        runner.runTest()

    def _load_securities(self, securities):
        symbol_filename = self.config.get(CONF_ANALYZER_SECTION, CONF_SYMBOL_FILE)
        assert symbol_filename is not None, "%s is required in config file" % CONF_SYMBOL_FILE

        LOG.info("loading securities from %s" % os.path.join(self.config.getDir(), symbol_filename))

        with open(os.path.join(self.config.getDir(), symbol_filename), "r") as securities_file:
            for symbol in securities_file:
                if securities not in map(lambda sec: sec.symbol, self.securities):
                    security = self.session.query(Security).filter_by(symbol=symbol.strip('\n')).first()
                    if security is None:
                        LOG.info('No security {0}. Skipping. Please import stock information'.format(symbol))
                        continue
                    self.securities.append(security)

        assert self.securities, "None symbol provided"

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
    def __init__(self, config, pubsub, session, metric_manager, securities, start_tick_date, endTradeDate, account, trade_type):
        self.config = config
        self.trade_type = trade_type
        self.account = account
        self.start_tick_date = start_tick_date
        self.end_trade_date = endTradeDate
        self.index_helper = IndexHelper()
        self.history = History()
        self.securities = securities
        self.metric_manager = metric_manager

        self._setup_trading_center()
        self._setup_tick_feeder()

        # wire things together
        self._setup_strategy()
        self.tick_feeder.trading_center = self.trading_center
        self.trading_engine.tickProxy = self.tick_feeder
        self.trading_engine.orderProxy = self.trading_center

    def _setup_trading_center(self):
        self.trading_center.start = 0
        self.trading_center.end = None

    def _setup_tick_feeder(self):
        self.tick_feeder.index_helper = self.index_helper
        i_symbol = self.config.get(CONF_ANALYZER_SECTION, CONF_INDEX)
        self.tick_feeder.index_symbol = i_symbol

    def _setup_strategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.create_strategy(
                self.config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
                self.securities,
                self.config)

        # register on trading engine
        self.trading_engine.register(strategy)

    def _execute(self):
        ''' run backtest '''
        LOG.info("Running backtest for %s" % self.securities)
        # start trading engine
        thread = Thread(target=self.trading_engine.runListener, args=())
        thread.setDaemon(False)
        thread.start()

        # start tickFeeder
        # share a queue and this should be another thread
        timePositions = self.account.positions
        startTradeDate = self.config.get(CONF_ANALYZER_SECTION, CONF_START_TRADE_DATE)
        if startTradeDate:
            startTradeDate = int(startTradeDate)
            timePositions = [tp for tp in timePositions if tp[0] >= startTradeDate]

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

        self.trading_engine.stop()
        thread.join(timeout=240)

    def _printResult(self):
        ''' print result'''
        LOG.info("account %s" % self.account)
        LOG.debug([str(order) for order in self.account.orders])
        LOG.debug("account position %s" % self.account.positions)

    def runTest(self):
        ''' run one test '''
        self._execute()
        self._printResult()


# ###########Util function################################
def getBackTestResultDbName(securities, strategyName, start_tick_date, endTradeDate):
    ''' get table name for back test result'''
    return "%s__%s__%s__%s" % ('_'.join(securities) if len(securities) <= 1 else len(securities), strategyName, start_tick_date, endTradeDate if endTradeDate else "Now")

if __name__ == "__main__":
    account = Account()
    account.deposit(1000)
    backtester = BackTester(
            "backtest_zscoreMomentumPortfolio.ini",
            account=account,
            start_tick_date=19901010,
            startTradeDate=19901010,
            endTradeDate=20131010)
    backtester.setup()
    backtester.runTests()
    backtester.printMetrics()
