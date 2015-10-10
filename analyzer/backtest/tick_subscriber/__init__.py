'''
Created on Nov 6, 2011

@author: ppa
'''
import abc
import uuid
import threading


class TickSubscriber(object):
    ''' tick subscriber '''
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        ''' constructor '''
        self.id = self.__generateId()
        self.name = name
        self.__threadLock = threading.Lock()

    def __generateId(self):
        return uuid.uuid4()

    def pre_consume(self, ticks):
        raise NotImplementedError('Abtract class method called')

    @abc.abstractmethod
    def tick_update(self, ticks):
        ''' consume ticks '''
        return

    def order_executed(self, order_dict):
        ''' call back for executed order with order id, should be overridden '''
        return

    #@abc.abstractmethod
    def complete(self):
        raise NotImplementedError('Abtract class method called')

