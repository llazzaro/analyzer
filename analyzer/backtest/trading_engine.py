import json
import logging

LOG=logging.getLogger(__name__)


class TradingEngine(object):
    '''
        has the responsability to execut strategies
        Sends actions to trading center
        does not store anything, used for realtime
    '''
    def __init__(self, pubsub, strategy, start=None, end=None):
        self.pubsub = pubsub
        self.strategy = strategy
        self.start = start
        self.end = end
        self.securities = []

    def listen(self, security):
        self.securities.append(security)
        self.pubsub.subscribe(security.symbol)

    def execute(self, tick):
        action = self.strategy.update(tick)
        if action:
            self.pubsub.publish('action', action)

    def consume(self):
        for security in self.securities:
            for tick in self.pubsub.listen():
                LOG.info('New tick {0}'.format(tick))
                if tick['type'] in 'subscribe':
                    continue
                # strategy will create actions
                # traging center will see the actions
                # and will place orders
                tick['security'] = security
                tick['data'] = json.loads(tick['data'].decode('utf-8').replace("'", '"'))
                self.execute(tick)
