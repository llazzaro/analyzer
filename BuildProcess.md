# INSTRUCTION #
Ultra-finance is a pure python project. It's easy to install dependencies and enjoy the fun of playing with the code.

# REQUIREMENTS #
Please install Python2.6 or Python2.7 first. Python 2.7.1 with Mac Lion is tested.

At this moment, we don't support Python3 because python package Numpy haven't been ported to Python3 yet.

We also require pip be installed so that library dependencies can be handled automatically.
Please refer to:
http://pypi.python.org/pypi/pip/

# PYTHON PACKAGE DEPENDENCIES #
## MINIMUM SET ##
Minimum set of Python package dependencies:

Backtesting: [SQLAlchemy](http://pypi.python.org/pypi/SQLAlchemy), [beautifulsoup](http://pypi.python.org/pypi/BeautifulSoup), [numpy](http://pypi.python.org/pypi/numpy), [mox](http://pypi.python.org/pypi/mox)

Ta-Lib: ［http://pypi.python.org/pypi/pandas pandas］

## OTHER PACKAGES ##
It will be nice to have other libraries installed as well to
[xlwt](http://pypi.python.org/pypi/xlwt), [xlrd](http://pypi.python.org/pypi/xlrd), [hbase-thrift](http://pypi.python.org/pypi/hbase-thrift), [matplotlib](http://pypi.python.org/pypi/matplotlib)

Note that on Mac Lion, numpy comes with Xcode4. There is no need for you to install it.


# FROM TAR FILE #
1. download tar file from http://code.google.com/p/ultra-finance/downloads/list

2. untar file:
```
$ unzip ultraFinance-0.0.3.zip -d ultraFinance
```

3. enter directory:
```
$ cd ultraFinance
```

4. install as develop mode (Python libraries as SQLAlchemy, beautifulsoup, numpy  will be installed automatically):
```
pan@mac $ sudo python setup.py develop
/System/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/distutils/dist.py:267: UserWarning: Unknown distribution option: 'install_not_requires'
  warnings.warn(msg)
running develop
running egg_info
writing requirements to ultrafinance.egg-info/requires.txt
writing ultrafinance.egg-info/PKG-INFO
writing top-level names to ultrafinance.egg-info/top_level.txt
writing dependency_links to ultrafinance.egg-info/dependency_links.txt
writing manifest file 'ultrafinance.egg-info/SOURCES.txt'
running build_ext
Creating /Library/Python/2.7/site-packages/ultrafinance.egg-link (link to .)
ultrafinance 1.0.1 is already the active version in easy-install.pth

Installed /Users/ppa/workspace/ultrafinance/trunk
Processing dependencies for ultrafinance==1.0.1
Searching for mox==0.5.3
Best match: mox 0.5.3
Processing mox-0.5.3-py2.7.egg
mox 0.5.3 is already the active version in easy-install.pth

Using /Library/Python/2.7/site-packages/mox-0.5.3-py2.7.egg
Searching for SQLAlchemy==0.7.8
Best match: SQLAlchemy 0.7.8
Processing SQLAlchemy-0.7.8-py2.7-macosx-10.7-intel.egg
SQLAlchemy 0.7.8 is already the active version in easy-install.pth

Using /Library/Python/2.7/site-packages/SQLAlchemy-0.7.8-py2.7-macosx-10.7-intel.egg
Searching for beautifulsoup4==4.1.1
Best match: beautifulsoup4 4.1.1
Processing beautifulsoup4-4.1.1-py2.7.egg
beautifulsoup4 4.1.1 is already the active version in easy-install.pth

Using /Library/Python/2.7/site-packages/beautifulsoup4-4.1.1-py2.7.egg
Searching for numpy==1.5.1
Best match: numpy 1.5.1
numpy 1.5.1 is already the active version in easy-install.pth

Using /System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python
Finished processing dependencies for ultrafinance==1.0.1
```

5. run unit test:
```
pan@mac:~/project/ultraFinance$ sudo python setup.py test
running test
....
```

6. run example:

a) retrieving daily/minute stock info(Open, Close, Low, High, Volumn).

We download historical prices from [Google Finance](http://www.google.com/finance/historical?q=NASDAQ:EBAY&output=csv)/Yahoo Finance, and store it to database.

Details
http://code.google.com/p/ultra-finance/wiki/stockCrawler


b) retrieving stock fundamental info(Revenue, Net Income, Diluted Normalized EPS...).

We parse page from [Google Finance](http://www.google.com/finance?q=NASDAQ:EBAY&fstype=ii), and store it to database.

Details
http://code.google.com/p/ultra-finance/wiki/FundamentalsCrawler


c) run backtesting. Once historical prices database is stored, you can run backtesting using the database.


Details
https://code.google.com/p/ultra-finance/wiki/Backtesting

# FROM SOURCE CODE #
Please refer to: http://code.google.com/p/ultra-finance/source/checkout