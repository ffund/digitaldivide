#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409 


import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)

if len(sys.argv)>1:

	csvloss = pd.read_csv('../dat/curr_udplatency.csv', error_bad_lines=False) 
	csvjitter = pd.read_csv('../dat/curr_udpjitter.csv', error_bad_lines=False)
	csvmspeeddown = pd.read_csv('../dat/curr_httpgetmt.csv', error_bad_lines=False)
	csvmspeedup = pd.read_csv('../dat/curr_httppostmt.csv', error_bad_lines=False)	

	house=int(sys.argv[1])

	loss = (csvloss[csvloss.unit_id == house][['unit_id', 'successes','failures']])
	if loss.empty:
		print "The inputted house_ID is not in the database. Please try again"
	else:
		jitter = (csvjitter[csvjitter.unit_id == house][['latency','jitter_up','jitter_down']])
		mspeeddown = (csvmspeeddown[csvmspeeddown.unit_id == house]['bytes_sec'])
		mspeedup = (csvmspeedup[csvmspeedup.unit_id == house]['bytes_sec'])
		
		totalsuccess = loss.successes.sum()
		totalfailure = loss.failures.sum()
		percentloss = (totalfailure/float(totalsuccess)) * 100.0

		
		#combined = pd.concat([loss, jitter, mspeeddown, mspeedup], axis=1)

		#print combined

		#print "percent loss:"
		#print percentloss
		
		latency = (jitter.latency.mean())/1000.0

		#print "latency:"
		#print latency
		
		jitterup = (jitter.jitter_up.mean())/1000.0
		jitterdown = (jitter.jitter_down.mean())/1000.0

		#print "jitteravg:"
		#print jitteravg

		speed = max(mspeeddown.mean(),mspeedup.mean())
		downspeed = int(round(mspeeddown.mean() * 0.008))
		upspeed = int(round(mspeedup.mean() * 0.008))

		#print "speed:"
		#print speed
		print "for user:"
		print "sudo tc qdisc add dev eth0 root handle 1:0 netem delay " + str(latency)+"ms "+ str(jitterup) + "ms loss "+str(percentloss)+"%"
		print "sudo qdisc add dev eth0 parent 1:1 handle 10: tbf rate "+str(upspeed)+"kbit"		
		print "for server:"
		print "sudo tc qdisc add dev eth0 root netem delay " + str(latency)+"ms "+ str(jitterdown) + "ms loss "+str(percentloss)+"%"
		print "sudo tc qdisc add dev eth0 parent 1:1 handle 10: tbf rate "+str(downspeed)+"kbit"

else:
	print "Please input a house_ID"


#I plan on passing the second argument (which will be the hous ID to sort the data
#The information taken from the filtered dataset will then be inputted 
#into a geni-lib function which will create the three node
#connection with the characteristics of the specified houshold

import geni.rspec.pg as PG
import geni.rspec.egext as EGX
import geni.rspec.igext as IGX


if loss.empty:
	print "The inputted house_ID is not in the database. Please try again"
else:
	r = PG.Request()

	links = []

	for i in range(1):
		links.insert(i, PG.LAN('lan%d' % i))
    # Link bandwidth depends on which tier it's in
		newspeed = int(round(speed * 0.0078125))
		links[i].bandwidth = newspeed

# The ith entry in the list, is a list of
# all the links that the ith VM is connected to
	con = [[0],[0]]

	ifaceCounter = 0
	vms = []
	for i in range(2):
        #will name it Tier1-0, Tier1-1, etc
		igvm = IGX.XenVM("Tier1-%d" % i)
		vms.insert(i, igvm)
    # Generate interfaces and connections for this VM
		for j in range(len(con[i])):
        		linkno = con[i][j]
        		iface = igvm.addInterface("if%d" % ifaceCounter)
        		ifaceCounter += 1
        		iface.addAddress(PG.IPv4Address("10.1.%d.%d" % (linkno, i+1), "255.255.255.0"))
        		links[linkno].addInterface(iface)
		r.addResource(igvm)

	for i in range(len(links)):
		r.addResource(links[i])

	r.writeXML("miniexperiment.xml")
	print "Rspec written to file"




