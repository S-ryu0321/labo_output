import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv

###par###
start_date = '2018-1-1'
end_date = '2019-11-18'

###read_timeseries###
date = pd.date_range(start=start_date, end=end_date, freq='14D')
LOS_ts = pd.read_csv('./LOS_all_timeseries.csv', header=None)
LOS_ts = np.array(LOS_ts)
print(date)
print(LOS_ts)
