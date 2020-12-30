import numpy as np
import pandas as pd
from datetime import datetime
import pickle
import strategy
import utilities


def backtest(start, end, strat, DATA, univ, tc, mom, fname):
    """
    ----------------------------------------------------------------------------
    Input
    start: datetime.date, the starting month for the backtest
    end  : datetime.date, the ending month for the backtest
    strat: function, the trading strategy to determine the positions
    DATA : pandas.DataFrame, the collection of returns for each month
    univ : dict, dictionary of list of equities to consider at each month
    tc   : float, transation cost rate in basis points
    fname: str, the name of the file for the results
    args : list, additional arguments for the strategy
    ----------------------------------------------------------------------------
    Output
    R    : pandas.Series, the time series of the strategy's returns
    ----------------------------------------------------------------------------
    """
    # Convert transaction costs from basis points to decimal.
    tc /= 10000
    # Get all available trading days.
    atd = DATA.index
    # Get the backtesting days.
    btd = atd[(atd >= start) & (atd <= end)]
    # Store the returns and everything else to track here.
    R = pd.DataFrame(index = btd, columns = ['Ret'])
    # No initial positions.
    Q = {}
    # Loop over the backtesting days.
    for t in btd:
        # Compute the returns of the current position.
        R.loc[t, 'Ret'] = utilities.compute_returns(Q, t, DATA)

        # Determine the new positions and weights for the next trading period.
        Q_prev = Q.copy()
        Q = strat(t, univ[t], DATA, atd, mom)

        # Account for transaction costs.
        R.loc[t, 'Ret'] -= utilities.transaction_costs(Q_prev, Q, tc)


    # Save the results in the provided file path and return the results.
    fname = '../../data/backtest_results/' + fname + '.csv'
    R.to_csv(fname)

    return R





# All trading days from the data.
fname = '../../data/processed_data/returns_master.csv'
DATA = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

fname = '../../data/processed_data/sp500_historical_constituents.p'
with open(fname, 'rb') as fp:
    sp500 = pickle.load(fp)

fname = '../../data/backtest_results/momentum_returns.csv'
mom = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')




#start = datetime(2000, 5, 31) # Earliest is 20120531
#end = datetime(2019, 12, 31)
start = datetime(2012, 5, 31)
end = datetime(2019, 12, 31)
print(backtest(start, end, strategy.HMETF, DATA, sp500, 5, mom, 'hmetf'))
