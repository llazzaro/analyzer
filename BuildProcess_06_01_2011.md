# INSTRUCTION #
Ultra-finance is a pure python project. It's easy to install dependencies and enjoy the fun of playing with the code.

# REQUIREMENT #
Please install python first. Python 2.6.6 is tested.

We also require setuptools be installed so that library dependencies can be handled automatically.
Please refer to:
http://pypi.python.org/pypi/setuptools

# FROM TAR FILE #
1. download tar file from http://code.google.com/p/ultra-finance/downloads/list

2. untar file:
```
$ unzip ultraFinance-0.0.2.zip -d ultraFinance
```

3. enter directory:
```
$ cd ultraFinance
```

4. install as develop mode (these python libraries PyDispatcher, xlrd, xlwt, matplotlib, scipy, numpy will be installed automatically):
```
pan@mac:~/project/ultraFinance$ sudo python setup.py develop
running develop
running egg_info
creating ultrafinance.egg-info
writing requirements to ultrafinance.egg-info/requires.txt
writing ultrafinance.egg-info/PKG-INFO
writing top-level names to ultrafinance.egg-info/top_level.txt
writing dependency_links to ultrafinance.egg-info/dependency_links.txt
writing manifest file 'ultrafinance.egg-info/SOURCES.txt'
reading manifest file 'ultrafinance.egg-info/SOURCES.txt'
writing manifest file 'ultrafinance.egg-info/SOURCES.txt'
running build_ext
Creating /opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/ultrafinance.egg-link (link to .)
Adding ultrafinance 1.0.0 to easy-install.pth file

Installed /Users/papan/project/ultraFinance
Processing dependencies for ultrafinance==1.0.0
Searching for scipy==0.9.0
Best match: scipy 0.9.0
Adding scipy 0.9.0 to easy-install.pth file

Using /opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages
Searching for numpy==1.6.0
Best match: numpy 1.6.0
Adding numpy 1.6.0 to easy-install.pth file

Using /opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages
Searching for xlrd==0.7.1
Best match: xlrd 0.7.1
Processing xlrd-0.7.1-py2.6.egg
xlrd 0.7.1 is already the active version in easy-install.pth
Installing runxlrd.py script to /opt/local/Library/Frameworks/Python.framework/Versions/2.6/bin

Using /opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/xlrd-0.7.1-py2.6.egg
Searching for xlwt==0.7.2
Best match: xlwt 0.7.2
Processing xlwt-0.7.2-py2.6.egg
xlwt 0.7.2 is already the active version in easy-install.pth

Using /opt/local/Library/Frameworks/Python.framework/Versions/2.6/lib/python2.6/site-packages/xlwt-0.7.2-py2.6.egg
Finished processing dependencies for ultrafinance==1.0.0
```

5. run unit test:
```
pan@mac:~/project/ultraFinance$ sudo python setup.py test
running test
Running tests: ['tests.unit.test_excel_lib', 'tests.unit.test_historical_data_storage',
'tests.unit.test_plot_portfolio', 'tests.unit.test_singleton',
'tests.unit.test_stock_measurement', 'tests.unit.test_trading_strategy_factory',
'tests.unit.test_yahoo_finance']
NOTE *** Ignoring non-worksheet data named u'Fig 2.1' (type 0x02 = Chart)
.BuildExls ['MMM', 'ACE', 'ABT', 'ANF', 'ADBE', 'AMD'], div 2
Saved ['MMM', 'ACE', 'ABT'] to /Users/pan/project/ultraFinance/tests/output/buildExl0.xls
Saved ['ANF', 'ADBE', 'AMD'] to /Users/pan/project/ultraFinance/tests/output/buildExl1.xls
.buildExlsFromFile /Users/pan/project/ultraFinance/tests/unit/stock.list, div 2
BuildExls ['MMM', 'ACE', 'ABT', 'ANF'], div 2
Saved ['MMM', 'ACE'] to /Users/pan/project/ultraFinance/tests/output/fromFile0.xls
Saved ['ABT', 'ANF'] to /Users/pan/project/ultraFinance/tests/output/fromFile1.xls
.....................
----------------------------------------------------------------------
Ran 24 tests in 39.768s

OK

```

6. run example:
a) plot google historical price
```
pan@mac:~/project/ultraFinance$ python examples/plotGoogle.py 
Using configuration file historicalStock.ini
Using configure file: /Users/pan/project/ultra/trunk/ultrafinance/processChain/config/historicalStock.ini
Start loading plugins.....
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/feeder
Plugin loaded: defaultFeeder
Plugin loaded: excelDataFeeder
Plugin loaded: historicalDataFeeder
Plugin loaded: indexDataFeeder
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/processor
Plugin loaded: avgDivProcessor
Plugin loaded: defaultProcessor
Plugin loaded: tradingStrategyProcessor
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/outputer
Plugin loaded: defaultOutputer
Plugin loaded: emailOutputer
Plugin loaded: plotStockOutputer
Plugin loaded: plotYearlyOutputer
Start setting up dispatcher......
connect historicalDataFeeder to receiver defaultProcessor
connect defaultProcessor to receiver plotStockOutputer
Running plugin: historicalDataFeeder
running HistoricalDataFeeder
send out signal historicalDataFeeder
running DefaultProcessor
send out signal defaultProcessor
running PlotStockOutputer
```

You will see a graph:
https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/google.png?attachauth=ANoY7cp_YlaHwJ9ih3dXVubkTsh08BHAIQUL_iPd_A0a5b33fnnY0hOACt4apiPfyI3pRjEnnmMHwfQcKhpzhko0DFdbA9dzCySZsbtZnTinNb_EovAI69ROw__iAVNwDZmlp3LKgenYxNCek3k7u5NFWldpXrtnFENWWunVBKz9VKC4mARwvjWR9sbtFdXMOvq6zR-oNWYk&attredirects=0

b) plot historical interest, hoursing, stock:
```
pan@mac:~/project/ultraFinance$ python examples/plotInterestHoursingStock.py 
Using configuration file interestHoursingStock.ini
Using configure file: /Users/papan/project/ultra/trunk/ultrafinance/processChain/config/interestHoursingStock.ini
Start loading plugins.....

Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/feeder
Plugin loaded: defaultFeeder
Plugin loaded: excelDataFeeder
Plugin loaded: historicalDataFeeder
Plugin loaded: indexDataFeeder
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/processor
Plugin loaded: avgDivProcessor
Plugin loaded: defaultProcessor
Plugin loaded: tradingStrategyProcessor
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/outputer
Plugin loaded: defaultOutputer
Plugin loaded: emailOutputer
Plugin loaded: plotStockOutputer
Plugin loaded: plotYearlyOutputer
Start setting up dispatcher......
connect excelDataFeeder to receiver defaultProcessor
connect defaultProcessor to receiver plotYearlyOutputer
Running plugin: excelDataFeeder
running ExcelDataFeeder
NOTE *** Ignoring non-worksheet data named u'Fig 2.1' (type 0x02 = Chart)
NOTE *** Ignoring non-worksheet data named u'PDVPlot' (type 0x02 = Chart)
NOTE *** Ignoring non-worksheet data named u'ConsumptionPlot' (type 0x02 = Chart)
send out signal excelDataFeeder
running DefaultProcessor
send out signal defaultProcessor
running PlotYearlyOutputer
send out signal plotYearlyOutputer
```

You will see a graph:
https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/interestHoursingStock.png?attachauth=ANoY7crc1Yp32jM36yRNyuwIlUb1MbiZQMwsypsfgnmD_rLQsKieQ-i1d_1BnQ7O1pYaOQwazwk2Qv5TXD4KkKcGbzgTOVTSYbey9M3pAJJh4h4u65iJNL0Dr9bBY9VRvIn5coQdc_kZNaXIUOCerf623imKt-P19Ng8Biw3stv3zWZQn9yeQ29AUe579UzXI3gkRmhtBULotiHMFDxQw3rSp1wGo9wafA%3D%3D&attredirects=0

c) run three trading strategies:
```
pan@mac:~/project/ultraFinance$ python examples/usTradingStrategy.py 
Using configuration file usTradingStrategy.ini
Using configure file: /Users/papan/project/ultra/trunk/ultrafinance/processChain/config/usTradingStrategy.ini
Start loading plugins.....

Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/feeder
Plugin loaded: defaultFeeder
Plugin loaded: excelDataFeeder
Plugin loaded: historicalDataFeeder
Plugin loaded: indexDataFeeder
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/processor
Plugin loaded: avgDivProcessor
Plugin loaded: defaultProcessor
Plugin loaded: tradingStrategyProcessor
Loading plugins under /Users/pan/project/ultra/trunk/ultrafinance/processChain/outputer
Plugin loaded: defaultOutputer
Plugin loaded: emailOutputer
Plugin loaded: plotStockOutputer
Plugin loaded: plotYearlyOutputer
Start setting up dispatcher......
connect indexDataFeeder to receiver tradingStrategyProcessor
connect tradingStrategyProcessor to receiver defaultOutputer
Running plugin: indexDataFeeder
running IndexDataFeeder
NOTE *** Ignoring non-worksheet data named u'PDVPlot' (type 0x02 = Chart)
NOTE *** Ignoring non-worksheet data named u'ConsumptionPlot' (type 0x02 = Chart)
send out signal indexDataFeeder
running TradingStrategyProcessor
send out signal tradingStrategyProcessor
running DefaultOutputer
{'adjustFixAmountPerPeriod': 78.580140747647647,
'fixAmountPerPeriodWithAddtionWhenDrop': 92.012559339770704,
'fixAmountPerPeriod': 74.635451845880709}
```

d) enumerate trading SPY500 in one week and print out return rate:
```
pan@mac:~/project/ultraFinance$ python examples/enumerateWeeklyTrading.py 
/Users/pan/project/ultraFinance/dataSource/SPY/spy
BuildExls ['SPY'], div 1
Saved ['SPY'] to /Users/papan/project/ultraFinance/dataSource/SPY/spy0.xls
(('THU.', 'MON.'), '-1.82')
(('FRI.', 'MON.'), '-14.65')
(('TUE.', 'FRI.'), '-29.86')
(('THU.', 'FRI.'), '-57.49')
(('FRI.', 'TUE.'), '-7.29')
(('WED.', 'FRI.'), '-9.92')
(('WED.', 'THU.'), '13.65')
(('WED.', 'MON.'), '17.25')
(('TUE.', 'WED.'), '18.95')
(('TUE.', 'THU.'), '22.06')
(('FRI.', 'WED.'), '23.16')
(('MON.', 'TUE.'), '23.84')
(('THU.', 'THU.'), '29.52')
(('FRI.', 'THU.'), '31.20')
(('THU.', 'TUE.'), '33.05')
(('MON.', 'WED.'), '36.53')
(('MON.', 'MON.'), '36.56')
(('TUE.', 'TUE.'), '38.00')
(('MON.', 'FRI.'), '4.47')
(('FRI.', 'FRI.'), '4.79')
(('TUE.', 'MON.'), '44.21')
(('MON.', 'THU.'), '50.16')
(('THU.', 'WED.'), '70.16')
(('WED.', 'WED.'), '70.76')
(('WED.', 'TUE.'), '76.80')
```

e) find Chinese stock list in file, download historical data from Yahoo Finance, calculate alphas, return rate and relative return rate for 1 day, 3 days, 30 days, 90 days, 250 days, 500 days and 750 days.
```
pan@mac:~/project/ultraFinance$ python examples/chinaReturn.py 
Save HistroyData Into Excel
buildExlsFromFile /Users/pan/project/ultraFinance/dataSource/CHINA/china10.list, div 5
BuildExls ['DL', 'DYP', 'EDU', 'EJ', 'GA', 'GRO', 'GSI', 'GU', 'LDK', 'LFT'], div 5
Saved ['DL', 'DYP'] to /Users/pan/project/ultraFinance/dataSource/CHINA/china0.xls
Saved ['EDU', 'EJ'] to /Users/pan/project/ultraFinance/dataSource/CHINA/china1.xls
Saved ['GA', 'GRO'] to /Users/pan/project/ultraFinance/dataSource/CHINA/china2.xls
Saved ['GSI', 'GU'] to /Users/pan/project/ultraFinance/dataSource/CHINA/china3.xls
Saved ['LDK', 'LFT'] to /Users/pan/project/ultraFinance/dataSource/CHINA/china4.xls
Start analyzing
Building BenchmarkValues
BenchmarkValues ['^STI', '^FTSE', '^GSPC', '^HSI'] built
Processing DL with benchmark ^GSPC
Analyzing DL break at 749
Processing DYP with benchmark ^GSPC
Analyzing DYP break at 354
Analyzing DYP break at 354
Processing EDU with benchmark ^GSPC
Processing EJ with benchmark ^GSPC
Processing GA with benchmark ^GSPC
Processing GRO with benchmark ^GSPC
Processing GSI with benchmark ^GSPC
Processing GU with benchmark ^GSPC
Processing LDK with benchmark ^GSPC
Processing LFT with benchmark ^GSPC
Days since going public [1, 3, 30, 90, 250, 500, 750]
returnRates: [0.0, -0.014251386643488273, -0.085734665898615323, 
-0.037434685594717229, -0.15847370067058217, -0.14205436608131056, 
0.20962726916629917]
alphas: [0, -7.1733008382642183, 0.097559081125037278, 0.11799264719957706, 
0.048317479223627433, 0.066711690865591505, 0.029693819862301941]
relativeReturnRates: [0.0, -0.014723355873883464, -0.085994842581676043, 
0.017847707469306646, 0.004720303339231402, 0.015996230718048045, 
0.32637241708639297]
```

# FROM SVN #
Please refer to: http://code.google.com/p/ultra-finance/source/checkout