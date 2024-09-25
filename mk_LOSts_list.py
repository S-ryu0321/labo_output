import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt

#####par#####
sim_num =50
numX = 190
numY = 150

move_rate = 0.5

start_date = '2018-1-1'
end_date = '2019-11-18'


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
	Mnoise = pd.read_csv('./noise_csv/'+"noise"+str(i+1)+".csv", header=None)
	Snoise = pd.read_csv('./noise_csv/'+"noise"+str(i+2)+".csv", header=None)
	Mnoise = np.array(Mnoise)
	Snoise = np.array(Snoise)
	noise_dif = Snoise - Mnoise
	LOSdisp = pd.read_csv("LOS0.csv", header=None)
	LOSdisp = np.array(LOSdisp)
	LOS_noise = LOSdisp + noise_dif
	print(len(LOS_noise))
	print(len(LOS_noise[0]))
	LOS_noise = LOS_noise.reshape(numX*numY, 1)
	ts = np.append(ts, LOS_noise, axis=1)
		
for i in range(4):
	print("================move===============")
	print(int(sim_num * move_rate)+i+1)
	print(int(sim_num * move_rate)+i+2)
	Mnoise = pd.read_csv('./noise_csv/'+"noise"+str(int(sim_num * move_rate)+i+1)+".csv", header=None)
	Snoise = pd.read_csv('./noise_csv/'+"noise"+str(int(sim_num * move_rate)+i+2)+".csv", header=None)
	Mnoise = np.array(Mnoise)
	Snoise = np.array(Snoise)
	noise_dif = Snoise - Mnoise
	LOSdisp = pd.read_csv("LOS2w.csv", header=None)
	LOSdisp = np.array(LOSdisp)
	LOS_noise = LOSdisp + noise_dif
	print(len(LOS_noise))
	print(len(LOS_noise[0]))
	LOS_noise = LOS_noise.reshape(numX*numY, 1)
	ts = np.append(ts, LOS_noise, axis=1)
	
for i in range(sim_num - int(sim_num * move_rate) - 4 - 1):
	print("================stay===============")
	print(int(sim_num * move_rate)+4+i+1)
	print(int(sim_num * move_rate)+4+i+2)
	Mnoise = pd.read_csv('./noise_csv/'+"noise"+str(int(sim_num * move_rate)+4+i+1)+".csv", header=None)
	Snoise = pd.read_csv('./noise_csv/'+"noise"+str(int(sim_num * move_rate)+4+i+2)+".csv", header=None)
	Mnoise = np.array(Mnoise)
	Snoise = np.array(Snoise)
	noise_dif = Snoise - Mnoise
	LOSdisp = pd.read_csv("LOS0.csv", header=None)
	LOSdisp = np.array(LOSdisp)
	LOS_noise = LOSdisp + noise_dif
	print(len(LOS_noise))
	print(len(LOS_noise[0]))
	LOS_noise = LOS_noise.reshape(numX*numY, 1)
	ts = np.append(ts, LOS_noise, axis=1)

#####export_csv_time-series##########
import csv
import pandas as pd

with open(r"LOS_all_timeseries.csv", 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerows(ts)


print(int(sim_num * move_rate)+1)
print(int(sim_num * move_rate)+5)
