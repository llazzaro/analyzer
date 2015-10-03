'''
Created on Dec 3, 2011

@author: ppa
'''
import os
import sys
import traceback
import logging
import logging.config

from pyStock.models import Account

from analyzer.backtest.tick_subscriber.strategies.strategy_factory import StrategyFactory
from analyzer.backtest.trading_center import TradingCenter
from analyzer.backtest.tick_feeder import TickFeeder
from analyzer.backtest.trading_engine import TradingEngine
from analyzer.ufConfig.pyConfig import PyConfig
from analyzerdam.DAMFactory import DAMFactory
from analyzer.backtest.stateSaver.stateSaverFactory import StateSaverFactory
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
    CONF_SAVER,
    CONF_OUTPUT_DB_PREFIX,
    CONF_STRATEGY_NAME
)
# from analyzer.backtest.metric import BasicMetric

from threading import Thread

LOG = logging.getLogger()


class BackTester(object):
    ''' back testing '''

    def __init__(self, config_file, session, account, startTickDate=0, startTradeDate=0, endTradeDate=None, symbolLists=None):
        LOG.debug("Loading config from %s" % config_file)
        self.config = PyConfig()
        self.session = session
        self.config.setSource(config_file)

        self.account = account
        self.__mCalculator = MetricManager()
        self.__symbolLists = symbolLists
        self.start_tick_date = startTickDate
        self.__startTradeDate = startTradeDate
        self.end_trade_date = endTradeDate
        self.__firstSaver = None

        ''' setup '''
        self.config.override(CONF_ANALYZER_SECTION, CONF_INIT_CASH, self.account.cash)
        self.config.override(CONF_ANALYZER_SECTION, CONF_START_TRADE_DATE, self.__startTradeDate)
        self.config.override(CONF_ANALYZER_SECTION, CONF_END_TRADE_DATE, self.end_trade_date)
        self._setupLog()
        LOG.debug(self.__symbolLists)
        if not self.__symbolLists:
            self._loadSymbols()

    @property
    def trade_type(self):
        return self.config.get(CONF_ANALYZER_SECTION, CONF_TRADE_TYPE)

    def _setupLog(self):
        ''' setup logging '''
        if self.config.getSection("loggers"):
            logging.config.fileConfig(self.config.getFullPath())

    def _runOneTest(self, symbols):
        ''' run one test '''
        LOG.debug("Running backtest for %s" % symbols)
        runner = TestRunner(
                self.config,
                self.session,
                self.__mCalculator,
                symbols,
                self.start_tick_date,
                self.end_trade_date,
                self.account,
                self.trade_type)
        runner.runTest()

    def _loadSymbols(self):
        ''' find symbols'''
        symbolFile = self.config.get(CONF_ANALYZER_SECTION, CONF_SYMBOL_FILE)
        assert symbolFile is not None, "%s is required in config file" % CONF_SYMBOL_FILE

        LOG.info("loading symbols from %s" % os.path.join(self.config.getDir(), symbolFile))
        if not self.__symbolLists:
            self.__symbolLists = []

        with open(os.path.join(self.config.getDir(), symbolFile), "r") as f:
            for symbols in f:
                if symbols not in self.__symbolLists:
                    self.__symbolLists.append([symbol.strip() for symbol in symbols.split()])

        assert self.__symbolLists, "None symbol provided"

    def runTests(self):
        ''' run tests '''
        for symbols in self.__symbolLists:
            try:
                self._runOneTest(symbols)
            except KeyboardInterrupt:
                LOG.error("User Interrupted")
                sys.exit("User Interrupted")
            except BaseException as excp:
                LOG.error("Unexpected error when backtesting %s -- except %s, traceback %s"
                          % (symbols, excp, traceback.format_exc(8)))

    def getMetrics(self):
        ''' get all metrics '''
        return self.__mCalculator.getMetrics()

    def printMetrics(self):
        ''' print metrics '''
        LOG.info(self.getMetrics())


class TestRunner(object):
    ''' back testing '''
    def __init__(self, config, session, metric_manager, symbols, startTickDate, endTradeDate, account, trade_type):
        self.config = config
        self.trade_type = trade_type
        self.account = account
        self.start_tick_date = startTickDate
        self.end_trade_date = endTradeDate
        self.tick_feeder = TickFeeder(
            start=startTickDate,
            end=endTradeDate,
            trade_type=trade_type,
            symbols=symbols,
            dam=self._create_dam(""),  # no need to set symbol because it's batch operation
        )
        self.trading_center = TradingCenter(session)
        self.trading_engine = TradingEngine()
        self.index_helper = IndexHelper()
        self.history = History()
        self.symbols = symbols
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

    def _create_dam(self, symbol):
        dam_name = self.config.get(CONF_ANALYZER_SECTION, CONF_INPUT_DAM)
        input_db = self.config.get(CONF_ANALYZER_SECTION, CONF_INPUT_DB)
        dam = DAMFactory.createDAM(dam_name, {'db': input_db})
        dam.symbol = symbol

        return dam

    def _setup_saver(self):
        ''' setup Saver '''
        saverName = self.config.get(CONF_ANALYZER_SECTION, CONF_SAVER)
        outputDbPrefix = self.config.get(CONF_ANALYZER_SECTION, CONF_OUTPUT_DB_PREFIX)
        if saverName:
            self.__saver = StateSaverFactory.createStateSaver(
                    saverName,
                    {
                        'db': outputDbPrefix + getBackTestResultDbName(
                            self.symbols,
                            self.config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
                            self.start_tick_date,
                            self.end_trade_date)})

    def _setup_strategy(self):
        ''' setup tradingEngine'''
        strategy = StrategyFactory.create_strategy(
                self.config.get(CONF_ANALYZER_SECTION, CONF_STRATEGY_NAME),
                self.symbols,
                self.config)

        # register on trading engine
        self.trading_engine.register(strategy)

    def _execute(self):
        ''' run backtest '''
        LOG.info("Running backtest for %s" % self.symbols)
        # start trading engine
        thread = Thread(target=self.trading_engine.runListener, args=())
        thread.setDaemon(False)
        thread.start()

        # start tickFeeder
        self.tick_feeder.execute()
        self.tick_feeder.complete()

        timePositions = self.account.positions
        startTradeDate = self.config.get(CONF_ANALYZER_SECTION, CONF_START_TRADE_DATE)
        if startTradeDate:
            startTradeDate = int(startTradeDate)
            timePositions = [tp for tp in timePositions if tp[0] >= startTradeDate]

        # get and save metrics
        # result = self.__metric_manager.calculate(self.symbols, timePositions, self.tick_feeder.iTimePositionDict)
        # self.__saver.writeMetrics(result[BasicMetric.START_TIME],
        #                          result[BasicMetric.END_TIME],
        #                          result[BasicMetric.MIN_TIME_VALUE][1],
        #                          result[BasicMetric.MAX_TIME_VALUE][1],
        #                          result[BasicMetric.SRATIO],
        #                          result[BasicMetric.MAX_DRAW_DOWN][1],
        #                          result[BasicMetric.R_SQUARED],
        #                          self.account.total,
        #                          self.account.holdings)

        # write to saver
        LOG.debug("Writing state to saver")
        # self.__saver.commit()

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
def getBackTestResultDbName(symbols, strategyName, startTickDate, endTradeDate):
    ''' get table name for back test result'''
    return "%s__%s__%s__%s" % ('_'.join(symbols) if len(symbols) <= 1 else len(symbols), strategyName, startTickDate, endTradeDate if endTradeDate else "Now")

if __name__ == "__main__":
    account = Account()
    account.deposit(1000)
    backtester = BackTester(
            "backtest_zscoreMomentumPortfolio.ini",
            account=account,
            startTickDate=19901010,
            startTradeDate=19901010,
            endTradeDate=20131010)
    backtester.setup()
    backtester.runTests()
    backtester.printMetrics()
