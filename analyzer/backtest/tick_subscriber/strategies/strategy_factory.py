'''
Created on Dec 26, 2011

@author: ppa
'''

# from analyzerstrategies.periodStrategy import PeriodStrategy
from analyzerstrategies.sma_strategy import SMAStrategy
# from analyzerstrategies.smaPortfolioStrategy import SMAPortfolioStrategy
# from analyzerstrategies.zscorePortfolioStrategy import ZscorePortfolioStrategy
# from analyzerstrategies.zscoreMomentumPortfolioStrategy import ZscoreMomentumPortfolioStrategy

from analyzer.lib.errors import Errors, UfException


class StrategyFactory(object):
    STRATEGY_DICT = {
            # 'period': PeriodStrategy,
            'sma': SMAStrategy,
            # 'smaPortfolio': SMAPortfolioStrategy,
            # 'zscorePortfolio': ZscorePortfolioStrategy,
            # 'zscoreMomentumPortfolio': ZscoreMomentumPortfolioStrategy
    }

    @staticmethod
    def create_strategy(name, securities, config):
        ''' create a metric '''
        if name not in StrategyFactory.STRATEGY_DICT:
            raise UfException(Errors.INVALID_STRATEGY_NAME,
                              "Strategy name is invalid %s" % name)
        return StrategyFactory.STRATEGY_DICT[name](config, securities)

    @staticmethod
    def available_strategies():
        ''' return all available types '''
        return StrategyFactory.STRATEGY_DICT.keys()
