#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409



import sys
import pandas as pd
import numpy as np
import math

pd.set_option('max_columns', 50)

#allcsv = pd.read_csv('newcompact.csv')
#URS = pd.read_csv('newURS.csv')
def householdPrice(houseID, allcsv, URS):

    us_state_abbrev = {
        'Alabama': 'AL',
        'Alaska': 'AK',
        'Arizona': 'AZ',
        'Arkansas': 'AR',
        'California': 'CA',
        'Colorado': 'CO',
        'Connecticut': 'CT',
        'Delaware': 'DE',
        'Florida': 'FL',
        'Georgia': 'GA',
        'Hawaii': 'HI',
        'Idaho': 'ID',
        'Illinois': 'IL',
        'Indiana': 'IN',
        'Iowa': 'IA',
        'Kansas': 'KS',
        'Kentucky': 'KY',
        'Louisiana': 'LA',
        'Maine': 'ME',
        'Maryland': 'MD',
        'Massachusetts': 'MA',
        'Michigan': 'MI',
        'Minnesota': 'MN',
        'Mississippi': 'MS',
        'Missouri': 'MO',
        'Montana': 'MT',
        'Nebraska': 'NE',
        'Nevada': 'NV',
        'New Hampshire': 'NH',
        'New Jersey': 'NJ',
        'New Mexico': 'NM',
        'New York': 'NY',
        'North Carolina': 'NC',
        'North Dakota': 'ND',
        'Ohio': 'OH',
        'Oklahoma': 'OK',
        'Oregon': 'OR',
        'Pennsylvania': 'PA',
        'Rhode Island': 'RI',
        'South Carolina': 'SC',
        'South Dakota': 'SD',
        'Tennessee': 'TN',
        'Texas': 'TX',
        'Utah': 'UT',
        'Vermont': 'VT',
        'Virginia': 'VA',
        'Washington': 'WA',
        'West Virginia': 'WV',
        'Wisconsin': 'WI',
        'Wyoming': 'WY',
    }

    try:
        inv_map = {v: k for k, v in us_state_abbrev.items()}

        house=allcsv[allcsv.unit_id==houseID]

        houseState= inv_map[house.STATE.values[0]]
        houseISP = house.isp.values[0]

        rates = URS[URS.State==houseState]
        rates = rates[rates.isp==houseISP]

        if rates.empty:
            rates = rates[rates.isp==houseISP]


        def distance(co1, co2):
            return math.sqrt(math.pow(abs(co1[0] - co2[0]), 2) + math.pow(abs(co1[1] - co2[1]), 2))

        if rates.empty:
            return float('NaN')

        rateTuples = zip(map(float,rates["Download Bandwidth Mbps "].values), map(float,rates["Upload Bandwidth Mbps"].values))

        housedown = float(house["SK down"].values[0])
        houseup = float(house["SK UP"].values[0])
        houseTuple = (housedown, houseup)

        nearest = min(rateTuples, key=lambda x: distance(x, houseTuple))

        r = rates[rates["Download Bandwidth Mbps "]==nearest[0]]
        r = r[r["Upload Bandwidth Mbps"]==nearest[1]]
        return r["Total Charge"].values[0]

    except:
        return float('NaN')

#print householdPrice(6)
#print householdPrice(15)


# to merge=[]
# for i in list(allcsv.unit_id):
# 	tomerge.append({'unit_id':i, 'price':pricefind(i)})
# def pricefind(unit):
# 	speedup=allcsv[allcsv.unit_id==unit]["SK UP"]
# 	speeddown=allcsv[allcsv.unit_id==unit]["SK down"]
# 	isp=allcsv[allcsv.unit_id==unit]["isp"]
# 	tech=allcsv[allcsv.unit_id==unit]["TECHNOLOGY"]
# 	state=allcsv[allcsv.unit_id==unit]["STATE"]
# 	URS=abs(URS[URS["Download Bandwidth Mbps"])


