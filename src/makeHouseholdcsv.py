
import sys
import pandas as pd
import numpy as np
import math

pd.set_option('max_columns', 50)

allcsv = pd.read_csv('compactInfo.csv')
#URS = pd.read_csv('newURS.csv')
profilemba = pd.read_csv('fixedunitprofile.csv')

new=pd.merge(allcsv,profilemba, on='unit_id', how='inner')
new.to_csv('workingcompact.csv')
print 'merged'
