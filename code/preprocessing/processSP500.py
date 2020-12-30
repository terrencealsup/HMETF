import pandas as pd
import numpy as np

# T
T = 7

# Sp500 constituents
sp = pd.read_csv('../sp500_constituents.csv')

# Equity data.
eq = pd.read_csv('../equity_prices.csv')
eq['PERMNO'].astype(int)
eq['date'].astype(int)
eq['RET'].astype(float)

# Process data from these periods
start = 19640101
end   = 20191231


trading_days = eq['date'].unique()
equity_list = eq['PERMNO'].unique()
backtest_days = trading_days[((trading_days >= start) & (trading_days <= end))]
tdays = trading_days.tolist()
equity_list = equity_list.tolist()
backtest_days = backtest_days.tolist()
tdays.sort()
backtest_days.sort()
eq.set_index(['date', 'PERMNO'], inplace = True)

monret = {}

# Loop over all the dates.
for i, t in enumerate(backtest_days):
    tindx = tdays.index(t)
    lookback = tdays[tindx - T]
    # Loop over all in SP500 at the time.
    elist = list(sp.loc[((sp['start'] <= lookback)
                    & (sp['ending'] > t)), 'permno'])
    eret = pd.DataFrame(elist, columns = ['PERMNO'])
    eret['RET'] = 0.
    eret['keep'] = 1
    for j, e in enumerate(elist):
        valid = True
        sum = 0.
        k = 0
        for k in range(T+1):
            b = eq.isin([(tdays[tindx - k], e)])['RET']
            if b.any():
                sum *= (1 + eq.loc[idx[t, e], 'RET'].values)
            else:
                valid = False
        if valid:
            eret.iloc[j, 1] = sum - 1
        else:
            eret.iloc[j, 2] = 0
        print(e)
    eret = eret.loc[eret['keep'] == 1]
    eret.drop(columns = ['keep'], inplace = True)

    monret[t] = eret
    print(t)

pickle.dump(monret, open('../sp500_constituent_returns.p', 'wb'))
