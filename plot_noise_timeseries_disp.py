import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#####par#####
sim_num =50
numX = 190
numY = 150

move_rate = 0.5

start_date = '2018-1-1'
end_date = '2019-11-18'

X_ts_minus_H = 60
Y_ts_minus_H = 115
X_ts_minus_M = 60
Y_ts_minus_M = 100
X_ts_minus_L = 60
Y_ts_minus_L = 90
X_ts_plus_H = 95
Y_ts_plus_H = 115
X_ts_plus_M = 95
Y_ts_plus_M = 100
X_ts_plus_L = 95
Y_ts_plus_L = 90
X_ts_0 = 20
Y_ts_0 = 20

date = pd.date_range(start=start_date, end=end_date, freq='14D')


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
	
ts_2d = ts.reshape(numX, numY, sim_num)
print(ts_2d)
print(len(ts_2d))
print(len(ts_2d[0]))
print(len(ts_2d[0][0]))

minusH_list = ts_2d[X_ts_minus_H][Y_ts_minus_H]
minusM_list = ts_2d[X_ts_minus_M][Y_ts_minus_M]
minusL_list = ts_2d[X_ts_minus_L][Y_ts_minus_L]
plusH_list = ts_2d[X_ts_plus_H][Y_ts_plus_H]
plusM_list = ts_2d[X_ts_plus_M][Y_ts_plus_M]
plusL_list = ts_2d[X_ts_plus_L][Y_ts_plus_L]
list_0 = ts_2d[X_ts_0][Y_ts_0]
###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, minusH_list, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'minusH_noise.png', format='png', dpi=200)

###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, minusM_list, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'minusM_noise.png', format='png', dpi=200)

###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, minusL_list, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'minusL_noise.png', format='png', dpi=200)

###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, plusH_list, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'plusH_noise.png', format='png', dpi=200)

###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, plusM_list, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'plusM_noise.png', format='png', dpi=200)

###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, plusL_list, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'plusL_noise.png', format='png', dpi=200)

###plot figure###
plt.figure(figsize=(15, 6))
plt.plot(date, list_0, label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('slc_'+str(sim_num)+'_0_noise.png', format='png', dpi=200)

