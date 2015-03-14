#usage of backtesting

BackTester is used to run backtesting on multiple stocks based on historical prices.

To run backtesting, you need run stock crawler first to get historical stock prices. Details for running stockCrawler can be found at
https://code.google.com/p/ultra-finance/wiki/stockCrawler

# Usage #
1 run stock crawler for stocks list under {project}/conf/stock.list, which saves historical data to sqlite database at {project}/data/stock.sqlite

```
ppa:~/workspace/ultrafinance/trunk $
==>python examples/stockCrawler.py -f conf/stock.list -s all
Retrieving data type: quote
Sqlite location: sqlite:////Users/ppa/workspace/ultrafinance/trunk/data/stock.sqlite
Retrieving quotes start from 19800101
Processed EBAY
Processed GOOG
Processed C
Succeeded: ['EBAY', 'GOOG', 'C']
Failed: []
```

2 run back tester which loads database from {project}/data/stock.sqlite and using conf at {project}/conf/backtest\_period.ini. Output includes account info and metrics liks highest point, lowest point, and sharp ratio.
```
ppa@mac:ppa: python examples/backTester.py 
12/07/25 23:49:11.128 INFO  [MainThread] Running backtest for EBAY
12/07/25 23:49:15.476 INFO  [Thread-1] create db sqlite:////Users/ppa/workspace/ultrafinance/trunk/conf/../data/output.sqlite with table EBAY_period with cols set(['updatedOrder', 'account-025d8eaa-689f-4ee7-9563-a45e3c15d344', 'placedOrder', 'EBAY'])
12/07/25 23:49:15.535 INFO  [Thread-1] committed table EBAY_period at sqlite:////Users/ppa/workspace/ultrafinance/trunk/conf/../data/output.sqlite
12/07/25 23:49:15.565 INFO  [MainThread] account {'holdings': {'EBAY': [5217.697471939725, 21.848717870877156]}, 'holdingCost': '114000.00', 'totalValue': '1120013.73', 'cash': '886000.00', 'accountId': '025d8eaa-689f-4ee7-9563-a45e3c15d344'}
12/07/25 23:49:15.582 INFO  [MainThread] Lowest point 956759.32 at 20090309; Highest point 1120013.73 at 20120720; STDDEV is 31381.02; Sharpe ratio is 0.26
12/07/25 23:49:15.583 INFO  [MainThread] Running backtest for GOOG
12/07/25 23:49:17.937 INFO  [Thread-3493] create db sqlite:////Users/ppa/workspace/ultrafinance/trunk/conf/../data/output.sqlite with table GOOG_period with cols set(['GOOG', 'account-43831361-f926-4692-9178-48f30203a23c', 'placedOrder', 'updatedOrder'])
12/07/25 23:49:17.973 INFO  [Thread-3493] committed table GOOG_period at sqlite:////Users/ppa/workspace/ultrafinance/trunk/conf/../data/output.sqlite
12/07/25 23:49:18.001 INFO  [MainThread] account {'holdings': {'GOOG': [145.06840162625818, 427.38459447379523]}, 'holdingCost': '62000.00', 'totalValue': '1026610.68', 'cash': '938000.00', 'accountId': '43831361-f926-4692-9178-48f30203a23c'}
12/07/25 23:49:18.015 INFO  [MainThread] Lowest point 989441.04 at 20081124; Highest point 1034393.65 at 20120104; STDDEV is 9387.26; Sharpe ratio is 0.24
12/07/25 23:49:18.017 INFO  [MainThread] Running backtest for C
12/07/25 23:49:22.022 INFO  [Thread-5502] create db sqlite:////Users/ppa/workspace/ultrafinance/trunk/conf/../data/output.sqlite with table C_period with cols set(['C', 'account-c070994a-5839-4191-8ba5-99cd0d018d3e', 'placedOrder', 'updatedOrder'])
12/07/25 23:49:22.092 INFO  [Thread-5502] committed table C_period at sqlite:////Users/ppa/workspace/ultrafinance/trunk/conf/../data/output.sqlite
12/07/25 23:49:22.118 INFO  [MainThread] account {'holdings': {'C': [1172.71601770855, 113.41194116191727]}, 'holdingCost': '133000.00', 'totalValue': '897338.16', 'cash': '867000.00', 'accountId': 'c070994a-5839-4191-8ba5-99cd0d018d3e'}
12/07/25 23:49:22.139 INFO  [MainThread] Lowest point 882607.21 at 20110506; Highest point 1049071.37 at 20061227; STDDEV is 47789.20; Sharpe ratio is -0.28
```

# View Result #
Trading details/records can be found at database at {project}/data/output.sqlite. You can view it by any Sqlite UI tools. Sqlite-manager on my laptop:
![http://ultra-finance.googlecode.com/files/backtest_output.png](http://ultra-finance.googlecode.com/files/backtest_output.png)