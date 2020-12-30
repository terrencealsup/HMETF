import pandas as pd
import pickle
from datetime import datetime


sp = pd.read_csv('../../data/raw_data/sp500_constituents.csv')
ms = pd.read_csv('../../data/processed_data/returns_master.csv')


def checkSP500(d, e, flagEnd = False):
    periods = sp[sp['permno'] == e]
    if not flagEnd:
        for i in periods.index:
            if ((periods.loc[i, 'start'] <= d) & (periods.loc[i, 'ending'] > d)):
                return True
    else:
        for i in periods.index:
            if ((periods.loc[i, 'start'] <= d) & (periods.loc[i, 'ending'] >= d)):
                return True
    return False


dates = list(ms['date'])
all_constituents = list(sp['permno'].unique())
#print(sp['permno'].value_counts())
#print(sp[sp['permno'] == 10233])

flag = False
constituents = {}
for d in dates:
    if d == dates[-1]:
        flag = True
    conlist = []
    for e in all_constituents:
        if checkSP500(int(d.replace('-','')), e, flag):
            conlist.append(e)
    dt = pd.Timestamp(datetime.strptime(d, '%Y-%m-%d'))
    constituents[dt] = conlist
    print(dt)

with open('../../data/processed_data/sp500_historical_constituents.p', 'wb') as fp:
    pickle.dump(constituents, fp)
print("Done")
