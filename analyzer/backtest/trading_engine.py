'''
Created on Nov 6, 2011

@author: ppa
'''
import logging

LOG=logging.getLogger(__name__)


class TradingEngine(object):
    '''
        has the responsability to execute strategies and send orders "the brain"
    '''
    def __init__(self, pubsub):
        self.strategies = set()
        self.trading_center=None
        self.pubsub = pubsub

    def stop(self):
        ''' set stop flag '''
        self._stop=True

    def listen(self, security):
        ''' register to a security
        '''
        self.pubsub.subscribe(security.symbol)

    def register(self, strategy):
        self.strategies.add(strategy)

    def unregister(self, strategy):
        self.strategies.remove(strategy)

    def consume(self):
        for tick in self.pubsub.listen():
            for strategy in self.strategies:
                # strategy will create orders
                # traging center will see the order as open
                strategy.update(tick)
