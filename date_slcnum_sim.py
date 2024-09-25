import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

start_date = '2018-1-1'
end_date = '2019-11-18'

ts = pd.date_range(start=start_date, end=end_date, freq='14D')
print(ts)
print(len(ts))
