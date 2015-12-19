'''
Created on Nov 6, 2011

@author: ppa
'''
import logging
import traceback

log=logging.getLogger(__name__)


class Feeder(object):
    '''
        This class has the responsability of broadcast ticks or quotes for one security only
    '''
    def __init__(self, publisher, security, dam, start=None, end=None):
        self.security = security
        self.dam=dam
        self.start=start
        self.end=end
        self.publisher = publisher

    def execute(self, start, end):
        for data in self.load(start, end):
            log.debug('Publish new tick')
            self.publisher.publish(self.security.symbol, data)


class TickFeeder(Feeder):

    def _get_symbol_data(self, security, start, end):
        return self.dam.ticks(security, start, end)

    def load(self, start, end):
        log.debug('Start loading ticks, it may take a while......')

        try:
            return self._get_symbol_data(self.security, start, end)

        except KeyboardInterrupt as ki:
            log.warn("Interrupted by user  when loading ticks for %s" % self.security)
            raise ki
        except BaseException as excp:
            log.warn("Unknown exception when loading ticks for %s: except %s, traceback %s" % (self.security, excp, traceback.format_exc(8)))


class QuoteFeeder(Feeder):

    def _get_symbol_data(self, security, start, end):
        return self.dam.quotes(security, start, end)

    def load(self, start, end):
        log.debug('Indexing quotes for %s' % self.security)
        try:
            return self._get_symbol_data(self.security, start, end)

        except KeyboardInterrupt as ki:
            log.warn("Interrupted by user  when loading quotes for %s" % self.security)
            raise ki
        except BaseException as excp:
            log.warn("Unknown exception when loading quotes for %s: except %s, traceback %s" % (self.security, excp, traceback.format_exc(8)))
