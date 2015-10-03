'''
Created on Nov 6, 2011

@author: ppa
'''
import logging
import traceback

from analyzer.backtest.constant import STATE_SAVER_INDEX_PRICE

LOG=logging.getLogger(__name__)


class Feeder(object):
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

    def clear(self):
        self.updated_tick=None

    def execute(self):
        self.data = self.load()

        for time_stamp in sorted(self.data):
            # make sure trading center finish updating first
            self._feed_trading_center(self.data[time_stamp])

            self._refresh_updated_tick(time_stamp, self.data[time_stamp])
            # self._updateHistory(timeStamp, self.time_ticks_dict[timeStamp], self.indexTicksDict.get(timeStamp))

    def _refresh_updated_tick(self, time_stamp, symbol_ticks_dict):
        ''' update self.__updatedTick '''
        self.updated_tick=(time_stamp, symbol_ticks_dict)

    def _feed_trading_center(self, ticks):
        ''' feed trading center ticks '''
        self.trading_center.consume_ticks(ticks)

    def complete(self):
        '''
        call when complete feeding ticks
        write history to saver
        '''
        try:
            if not self.saver:
                return

            time_ticks_dict=self._load_index()
            if time_ticks_dict:
                for c_time, symbol_dict in time_ticks_dict.iteritems():
                    for symbol in symbol_dict.keys():
                        self.saver.write(c_time, STATE_SAVER_INDEX_PRICE, symbol_dict[symbol].close)
#                        self.iTimePositionDict[time]=symbol_dict[symbol].close
                        break  # should only have one benchmark

        except Exception as ex:
            LOG.warn("Unknown error when recording index info:" + str(ex))

    def validate(self, subscriber):
        symbols = []
        return symbols

    def register(self):
        pass


class TickFeeder(Feeder):

    def _get_symbol_data(self, symbols):
        ticks=self.dam.read_ticks(symbols, self.start, self.end)
        return ticks

    def load(self):
        ''' generate time_ticks_dict based on source DAM'''
        LOG.info('Start loading ticks, it may take a while......')

        LOG.info('Indexing ticks for %s' % self.symbols)
        try:
            return self._get_symbol_data(self.symbols)

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.symbols)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.symbols, excp, traceback.format_exc(8)))

    def _load_index(self):
        ''' generate time_ticks_dict based on source DAM'''
        LOG.debug('Start loading index ticks, it may take a while......')
        try:
            return self._get_symbol_data([self.index_symbol])

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.index_symbol)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.index_symbol, excp, traceback.format_exc(8)))

        return {}


class QuoteFeeder(Feeder):

    def _get_symbol_data(self, symbols):
        ''' get quotes from one dam'''
        quotes=[]
        quotes=self.dam.read_quotes(symbols, self.start, self.end)
        return quotes

    def load(self):
        LOG.info('Start loading quotes, it may take a while......')

        LOG.info('Indexing quotes for %s' % self.symbols)
        try:
            return self._get_symbol_data(self.symbols)

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading quotes for %s" % self.symbols)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading quotes for %s: except %s, traceback %s" % (self.symbols, excp, traceback.format_exc(8)))

    def _load_index(self):
        ''' generate time_ticks_dict based on source DAM'''
        LOG.debug('Start loading index ticks, it may take a while......')
        try:
            return self._get_symbol_data([self.index_symbol])

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for {0}".format(self.index_symbol))
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for {0}: except {1}, traceback {2}".format(self.index_symbol, excp, traceback.format_exc(8)))

        return {}
