#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409 


import sys
import pandas as pd
import numpy as np
pd.set_option('max_columns', 50)

if len(sys.argv)>1:

	allcsv = pd.read_csv('compactInfo.csv')	

	house=int(sys.argv[1])
	
	splitup = (allcsv[allcsv.unit_id == house][['Percent Loss','Latency','jitter_up','jitter_down','Speed_up','Speed_down']])
	#convert it so it works in python histogram etc. float is python float64 is from numpy print float(splitup['Percent Loss'])
	if splitup.empty:
		print "The inputted house_ID is not in the database. Please try again"
	else:
		percentloss = float(splitup['Percent Loss'])
		
		latency = float(splitup['Latency'])/1000.0
		
		jitterup = float(splitup['jitter_up'])/1000.0
		jitterdown = float(splitup['jitter_down'])/1000.0

		speed = max(float(splitup['Speed_up']),float(splitup['Speed_down']))
		downspeed = int(round(splitup['Speed_down'] * 0.008))
		upspeed = int(round(splitup['Speed_up'] * 0.008))
		print "for user:"
		print "sudo tc qdisc add dev eth1 root handle 1:0 netem delay " + str(latency/2)+"ms "+ str(jitterup) + "ms loss "+str(percentloss)+"%"
		print "sudo qdisc add dev eth1 parent 1:1 handle 10: tbf rate "+str(upspeed)+"kbit limit 500000000 burst 100000"		
		print "for server:"
		print "sudo tc qdisc add dev eth1 root netem delay " + str(latency/2)+"ms "+ str(jitterdown) + "ms loss "+str(percentloss)+"%"
		print "sudo tc qdisc add dev eth1 parent 1:1 handle 10: tbf rate "+str(downspeed)+"kbit limit 500000000 burst 100000"

else:
	print "Please input a house_ID"


import geni.rspec.pg as PG
import geni.rspec.egext as EGX
import geni.rspec.igext as IGX


if splitup.empty:
	print "The inputted house_ID is not in the database. Please try again"
else:
	r = PG.Request()

	links = []

	for i in range(1):
		links.insert(i, PG.LAN('lan%d' % i))
    # Link bandwidth depends on which tier it's in
		newspeed = int(round(speed * 0.008))
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

thejfile= '''{
    "content": {
        "down": {
            "corruption": {
                "correlation": 0,
                "percentage": 0
            },
            "delay": {
                "correlation": 0,
                "delay":"'''+str(latency/2)+'''",
                "jitter":"'''+str(jitterdown)+'''"
            },
            "iptables_options": [],
            "loss": {
                "correlation": 0,
                "percentage":"'''+str(percentloss)+'''"
            },
            "rate":"'''+str(downspeed)+'''",
            "reorder": {
                "correlation": 0,
                "gap": 0,
                "percentage": 0
            }
        },
        "up": {
            "corruption": {
                "correlation": 0,
                "percentage": 0
            },
            "delay": {
                "correlation": 0,
                "delay":"'''+str(latency/2)+'''",
                "jitter":"'''+str(jitterup)+'''"
            },
            "iptables_options": [],
            "loss": {
                "correlation": 0,
                "percentage":"'''+str(percentloss)+'''"
            },
            "rate":"'''+str(upspeed)+'''",
            "reorder": {
                "correlation": 0,
                "gap": 0,
                "percentage": 0
            }
        }
    },
    "id": 10,
    "name": "house'''+str(house)+'''"
}'''

print thejfile



