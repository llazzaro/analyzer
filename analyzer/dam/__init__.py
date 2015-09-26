import abc


class BaseDAM(object):
    ''' base class for DAO '''
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.symbol = None

    def read_quotes(self, start, end):
        raise NotImplementedError('Abstract method called')

    def write_quotes(self, quotes):
        raise NotImplementedError('Abstract method called')

    def read_ticks(self, start, end):
        raise NotImplementedError('Abstract method called')

    def write_ticks(self, ticks):
        raise NotImplementedError('Abstract method called')

    def read_fundamental(self):
        raise NotImplementedError('Abstract method called')

    def write_fundamental(self, keyTimeValueDict):
        raise NotImplementedError('Abstract method called')

    def setup(self, settings):
        raise NotImplementedError('Abstract method called')

    def commit(self):
        raise NotImplementedError('Abstract method called')
