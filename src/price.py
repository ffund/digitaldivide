#Some house_ids with data:
#6   15   83   360   362   365   368   380   382   385   386   390   404   405   409


import sys
import pandas as pd
import numpy as np
pd.set_option('max_columns', 50)

if len(sys.argv)>1:

        allcsv = pd.read_csv('compactInfo.csv')

        house=int(sys.argv[1])


