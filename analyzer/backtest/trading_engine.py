'''
Created on Nov 6, 2011

@author: ppa
'''
import logging

LOG=logging.getLogger(__name__)


class TradingEngine(object):
    '''
        has the responsability to keep track
        and execute strategies
        Sends actions to trading center
    '''
    def __init__(self, pubsub):
        self.strategies = set()
        self.trading_center=None
        self.pubsub = pubsub

    def stop(self):
        ''' set stop flag '''
        self._stop=True

    def listen(self, security):
        LOG.info('Trading engine listening to {0}'.format(security.symbol))
        self.pubsub.subscribe(security.symbol)

    def register(self, strategy):
        self.strategies.add(strategy)

    def unregister(self, strategy):
        self.strategies.remove(strategy)

    def _convert_raw_tick_to_object(self):
        pass

    def consume(self):
        for tick in self.pubsub.listen():
            LOG.info('New tick {0}'.format(tick))
            for strategy in self.strategies:
                # strategy will create actions
                # traging center will see the actions
                # and will place orders
                action = strategy.update(tick)
                if action:
                    self.pubsub.publish('action', action)
