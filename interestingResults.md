#some interesting results by UltraFinance

# Introduction #

Something interesting is found during using ultraFinance.


# Hoursing VS Stock #
Modules: excelLib.py, plotDateValueDict.py

Compare housing market and stock market for U.S. for last 100 years, return rate for housing is only 100%, while stock is more than 100,00%
https://4823890030545858663-a-1802744773732722657-s-sites.googlegroups.com/site/diyfiner/housing_interest_stock.png?attachauth=ANoY7crtC7pAbmtzsyDGLukXzsOavzNPUgVp9TOSlbPRnVKvvcOhscA8QVo6zCaN_H9vsLnu_9UH8VPKeyqVYfjtklg1_nDs8itBlEkIUCVQHHtPaQHPba6Ugj-dvBq2zyQZRkuHr9jkYGWdtoYqKgKGBNVObR-_-KBW6_EZlUvDOtewluUs24s5OkEoicYYwYtPixGh7UZbsW5-jxS70T59v6KCZ8aSxA%3D%3D&attredirects=0

# Which is the best result of weekly trading #
Modules: historicalDataStorage.py, excelLib.py, stockMeasument.py

For SPY500 since 1993 with $1000, if you buy on Wed and sell on next Tue., you will win $76; If you buy on Thu. and sell on the next day, you will lose $58
| Buy/Sell| Mon.   | Tue.    | Wed.   | Thu.   | Fri.   |
|:--------|:-------|:--------|:-------|:-------|:-------|
| Mon.    | 33.5   | 19.0    | 30.5   | 41.8   | 0.29   |
| Tue.    | 53.2   | 26.1    | 16.0   | 15.6   | -30.1  |
| Wed.    | 31.3   | 76.5    | 64.7   | 14.7   | -4.8   |
| Thu.    |  7.7   | 28.7    | 67.6   | 23.2   | -58.6  |
| Fri.    | -1.43  | -3.9    | 29.1   | 34.0   | 5.4    |

# Is automatic investment plan good enough #
Modules: historicalDataStorage.py, excelLib.py, stockMeasument.py, tradingStrategyFactory.py

For SPY500 from year 1900 - 2010,
  * if you continue buying $1000 at the end of each year, the total return rate will be 74.63.
  * if you continue buying $1000 at the end of each year plus an addition $1000 if SPY is the lowest during last 3 years, the total return rate will be 98.30
  * if you continue buying $1000 at the end of each year plus an addition $1000 if SPY is the lowest during last 5 years, the total return rate will be 92.01
  * if you continue buying $5000 for each 5 years the the price is the lowest for last 5 years, or at the the of 5 years period, the total return rate will be 78.58, which is not that good.

# Are Chinese companies good? #
Modules: historicalDataStorage.py, excelLib.py, stockMeasument.py

By analyzing 524 Chinese companies in U.S., British, Hong Kong and Singapore，Chinese companies are doing very well.
| days after list       | 3   | 30   | 90   | 250   | 500   | 750   |
|:----------------------|:----|:-----|:-----|:------|:------|:------|
| return(%)             | 2.2 | 0.8  | 28   | 49    | 57    | 79    |
| outperform to index(%)| 2.3 | 0.2  | 27   | 45    | 51    | 68    |
| alpha                 | -14 | 0.13 | 0.35 | 0.37  | 0.36  | 0.34  |

# Buy Google for high EPS? #
Module: stockPicker.py, googleFinance.py

Top 10 sorted by Diluted Normalized EPS Increasing
|GOOG|18.95|
|:---|:----|
|DO|8.01|
|BRKb|6223.14|
|MA|10.96|
|IBM|9.54|
|CVX|8.84|
|AZO|11.32|
|LO|9.33|
|CME|14.27|
|LMT|7.49|