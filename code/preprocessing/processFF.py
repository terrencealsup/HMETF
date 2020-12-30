"""
Take the raw data from Kenneth French's website and process it to files called:
1. ff3.csv for the monthly Fama-French 3 factors.
2. ff5.csv for the monthly Fama-French 5 factors.

From the original file:
" This file was created by CMPT_ME_BEME_RETS using the 202010 CRSP database.
The 1-month TBill return is from Ibbotson and Associates, Inc. "
"""
import pandas as pd

# Read in the raw Fama French factor data and save it as new csv files.
ff3 = pd.read_csv('../F-F_Research_Data_Factors.CSV', skiprows = 3)
ff5 = pd.read_csv('../F-F_Research_Data_5_Factors_2x3.CSV', skiprows = 3)

# Rename the first column to be the data (does not include the day).
ff3.rename(columns = {'Unnamed: 0':'date'}, inplace = True)
ff5.rename(columns = {'Unnamed: 0':'date'}, inplace = True)

ff3.to_csv('../ff3.csv', index = False)
ff5.to_csv('../ff5.csv', index = False)

print("Done")
