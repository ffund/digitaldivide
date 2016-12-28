import csv
import sys
import pandas as pd
import numpy as np
import math
import priceForEachHouse

csvloss = pd.read_csv('dat/curr_udplatency.csv', error_bad_lines=False)
csvjitter = pd.read_csv('dat/curr_udpjitter.csv', error_bad_lines=False)
csvmspeeddown = pd.read_csv('dat/curr_httpgetmt.csv', error_bad_lines=False)
csvmspeedup = pd.read_csv('dat/curr_httppostmt.csv', error_bad_lines=False)




jitter = (csvjitter[['unit_id','latency','jitter_up','jitter_down']])
mspeeddown = (csvmspeeddown[['unit_id','bytes_sec']])
mspeedup = (csvmspeedup[['unit_id','bytes_sec']])
loss = (csvloss[['unit_id', 'successes','failures']])

alllist = list(set(csvmspeeddown.unit_id) | set(csvmspeedup.unit_id) | set(csvjitter.unit_id) | set(csvloss.unit_id))
lossavg=[]
jitterupavg=[]
jitterdownavg=[]
speedupavg=[]
speeddownavg=[]
latencyavg=[]
for i in alllist:
	try:
		lossavg.append({'unit_id':i, 'Percent Loss':(loss[loss.unit_id == i]['failures'].sum())/float((loss[loss.unit_id == i]['successes'].sum()))*100})
	except:
		z="does it work"
	jitterupavg.append({'unit_id':i, 'jitter_up':(jitter[jitter.unit_id == i]['jitter_up'].mean())})
  jitterdownavg.append({'unit_id':i, 'jitter_down':(jitter[jitter.unit_id == i]['jitter_down'].mean())})	
  speedupavg.append({'unit_id':i, 'Speed_up':(mspeedup[mspeedup.unit_id == i]['bytes_sec'].mean())})
  speeddownavg.append({'unit_id':i, 'Speed_down':(mspeeddown[mspeeddown.unit_id == i]['bytes_sec'].mean())})
  latencyavg.append({'unit_id':i, 'Latency':(jitter[jitter.unit_id == i]['latency'].mean())})
lossfinal=pd.DataFrame(lossavg)
jitterupfinal=pd.DataFrame(jitterupavg)
jitterdownfinal=pd.DataFrame(jitterdownavg)
speedupfinal=pd.DataFrame(speedupavg)
speeddownfinal=pd.DataFrame(speeddownavg)
latencyfinal=pd.DataFrame(latencyavg)

mergetwo = pd.merge(lossfinal,jitterupfinal, on='unit_id', how="inner")
mergethree = pd.merge(mergetwo,jitterdownfinal, on='unit_id', how="inner")
mergefour = pd.merge(mergethree,speedupfinal, on='unit_id' how="inner")
mergefive = pd.merge(mergefour,speeddownfinal, on='unit_id', how="inner")

finalmerge = pd.merge(mergefive,latencyfinal, on='unit_id', how="inner")
profilemba = pd.read_csv('fixedunitprofile.csv')

new=pd.merge(finalmerge,profilemba, on='unit_id', how='inner')


pd.set_option('max_columns', 50)
allcsv = new
URS = pd.read_csv('dat/newURS.csv')

p = priceForEachHouse.householdPrice(houseID, allcsv, URS)
l = list(set(allcsv.unit_id))
prices = [priceForEachHouse.householdPrice(litem, allcsv, URS) for litem in l]
sum(numpy.logical_not(numpy.isnan(prices)))

addprice=[]
x=0
for i in l:
	addprice.append({'unit_id':i, 'price':prices[x]})
	x+=1
pricefinal=pd.DataFrame(addprice)
new=pd.merge(allcsv,pricefinal, on='unit_id', how='inner')
new.to_csv('dat/full.csv')
print 'merged'



