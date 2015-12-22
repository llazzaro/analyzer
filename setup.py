'''
Created on July 1, 2011

@author: ppa
'''
from setuptools import setup

from analyzer import __version__ as ANALYZER_VERSION

setup(name='analyzer',
      version=ANALYZER_VERSION,
      description="python project for finance: realtime data collection, analyze, algorithmic trading",
      long_description="""""",
      classifiers=[
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
      ],
      keywords='python, Finance, Algorithm, Trading, Realtime, QuantLib, pydispather',
      author='Leonardo Lazzaro',
      author_email='llazzaro@dc.uba.ar',
      url='https://github.com/llazzaro/analyzer',
      license='MIT',

      install_not_requires=[
          'hbase-thrift>=0.20.4',
          'redis',
          'pandas',
          'xlwt',
          'xlrd',
          'matplotlib>=1.1.0',
      ],
      packages=['analyzer'],
      include_package_data=True,
      install_requires=[
          'Quandl',
          'requests',
          'arctic',
          'redis',
          'numpy>=1.5.1',
          'scipy>=0.13.0',
          'beautifulsoup4',
          'SQLAlchemy>=0.8',
          'pbr<1.7.0',
          'pandas',
          'pystock',
          'analyzerdam>=0.1.0',
          'analyzerstrategies>=0.1.3'
          'psycopg2',
      ],
      tests_require=[
          'numpy',
          'mox3',
          'xlrd',
          'xlwt',
          'matplotlib',
          'coveralls',
          'mockredispy',
      ],
      test_suite='tests',
      entry_points={'console_scripts': [
            'alarms = analyzer.scripts.alarms:main',
            'backtester = analyzer.scripts.backtester:main',
            'feeder = analyzer.scripts.feeder:main',
            'trading_center = analyzer.scripts.trading_center:main',
            'shell = analyzer.scripts.shell:main',
            'trading_engine = analyzer.scripts.trading_engine:main', ]})
