![Logo](https://cloud.githubusercontent.com/assets/568181/11385720/44413bac-92fa-11e5-87e7-0ec09f5eff1d.jpg)

[![Build Status](https://travis-ci.org/llazzaro/analyzer.svg?branch=master)](https://travis-ci.org/llazzaro/analyzer)
[![Coverage Status](https://coveralls.io/repos/llazzaro/analyzer/badge.svg)](https://coveralls.io/r/llazzaro/analyzer)
[![Code Health](https://landscape.io/github/llazzaro/analyzer/master/landscape.svg?style=flat)](https://landscape.io/github/llazzaro/analyzer/master)

[![Join the chat at https://gitter.im/llazzaro/analyzer](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/llazzaro/analyzer?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Donate bitcoins to this project.

        BTC: 1GeVxWa5jzLNwr4GfyNYEYgdrLc1r7tv76

Python project for real-time financial analyzing and backtesting trading strategies

#How to install

```
pip install analyzer
```

# How to use it

After project installation the following executable will be available:

* feeder
* trading_center
* trading_engine
* alarms
* backtester

*feeder* will retrieve quotes or ticks from the configured DAM in the .ini file

*trading_center* will process each quote or tick and execute the strategies selected on the .ini

*trading_center* will execute order to the exchanger (example to cex.io)

*alarms* if an action was triggered, this activate the alarms. Currently only EmailAlarm is implemented

*backtester* uses .ini to back test strategies with tick or quote information

## Example of realtime configuration
```
tmuxp load realtime_session.yml
```

#Architecture

![Architecture](https://cloud.githubusercontent.com/assets/568181/10708823/4d2d9174-79ec-11e5-8390-1f8533faed53.png)


Originally DAM and model were in the ultrafinance project, but I wanted to have DAM more as plugin.
Since I already have a stock market relational model I wanted to adapt it for this project.
Moving DAM and model to a new project will maintain a minimalistic analyzer code.

Check these projects:

 * Data Access https://github.com/llazzaro/analyzerdam 
 * Model https://github.com/llazzaro/pystock
 * Strategies https://github.com/llazzaro/analyzerstrategies

important: this project is a fork of the original https://github.com/panpanpandas/ultrafinance
