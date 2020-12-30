import pandas as pd
import pickle
from datetime import datetime

# Merge the equity, t-bill, sp500, ETF and fama-french data into one master
# dataframe.

# Need to handle these dates separately.
eq = pd.read_csv('../../data/raw_data/raw_equity.csv')
ff3 = pd.read_csv('../../data/raw_data/ff3.csv')

tbill = pd.read_csv('../../data/raw_data/tbill.csv', parse_dates = ['caldt'])
sp = pd.read_csv('../../data/raw_data/sp500.csv', parse_dates = ['DATE'])
etf = pd.read_csv('../../data/raw_data/etf.csv', parse_dates = ['date'])



# Check if a variable is a number.
def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False


# Merge T-bill with S&P 500 return data.
tbill.drop(columns = ['t30ind'], inplace = True)
sp.drop(columns = ['spindx'], inplace = True)
tbill.columns = ['date', 'T-bill']
sp.columns = ['date', 'SP500']
master1 = pd.merge(tbill, sp, how = 'inner', on = 'date')

# Process the ETF data.
etf.drop(columns = ['SHRCD', 'TICKER', 'COMNAM'], inplace = True)
# Convert the columns to floats.
a = etf['RET'].apply(isnumber)
b = etf['RET'][a].apply(float)
etf['RET'] = b
etf = etf.pivot(index = 'date', columns = 'PERMNO', values = 'RET')

master2 = pd.merge(master1, etf, how = 'left', on = 'date')
# Rename the ETF columns to their tickers for readability.
master2.columns = ['date', 'T-bill', 'SP500', 'SPY', 'IWM', 'QQQ']


# Adjust Fama-French data from percentages to decimals and drop the risk free
# rate column since it is just the T-bill rate.
ff3.drop(columns = ['RF'], inplace = True)
ff3col = ['date', 'Mkt-RF', 'SMB', 'HML']
ff3.columns = ff3col
# Change from percentages to decimals.
ff3[ff3col[1:]] /= 100.
# Cut off the last 10 rows since the equity data is not available past 2019.
ff3 = ff3[ff3['date'] < 202001]
# Convert FF dates to include month-end day.
# The equity data set has dates going back before 196307 so use that for
# reference.
def convert_date(d, ref_dates):
    for d1 in ref_dates:
        if d1//100 == d:
            return d1
ref_dates = eq['date'].unique()
ref_dates.sort()
ff3['date'] = ff3['date'].apply(lambda d: convert_date(d, ref_dates))
ff3.dropna(inplace = True)
ff3['date'] = ff3['date'].astype(int).astype(str)
ff3['date'] = pd.to_datetime(ff3['date'], format = '%Y-%m-%d')

master3 = pd.merge(master2, ff3, how = 'left', on = 'date')

# Merge with the equity data returns.

# Process equity data.
a = eq['RET'].apply(isnumber)
b = eq['RET'][a].apply(float)
eq['RET'] = b
eq['date'] = pd.to_datetime(eq['date'].astype(str), format = '%Y-%m-%d')
eq = eq.pivot(index = 'date', columns = 'PERMNO', values = 'RET')

# Merge with the other data.
master = pd.merge(master3, eq, how = 'inner', on = 'date')
master.to_csv('../../data/processed_data/returns_master.csv', index = False)
