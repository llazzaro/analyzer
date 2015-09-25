'''
Created on Dec 25, 2011

@author: ppa
'''
import abc
from analyzer.backtest.tick_subscriber import TickSubscriber
from analyzer.lib.errors import Errors, UfException
from analyzer.backtest.constant import EVENT_TICK_UPDATE, EVENT_ORDER_EXECUTED

import logging
LOG=logging.getLogger()


class BaseStrategy(TickSubscriber):
    ''' trading center '''
    __meta__=abc.ABCMeta

    def __init__(self, name, symbols):
        super(BaseStrategy, self).__init__(name)
        self.account=None
        self.trading_engine=None
        self.config_dict={}

        self.symbols=symbols
        self.cur_time=''
        self.index_helper=None
        self.history=None
        self.account_manager=None

    def subscriber_rules(self):
        ''' override function '''
        return (self.symbols, [EVENT_TICK_UPDATE, EVENT_ORDER_EXECUTED])

    @property
    def ready(self):
        '''
        whether strategy has been set up and ready to run
        TODO: check trading engine
        '''
        if self.account is None:
            raise UfException(Errors.NONE_ACCOUNT_ID,
                              "Account id is none")

        return True

    def place_order(self, order):
        ''' place order and keep record'''
        order_id=self.trading_engine.place_order(order)

        return order_id

    def complete(self):
        ''' complete operation '''
        pass
