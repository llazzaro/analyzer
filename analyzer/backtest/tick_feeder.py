'''
Created on Nov 6, 2011

@author: ppa
'''
from analyzer.lib.errors import UfException, Errors
from threading import Thread

from analyzer.backtest.constant import TICK, QUOTE
from analyzer.backtest.constant import STATE_SAVER_INDEX_PRICE

import traceback
import time
import logging
LOG=logging.getLogger()


class TickFeeder(object):
    '''
        no tick operation should take more that 2 second
        threadMaxFails indicates how many times thread for a subscriber can timeout,
        if it exceeds, them unregister that subscriber
    '''
    def __init__(self, interval_timeout=2, start=0, end=None, trade_type=None, symbols=None, dam=None):
        self.subs={}  # securityIds: sub
        self.symbols=symbols
        self.inde_symbol=None
        self.dam=dam
        self.interval_timeout=interval_timeout
        self.start=start
        self.end=end
        self.trading_center=None
        self.saver=None
        self.updated_tick=None
        self.time_ticks_dict={}
        self.i_time_position_dict={}
        self.trade_type=trade_type

    def get_updated_tick(self):
        ''' return timeTickTuple with status changes '''
        timeTicksTuple=self.__updatedTick

        return timeTicksTuple

    def clear_update_tick(self):
        ''' clear current ticks '''
        self.updated_tick=None

    def _get_symbol_ticks_dict(self, symbols):
        ''' get ticks from one dam'''
        ticks=[]
        if TICK == self.trade_type:
            ticks=self.__dam.readBatchTupleTicks(symbols, self.start, self.end)
        elif QUOTE == self.trade_type:
            ticks=self.__dam.readBatchTupleQuotes(symbols, self.start, self.end)
        else:
            raise UfException(Errors.INVALID_TYPE,
                              'Type %s is not accepted' % self.trade_type)

        return ticks

    def __load_ticks(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.info('Start loading ticks, it may take a while......')

        LOG.info('Indexing ticks for %s' % self.__symbols)
        try:
            self.timeTicksDict=self._getSymbolTicksDict(self.__symbols)

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.__symbols)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.__symbols, excp, traceback.format_exc(8)))

    def __load_index(self):
        ''' generate timeTicksDict based on source DAM'''
        LOG.debug('Start loading index ticks, it may take a while......')
        try:
            return self._getSymbolTicksDict([self.index_symbol])

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.index_symbol)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.index_symbol, excp, traceback.format_exc(8)))

        return {}

    def execute(self):
        ''' execute func '''
        self.__loadTicks()

        for timeStamp in sorted(self.timeTicksDict.iterkeys()):
            # make sure trading center finish updating first
            self._freshTradingCenter(self.timeTicksDict[timeStamp])

            self._freshUpdatedTick(timeStamp, self.timeTicksDict[timeStamp])
            # self._updateHistory(timeStamp, self.timeTicksDict[timeStamp], self.indexTicksDict.get(timeStamp))

            while self.__updatedTick:
                time.sleep(0)

    def _fresh_updated_tick(self, timeStamp, symbolTicksDict):
        ''' update self.__updatedTick '''
        self.__updatedTick=(timeStamp, symbolTicksDict)

    def _fresh_trading_center(self, symbolTicksDict):
        ''' feed trading center ticks '''
        self.tradingCenter.consumeTicks(symbolTicksDict)

    def complete(self):
        '''
        call when complete feeding ticks
        write history to saver
        '''
        try:
            if not self.saver:
                return

            timeITicksDict=self.__loadIndex()
            if timeITicksDict:
                for c_time, symbolDict in timeITicksDict.iteritems():
                    for symbol in symbolDict.keys():
                        self.saver.write(c_time, STATE_SAVER_INDEX_PRICE, symbolDict[symbol].close)
                        self.iTimePositionDict[time]=symbolDict[symbol].close
                        break  # should only have one benchmark

        except Exception as ex:
            LOG.warn("Unknown error when recording index info:" + str(ex))

    def set_index_symbol(self, index_symbol):
        ''' set symbols '''
        self.index_symbol=index_symbol

    def pub_ticks(self, ticks, sub):
        ''' publish ticks to sub '''
        thread=Thread(target=sub.pre_consume, args=(ticks,))
        thread.setDaemon(False)
        thread.start()
        return thread
