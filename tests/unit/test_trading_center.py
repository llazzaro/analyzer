'''
Created on Dec 18, 2011

@author: ppa
'''
import unittest
from analyzer.backtest.trading_center import TradingCenter
from pyStock.models import (
    Stock,
    Tick,
    BuyOrder,
    SellOrder,
    CancelOrderStage,
    Account,
)
from analyzer.lib.errors import UfException


class testTradingCenter(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testGetCopyAccounts(self):
        tc=TradingCenter()
        tc.createAccountWithMetrix(100000, 0)
        tc.createAccountWithMetrix(200000, 0)

        accounts=tc.getCopyAccounts('.*')
        print([str(account) for account in accounts])
        self.assertEquals(2, len(accounts))

    def testGetCopyAccount(self):
        tc=TradingCenter()
        accountId1=tc.createAccountWithMetrix(100000, 0)

        account=tc.getCopyAccount(accountId1)
        print(account)
        self.assertEquals(100000, account.cash)

    def testIsOrderMet(self):
        tc=TradingCenter()
        tick1=Tick('time', 'open', 'high', 'low', 13.20, 'volume')
        order1=BuyOrder(accountId=None, symbol='symbol', price=13.25, share=10)
        order2=BuyOrder(accountId=None, symbol='symbol', price=13.15, share=10)
        order3=SellOrder(accountId=None, symbol='symbol', price=13.25, share=10)
        order4=SellOrder(accountId=None, symbol='symbol', price=13.15, share=10)

        self.assertEquals(True, tc.isOrderMet(tick1, order1))
        self.assertEquals(False, tc.isOrderMet(tick1, order2))
        self.assertEquals(False, tc.isOrderMet(tick1, order3))
        self.assertEquals(True, tc.isOrderMet(tick1, order4))

    def testValidOrder(self):
        """
            Order instantiation raises exception if it is not valid
        """

        account=Account()
        unknown_acc=Account()
        stock=Stock(symbol='symbol')
        BuyOrder(account=account, security=stock, price=13.25, share=10)
        BuyOrder(account=unknown_acc, security=stock, price=13.25, share=10)

    def test_open_orders_by_order_id(self):
        account = Account()
        stock=Stock(symbol='symbol')
        order1=BuyOrder(account=account, security=stock, price=13.2, share=10)
        BuyOrder(account=account, security=stock, price=13.25, share=10)

        tc=TradingCenter()
        order=tc.open_order_by_id(order1.id)
        self.assertEquals(order1, order)

        order=tc.open_order_by_id(100)
        self.assertEquals(None, order)

    def testGetOpenOrdersBySymbol(self):

        account = Account()
        stock=Stock(symbol='symbol')
        order1=BuyOrder(account=account, security=stock, price=13.2, share=10)
        order2=BuyOrder(account=account, security=stock, price=13.25, share=10)

        tc=TradingCenter()
        orders=tc.open_orders_by_symbol('symbol1')
        self.assertEquals([order1, order2], orders)

    def testCancelOrder(self):

        account = Account()
        stock=Stock(symbol='symbol')
        order1=BuyOrder(account=account, symbol=stock, price=13.2, share=10)
        order2=BuyOrder(account=account, symbol=stock, price=13.25, share=10)


        tc=TradingCenter()

        tc.cancelOrder('id1')
        print(tc._TradingCenter__openOrders)
        print(tc._TradingCenter__closedOrders)
        self.assertEquals({'symbol1': [order2]}, tc._TradingCenter__openOrders)
        self.assertEquals({'id1': order1}, tc._TradingCenter__closedOrders)
        self.assertEquals(CancelOrderStage, type(order1.current_stage))

        tc.cancelOrder('id2')
        print(tc._TradingCenter__openOrders)
        print(tc._TradingCenter__closedOrders)
        self.assertEquals({}, tc._TradingCenter__openOrders)
        self.assertEquals({'id1': order1, 'id2': order2}, tc._TradingCenter__closedOrders)

    def testCancelAllOpenOrders(self):
        order1=BuyOrder(accountId='accountId', symbol='symbol1', price=13.2, share=10, orderId='id1')
        order2=BuyOrder(accountId='accountId', symbol='symbol1', price=13.25, share=10, orderId='id2')

        tc=TradingCenter()
        tc._TradingCenter__openOrders={'symbol1': [order1, order2]}

        tc.cancelAllOpenOrders()
        print(tc._TradingCenter__openOrders)
        print(tc._TradingCenter__closedOrders)
        self.assertEquals({}, tc._TradingCenter__openOrders)
        self.assertEquals({'id1': order1, 'id2': order2}, tc._TradingCenter__closedOrders)

    def testConsume(self):
        pass

    def testPostConsume(self):
        pass

    def testCreateAccountWithMetrix(self):
        pass
