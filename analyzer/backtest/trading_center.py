'''
Created on Dec 18, 2011

@author: ppa
'''
import uuid
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
        self.__openOrders={}  # SAMPLE: {"EBAY": {orderId1: order1, orderId2: order2}}
        self.__closedOrders={}  # SAMPLE {"EBAY": [order1, order2]}
        self.__updatedOrder={}  # SAMPLE {"EBAY": [order1, order2]}
        self.__placedOrder={}  # SAMPLE {"EBAY": [order1, order2]}
        self.__lastTickDict=None

    def getUpdatedOrder(self):
        ''' return orders with status changes '''
        updatedOrder={}
        updatedOrder.update(self.__updatedOrder)
        self.__updatedOrder.clear()

        return updatedOrder

    def getPlacedOrder(self):
        ''' return orders that has been placed '''
        placedOrder={}
        placedOrder.update(self.__placedOrder)
        self.__placedOrder.clear()

        return placedOrder

    def __generateId(self):
        ''' generate id '''
        return uuid.uuid4()

    def cancelOrder(self, symbol, orderId):
        ''' cancel an order '''
        if symbol not in self.__openOrders:
            LOG.warn("Can't cancel order %s because there is no open orders for symbol %s" % (orderId, symbol))
            return

        if orderId not in self.__openOrders[symbol]:
            LOG.warn("Can't cancel order %s because there is no open orders for order id %s with symbol %s" % (orderId, orderId, symbol))
            return

        # TODO cancel the order and update history
        del self.__openOrders[symbol][orderId]

        # if no open orders left for that symbol, remove it
        if not len(self.__openOrders[symbol]):
            del self.__openOrders[symbol]

        LOG.debug("Order canceled: %s" % orderId)

    def cancelAllOpenOrders(self):
        ''' cancel all open order '''
        for symbol, orderIdAndOrderDict in self.__openOrders.items():
            for orderId, order in orderIdAndOrderDict.values():
                order.status=Order.CANCELED  # change order state
                self.__closedOrders[orderId]=order

            del self.__openOrders[symbol]

    def consumeTicks(self, tickDict):
        ''' consume ticks '''
        self._checkAndExecuteOrders(tickDict)
        self.accountManager.updateAccountsPosition(tickDict)

    def _checkAndExecuteOrders(self, tickDict):
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

    def __executeOrder(self, tick, order):
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

    def isOrderMet(self, tick, order):
        ''' whether order can be execute or not '''
        return order.is_order_met(tick)
