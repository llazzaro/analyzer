from datetime import datetime
from threading import Thread

from analyzer.module.backtester import BackTester
from analyzer.backtest.tick_feeder import TickFeeder
from analyzer.backtest.trading_center import TradingCenter
from analyzerdam.DAMFactory import DAMFactory

from analyzer.backtest.constant import (
    CONF_ANALYZER_SECTION,
    CONF_INPUT_DAM,
    CONF_INPUT_DB,
)


class TickFeederThread(Thread):

    def __init__(self, config, pubsub, securities, start=None, end=None):
        Thread.__init__(self)
        self.config = config
        self.tick_feeder = TickFeeder(
            publisher=pubsub,
            securities=securities,
            dam=self._create_dam(""),  # no need to set symbol because it's batch operation
        )
        self.last_execution = datetime.now()

    def _create_dam(self, symbol):
        dam_name = self.config.get(CONF_ANALYZER_SECTION, CONF_INPUT_DAM)
        input_db = self.config.get(CONF_ANALYZER_SECTION, CONF_INPUT_DB)
        dam = DAMFactory.createDAM(dam_name, {'db': input_db})
        dam.symbol = symbol

        return dam

    def run(self):
        self.last_execution = datetime.now()
        self.tick_feeder.execute(self.last_execution, datetime.now())


class TradingCenterThread(Thread):

    def __init__(self, session, pubsub):
        Thread.__init__(self)
        self.trading_center = TradingCenter(session, pubsub)

    def run(self):
        while True:
            self.trading_center.consume()


class BackTesterThread(Thread):
    def __init__(self, config, pubsub, session, account, securities, trading_engine, start_tick_date=0, start_trade_date=0, end_trade_date=None):
        Thread.__init__(self)
        self.back_tester=BackTester(
                config=config,
                pubsub=pubsub,
                session=session,
                account=account,
                securities=securities,
                trading_engine=trading_engine,
                start_tick_date=start_tick_date,
                start_trade_date=start_trade_date,
                end_trade_date=end_trade_date)

    def run(self):
        self.back_tester.run_tests()
