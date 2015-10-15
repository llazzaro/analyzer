'''
Created on Dec 18, 2011

@author: ppa
'''
import logging

from pyStock.models import (
    Order,
)

LOG=logging.getLogger()


class TradingCenter(object):
    '''
        receives actions from strategies
        could use metrics (option)
        creates orders, cancel orders, etc
    '''
    def __init__(self, session, pubsub):
        self.session = session
        self.pubsub = pubsub

    def cancel_orders(self):
        orders_to_cancel = filter(lambda order: order.current_stage.is_open, self.session.query(Order).all())
        for order in orders_to_cancel:
            order.cancel()
        return orders_to_cancel

    def listen(self, security):
        self.pubsub.subscribe('actions')

    def _load_action(self, action):
        raise NotImplementedError()

    def consume(self):
        # this trading center executes all actions
        # you could filter action source strategy.
        # combine strategies, etc
        for action in self.pubsub.listen():
            action = self._load_action(action)
            if not action.is_backtest:
                action.execute()

    def open_orders(self, security):
        return filter(lambda order: order.current_stage.is_open, self.session.query(Order).filter_by(security=security))
