'''
Created on Nov 6, 2011

@author: ppa
'''
from analyzer.lib.errors import Errors, UfException

import logging
LOG = logging.getLogger()


class StateSaverFactory(object):
    ''' factory for output saver '''
    @staticmethod
    def createStateSaver(name, setting):
        ''' create state saver '''
        if 'sql' == name:
            from analyzer.backtest.stateSaver.sqlSaver import SqlSaver
            saver = SqlSaver()
        else:
            raise UfException(Errors.INVALID_SAVER_NAME,
                              "Saver name is invalid %s" % name)

        saver.setup(setting)
        return saver
