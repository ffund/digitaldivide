import sys
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
pd.set_option('max_columns', 50)

csvfile = pd.read_csv('compactInfo.csv', error_bad_lines=False) 
print csvfile
