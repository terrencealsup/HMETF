import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num
import statsmodels.api as sm

# Start and end times in YYYYMMDD.
start = datetime(1970, 1, 1)
end = datetime(2011, 12, 31)

# Test name
test_name = "longonly"
fname = '../../data/backtest_results/' + test_name + '.csv'


# Read data of the backtest.
Rpf = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')


# Load in the master data set of returns.
fname = '../../data/processed_data/returns_master.csv'
DATA = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')
atd = DATA.index # All trading dates.
btd = atd[(atd >= start) & (atd <= end)]



f3betas = pd.DataFrame(index = Rpf.index.copy())
f3betas['Mkt-Rf'] = 0.
f3betas['SMB'] = 0.
f3betas['HML'] = 0.

T = 12
i = 0
for t in btd:
    tidx = atd.get_loc(t)
    if i >= T:
        lb = atd[tidx - T]
        tm1 = atd[tidx - 1]

        Rm = Rpf.loc[lb:t, 'Ret']
        rf = DATA.loc[lb:t, 'T-bill']

        ff3 = DATA.loc[lb:t, ['Mkt-RF', 'SMB', 'HML']]
        # Regression of momentum returns on ETF returns.
        ff3 = sm.add_constant(ff3)
        model = sm.OLS(Rm-rf, ff3, missing = 'drop')
        res = model.fit()


        f3betas.loc[t, 'Mkt-Rf'] = res.params[1]
        f3betas.loc[t, 'SMB'] = res.params[2]
        f3betas.loc[t, 'HML'] = res.params[3]
    i += 1
f3betas['Mkt-Rf'].plot(label = 'Mkt-Rf')

f3betas['SMB'].plot(label = 'SMB')

f3betas['HML'].plot(label = 'HML')
plt.xlabel('Date')
plt.ylabel('Factor loading')
plt.title('Momentum time-varying exposures')
plt.legend()
plt.grid()
plt.show()
