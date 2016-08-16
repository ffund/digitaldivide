#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409


import sys
import pandas as pd
import numpy as np
pd.set_option('max_columns', 50)

allcsv = pd.read_csv('compactInfo.csv')
URS = pd.read_csv('URS.csv')
profilemba = pd.read_csv('fixedishunitprofile.csv')
#print URS
URS = URS[URS.Technology != "Other"]
URS = URS.rename(columns={'Provider': 'isp', 'Technology': 'TECHNOLOGY'})
#URS=URS.replace("Provider","isp")
#URS=URS.replace("Technology","TECHNOLOGY")
URS=URS.replace("AT&T Services, Inc.", "AT&T")
URS=URS.replace("Charter Communications, Inc.","Charter")
URS=URS.replace("Charter Communications","Charter")
URS=URS.replace('Mediacom Minnesota LLC','Mediacom')
URS=URS.replace('Mediacom Illinois LLC','Mediacom')
URS=URS.replace('Mediacom Iowa LLC','Mediacom')
URS=URS.replace('Verizon New England Inc.','Verizon')
URS=URS.replace('Verizon California Inc.','Verizon')
URS=URS.replace('Verizon New Jersey Inc.','Verizon')
URS=URS.replace('Verizon Florida LLC','Verizon')
URS=URS.replace('Verizon Pennsylvania Inc.','Verizon')
URS=URS.replace('Verizon New York Inc.','Verizon')
URS=URS.replace('Verizon Virginia Inc.','Verizon')
profilemba=profilemba.replace('Verizon DSL','Verizon')
URS=URS.replace('Frontier Communications Corporation','Frontier')
URS=URS.replace('Cox Communications, Inc','Cox')
URS=URS.replace('Time Warner Cable Enterprises LLC','Time Warner Cable')
URS=URS.replace('Time Warner Cable Inc.','Time Warner Cable')
URS=URS.replace('BENTON CABLEVISION, INC.','Cablevision')
URS=URS.replace('Windstream Corporation','Windstream')
URS=URS.replace('COMCAST CABLE COMMUNICATIONS, INC.','Comcast')
URS=URS.replace('CenturyLink, Inc.','CenturyLink')
URS=URS.replace('Fixed wireless','SATELLITE')
URS=URS.replace('FTTH','FIBER')
URS=URS.replace('Cable','CABLE')
URS.to_csv("testchange.csv")
#print "written"
URSlist= ['Frontier Communications','Liberty Cablevision of Puerto Rico LLC','Canby Telephone Association', 'COMCAST CABLE COMMUNICATIONS, INC.', 'Northern New England Telephone Operations LLC', 'RCN Telecom Services (Lehigh) LLC', 'SureWest Kansas Operations, LLC', 'Hopper Telecommunications LLC', 'Savage Communications Inc.', 'Simply Bits, LLC', 'Sonic Telecom, LLC', 'The Computer Works', 'DerbyNet, LLC', 'Cable One, Inc.', 'RCN Telecom Services of New York, LP', 'WireFree Communications, Inc.', 'Armstrong Utilities, Inc.', 'RCN Telecom Services of Philadelphia, LLC', 'Cincinnati Bell Extended Territories LLC', 'Ranch Wireless, Inc.', 'ImOn Communications, LLC', 'Freedom Wireless Broadband, LLC', 'TDS TELECOMMUNICATIONS CORPORATION', 'Bright House Networks, LLC', 'Excel.Net, Inc.', 'Shidler Telephone Company', 'Chesnee Cable, Inc.', 'Farmers Telephone Cooperative, Inc.', 'MTCO Communications, Inc.', 'Google Fiber Kansas, LLC', 'DigitalPath, Inc.', 'MCC Georgia LLC', 'Netwurx', 'Puerto Rico Cable Acquisition Company Inc.', 'Otelco Telephone', 'GoldStar Communications, LLC', 'WEHCO Video, Inc.', 'Puerto Rico Telephone Company, Inc.', 'Enterprises LLC' , 'Digis LLC', 'Hawaiian Telcom, Inc.', 'Mega Broadband, Inc', 'E-Vergent.Com LLC', 'CentraCom Interactive', 'CSC Holdings LLC', 'Community Cable & Broadband, Inc.', 'Moose Lake, Village Of/dba, Moose-Tec', 'Chesnee Telephone Company, Inc. d/b/a Chesnee Communications', 'SpeedConnect LLC', '3 Rooms Communications LLC', 'Texas Communications of Bryan Inc.', 'FTC Diversified Services, LLC', 'BlountBroadband LLC', 'Atlantic Telephone Membership Corporation', 'Knology of Alabama, Inc.', 'Miles Wireless', 'Blountsville Telephone LLC', 'Fire2Wire', 'Blue Ridge Cable Technologies, Inc.', 'VTX Communications, LLC', 'Surf Air Wireless', '4 SIWI LLC', 'Beehive Broadband LLC UTAH', 'Delta Communications', 'ALASKA COMMUNICATIONS SYSTEMS HOLDING, INC.', 'Suddenlink Communications', 'Cimarron Telephone Company', 'MetaLINK Technologies, Inc.', 'Google Fiber Missouri, LLC', 'MetroCast Communications of Connecticut, LLC', 'Buford Communications 1, L.P.', 'Atlantic Broadband (Penn), LLC', 'Ultra Communications Group, LLC', 'FBN Indiana Inc.', 'WaveDivision Holdings, LLC', 'Orlando Telephone Company', 'GCI Communication Corp.', 'VTX Telecom, LLC.', 'Amplex Electric, Inc.', 'SureWest TeleVideo', 'Service Electric Cable TV, Inc.', 'AlasConnect, Inc.', 'Knology of Florida, Inc.', 'TRANSWORLD NETWORK, CORP', 'Cequel Communications, LLC']
for i in URSlist:
	URS=URS[URS.isp != i]
mbalist = ['Wildblue/ViaSat', 'Brighthouse', 'Hughes', 'Insight',  'Qwest']
for j in mbalist:
	profilemba=profilemba[profilemba.isp != j]
#"FTTH"="FIBER"
#"Fixed wireless"="SATELLITE"
#"Cable"="CABLE"
#"DSL"="DSL"
#print "profile:"
#print list(set(profilemba["isp"]))
#print list(set(profilemba["TECHNOLOGY"]))


#print "URS:"
#print list(set(URS["isp"]))
#print list(set(URS["TECHNOLOGY"]))
pd.merge(allcsv,profilemba, on='unit_id', how='inner')
print 'merged'
