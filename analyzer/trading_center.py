'''
Created on Dec 18, 2011

@author: ppa
'''
import json
import logging

from pystock.models import (
    Order,
)

log=logging.getLogger(__name__)


class TradingCenter(object):
    '''
        receives actions from strategies
        could use metrics (option)
        creates orders, cancel orders, etc
    '''
    def __init__(self, session, pubsub):
        self.session = session
        self.pubsub = pubsub
        self.pubsub.subscribe('actions')

    def cancel_orders(self):
        orders_to_cancel = list(filter(lambda order: order.current_stage.is_open, self.session.query(Order).all()))
        for order in orders_to_cancel:
            order.cancel()
        return orders_to_cancel

    def _load_action(self, action):
        return json.loads(action['data'])

    def consume(self):
        # this trading center executes all actions
        # you could filter action source strategy.
        # combine strategies, etc
        for action in self.pubsub.listen():
            if action['type'] == 'subscribe':
                return

            log.info('Received action {0}'.format(action))
            action = self._load_action(action)
            if not action['is_backtest']:
                action.execute()

    def open_orders(self, security):
        return list(filter(lambda order: order.current_stage.is_open, self.session.query(Order).filter_by(security=security)))
