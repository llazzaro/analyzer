#usage of stock crawler

Stock Crawler is used to save quotes or ticks from Google Finance to sqlite or HBase. By default, it saves quotes to to sqlite database as stock.sqlite located at "{project folder}/data/" directory.

To view data from sqlite, a few tools are available, e.g.
https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/

# Usage #
```
ppa@mac:~/ultra/examples$python stockCrawler.py -h
Usage: stockCrawler.py [options]

Options:
  -h, --help            show this help message and exit
  -f SYMBOLFILE, --symbolFile=SYMBOLFILE
                        file that contains symbols for each line
  -t DATATYPE, --dataType=DATATYPE
                        data type that will be stored, e.g. quote|tick|all
  -s START, --start=START
                        start date, all|month
  -o OUTPUTDAM, --outputDAM=OUTPUTDAM
                        output dam, e.g. sql|hbase
```

# Get Historical Data of Stocks for Last Month #
```
ppa@mac:~/ultra/examples$python stockCrawler.py -f ../data/symbols/SPY500.list
Retrieving data type quote
Sqlite location: sqlite:////Users/pan/stock.sqlite
Retrieving data start from 20120202
Processed MMM
Processed ACE
...
Processed ZMH
Processed ZION
Succeeded: ['MMM', 'ACE', 'ABT'...]
Failed: ['CEPH', 'FO', 'GENZ'...]
```

# Get Historical Ticks for Last 15 Days #
Unfortunately, Google Finance only provides ticks for last 15 days, and since the data is huge, it may takes up to 1.5 hours to store all ticks of SPY500.
```
ppa@mac:~/ultra/examples$python stockCrawler.py -f ../data/symbols/SPY500.list -t tick
Retrieving data type tick
Sqlite location: sqlite:////Users/pan/stock.sqlite
Retrieving ticks for last 15 days
Processed MMM
Processed ACE
Processed ABT
.....
```

# View Result #
A file named sqldam.sqlite will be generated in "{project folder}/trunk/data/". You can view it by any Sqlite UI tools. Sqlite-manager on my laptop:
![http://ultra-finance.googlecode.com/files/quoteSqlite.png](http://ultra-finance.googlecode.com/files/quoteSqlite.png)