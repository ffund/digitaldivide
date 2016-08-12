import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#pd.set_option('max_columns', 50)

csvfile = pd.read_csv('compactInfo.csv', error_bad_lines=False) 
print len(csvfile.unit_id)-csvfile.count(0)
#df = pd.read_csv("compactInfo.csv")
#df.dropna(axis=0)
#df.to_csv('nonan.csv')
