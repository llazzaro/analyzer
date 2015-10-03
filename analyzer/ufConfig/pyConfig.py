'''
Created on Nov 30, 2010

@author: ppa
'''
import ConfigParser
from os import path
from analyzer.lib.errors import UfException, Errors

import logging
LOG = logging.getLogger()


class PyConfig(object):
    ''' class that handles configuration '''
    def __init__(self):
        ''' Constructor '''
        self.__dir = None
        self.parser = None
        self.full_path = None

    def setSource(self, file_name):
        '''
        set source file name
        assume the file_name is full path first, if can't find it, use conf directory
        '''
        fullPath = path.abspath(file_name)

        if not path.exists(fullPath):
            fullPath = path.join(path.join(path.dirname(path.dirname(path.dirname(path.abspath(__file__)))), 'conf'),
                                 file_name)
            if not path.exists(fullPath):
                msg = "config file doesn't exist at: %s or %s" % (file_name, fullPath)
                LOG.error(msg)
                raise UfException(Errors.FILE_NOT_EXIST, msg)

        self.parser = ConfigParser.SafeConfigParser(defaults={"here": self.__dir})
        self.parser.read(fullPath)
        self.full_path = fullPath

    def getDir(self):
        ''' get directory of conf file'''
        self.__validateConfig()
        return path.dirname(self.full_path)

    def getSection(self, section):
        ''' load all configuration '''
        self.__validateConfig()

        configs = {}
        if self.parser and self.parser.has_section(section):
            for name, value in self.parser.items(section):
                configs[name] = value
            return configs

        return configs

    def get(self, section, option):
        ''' whether an option exists in the section '''
        self.__validateConfig()

        if self.parser and self.parser.has_option(section, option):
            return self.parser.get(section, option)
        else:
            return None

    def getFullPath(self):
        ''' get full path of config '''
        return self.full_path

    def override(self, section, key, value):
        ''' override/set a key value pair'''
        if not self.parser.has_section(section):
            self.parser.add_section(section)

        self.parser.set(section, key, str(value))

    def __validateConfig(self):
        ''' validate config is ok '''
        if self.parser is None:
            msg = "No config file is loaded, please use setSource method first"
            LOG.error(msg)
            raise UfException(Errors.FILE_NOT_EXIST, msg)


if __name__ == '__main__':
    config = PyConfig()
    config.setSource('test.ini')
    config.override("testSection", "123", "456")
    config.override("testSection", "123", "567")
    print(config.get('app_main', 'feeder'))
    print(config.getSection('app_main'))
    print(config.get("testSection", "123"))
