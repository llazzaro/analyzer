#it's so painful to work with quantlib SWIG python under windows

# Introduction #

I spent a whole night to figure out how to build the shit.


# Details #
  * My enviroment: WINDOWS 7 + VS2010 + PYTHON2.6(check http://quantlib.org/install/vc9.shtml)
  * svn co https://quantlib.svn.sourceforge.net/svnroot/quantlib/branches/R01010x-branch quantlib
  * install boost
  * set boost path in vs2010
  * compile the project
  * python setup.py build --compiler=mingw32