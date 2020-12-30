import pandas as pd
import numpy as np
import statsmodels.api as sm

# Test name
test_name = "hmetf"



# Read data.
fname = '../../data/backtest_results/' + test_name + '.csv'
R = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

fname = '../../data/processed_data/returns_master.csv'
DATA = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

print(DATA)
sp = DATA.loc[R.index, ['SP500']]

# Fama-French 3 factors.
ff3 = DATA.loc[R.index, ['Mkt-RF', 'SMB', 'HML']]
rf  = DATA.loc[R.index, ['T-bill']]

Y = R['Ret'] - rf['T-bill']
#Y = sp['SP500'] - rf['T-bill']
X = sm.add_constant(ff3)



model = sm.OLS(Y, X, missing = 'drop')
res = model.fit()
print(res.summary(yname = 'Exc Ret', xname = ['alpha', 'Mkt-RF', 'SMB', 'HML']))
