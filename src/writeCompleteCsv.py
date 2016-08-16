import sys
import pandas as pd
import numpy as np
import price
import numpy 

import math

pd.set_option('max_columns', 50)

allcsv = pd.read_csv('workingcompact.csv')
URS = pd.read_csv('newURS.csv')

houseID = 405

p = price.householdPrice(houseID, allcsv, URS)

l = list(set(allcsv.unit_id))
prices = [price.householdPrice(litem, allcsv, URS) for litem in l]
sum(numpy.logical_not(numpy.isnan(prices)))

allcsv['price'] = pd.Series(prices, index=allcsv.index)