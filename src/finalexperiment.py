
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
parser.add_argument("--state", help="Specify a state from which to draw a sample household. (two letter state code)")
parser.add_argument("--houseid", help="Specify a household ID from the Measuring Broadband America data set.")
parser.add_argument("--price-range", help="A number, followed by a '-', followed by a number greater than the first (number is amount in dollars). Only integer values, please.")
parser.add_argument("--technology", help="CABLE, FIBER, SATELLITE, or DSL.")
parser.add_argument("--users", help="(Integer) number of end users to represent (default: 1)")
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
		housearray = allcsv[allcsv.unit_id == house]
	if not args.houseid:
		if args.state:
			allcsv=allcsv[allcsv.STATE == args.state]
		if args.price_range:
			allcsv=allcsv[allcsv.price >= int(args.price_range.split("-")[0])]
			allcsv=allcsv[allcsv.price <= int(args.price_range.split("-")[1])]
		if args.technology:
			allcsv=allcsv[allcsv.TECHNOLOGY == args.technology.upper()]
		nusers = int(args.users) if args.users else 1

		housearray = allcsv.sample(n=nusers)
except ValueError:
	print "\nThere are no households meeting the criteria you have set.\n"
	sys.exit()


# Compiling the rspec for geni
r = PG.Request()

vms = []
links = []

servervm = IGX.XenVM('server')

housecount = 0

for rowindex, houseinfo in housearray.iterrows():

    house = int(houseinfo.unit_id)
    # Extract data for the selected household
    splitup = houseinfo[['Percent Loss','Latency','jitter_up','jitter_down','Speed_up','Speed_down', 'SK down', 'SK UP', 'STATE', 'isp', 'price']]

    if splitup.empty:
    	# Get a random sample to suggest house id's to try
    	sample_ids = allcsv.sample(n=5)['unit_id'].tolist()
    	print "\nThere is no such houseid in the database."
    	print "Try these: %s\n" % ", ".join(map(str, sample_ids))
        sys.exit()

    # Reading parameters, conversions
    percentloss = float(splitup['Percent Loss']) / 2.0
    delay = float(splitup['Latency']) / 1000.0 / 2

    jitterup = float(splitup['jitter_up']) / 1000.0
    jitterdown = float(splitup['jitter_down']) / 1000.0

    downspeed = int(round(splitup['Speed_down'] * 0.008))
    upspeed = int(round(splitup['Speed_up'] * 0.008))

    speed = max(downspeed, upspeed)

    print "Selected household %d has the following characteristics:" % house
    print "Plan: %s/%s (Mbps down/up), %s %s" % (splitup['SK down'], splitup['SK UP'], splitup['isp'], splitup['STATE'])
    if not np.isnan(float(splitup['price'])):
        print "Estimated price per month: $%s" % splitup['price']
    print "--------------------------------------------------------"
    print " Upload rate (kbps)    | %d                             " % upspeed
    print " Download rate (kbps)  | %d                             " % downspeed
    print " Round-trip delay (ms) | %f                             " % (delay*2)
    print " Uplink jitter (ms)    | %f                             " % jitterup
    print " Downlink jitter (ms)  | %f                             " % jitterdown
    print " Packet loss (%%)       | %f                             " % (percentloss*2)
    print "--------------------------------------------------------"


    def netem_template(delay, jitter, percentloss, speed, ip):
    	statements = [
    	"sudo tc qdisc add dev $(ip route get %s | head -n 1 | cut -d \  -f4) root handle 1:0 netem delay %0.6fms %0.6fms loss %0.6f%%" % (ip, delay, jitter, percentloss),
    	"sudo tc qdisc add dev $(ip route get %s | head -n 1 | cut -d \  -f4) parent 1:1 handle 10: tbf rate %dkbit limit 500000000 burst 100000" % (ip, speed)
    	]
    	return "; ".join(statements)

    ip_netem = "10.0.%d.0" % housecount
    user_netem = netem_template(delay, jitterup, percentloss, upspeed, ip_netem)
    server_netem = netem_template(delay, jitterdown, percentloss, downspeed, ip_netem)

    links.insert(housecount, PG.LAN('lan%d' % housecount))
    links[housecount].bandwidth = speed


    igvm = IGX.XenVM("house-%d" % house)
    igvm.addService(PG.Execute(shell="/bin/sh", command=user_netem))
    igvm.addService(PG.Execute(shell="/bin/sh", command="sudo apt-get update; sudo apt-get -y install iperf"))
    vms.insert(housecount, igvm)

    servervm.addService(PG.Execute(shell="/bin/sh", command=server_netem))


    # Generate interfaces and connections for this VM
    iface = igvm.addInterface("if-%d-1" % housecount)
    iface.addAddress(PG.IPv4Address("10.0.%d.1" % housecount, "255.255.255.0"))
    links[housecount].addInterface(iface)

    # Generate interfaces and connections for this VM
    server_iface = servervm.addInterface("if-%d-2" % housecount)
    server_iface.addAddress(PG.IPv4Address("10.0.%d.2" % housecount, "255.255.255.0"))
    links[housecount].addInterface(server_iface)


    r.addResource(igvm)
    r.addResource(links[housecount])

    housecount += 1

    jfile = os.path.join( os.getcwd(), "house-%d.json" % house)
    f = open(jfile, 'w')
    json.dump(getJSON(delay, jitterdown, jitterup, upspeed, downspeed, percentloss, house), f)
    f.close()
    print "Json written to %s" % jfile

vms.insert(housecount, servervm)

servervm.addService(PG.Execute(shell="/bin/sh", command="sudo apt-get update; sudo apt-get -y install iperf"))
r.addResource(servervm)

# Determining the location for rspec
rspec = os.path.join(os.getcwd(), "houses.xml")
r.writeXML(rspec)
print "Rspec written to %s\n" % rspec
