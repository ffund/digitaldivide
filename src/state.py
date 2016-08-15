#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409


import sys
import pandas as pd
import numpy as np

statestuff = pd.read_csv("dat/unit_report.csv",error_bad_lines=False)
statestuff = statestuff.dropna()
statestuff = statestuff[statestuff.country == "US"]
states = statestuff.region.unique()
#print statestuff.head()
#create a data frame dictionary to store your data frames
DataFrameDict = {elem : pd.DataFrame for elem in states}

for key in DataFrameDict.keys():
    DataFrameDict[key] = statestuff[:][statestuff.region == key]

print DataFrameDict['Massachusetts']['speed'].mean()

speeds =  [ DataFrameDict[key]['speed'].mean() for key in DataFrameDict ]
#print speeds
#print DataFrameDict.keys()
#print DataFrameDict.keys().index("Massachusetts")
#print speeds[24]
table = [[DataFrameDict.keys()],[speeds]]
df = pd.DataFrame(table)
df = df.transpose()
cols=["state","speed"]
df.columns=cols
df.to_csv("statespeeds.csv") #comment so it doesn't do it if ran again accidentally
