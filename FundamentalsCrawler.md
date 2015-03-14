#usage of stock crawler

Fundamentals Crawler is used to save fundamentals from Google Finance to sqlite or HBase. By default, it saves fundamentals to sqlite database as fundamental.sqlite located at "{project folder}/trunk/data/" directory.

To view data from sqlite, a few tools are available, e.g.
https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/

# Usage #
```
ppa@mac:~/ultra/trunk/examples$ python fundamentalCrawler.py -h
Usage: fundamentalCrawler.py [options]

Options:
  -h, --help            show this help message and exit
  -f SYMBOLFILE, --symbolFile=SYMBOLFILE
                        file that contains symbols for each line
  -o OUTPUTDAM, --outputDAM=OUTPUTDAM
                        output dam, e.g. sql|hbase

```

# Get Fundamentals #
```
ppa@mac:~/ultra/trunk/examples$python fundamentalCrawler.py -f ../data/symbols/SPY500.list 
Sqlite location: sqlite:////Users/ppa/workspace/ultrafinance/trunk/data/fundamental.sqlite
Processed MMM
Processed ACE
...
Processed ZMH
Processed ZION
Succeeded: ['MMM', 'ACE', 'ABT', 'ANF', 'ADBE', 'AMD', 'AES', 'AET', 'AFL', 'A', 'APD', 'ARG', 'AKS', 'AKAM', 'AA', 'ATI', 'AGN', 'ALL', 'ALTR', 'MO', 'AMZN', 'AEE', 'AEP', 'AXP', 'AIG', 'AMT', 'AMP', 'ABC', 'AMGN', 'APH', 'APC', 'ADI', 'AON', 'APA', 'AIV', 'APOL', 'AAPL', 'AMAT', 'ADM', 'AIZ', 'T', 'ADSK', 'ADP', 'AN', 'AZO', 'AVB', 'AVY', 'AVP', 'BHI', 'BLL', 'BAC', 'BK', 'BCR', 'BAX', 'BBT', 'BDX', 'BBBY', 'BMS', 'BRKb', 'BBY', 'BIG', 'BIIB', 'HRB', 'BMC', 'BA', 'BXP', 'BSX', 'BMY', 'BRCM', 'BFb', 'CHRW', 'CA', 'CVC', 'COG', 'CAM', 'CPB', 'COF', 'CAH', 'CFN', 'KMX', 'CCL', 'CAT', 'CBG', 'CBS', 'CELG', 'CNP', 'CTL', 'CERN', 'CF', 'SCHW', 'CHK', 'CVX', 'CB', 'CI', 'CINF', 'CTAS', 'CSCO', 'C', 'CTXS', 'CLF', 'CLX', 'CME', 'CMS', 'COH', 'KO', 'CCE', 'CTSH', 'CL', 'CMCSA', 'CMA', 'CSC', 'CPWR', 'CAG', 'COP', 'CNX', 'ED', 'STZ', 'CEG', 'GLW', 'COST', 'CVH', 'COV', 'CSX', 'CMI', 'CVS', 'DHI', 'DHR', 'DRI', 'DVA', 'DF', 'DE', 'DELL', 'DNR', 'XRAY', 'DVN', 'DV', 'DO', 'DTV', 'DFS', 'DISCA', 'D', 'RRD', 'DOV', 'DOW', 'DPS', 'DTE', 'DD', 'DUK', 'DNB', 'ETFC', 'EMN', 'ETN', 'EBAY', 'ECL', 'EIX', 'EP', 'ERTS', 'EMC', 'EMR', 'ETR', 'EOG', 'EQT', 'EFX', 'EQR', 'EL', 'EXC', 'EXPE', 'EXPD', 'XOM', 'FFIV', 'FDO', 'FAST', 'FII', 'FDX', 'FIS', 'FITB', 'FHN', 'FSLR', 'FE', 'FISV', 'FLIR', 'FLS', 'FLR', 'FMC', 'FTI', 'F', 'FRX', 'FO', 'BEN', 'FCX', 'FTR', 'GME', 'GCI', 'GPS', 'GD', 'GE', 'GIS', 'GPC', 'GNW', 'GILD', 'GS', 'GR', 'GT', 'GOOG', 'GWW', 'HAL', 'HOG', 'HAR', 'HRS', 'HIG', 'HAS', 'HCP', 'HCN', 'HNZ', 'HP', 'HES', 'HPQ', 'HD', 'HON', 'HRL', 'HSP', 'HST', 'HCBK', 'HUM', 'HBAN', 'ITW', 'TEG', 'INTC', 'ICE', 'IBM', 'IFF', 'IGT', 'IP', 'IPG', 'INTU', 'ISRG', 'IVZ', 'IRM', 'ITT', 'JBL', 'JEC', 'JNS', 'JDSU', 'JNJ', 'JCI', 'JOYG', 'JPM', 'JNPR', 'K', 'KEY', 'KMB', 'KIM', 'KLAC', 'KSS', 'KFT', 'KR', 'LLL', 'LH', 'LM', 'LEG', 'LEN', 'LUK', 'LXK', 'LIFE', 'LLY', 'LTD', 'LNC', 'LLTC', 'LMT', 'L', 'LO', 'LOW', 'LSI', 'MTB', 'M', 'MRO', 'MAR', 'MMC', 'MAS', 'MEE', 'MA', 'MAT', 'MKC', 'MCD', 'MHP', 'MCK', 'MJN', 'MWV', 'MDT', 'WFR', 'MRK', 'MET', 'PCS', 'MCHP', 'MU', 'MSFT', 'MOLX', 'TAP', 'MON', 'MWW', 'MCO', 'MS', 'MMI', 'MSI', 'MUR', 'MYL', 'NBR', 'NDAQ', 'NOV', 'NSM', 'NTAP', 'NFLX', 'NFX', 'NEM', 'NWSA', 'NEE', 'GAS', 'NKE', 'NI', 'NE', 'NBL', 'JWN', 'NSC', 'NTRS', 'NOC', 'NU', 'NVLS', 'NRG', 'NUE', 'NVDA', 'NYX', 'ORLY', 'OXY', 'OMC', 'OKE', 'ORCL', 'OI', 'PCAR', 'IR', 'PLL', 'PH', 'PDCO', 'PAYX', 'BTU', 'JCP', 'PBCT', 'POM', 'PEP', 'PKI', 'PFE', 'PCG', 'PM', 'PNW', 'PXD', 'PBI', 'PCL', 'PNC', 'RL', 'PPG', 'PPL', 'PX', 'PCP', 'PCLN', 'PFG', 'PG', 'PGN', 'PGR', 'PLD', 'PRU', 'PEG', 'PSA', 'PHM', 'QEP', 'PWR', 'QCOM', 'DGX', 'RSH', 'RRC', 'RTN', 'RHT', 'RF', 'RSG', 'RAI', 'RHI', 'ROK', 'COL', 'ROP', 'ROST', 'RDC', 'R', 'SWY', 'SAI', 'CRM', 'SNDK', 'SCG', 'SLB', 'SNI', 'SEE', 'SHLD', 'SRE', 'SHW', 'SIAL', 'SPG', 'SLM', 'SJM', 'SNA', 'SO', 'LUV', 'SWN', 'SE', 'S', 'STJ', 'SWK', 'SPLS', 'SBUX', 'HOT', 'STT', 'SRCL', 'SYK', 'SUN', 'STI', 'SVU', 'SYMC', 'SYY', 'TROW', 'TGT', 'TE', 'TLAB', 'THC', 'TDC', 'TER', 'TSO', 'TXN', 'TXT', 'HSY', 'TRV', 'TMO', 'TIF', 'TWX', 'TWC', 'TIE', 'TJX', 'TMK', 'TSS', 'TSN', 'TYC', 'USB', 'UNP', 'UNH', 'UPS', 'X', 'UTX', 'UNM', 'URBN', 'VFC', 'VLO', 'VAR', 'VTR', 'VRSN', 'VZ', 'VIAb', 'V', 'VNO', 'VMC', 'WMT', 'WAG', 'DIS', 'WPO', 'WM', 'WAT', 'WPI', 'WLP', 'WFC', 'WDC', 'WU', 'WY', 'WHR', 'WFMI', 'WIN', 'WMB', 'WEC', 'WYN', 'WYNN', 'XEL', 'XRX', 'XLNX', 'XL', 'YHOO', 'YUM', 'ZMH', 'ZION']
Failed: ['CEPH', 'ESRX', 'GENZ', 'MI', 'MHS', 'NWL', 'NOVL', 'Q', 'SLE']
```

# View Result #
A file named fundamental.sqlite will be generated in "{project folder}/trunk/data/". You can view it by any Sqlite UI tools. Sqlite-manager on my laptop:
![http://ultra-finance.googlecode.com/files/fundamentalSqlite.png](http://ultra-finance.googlecode.com/files/fundamentalSqlite.png)