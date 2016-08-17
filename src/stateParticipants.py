import pandas as pd
import numpy as np


statestuff = pd.read_csv("dat/unit_report.csv",error_bad_lines=False)

statestuff = statestuff.dropna()
statestuff = statestuff[statestuff.country == "US"]
states = statestuff.region.unique()

DataFrameDict = {elem : pd.DataFrame for elem in states}

for key in DataFrameDict.keys():
    DataFrameDict[key] = statestuff[:][statestuff.region == key]


counts =  [ DataFrameDict[key]['region'].count() for key in DataFrameDict ]
#print DataFrameDict.keys()
#print counts
table = [DataFrameDict.keys(),counts]
df = pd.DataFrame(table)
df = df.transpose()
cols=["state","number of households tested"]
df.columns=cols
df.to_csv("statenumbers.csv") #comment so it doesn't do it if ran again accidentally
