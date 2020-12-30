import numpy as np
import pandas as pd
from datetime import datetime
import pickle
import strategy
import utilities


def backtest(start, end, DATA, univ, tc, fname):
    """
    start: datetime.date, the starting month for the backtest
    end  : datetime.date, the ending month for the backtest
    DATA : pandas.DataFrame, the collection of returns for each month
    univ : dict, dictionary of list of equities to consider at each month
    tc   : float, transation cost rate in basis points
    fname: str, the name of the file for the results
    """
    atd = DATA.index.values
    print(atd)
    print(type(atd))



# All trading days from the data.
fname = '../../data/processed_data/returns_master.csv'
DATA = pd.read_csv(fname, parse_dates = ['date'], index_col = 'date')

backtest(0, 0, DATA, 0, 0, 0)
