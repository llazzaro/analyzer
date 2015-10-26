'''
Created on Nov 6, 2011

@author: ppa
'''
import logging

LOG=logging.getLogger(__name__)


class TradingEngine(object):
    '''
        has the responsability to execut strategies
        Sends actions to trading center
        does not store anything, used for realtime
    '''
    def __init__(self, pubsub, securities, start=None, end=None):
        self.pubsub = pubsub
        self.securities = securities
        self.start = start
        self.end = end

    def execute(self, tick):
        action = self.strategy.update(tick)
        if action:
            self.pubsub.publish('action', action)

    def consume(self):
        for security in self.securities:
            for tick in self.pubsub.listen():
                LOG.info('New tick {0}'.format(tick))
                # strategy will create actions
                # traging center will see the actions
                # and will place orders
                self.execute(tick)
