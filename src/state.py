#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409


import sys
import pandas as pd
import numpy as np

#statestuff = pd.read_csv("dat/unit_report.csv",error_bad_lines=False)
#profile = pd.read_excel("dat/unitprofile.xls")
#URS = pd.read_excel("dat/URS.xlsx")
#fullcsv = pd.read_csv("dat/compactInfo.csv")
#print profile.head()
#print URS.head()
#profile = profile[profile.STATE !="UNKNOWN"]
#profile = profile[profile["SK UP"] !="MISC"]
#profile = profile[profile["SK UP"] !="REMOVE"]
#profile = profile[profile["TECHNOLOGY"] != "REMOVE"]
#print type(profile[profile.unit_id==901]["SK UP"].tolist()[0])


#print profile.head()
#profile.to_csv("fixedunitprofile.csv")
#URS.to_csv("URS.csv")
#print "profile:"
#print list(set(profile["isp"]))
#print list(set(profile["TECHNOLOGY"]))
#print profile.head()
#print "URS:"
#print list(set(URS["Provider"]))
#print list(set(URS["Technology"]))
#tomerge=[]
#for i in list(moreinfo[moreinfo.unit_id]):
#        tomerge.append({'unit_id':i, 'isp':moreinfo[moreinfo.unit_id==i["maxmind_isp"]]})
#statestuff = statestuff.dropna()
#statestuff = statestuff[statestuff.country == "US"]
#states = statestuff.region.unique()
#print statestuff.head()
#create a data frame dictionary to store your data frames
#DataFrameDict = {elem : pd.DataFrame for elem in states}

#for key in DataFrameDict.keys():
#    DataFrameDict[key] = statestuff[:][statestuff.region == key]

#print DataFrameDict['Massachusetts']['speed'].mean()

#speeds =  [ DataFrameDict[key]['speed'].mean()*.0000080 for key in DataFrameDict ]
#print speeds
#print DataFrameDict.keys()
#print DataFrameDict.keys().index("Massachusetts")
#print speeds[24]
#table = [DataFrameDict.keys(),speeds]
#df = pd.DataFrame(table)
#df = df.transpose()
#cols=["state","speed"]
#df.columns=cols
#df.to_csv("statespeeds.csv") #comment so it doesn't do it if ran again accidentally
