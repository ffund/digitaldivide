import csv
import sys
import pandas as pd
import numpy as np


csvloss = pd.read_csv('dat/curr_udplatency.csv', error_bad_lines=False)
csvjitter = pd.read_csv('dat/curr_udpjitter.csv', error_bad_lines=False)
csvmspeeddown = pd.read_csv('dat/curr_httpgetmt.csv', error_bad_lines=False)
csvmspeedup = pd.read_csv('dat/curr_httppostmt.csv', error_bad_lines=False)




jitter = (csvjitter[['unit_id','latency','jitter_up','jitter_down']])
mspeeddown = (csvmspeeddown[['unit_id','bytes_sec']])
mspeedup = (csvmspeedup[['unit_id','bytes_sec']])
loss = (csvloss[['unit_id', 'successes','failures']])

alllist = list(set(csvmspeeddown.unit_id) | set(csvmspeedup.unit_id) | set(csvjitter.unit_id) | set(csvloss.unit_id))
#combined = pd.concat([loss, jitter, mspeeddown, mspeedup], axis=1)
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

#finalmerge = pd.merge(lossfinal,jitterupfinal,jitterdownfinal,speedupfinal,speeddownfinal,latencyfinal, on="unit_id", how="outer")
#print finalmerge


mergetwo = pd.merge(lossfinal,jitterupfinal, on="unit_id", how="outer")
mergethree = pd.merge(mergetwo,jitterdownfinal, on="unit_id", how="outer")
mergefour = pd.merge(mergethree,speedupfinal, on="unit_id", how="outer")
mergefive = pd.merge(mergefour,speeddownfinal, on="unit_id", how="outer")
finalmerge = pd.merge(mergefive,latencyfinal, on="unit_id", how="outer")
finalmerge.to_csv("compactInfo.csv")
print "added to csv"
