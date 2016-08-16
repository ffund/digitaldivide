import sys
import pandas as pd
import numpy as np

#statestuff = pd.read_csv("dat/unit_report.csv",error_bad_lines=False)
profile = pd.read_excel("dat/fixedunitprofile.csv",error_bad_lines=False)
URS = pd.read_excel("dat/URS.csv")
fullcsv = pd.read_csv("dat/compactInfo.csv")

print list(set(profile[profile.isp]))
