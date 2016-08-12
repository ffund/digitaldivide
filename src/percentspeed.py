import matplotlib
matplotlib.use('Agg')
import pylab as plt
from matplotlib.ticker import FuncFormatter
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns
import sys
import pandas as pd
import numpy as np
pd.set_option('max_columns', 50)

full = pd.read_csv('compactInfo.csv', error_bad_lines=False)[['unit_id','Speed_down','Speed_up']]
#csvmspeeddown = pd.read_csv('dat/curr_httpgetmt.csv', error_bad_lines=False)[['unit_id','bytes_sec']]
#csvmspeedup = pd.read_csv('dat/curr_httppostmt.csv', error_bad_lines=False)[['unit_id','bytes_sec']]
unique = list(full.unit_id)
downs=[]
tofive=[]
toeight=[]
tofifteen=[]
plus=[]
#print full[full.unit_id == 6]['Speed_down'][0]
downs = [float((full[full.unit_id == i]['Speed_down']) * .0000080) for i in unique]
#print downs
for i in unique:
	pass
	'''#print "avg DL of house "+str(i)+" : "+str(downspeed)
	if downspeed < 5:
		tofive.append(downspeed)
	elif downspeed < 15:
		toeight.append(downspeed)
	elif downspeed < 30:
		tofifteen.append(downspeed)
	elif downspeed >= 30:
		plus.append(downspeed)
total=float(len(uniquedown))
percentfive = len(tofive)/total
percenteight = len(toeight)/total
percentfifteen = len(tofifteen)/total
percentplus = len(plus)/total
print "DL info:"
print percentfive, percenteight, percentfifteen, percentplus
'''
#downplot = sns.barplot(x="speed range", y="percent", data=downs)

#def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
#    s = str(100 * y)

    # The percent symbol needs escaping in latex
#    if matplotlib.rcParams['text.usetex'] is True:
#        return s + r'$\%$'
#    else:
#        return s + '%'
'''plt.xlabel('Average DL speed of households(Mbps)')
plt.ylabel('Frequency')
weights = np.ones_like(downs)/len(downs)
plt.hist(downs, bins=75, weights=weights)'''
sns.distplot(downs, bins=20, kde=False)
#formatter = FuncFormatter(to_percent)
#plt.gca().yaxis.set_major_formatter(formatter)
#plt.show()
sns_plot.savefig("seaborntry.png")
#plt.savefig("percentDL.png")


ups=[]
tofiveup=[]
toeightup=[]
tofifteenup=[]
plusup=[]

ups = [float((full[full == j]['Speed_up']) * .0000080) for j in unique]

for j in unique:
	pass	
	'''#print "avg UL of house "+str(j)+" : "+str(upspeed)
	if upspeed < 5:
                tofiveup.append(upspeed)
        elif upspeed < 15:
                toeightup.append(upspeed)
        elif upspeed < 30:
                tofifteenup.append(upspeed)
        elif upspeed >= 30:
                plusup.append(upspeed)
total=float(len(uniqueup))
percentfiveup = len(tofiveup)/total
percenteightup = len(toeightup)/total
percentfifteenup = len(tofifteenup)/total
percentplusup = len(plusup)/total
print "UL info:"
print percentfiveup,percenteightup,percentfifteenup,percentplusup
'''
#upplot=sns.barplot(x="speed range", y="percent", data=ups)
'''plt.xlabel('Average DL speed of households(Mbps)')
plt.ylabel('Frequency')
weights = np.ones_like(ups)/len(ups)
plt.hist(ups, bins=75, weights=weights)
#formatter = FuncFormatter(to_percent)
#plt.gca().yaxis.set_major_formatter(formatter)
#plt.show()
plt.savefig("percentUL.png")'''

