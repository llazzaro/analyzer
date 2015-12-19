import logging

from analyzer.constant import (
    BUY,
    SELL,
)
from pystock.models import (
    BuyOrder,
    SellOrder,
)

log=logging.getLogger(__name__)


class BackTester(object):
    '''
        has the responsability to keep track
        and execute strategies
        broadcast actions for backtesting
    '''
    def __init__(self, session, account, store, pubsub, security, strategy, start=None, end=None):
        self.store = store
        self.account = account
        self.session = session
        self.strategy = strategy
        self.pubsub = pubsub
        self.security = security
        self.start = start
        self.end = end

    def _retrieve_ticks(self, security, start, end):
        return self.store[security.exchange.code].read(security.symbol)

    def execute(self, action):
        # back tester buy and sells everything
        if action.action() == BUY:
            order = BuyOrder(account=self.account, security=self.security, price=action.price(), share=self.calculate_buy_share(security))
        if action.action() == SELL:
            order = SellOrder(account=self.account, security=self.security, price=action.price(), share=self.calculate_sellshare(security))

        self.session.add(order)
        self.session.commit()

    def consume(self):
        log.info('Processing security {0}'.format(self.security))
        # strategy will create actions
        # traging center will see the actions
        # and will place orders
        data_frame = self._retrieve_ticks(self.security, self.start, self.end).data
        for action in self.strategy.update(security, data_frame):
            if action:
                action.is_backtest = True
                self.execute(action)
                self.pubsub.publish('actions', action.__json__())
