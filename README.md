# HMETF
Hedged Momentum Strategy using ETFs.

Paper: Martin Martens and Arco van Oord, [Hedging the time-varying risk exposures of momentum returns](https://www.sciencedirect.com/science/article/abs/pii/S0927539814000590), Journal of Empirical Finance, Volume 28, pages 78-89, September 2014

## Data sources:

1. CRSP equity data of all U.S. common stocks (share code = 10, 11) on the NYSE, NYSE MKT, NASDAQ, and Arca exchanges.  The data is monthly (end of month) from January 1950 to December 2019.

2. Fama-French 3 factor model factors data from obtained from Kenneth French's website
[http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html](http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
The Fama-French 3 factor model data is monthly from July 1926 to October 2020.

3. 1-month Treasury bill rates obtained from CRSP.  The data is monthly (end of
  month) from January 1952 to December 2019.

4. S&P500 returns from CRSP.  The data is monthly (end of month) from January 1960
to December 2019.

5. S&P500 constituents from CRSP.  The data is a list of companies (identified by
  their CRSP PERMNO) with corresponding start and end dates of when they entered and
  exited the S&P500 list.

6. Returns for the SPY, IWM, and QQQ ETFs obtained from CRSP (ETFs have a share code of 73 in WRDS).  The data is monthly from January 1950 to December 2019.
