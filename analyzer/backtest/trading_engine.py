'''
Created on Nov 6, 2011

@author: ppa
'''
import json
import logging
from time import sleep
from threading import Thread
from collections import defaultdict

from analyzer.backtest.constant import EVENT_TICK_UPDATE, EVENT_ORDER_EXECUTED
from analyzer.backtest.constant import STATE_SAVER_UPDATED_ORDERS, STATE_SAVER_PLACED_ORDERS


LOG=logging.getLogger()


class TradingEngine(object):
    '''
        no tick operation should take more that 0.5 second
        threadMaxFails indicates how many times thread for a subscriberscriber can timeout,
        if it exceeds, them unregister that subscriberscriber
    '''
    def __init__(self, threadTimeout=2, threadMaxFail=10):
        self.subscribers=defaultdict(dict)  # {'event': {subscriber: {symbols: subscriber} }
        self.tickProxy=None
        self.orderProxy=None
        self.saver=None
        self._threadTimeout=threadTimeout
        self._threadMaxFail=threadMaxFail
        self._curTime=""
        self._stop=False

    def stop(self):
        ''' set stop flag '''
        self._stop=True

    def validate(self, subscriber):
        ''' validate subscriberscriber '''
        symbols, rules = subscriber.subscriber_rules()

        '''
        if not symbols:
            raise UfException(Errors.SYMBOL_NOT_IN_SOURCE,
                               "can't find any symbol with re %s in source %s" % (symbolRe, self._source.keys()))
        '''
        # TODO: validate rules
        return symbols, rules, subscriber

    def register(self, subscriber):
        ''' register a subscriberscriber
            rule is not used for now
        '''
        symbols, events, subscriber=self.validate(subscriber)

        for event in events:
            self.subscribers[event][subscriber]={'symbols': symbols, 'fail': 0}
            LOG.debug('register %s with id %s to event %s, symbols %s'
                      % (subscriber.name, subscriber.id, event, symbols))

    def unregister(self, subscriber):
        ''' unregister subscriberscrip
        '''
        for event, subscriberDict in self.subscribers.items():
            if subscriber in subscriberDict.keys():
                del self.subscribers[event][subscriber]

                # remove whole subscribers[event] if it's empty
                if not self.subscribers[event]:
                    del self.subscribers[event]

                LOG.debug('unregister %s with id %s' % (subscriber.name, subscriber.id))

    # TODO: in real time trading, change this function
    def runListener(self):
        ''' execute func '''

        while True:
            if self._stop:
                LOG.debug("Stopping trading engine...")
                self._complete()
                break

            else:
                timeTicksTuple=self.tickProxy.getUpdatedTick()

                if not timeTicksTuple:
                    sleep(0)
                    continue

                if timeTicksTuple:
                    self._curTime=timeTicksTuple[0]
                    self._tick_update(timeTicksTuple)

                updatedOrderDict=self.orderProxy.getUpdatedOrder()
                placedOrderDict=self.orderProxy.getPlacedOrder()
                if updatedOrderDict:
                    self._orderUpdate(updatedOrderDict)

                # record order
                if self.saver:
                    self.saver.write(self._curTime, STATE_SAVER_UPDATED_ORDERS, json.dumps([str(order) for order in updatedOrderDict.values()]))
                    self.saver.write(self._curTime, STATE_SAVER_PLACED_ORDERS, json.dumps([str(order) for order in placedOrderDict.values()]))

                self.tickProxy.clearUpdateTick()

    def _complete(self):
        ''' call when complete feeding ticks '''
        for subscriberDict in self.subscribers.itervalues():
            for subscriber in subscriberDict.iterkeys():
                subscriber.complete()

    def consumeTicks(self, ticks, subscriber, event):
        ''' publish ticks to subscriber '''
        thread=Thread(target=getattr(subscriber, event), args=(ticks,))
        thread.setDaemon(False)
        thread.start()
        return thread

    def consumeExecutedOrders(self, orderDict, subscriber, event):
        ''' publish ticks to subscriber '''
        thread=Thread(target=getattr(subscriber, event), args=(orderDict,))
        thread.setDaemon(False)
        thread.start()
        return thread

    def placeOrder(self, order):
        ''' called by each strategy to place order '''
        orderId=self.orderProxy.placeOrder(order)
        return orderId

    def cancelOrder(self, symbol, orderId):
        ''' cancel order '''
        self.orderProxy.cancelOrder(symbol, orderId)

    def _orderUpdate(self, orderDict):
        '''
        order status changes
        '''
        event=EVENT_ORDER_EXECUTED
        for subscriber, attrs in self.subscribers[EVENT_ORDER_EXECUTED].items():
            thread=self.consumeExecutedOrders(orderDict, subscriber, event)
            thread.join(timeout=self._threadTimeout * 1000)
            if thread.isAlive():
                LOG.error("Thread timeout for order update subscriberId %s" % subscriber.subscriberId)
                attrs['fail'] += 1

            if attrs['fail'] > self._threadMaxFail:
                LOG.error("For order update, subscriberId %s fails for too many times" % subscriber.subscriberId)
                self.unregister(subscriber)

    def _tick_update(self, timeTicksTuple):
        ''' got tick update '''
        time, symbolTicksDict=timeTicksTuple
        # TODO: remove hard coded event
        # This should not happen
        event=EVENT_TICK_UPDATE
        if event not in self.subscribers:
            LOG.warn("EVENT_TICK_UPDATE not in self.subscribers %s" % self.subscribers)
            return

        for subscriber, attrs in self.subscribers[event].items():
            ticks={}
            for symbol in attrs['symbols']:
                if symbol in symbolTicksDict:
                    ticks[symbol]=symbolTicksDict[symbol]

            thread=self.consumeTicks(ticks, subscriber, event)
            thread.join(timeout=self._threadTimeout * 1000)
            if thread.isAlive():
                LOG.error("Thread timeout for tick update, subscriberId %s at time %s" % (subscriber.subscriberId, time))
                attrs['fail'] += 1

            if attrs['fail'] > self._threadMaxFail:
                LOG.error("For tick update, subscriberId %s fails for too many times" % subscriber.subscriberId)
                self.unregister(subscriber)

        if self.saver and len(symbolTicksDict) < 10:
            for symbol in symbolTicksDict:
                self.saver.write(self._curTime, symbol, str(symbolTicksDict[symbol]))
