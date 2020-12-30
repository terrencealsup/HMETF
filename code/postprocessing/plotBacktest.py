import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from matplotlib.dates import date2num

# Test name
test_name = "hmetf"
fname = '../../data/backtest_results/' + test_name + '.csv'


# Read data.
Rpf = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

#Rpf = Rpf.truncate(before = datetime(2012, 5, 31)) - 5/10000

fname = '../../data/processed_data/returns_master.csv'
DATA = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

# Merge the portfolio returns with the S&P 500 and T-bill returns.
R = pd.merge(Rpf, DATA['SP500'], how = 'left', on = 'date')
R = pd.merge(R, DATA['T-bill'], how = 'left', on = 'date')

rp = R['Ret']
rf = R['T-bill']
sp = R['SP500']

print(R)

# Compute annualized Sharpe ratios.
sharpe = np.sqrt(12)*(rp.mean() - rf.mean())/(rp - rf).std()
sharpe1 = np.sqrt(12)*(sp.mean() - rf.mean())/(sp - rf).std()
print("Strategy Sharpe Ratio = {:0.3f}".format(sharpe))
print("S&P 500  Sharpe Ratio = {:0.3f}".format(sharpe1))


# Compute Sortino ratio.
r1 = R['Ret'].values
r2 = R['SP500'].values
r3 = R['T-bill'].values
temp1 = r1 - r3
sortino1 = np.sqrt(12)*np.mean(temp1)/np.std(temp1*( temp1 < 0 ))
print("Strategy Sortino Ratio = {:0.3f}".format(sortino1))
temp2 = r2 - r3
sortino2 = np.sqrt(12)*np.mean(temp2)/np.std(temp2*( temp2 < 0 ))
print("S&P 500  Sortino Ratio = {:0.3f}".format(sortino2))


print(np.mean(r1)*100)
print(np.std(r1)*100)
"""
print(np.mean(r2))
print(np.std(r2))
print(np.mean(r3))
print(np.std(r3))
"""

# Compute max drawdown.
m1=np.cumprod(r1+1)
mdd1 = np.ptp(m1)/np.max(m1)
print("Strategy Max drawdown = {:0.3f}".format(mdd1))
m2=np.cumprod(r2+1)
mdd2 = np.ptp(m2)/np.max(m2)
print("S&P 500  Max drawdown = {:0.3f}".format(mdd2))



R['Equity'] = (rp + 1).cumprod()
R['SPRET'] = (sp + 1).cumprod()
R['RFCUM'] = (rf + 1).cumprod()



# Plot data.

fig, ax = plt.subplots(1,1)
ax.plot(R['Equity'], lw = 3, c = 'b', label = 'Long-only')
ax.plot(R['SPRET'], lw = 3, c = 'r', label = 'S&P 500')
ax.plot(R['RFCUM'], lw = 3, c = 'g', label = 'Risk Free')

# Uncomment to plot recessions.
"""
ax.axvspan(date2num(datetime(1973,11,1)), date2num(datetime(1975,3,30)),
           color="gray", alpha=0.3)

ax.axvspan(date2num(datetime(1980,1,1)), date2num(datetime(1980,7,30)),
           color="gray", alpha=0.3)

ax.axvspan(date2num(datetime(1981,7,1)), date2num(datetime(1982,11,30)),
           color="gray", alpha=0.3)

ax.axvspan(date2num(datetime(1990,7,1)), date2num(datetime(1991,3,30)),
           color="gray", alpha=0.3)

ax.axvspan(date2num(datetime(2001,3,1)), date2num(datetime(2001,11,30)),
           color="gray", alpha=0.3)

ax.axvspan(date2num(datetime(2007,1,12)), date2num(datetime(2009,6,1)),
           label="Recessions",color="gray", alpha=0.3)
"""

#ax.set_yscale('log')
ax.set_ylabel('Equity ($USD)')
ax.set_xlabel('Date')
ax.set_title('Equity Curve for Momentum Strategy')
plt.legend()
plt.grid()
plt.show()
