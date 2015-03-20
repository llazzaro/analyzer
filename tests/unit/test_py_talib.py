'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest
from ultrafinance.pyTaLib.indicator import Sma


class testPyTaLib(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testSma(self):
        period = 3
        sma=Sma(period=period)
        expectedAvgs=[1, 1.3333333333333333, 2, 3, 4]
        for index, number in enumerate([1, 1, 1, 1, 2, 3, 4, 5]):
            result = sma(number)
            if index > period:
                self.assertEqual(expectedAvgs[index - period], result)
