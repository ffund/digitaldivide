import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)

csvfile = pd.read_csv('curr_multicast.csv', error_bad_lines=False, nrows=1000) 
print csvfile['target'][:100]
