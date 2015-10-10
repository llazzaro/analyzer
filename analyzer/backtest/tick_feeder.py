'''
Created on Nov 6, 2011

@author: ppa
'''
import logging
import traceback
from redis import StrictRedis

LOG=logging.getLogger(__name__)


class Feeder(object):
    '''
        This class has the responsability of broadcast ticks or quotes
    '''
    def __init__(self, publisher, interval_timeout=2, start=0, end=None, trade_type=None, securities=None, dam=None):
        self.subs={}  # securityIds: sub
        self.securities = securities
        self.inde_symbol=None
        self.dam=dam
        self.interval_timeout=interval_timeout
        self.start=start
        self.end=end
        self.trading_center=None
        self.saver=None
        self.time_ticks_dict={}
        self.i_time_position_dict={}
        self.trade_type=trade_type
        self.publisher = publisher

    def execute(self):
        for security, data in self.load():
            self.publisher.publish(security.symbol, data)

    def complete(self):
        '''
        call when complete feeding ticks
        write history to saver
        '''
        self.session.commit()

    def validate(self, subscriber):
        securities = []
        return securities

    def register(self, instance, symbol):
        pass


class TickFeeder(Feeder):

    def _get_symbol_data(self, securities):
        yield self.dam.read_ticks(securities, self.start, self.end)

    def load(self):
        ''' generate time_ticks_dict based on source DAM'''
        LOG.info('Start loading ticks, it may take a while......')

        LOG.info('Indexing ticks for %s' % self.securities)
        try:
            yield self._get_symbol_data(self.securities)

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading ticks for %s" % self.securities)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.securities, excp, traceback.format_exc(8)))

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

    def _get_symbol_data(self, securities):
        yield self.dam.read_quotes(securities, self.start, self.end)

    def load(self):
        LOG.info('Start loading quotes, it may take a while......')

        LOG.info('Indexing quotes for %s' % self.securities)
        try:
            yield self._get_symbol_data(self.securities)

        except KeyboardInterrupt as ki:
            LOG.warn("Interrupted by user  when loading quotes for %s" % self.securities)
            raise ki
        except BaseException as excp:
            LOG.warn("Unknown exception when loading quotes for %s: except %s, traceback %s" % (self.securities, excp, traceback.format_exc(8)))
