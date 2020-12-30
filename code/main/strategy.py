"""
The different trading strategies to consider.
"""
import pandas as pd
import numpy as np
import utilities
import statsmodels.api as sm


def momentum(t, univ, DATA, atd, mom):
    """
    ----------------------------------------------------------------------------
    Input

    ----------------------------------------------------------------------------
    Output

    ----------------------------------------------------------------------------
    """

    # Get the returns of each equity in the universe for the past T periods.
    T = 7
    tid = atd.get_loc(t)
    lb = atd[tid - T]
    rT = DATA.loc[lb:t]
    rT = rT.dropna(axis = 1)
    # Get the equities for the universe at time t.
    eqty = [str(x) for x in univ]
    rT = rT.reindex(columns = eqty)
    # Drop current and previous month.
    rT = rT.iloc[:-2,:]
    # Compute the cumulative returns over the period.
    crT = (1 + rT).prod() - 1
    # Sort the equities based on their cumulative returns.
    crT.sort_values(inplace = True, ascending = False)
    # Go long on the top N stocks and give them equal weights.
    N = 5
    """
    long = (crT.index.values[:N]).astype(str)
    Q = {}
    for p in long:
        Q[str(p)] = 1/N
    """
    long = (crT.index.values[:N]).astype(str)
    Q = {}
    for p in long:
        Q[str(p)] = 1/N
    """
    short = (crT.index.values[-N:]).astype(str)
    for p in short:
        Q[str(p)] = -1/(2*N)
    """
    return Q



def HMETF(t, univ, DATA, atd, mom):
    """
    ----------------------------------------------------------------------------
    Input

    ----------------------------------------------------------------------------
    Output

    ----------------------------------------------------------------------------
    """
    # Get the positions from the momentum strategy.
    Q = momentum(t, univ, DATA, atd, mom)
    # Get the momentum returns for the past 5 years (60 months)
    T = 60
    tidx = atd.get_loc(t)
    lb = atd[tidx - T]
    Rm = mom.loc[lb:t, 'Ret']
    rf = DATA.loc[lb:t, 'T-bill']
    # Get the ETF returns for the past 5 years.
    etf = DATA.loc[lb:t, ['SPY', 'IWM', 'QQQ']]
    # Regression of momentum returns on ETF returns.
    etf = sm.add_constant(etf)
    model = sm.OLS(Rm-rf, etf, missing = 'drop')
    res = model.fit()
    beta = res.params[1:]
    # Reweight using the regression coefficients.
    bsum = np.sum(beta)
    Q['SPY'] = -beta[0]/(1 + bsum)
    Q['IWM'] = -beta[1]/(1 + bsum)
    Q['QQQ'] = -beta[2]/(1 + bsum)
    for p in Q.keys():
        Q[p] /= (1 + bsum)
    return Q


def HMFF3(t, univ, DATA, atd, mom):
    """
    ----------------------------------------------------------------------------
    Input

    ----------------------------------------------------------------------------
    Output

    ----------------------------------------------------------------------------
    """
    # Get the positions from the momentum strategy.
    Q = momentum(t, univ, DATA, atd, mom)
    # Get the momentum returns for the past 5 years (60 months)
    T = 60
    tidx = atd.get_loc(t)
    lb = atd[tidx - T]
    Rm = mom.loc[lb:t, 'Ret']
    rf = DATA.loc[lb:t, 'T-bill']
    # Get the ETF returns for the past 5 years.
    ff3 = DATA.loc[lb:t, ['Mkt-RF', 'SMB', 'HML']]
    # Regression of momentum returns on ETF returns.
    ff3 = sm.add_constant(ff3)
    model = sm.OLS(Rm-rf, ff3, missing = 'drop')
    res = model.fit()
    beta = res.params[1:]
    # Reweight using the regression coefficients.
    bsum = np.sum(beta)
    Q['Mkt-Rf'] = -beta[0]/(1 + bsum)
    Q['SMB'] = -beta[1]/(1 + bsum)
    Q['HML'] = -beta[2]/(1 + bsum)
    for p in Q.keys():
        Q[p] /= (1 + bsum)
    return Q
