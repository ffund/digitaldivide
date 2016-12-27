import sys
import pandas as pd
import numpy as np
import priceForEachHouse
import numpy 
import math

pd.set_option('max_columns', 50)

allcsv = pd.read_csv('dat/household.csv')
URS = pd.read_csv('dat/newURS.csv')

houseID = 405

p = priceForEachHouse.householdPrice(houseID, allcsv, URS)

l = list(set(allcsv.unit_id))
prices = [priceForEachHouse.householdPrice(litem, allcsv, URS) for litem in l]
sum(numpy.logical_not(numpy.isnan(prices)))

addprice=[]
x=0
for i in l:
	addprice.append({'unit_id':i, 'price':prices[x]})
	x+=1
#allcsv['price'] = pd.Series(prices, index=allcsv.index)
pricefinal=pd.DataFrame(addprice)
new=pd.merge(allcsv,pricefinal, on='unit_id', how='inner')
new.to_csv('dat/full.csv')
print 'merged'

