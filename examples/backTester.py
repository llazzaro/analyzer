'''
Created on Dec 3, 2011

@author: ppa
'''
from analyzer.module.backtester import BackTester
from pyStock.models import Account
from pyStock.models.money import Money, Currency

if __name__ == "__main__":

    account = Account()
    pesos = Currency(name='Pesos', code='ARG')
    account.deposit(Money(amount=1000, currency=pesos))
    back_tester=BackTester("backtest_smaPortfolio.ini", startTickDate=20101010, startTradeDate=20111220, account=account)
    back_tester.runTests()
    back_tester.printMetrics()
