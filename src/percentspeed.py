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


csvmspeeddown = pd.read_csv('dat/curr_httpgetmt.csv', error_bad_lines=False)[['unit_id','bytes_sec']]
csvmspeedup = pd.read_csv('dat/curr_httppostmt.csv', error_bad_lines=False)[['unit_id','bytes_sec']]
uniquedown = list(set(csvmspeeddown.unit_id))
downs=[]
tofive=[]
toeight=[]
tofifteen=[]
plus=[]

downs = [(csvmspeeddown[csvmspeeddown.unit_id == i]['bytes_sec']).mean() * .0000080 for i in uniquedown]
for i in uniquedown:
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

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(100 * y)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'


plt.hist(downs, bins=5, normed=True)
formatter = FuncFormatter(to_percent)
plt.gca().yaxis.set_major_formatter(formatter)
plt.show()

uniqueup = list(set(csvmspeedup.unit_id))
ups=[]
tofiveup=[]
toeightup=[]
tofifteenup=[]
plusup=[]

ups = [(csvmspeedup[csvmspeedup.unit_id == j]['bytes_sec']).mean() * .0000080 for j in uniqueup]

for j in uniqueup:
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
