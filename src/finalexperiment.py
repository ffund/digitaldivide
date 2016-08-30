
import random
import sys
import pandas as pd
import numpy as np
import os
import json

# Importing geni-lib
import geni.rspec.pg as PG
import geni.rspec.egext as EGX
import geni.rspec.igext as IGX

# Setting command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--state", help="Specify a state from which to draw a sample household. (two letters)")
parser.add_argument("--houseid", help="Specify a household ID from the Measuring Broadband America data set.")
parser.add_argument("--price-range", help="A number, followed by a '-', followed by a number greater than the first (number is amount in dollars). Only whole numbers please.")
parser.add_argument("--technology", help="CABLE, FIBER, SATELLITE, or DSL.")
args = parser.parse_args()

# Json helper function
def getJSON(delay, jitterdown, jitterup, upspeed, downspeed, percentloss, house):
	js = {
	    "content": {
	        "down": {
	            "corruption": {
	                "correlation": 0,
	                "percentage": 0
	            },
	            "delay": {
	                "correlation": 0,
	                "delay": str(int(round(delay))),
	                "jitter": str(int(round(jitterdown)))
	            },
	            "iptables_options": [],
	            "loss": {
	                "correlation": 0,
	                "percentage": str(percentloss)
	            },
	            "rate": str(int(round(downspeed))),
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
	                "delay": str(int(round(delay))),
	                "jitter": str(int(round(jitterup)))
	            },
	            "iptables_options": [],
	            "loss": {
	                "correlation": 0,
	                "percentage": str(percentloss)
	            },
	            "rate":str(int(round(upspeed))),
	            "reorder": {
	                "correlation": 0,
	                "gap": 0,
	                "percentage": 0
	            }
	        }
	    },
	    "id": 10,
	    "name": "house" + str(house)
	}
	return js


# Reading the database
allcsv = pd.read_csv('full.csv')

try:
	if args.houseid:
		house = int(args.houseid)
		houseinfo = allcsv[allcsv.unit_id == house]
	if not args.houseid:
		if args.state:
			allcsv=allcsv[allcsv.STATE == args.state]
		if args.price_range:
			allcsv=allcsv[allcsv.price >= int(args.price_range.split("-")[0])]
			allcsv=allcsv[allcsv.price <= int(args.price_range.split("-")[1])]
		if args.technology:
			allcsv=allcsv[allcsv.TECHNOLOGY == args.technology.upper()]

		houseinfo = allcsv.sample(n=1)
		house = int(houseinfo.unit_id)
except ValueError:
	print "\nThere are no households meeting the criteria you have set.\n"
	sys.exit()

# Extract data for the selected household
splitup = houseinfo[['Percent Loss','Latency','jitter_up','jitter_down','Speed_up','Speed_down']]

if splitup.empty:
	# Get a random sample to suggest house id's to try
	sample_ids = allcsv.sample(n=5)['unit_id'].tolist()
	print "\nThere is no such houseid in the database."
	print "Try these: %s\n" % ", ".join(map(str, sample_ids))
        sys.exit()

# Reading parameters, conversions
percentloss = float(splitup['Percent Loss'])
delay = float(splitup['Latency']) / 1000.0 / 2

jitterup = float(splitup['jitter_up']) / 1000.0
jitterdown = float(splitup['jitter_down']) / 1000.0

downspeed = int(round(splitup['Speed_down'] * 0.008))
upspeed = int(round(splitup['Speed_up'] * 0.008))
speed = max(downspeed, upspeed)

print "Selected household %d has the following characteristics:" % house
print "--------------------------------------------------------"
print " Upload rate (kbps)    | %d                             " % upspeed
print " Download rate (kbps)  | %d                             " % downspeed
print " Round-trip delay (ms) | %f                             " % (delay*2)
print " Uplink jitter (ms)    | %f                             " % jitterup
print " Downlink jitter (ms)  | %f                             " % jitterdown
print " Packet loss (%%)       | %f                             " % percentloss
print "--------------------------------------------------------"


def netem_template(delay, jitter, percentloss, speed):
	statements = [
	"sudo tc qdisc add dev eth1 root handle 1:0 netem delay %0.6fms %0.6fms loss %0.6f%%" % (delay, jitter, percentloss),
	"sudo tc qdisc add dev eth1 parent 1:1 handle 10: tbf rate %dkbit limit 500000000 burst 100000" % speed
	]
	return "; ".join(statements)

user_netem = netem_template(delay, jitterup, percentloss, upspeed)
server_netem = netem_template(delay, jitterdown, percentloss, downspeed)

# Compiling the rspec for geni
r = PG.Request()

links = []
for i in range(1):
	links.insert(i, PG.LAN('lan%d' % i))
	links[i].bandwidth = speed

con = [[0],[0]]
ifaceCounter = 0
vms = []
for i in range(len(con)):
	if i == 0:
		nodename = "user"
		netem = user_netem
	else:
		nodename = "server"
		netem = server_netem

	igvm = IGX.XenVM(nodename)
	igvm.addService(PG.Execute(shell="/bin/sh", command=netem))
	igvm.addService(PG.Execute(shell="/bin/sh", command="sudo apt-get update; sudo apt-get -y install iperf"))
	vms.insert(i, igvm)

	# Generate interfaces and connections for this VM
	for j in range(len(con[i])):
		linkno = con[i][j]
		iface = igvm.addInterface("if%d" % ifaceCounter)
		ifaceCounter += 1
		iface.addAddress(PG.IPv4Address("10.1.%d.%d" % (linkno, i+1), "255.255.255.0"))
		links[linkno].addInterface(iface)
	r.addResource(igvm)

for l in links:
	r.addResource(l)

# Determining the location for rspec
rspec = os.path.join(os.getcwd(), "house-%d.xml" % house)
r.writeXML(rspec)
print "Rspec written to %s" % rspec

jfile = os.path.join( os.getcwd(), "house-%d.json" % house)
f = open(jfile, 'w')
json.dump(getJSON(delay, jitterdown, jitterup, upspeed, downspeed, percentloss, house), f)
f.close()
print "Json written to %s" % jfile
