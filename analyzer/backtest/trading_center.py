'''
Created on Dec 18, 2011

@author: ppa
'''
import logging

from pyStock.models import (
    Order,
    FillOrderStage,
)

LOG=logging.getLogger()


class TradingCenter(object):
    '''
        receives orders
    '''
    def __init__(self, session, pubsub):
        self.session = session
        self.pubsub = pubsub

    def cancel_order(self, order):
        if order not in self.open_orders(order.security):
            LOG.warn("Can't cancel order %s because there is no open orders for symbol {0}".format(order.security.symbol))
            return

        order.cancel()
        LOG.debug("Order canceled: {0}" .format(order.pk))

    def cancel_all_open_orders(self):
        for order in self.open_orders:
            order.cancel()

    def consume(self):
        for tick in self.pubsub.listen():
            self._check_and_execute_orders(tick)

    def _check_and_execute_orders(self, tick):
        LOG.debug("_check_and_execute_orders symbol %s with tick %s, price %s" % (tick.security, tick.time, tick.close))
        if self.open_orders(tick.security).count() == 0:
            LOG.debug("_check_and_execute_orders no open orders for symbol %s with tick %s, price %s" % (tick.security, tick.time, tick.close))
            return

        for order in self.open_orders(tick.security):
            if order.is_order_met(tick):
                self._execute_order(tick, order)

    def _check_and_execute_order(self, order):
        tick=self.last_tick_dict.get(order.symbol)
        if tick is None:
            LOG.debug("_check_and_execute_order no open orders for symbol %s with tick %s, price %s" % (order.symbol, tick.time, tick.close))
            return

        if order.is_order_met(tick):
            self._execute_order(tick, order)

    def _execute_order(self, tick, order):
        LOG.debug("executing order {0}".format(order))
        order.update_stage(FillOrderStage())

    def open_orders(self, security):
        return filter(lambda order: order.current_stage.is_open, self.session.query(Order).filter(security=security))
