import pandas as pd
import numpy as np


def transaction_costs(Q_prev, Q, tc):

    all_pos = set(list(Q_prev.keys()) + list(Q.keys()))
    sum = 0.
    for p in all_pos:
        if p in Q_prev.keys() and p in Q.keys():
            sum += np.abs(Q[p] - Q_prev[p])
        elif p in Q_prev.keys():
            sum += np.abs(Q_prev[p])
        else:
            sum += np.abs(Q[p])
    return tc*sum



def compute_returns(Q, t, DATA):
    sum = 0.
    for p in Q.keys():
        try:
            r = DATA.loc[t, str(p)]
            if np.isnan(r):
                r = 0
        except:
            r = 0
        sum += Q[p]*r
    return sum
