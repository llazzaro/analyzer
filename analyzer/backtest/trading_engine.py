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
    def __init__(self, pubsub, strategy):
        self.strategy = strategy
        self.trading_center=None
        self.pubsub = pubsub

    def stop(self):
        ''' set stop flag '''
        self._stop=True

    def listen(self, security):
        LOG.info('Trading engine listening to {0}'.format(security.symbol))
        self.pubsub.subscribe(security.symbol)

    def consume(self):
        for tick in self.pubsub.listen():
            LOG.info('New tick {0}'.format(tick))
            # strategy will create actions
            # traging center will see the actions
            # and will place orders
            action = self.strategy.update(tick)
            if action:
                self.pubsub.publish('action', action)
