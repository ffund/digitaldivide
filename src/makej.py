#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409


import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)

if len(sys.argv)>1:

        #csvloss = pd.read_csv('dat/curr_udplatency.csv', error_bad_lines=False)
        #csvjitter = pd.read_csv('dat/curr_udpjitter.csv', error_bad_lines=False)
        #csvmspeeddown = pd.read_csv('dat/curr_httpgetmt.csv', error_bad_lines=False)
        #csvmspeedup = pd.read_csv('dat/curr_httppostmt.csv', error_bad_lines=False)
        allcsv = pd.read_csv('compactInfo.csv')

        house=int(sys.argv[1])

        #loss=(csvloss[csvloss.unit_id == house][['unit_id','successes','failures']])
        splitup = (allcsv[allcsv.unit_id == house][['Percent Loss','Latency','jitter_up','jitter_down','Speed_up','Speed_down']])
        if splitup.empty:
                print "The inputted house_ID is not in the database. Please try again"
        else:
                #jitter = (csvjitter[csvjitter.unit_id == house][['latency','jitter_up','jitter_down']])
                #mspeeddown = (csvmspeeddown[csvmspeeddown.unit_id == house]['bytes_sec'])
                #mspeedup = (csvmspeedup[csvmspeedup.unit_id == house]['bytes_sec'])
                #totalsuccess = loss.successes.sum()
                #totalfailure = loss.failures.sum()
                percentloss = splitup['Percent Loss'][0]


                #combined = pd.concat([loss, jitter, mspeeddown, mspeedup], axis=1)

                #print combined

                #print "percent loss:"
                #print percentloss

                latency = splitup['Latency'][0]/1000.0

                #print "latency:"
                #print latency

                jitterup = splitup['jitter_up'][0]/1000.0
                jitterdown = splitup['jitter_down'][0]/1000.0

                #print "jitteravg:"
                #print jitteravg

                speed = max(splitup['Speed_up'][0],splitup['Speed_down'][0])
                downspeed = int(round(splitup['Speed_down'][0] * 0.008))
                upspeed = int(round(splitup['Speed_up'][0] * 0.008))

thefile= '''{
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
    "name": "test"
}'''

print thefile
