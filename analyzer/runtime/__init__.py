from datetime import datetime
from threading import Thread

from analyzer.backtest.tick_feeder import TickFeeder
from analyzer.backtest.trading_engine import TradingEngine
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
        self.tick_feeder.complete()


class TradingCenterThread(Thread):

    def __init__(self, session, pubsub):
        Thread.__init__(self)
        self.trading_center = TradingCenter(session, pubsub)

    def run(self):
        while True:
            self.trading_center.consume()


class TradingEngineThread(Thread):
    def __init__(self, pubsub):
        Thread.__init__(self)
        self.trading_engine = TradingEngine(pubsub)

    def run(self):
        pass


class BackTesterThread(Thread):
    pass
