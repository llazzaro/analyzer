import logging

LOG=logging.getLogger(__name__)


class BackTester(object):
    '''
        has the responsability to keep track
        and execute strategies
        broadcast actions for backtesting
    '''

    def __init__(self, store, securities, start=None, end=None):
        self.store = store
        self.securities = securities
        self.start = start
        self.end = end

    def _retrieve_ticks(self, start, end):
        raise NotImplementedError()

    def consume(self):
        for tick in self._retrieve_ticks(self.start, self.end):
            LOG.info('New tick {0}'.format(tick))
            # strategy will create actions
            # traging center will see the actions
            # and will place orders
            action = self.strategy.update(tick)
            if action:
                action.is_backtest = True
                self.pubsub.publish('action', action)
