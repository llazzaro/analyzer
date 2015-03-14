#summary what happen during developing
#labels Featured,python,excel,demo,eventdriven

# what happen during developing #
Interesting things happen in developing progress. You may want to know our stories:)

# 12/18/2010 #
First feeder(Yahoo Finance Feeder) is added into ultra-finance. I planed to use Google finance first, after checking online documents, it turns out that Google provides limit API that can only checking/change one's portfolio/transition, which is not enough for ultra-finance. So Yahoo Finance is chosen as our real-time data feeder.

# 12/18/2010 #
I like pylons configuration style(separately session and app\_global), I tried to mimic it in utlra-finance. My implementation is not elegant. Need to change later.

# 12/18/2010 #
You can send email to your gmail account now. The user name and password need to be set first.

# 12/21/2010 #
postpone multi-thread event driven platform. The reason is:
  * 1 if GUI is used, event driven is already provided
  * 2 if realtime trading platform need to be achieved, the best way may be to have a pool(sharing memeory or sharing database) with all threads running. So event-driven will be redundant.

# 12/21/2010 #
I am considering adding plotting into ultraFinance as outputer. A good article can be found at:
http://wiki.python.org/moin/NumericAndScientific/Plotting

ok, after some digging, i decide to use matplotlib for its full document and long term development. Numpy is required to install, whose 64 bit version can be found at:
http://www.lfd.uci.edu/~gohlke/pythonlibs/

# 12/25/2010 #
plotting ouputer done: get first graph for GOOG stock

https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/GOOGgraph.png?attachauth=ANoY7coK_n428Kpthsun1NWFKjUL2HlAExWS-i4KsAe9ZaV7HgVAIGuUk7Axzc1fhAyIPsyUGhOay76hrfvrtwvkhEysp4s-E21JTHkl0-bYQc7ay1g0aI2aMRHhQvOmRvYIfC5ix3DfKyeykc1i343_nG1MKVpK--EEcP2Ps5KwzxxU6LMxXXTHWrUiH0HHDrTATX3KnbBF&attredirects=0

# 12/26/2010 #
after two days trying with pydispatcher, I give up. It turns out that event driven is not suitable for multiple layer message/data processing. I am going to use pub/sub instead.

# 12/31/2010 #
i change the code structure quite a bit, and finally the pydispatcher works. Event-driven sounds so good:) Now it's time to do some real financial work

just find a project named pandas(wow, my usual web is panpandas), which provides a nice python financial library. it also uses matlibplot for plotting. And command console is provided(similiar to matlab). It's a good alternative comparing to UI.

Take a look:
http://code.google.com/p/pandas/

# 1/5/2011 #
calculate daily alpha and beta from web, Thanks to Jing He for helping calculation:)
my result for google since it starts:
{'standard deviation': 132.63009133956268, 'alpha': 0.00088338584008639898, 'beta': 0.99905902516274392, 'avg': 427.68574362165486, 'days': 1607}

# 1/10/2011 #
repolish data structure returned by yahoo financial feeder. plot grid graph.
my result for google since changes to:
{'standard deviation': 132.74733009492999, 'alpha': 0.08340930778923332, 'beta': 0.9178049215380969, 'avg': 428.03105590062069, 'days': 1610}

# 1/17/2011 #
project deadline in one week...will continue adding news features after that.

# 1/23/2011 #
integrating excel reading and writing using xlutils. Will update in a week.

# 1/31/2011 #
add excel reading module, plot hoursing market index graph
https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/hoursing.png?attachauth=ANoY7cpJflxe2vK-HEoflfkNulvS9JPQF4CK4aGPNKg_a8qU3ZvJyBRMLAqe05Jx2rrRFwhE_UYzhHxMm9xIwOc30TbhHGrxQuEhqMx1L8uxU3MAvmPN4s-H51l2GlfPfut19lOASr6YcjySdFcN0a9zYJRXK9n94ze6MbBTKF-bmRpaKtrHjektzwyU29LZ0XBVvCkMugRg&attredirects=0

# 1/31/2011 #
define date types; create PlotDateValue class to plot multiple lines
https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/housing_interest_stock.png?attachauth=ANoY7crtC7pAbmtzsyDGLukXzsOavzNPUgVp9TOSlbPRnVKvvcOhscA8QVo6zCaN_H9vsLnu_9UH8VPKeyqVYfjtklg1_nDs8itBlEkIUCVQHHtPaQHPba6Ugj-dvBq2zyQZRkuHr9jkYGWdtoYqKgKGBNVObR-_-KBW6_EZlUvDOtewluUs24s5OkEoicYYwYtPixGh7UZbsW5-jxS70T59v6KCZ8aSxA%3D%3D&attredirects=0

# 2/20/2011 #
portfolio graph:
https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/portfolios.png?attachauth=ANoY7coMMDdnX4Cd9XQOxUpHSYwMzj2z-_CVbLNK0N1YW_zC_3Bo_SKvWGKvwlgyxuI1CWn-WzfpH12ahZXGlhvsKswPHjES6scBrw51Ij2SUy7pAvfwnwnN-pkep_cX1DwzYZNzcTpNHsLsEXH3B7oy-Ziun9_MxeV_8E668GpAUHnjtuY6snGNIjbwx_6dSTLdWxLAtBr4&attredirects=0

# 2/26/2011 #
implemented two trading strategy. For spy500
  * if buying $1000 at the end of each year, the total return rate will be 74.63.
  * if buying $1000 at the end of each year plus an addition $1000 if index is the lowest during last 3 years, the total return rate will be 98.30
  * if buying $1000 at the end of each year plus an addition $1000 if index is the lowest during last 5 years, the total return rate will be 92.01
  * if buying $5000 for each 5 years the the price is the lowest for last 5 years, or at the the of 5 years period, the total return rate will be 78.58, which is not that good.

# 3/20/2011 #
add a module that grab all historical data of SPY500 companies and save to excel:) Now I am my own data suit

# 3/26/2011 #
learning quantlib design at http://quantlib.org/docs.shtml
considering using Array instead of List in python to gain better speed

# 3/27/2011 #
Add one trading strategy, buying and selling in one week. For SPY500 since 1993, if you buy on Wed and sell on next Tue., you will win $76; If you buy on Thu. and sell on the next day, you will lose $58

# 4/25/2011 #
Doing analyze of all Chinese stocks in U.S., U.K., Hong Kong and Singapore, a lot of bug that needs to be fixed

# 5/1/2011 #
Finish Analyzing Chinese stocks' return, alpha for 1 day, 1 week, 3 months and 1 year. Will post data soon

# 5/6/2011 #
Working on exception handling, logging, unittest and code clean up. It's boring and painful, but necessary for project quality:)

# 5/7/2011 #
add 6 unittests, add exception handling, add logging(not finished yet), move processor, feeder and outputer into processChain. Get sick of doing the re-factory work.... Will continue when I have time:)

# 5/8/2011 #
Just realize I will be super busy till early June, may not have extra time working on coding:( But I will keep on working on wiki and documents, and continue working after May:)

# 6/5/2011 #
i am back:)

# 6/11/2011 #
finish logging and exception handling

# 6/11/2011 #
Ipython is a powerful python shell easy to install, easy to use. Check http://ipython.org/ipython-doc/rel-0.10.2/html/ for more details

# 6/16/2011 #
fix processChain, add singleton design pattern

# 7/5/2011 #
support "python setup.py test" - unit test, "python setup.py clean" - clean **.pyc, "python setup.py develop" - development mode, "python setup.py install" - installation mode.
example/chinaReturn.py can run directly**

almost ready for first release

# 7/7/2011 #
add processChain.py into example. Need more exampel before first release

# 7/18/2011 #
add three more test cases, ready to build first release

# 7/30/2011 #
make a second build 0.0.2, which fix some bugs, and remove scipy dependency(it's so hard to install on mac and windows). This may be the first stable version.
I am going to add more documents.

# 7/31/2011 #
add observer design pattern,
add googleFinance.py to get historical data, P/E, avenue. etc. from Google Finance

# 8/12/2011 #
add stock picker, which get data from google finance, find the top 20 highest Diluted Normalized EPS

# 8/28/2011 #
reading.... find a good book online at: http://www.irinaclimbs.com/Books/ErnestChan_great_book.pdf

# 9/3/2011 #
performance tuning is soooooo painful for python code. looks like python is not the right language to do realtime trading...

# 9/25/2011 #
get tick data from google finance, so sad that google only provide tick data for half a month....

# 9/26/2011 #
installed Hadoop and HBase, can't find a good python client....plan to provide a interface to store all data in HBase

# 10/6/2011 #
doing design and adding Talib support

# 10/7/2011 #
tired of SWIG (used by quantLib and TA-lib). I am going to do my own TA-lib python implementation. For the beginning, I will do the most simplest ones.

# 10/23/2011 #
doing design..

# 11/05/2011 #
finished up draft design, ready to do implementation

# 11/06/2011 #
finished some basic part: model definition(tick, dateValue, dayTick), tickFeeder, tickSubsriber and tickManager.

So many things left...
Goal for next week: finish trading center, account, metric(base class and one concreate class).

# 11/08/2011 #
find another library named Pandas: https://github.com/wesm/pandas

so many pandas...

Just tried pandas, it's not pure python, Cpython is required for performance tuning. Will not use it for now.

statsmodels looks good, will consider integrate it.

# 11/26/2011 #
taking vacation for thanksgiving...

# 12/03/2011 #
finally complete all Data Access Module(DAM), need to clean up redudent files and build app that getting and saving historical quote/tick

# 12 /17/2011 #
what should be a good way to calculate moving average?
TA-Lib is doing it as
http://ta-lib.org/d_api/d_api.html
while a more pythonic way can be found at http://rosettacode.org/wiki/Averages/Simple_moving_average#Python

It seams to me that TA-Lib is good at analyzing data while the second one keep previous calculated data in memory, which makes it better for calculating MA as data come in the way.

# 12/18/2011 #
Finish coding tradingCenter. Things left: TickFeeder and strategies. Hopefully we can get first version by new year.

# 12/25/2011 #
working on first version of backtesting... So many features in wish list~

# 12/30/2011 #
finally get new backtesting setup and working with a testing strategy.
TODO: a. debug metrix
b. debug config module
c. debug logging module
d. add sharp ration and MACD strategy
e. add unit test, change example to read data from excel instead of hbase

# 1/2/2012 #
try
http://sourceforge.net/projects/hbaseexplorer/ which works great to view data in hbase
For a standalone hbase, zookeeper is running at 127.0.0.1:2181, which you need to fill in hbaseexplorer

# 1/7/2012 #
implemented a outputSaver module which save internal state(simulation details) to hbase, turns out the speed is extremely slow(take 5 minutes to do backtesting that costed only 1 minute). Need rethink about this module.

# 1/15/2012 #
adding unit tests

# 1/18/2012 #
Looks like I over simplified the backtesting model. Need to do refactory.

# 1/29/2012 #
refactory backtesting structure; decouple logic within tick feeder, trading engine, trading center and account manager; with this structure, it should be much easier to do realtime trading with some changes.

unittest is broken again.....

# 2/1/2012 #
add outputSaver to trading engine. get good status records.

# 2/2/2012 #
xxx Hbase, after fails installing updates on mac and reboot the machine, hbase crashed....
Solution is deleting temp files at /tmp/hbase-{username}

for account, add saver function that saves account value for each tick

# 2/11/2012 #
Busy doing other things. Will focus on documents instead of coding.

# 2/20/2012 #
Complete sqlDAM; after integration with backtesting, it should be good for second release

# 2/26/2012 #
bug fix for sql dam; add multi-threading to symbolCrawler, reduce time for collecting 500 stocks quotes to 17 mins; add sql storage support for symbolCrawler

# 3/08/2012 #
done with integration with sqlalchemy. All quotes are saved to sqlite, output of backtest is also written to sqlite. Need to add unit test and exception handling.

# 4/15/2012 #
thanks to Bruno Franca!! tons of technical indicators are added to pyTA-lib. Notice that pandas library is requested to use it.

# 5/28/2012 #
add fundamental crawler that fetches data from Google Finance into local data base; Add helper to back testing so that strategy is able to use history price and index price; fundamental info will not be available for backtesting because there is no good data source(can feed infor data to backtesting framework by splitting free data from Google Website)

# 7/21/2012 #
tries to port the proj from python 2.6 to python 3.2, fails because dependencies as numpy and pandas don't have a working version on mac lion with python 3.2

# 7/29/2012 #
converts svn to git

# 10/16/2012 #
reading books... I try to find a useful trading strategy and tuning the current code with real user case. The idea I follow is to make the project business driven instead of technique driven. The code should solve real world problem first.

# 01/01/2013 #
worked on another open source projec, which may potential be used as frontend UI

# 7/5/2013 #
Time flies~ I haven't seen any major changes or needs for numpy. I will update the whole project to Python 3 (for backtesting and data access/processing)
Find an interesting website: https://www.quantopian.com/