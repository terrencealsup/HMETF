import pandas as pd
import matplotlib.pyplot as plt

eq = pd.read_csv('../../data/raw_data/raw_equity.csv')

# Returns in column 'RET' could have a value of B or C.
# B corresponds to being off the exchange for that period.
# C corresponds to no valid previous price available.
# Set both of these to NaN


# Check if a variable is a number.
def isnumber(x):
    try:
        float(x)
        return True
    except:
        return False

# Filter
a = eq['RET'].apply(isnumber)
b = eq['RET'][a].apply(float)
eq['RET'] = b

# Add in adjusted price as well.
eq['ADJPRC'] = eq['PRC']/eq['CFACPR']

eq.to_csv('../../data/processed_data/equity.csv', index = False)

print("Done")
