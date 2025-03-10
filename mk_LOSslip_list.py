import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import sys

#####par#####
sim_num = int(sys.argv[1])
numX = int(sys.argv[2])
numY = int(sys.argv[3])

move_rate = float(sys.argv[4])

start_date = sys.argv[5]
end_date = sys.argv[6]


#############mk_time-series########################
#####parameter#####
ts = np.zeros(numX*numY, float).reshape(numX*numY, 1)
print(len(ts))
print(len(ts[0]))
LOSdisp = pd.read_csv("LOS0.csv", header=None)
for i in range(int(sim_num * move_rate)):
	print("================stay===============")
	print(i+1)
	print(i+2)
	LOSdisp = pd.read_csv("LOS0.csv", header=None)
	LOSdisp = np.array(LOSdisp)
	LOSdisp = LOSdisp.reshape(numX*numY, 1)
	ts = np.append(ts, LOSdisp, axis=1)
		
for i in range(4):
	print("================move===============")
	print(int(sim_num * move_rate)+i+1)
	print(int(sim_num * move_rate)+i+2)
	LOSdisp = pd.read_csv("LOS2w.csv", header=None)
	LOSdisp = np.array(LOSdisp)
	LOSdisp = LOSdisp.reshape(numX*numY, 1)
	ts = np.append(ts, LOSdisp, axis=1)
	
for i in range(sim_num - int(sim_num * move_rate) - 4 - 1):
	print("================stay===============")
	print(int(sim_num * move_rate)+4+i+1)
	print(int(sim_num * move_rate)+4+i+2)
	LOSdisp = pd.read_csv("LOS0.csv", header=None)
	LOSdisp = np.array(LOSdisp)
	LOSdisp = LOSdisp.reshape(numX*numY, 1)
	ts = np.append(ts, LOSdisp, axis=1)

for i in range(len(ts)):
	ts[i] = np.cumsum(ts[i])

#####export_csv_time-series##########
import csv
import pandas as pd

with open(r"LOS_slip_all_timeseries.csv", 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerows(ts)


print(int(sim_num * move_rate)+1)
print(int(sim_num * move_rate)+5)
