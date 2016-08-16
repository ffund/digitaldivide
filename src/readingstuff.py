import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#pd.set_option('max_columns', 50)

csvfile = pd.read_csv('newURS.csv', error_bad_lines=False) 
#print len(csvfile.unit_id)-csvfile.count(0)
#df = pd.read_csv("compactInfo.csv")
#df.dropna(axis=0)
#df.to_csv('nonan.csv')
print csvfile.head()
#print len(csvfile.unit_id)
#uniquedown=list(csvfile.unit_id)
#print len(uniquedown)
#print max(list(csvfile.upload_speed))*.0000080
#downs=[]
#for i in uniquedown:
#        splitup=csvfile[csvfile.unit_id == i]["speed"].tolist()[0]
#	downs.append(splitup)
#print max(downs)
#print max(downs)*.0000080
