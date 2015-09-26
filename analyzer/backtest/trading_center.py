'''
Created on Dec 18, 2011

@author: ppa
'''
import logging

from pyStock.models import (
    Order,
    Security,
    FillOrderStage,
)

LOG=logging.getLogger()


class TradingCenter(object):
    '''
    trading center
    Note: set metricNames before adding accounts
    '''
    def __init__(self, session):
        self.session = session
        self.updated_order={}  # SAMPLE {"EBAY": [order1, order2]}
        self.placed_order={}  # SAMPLE {"EBAY": [order1, order2]}
        self.last_tick_dict=None

    def updated_order(self):
        updatedOrder={}
        updatedOrder.update(self.updated_order)
        self.updated_order.clear()

        return updatedOrder

    def placed_order(self):
        placedOrder={}
        placedOrder.update(self.placed_order)
        self.placed_order.clear()

        return placedOrder

    def cancel_order(self, order):
        if order not in self.open_orders:
            LOG.warn("Can't cancel order %s because there is no open orders for symbol {0}".format(order.security.symbol))
            return

        order.cancel()
        LOG.debug("Order canceled: {0}" .format(order.pk))

    def cancel_all_open_orders(self):
        for order in self.open_orders:
            order.cancel()

    def consume_ticks(self, raw_tick):
        self._check_and_execute_orders(raw_tick)

    def _check_and_execute_orders(self, raw_tick):
        self.last_tick_dict=raw_tick
        for symbol, tick in raw_tick.iteritems():
            LOG.debug("_check_and_execute_orders symbol %s with tick %s, price %s" % (symbol, tick.time, tick.close))
            if symbol not in self.open_orders:
                LOG.debug("_check_and_execute_orders no open orders for symbol %s with tick %s, price %s" % (symbol, tick.time, tick.close))
                continue

            for order in self.open_orders[symbol].values():
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
        account=order.account
        LOG.debug("executing order {0}".format(order))
        account.execute(order, tick)
        order.update_stage(FillOrderStage())

    def open_order_by_id(self, id):
        return self.session.query(Order).filter_by(id=id).first()

    def open_orders_by_symbol(self, symbol):
        return self.session.query(Order).join(Security).filter_by(symbol=symbol)

    @property
    def open_orders(self):
        return self.session.query(Order).all()
