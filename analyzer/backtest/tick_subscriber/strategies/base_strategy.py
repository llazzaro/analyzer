'''
Created on Dec 25, 2011

@author: ppa
'''
import abc
from analyzer.backtest.tick_subscriber import TickSubscriber

import logging
LOG=logging.getLogger()


class BaseStrategy(TickSubscriber):
    ''' trading center '''
    __meta__=abc.ABCMeta

    def __init__(self, name, account):
        super(BaseStrategy, self).__init__(name)
        self.account=account
        self.trading_engine=None
        self.config_dict={}

        self.cur_time=''
        self.index_helper=None
        self.history=None
        self.account=account
