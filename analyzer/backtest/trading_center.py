'''
Created on Dec 18, 2011

@author: ppa
'''
import time

import logging

from pyStock.models import Order
from analyzer.lib.errors import Errors, UfException

LOG=logging.getLogger()


class TradingCenter(object):
    '''
    trading center
    Note: set metricNames before adding accounts
    '''
    def __init__(self):
        ''' constructor '''
        self.accountManager=None
        self.__updatedOrder={}  # SAMPLE {"EBAY": [order1, order2]}
        self.__placedOrder={}  # SAMPLE {"EBAY": [order1, order2]}
        self.__lastTickDict=None

    def updated_order(self):
        ''' return orders with status changes '''
        updatedOrder={}
        updatedOrder.update(self.__updatedOrder)
        self.__updatedOrder.clear()

        return updatedOrder

    def placed_order(self):
        ''' return orders that has been placed '''
        placedOrder={}
        placedOrder.update(self.__placedOrder)
        self.__placedOrder.clear()

        return placedOrder

    def cancel_order(self, symbol, orderId):
        ''' cancel an order '''
        if symbol not in self.__openOrders:
            LOG.warn("Can't cancel order %s because there is no open orders for symbol %s" % (orderId, symbol))
            return

        if orderId not in self.open_orders(symbol):
            LOG.warn("Can't cancel order %s because there is no open orders for order id %s with symbol %s" % (orderId, orderId, symbol))
            return

        # TODO cancel the order and update history
        del self.__openOrders[symbol][orderId]

        # if no open orders left for that symbol, remove it
        if not len(self.__openOrders[symbol]):
            del self.__openOrders[symbol]

        LOG.debug("Order canceled: %s" % orderId)

    def cancel_all_open_orders(self):
        ''' cancel all open order '''
        for symbol, orderIdAndOrderDict in self.__openOrders.items():
            for orderId, order in orderIdAndOrderDict.values():
                order.status=Order.CANCELED  # change order state
                self.__closedOrders[orderId]=order

            del self.__openOrders[symbol]

    def consume_ticks(self, tickDict):
        ''' consume ticks '''
        self._checkAndExecuteOrders(tickDict)
        self.accountManager.updateAccountsPosition(tickDict)

    def _check_and_execute_orders(self, tickDict):
        ''' check and execute open order '''
        self.__lastTickDict=tickDict
        for symbol, tick in tickDict.iteritems():
            LOG.debug("_checkAndExecuteOrders symbol %s with tick %s, price %s" % (symbol, tick.time, tick.close))
            if symbol not in self.__openOrders:
                LOG.debug("_checkAndExecuteOrders no open orders for symbol %s with tick %s, price %s" % (symbol, tick.time, tick.close))
                continue

            for order in self.__openOrders[symbol].values():
                if self.isOrderMet(tick, order):
                    self.__executeOrder(tick, order)

    def __checkAndExecuteOrder(self, order):
        ''' check and execute one order '''
        tick=self.__lastTickDict.get(order.symbol)
        if tick is None:
            LOG.debug("_checkAndExecuteOrder no open orders for symbol %s with tick %s, price %s" % (order.symbol, tick.time, tick.close))
            return

        if self.isOrderMet(tick, order):
            self.__executeOrder(tick, order)

    def __execute_order(self, tick, order):
        ''' execute an order '''
        account=self.accountManager.getAccount(order.accountId)
        if not account:
            raise UfException(Errors.INVALID_ACCOUNT,
                              ''' Account is invalid with accountId %s for order %s''' % (order.accountId, order.orderId))
        else:
            LOG.debug("executing order %s" % order)
            try:
                account.execute(order, tick)
                order.status=Order.FILLED
                order.filledTime=time.time()

                self.__closedOrders[order.orderId]=order
                self.__updatedOrder[order.orderId]=order
            except Exception as ex:
                LOG.error("Got exception when executing order %s: %s" % (order, ex))

            del self.__openOrders[order.symbol][order.orderId]
            if not len(self.__openOrders[order.symbol]):
                del self.__openOrders[order.symbol]

    def is_order_met(self, tick, order):
        ''' whether order can be execute or not '''
        return order.is_order_met(tick)

    def open_order_by_id(self, id):
        raise NotImplementedError()
