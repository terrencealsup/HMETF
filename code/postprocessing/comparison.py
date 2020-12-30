import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num

# Test name
test_name = "longonly"
fname = '../../data/backtest_results/' + test_name + '.csv'


# Read data.
Rpf = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')
Rpf.columns = ['Eqty1']
#Rpf = Rpf.truncate(before = datetime(2012, 5, 31)) - 5/10000

fname = '../../data/processed_data/returns_master.csv'
DATA = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

# Merge the portfolio returns with the S&P 500 and T-bill returns.
R = pd.merge(Rpf, DATA['SP500'], how = 'left', on = 'date')
R = pd.merge(R, DATA['T-bill'], how = 'left', on = 'date')


test_name = "hmff3"
fname = '../../data/backtest_results/' + test_name + '.csv'
# Read data.
Rpf = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')
Rpf.columns = ['Eqty2']
R = pd.merge(Rpf, R, how = 'left', on = 'date')

test_name = "hmetf"
fname = '../../data/backtest_results/' + test_name + '.csv'
# Read data.
Rpf = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')
Rpf.columns = ['Eqty3']
R = pd.merge(Rpf, R, how = 'left', on = 'date')


test_name = "long_tc50"
fname = '../../data/backtest_results/' + test_name + '.csv'
# Read data.
Rpf = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')
Rpf.columns = ['Eqty4']
R = pd.merge(Rpf, R, how = 'left', on = 'date')


rp1 = R['Eqty1']
rp2 = R['Eqty2']
rp3 = R['Eqty3']
rp4 = R['Eqty4']
rf = R['T-bill']
sp = R['SP500']


R['Eqty1'] = (rp1 + 1).cumprod()
R['Eqty2'] = (rp2 + 1).cumprod()
R['Eqty3'] = (rp3 + 1).cumprod()
R['Eqty4'] = (rp4 + 1).cumprod()
R['SPRET'] = (sp + 1).cumprod()
R['RFCUM'] = (rf + 1).cumprod()









# Plot data.

fig, ax = plt.subplots(1,1)
ax.plot(R['Eqty1'], lw = 3, c = 'k', label = 'Long-only')
ax.plot(R['Eqty2'], lw = 3, c = 'm', label = 'HMFF3')
ax.plot(R['Eqty3'], lw = 3, c = 'c', label = 'HMETF')
#ax.plot(R['Eqty4'], lw = 3, c = 'b', label = '50bp x-cost')
ax.plot(R['SPRET'], lw = 3, c = 'r', ls = '--', label = 'S&P 500')
ax.plot(R['RFCUM'], lw = 3, c = 'g', ls = ':', label = 'Risk Free')



#ax.set_yscale('log')
ax.set_ylabel('Equity ($USD)')
ax.set_xlabel('Date')
ax.set_title('Equity Curve for Momentum Strategies')
plt.legend()
plt.grid()
plt.show()
