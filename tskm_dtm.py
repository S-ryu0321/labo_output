import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

###Elbow method lib###
from tslearn.clustering import TimeSeriesKMeans
from tslearn.utils import to_time_series_dataset
from tslearn.preprocessing import TimeSeriesScalerMeanVariance


###parameter setting###
sim_num = 50
start_date = '2018-1-1'
end_date = '2019-11-18'
numX = 190
numY = 150
move_rate = 0.5

###visual all time-series###
date = pd.date_range(start=start_date, end=end_date, freq='14D')
LOS_ts = pd.read_csv('./LOS_all_timeseries.csv', header=None)
LOS_ts = np.array(LOS_ts)
print(LOS_ts)
print(len(LOS_ts))
print(len(LOS_ts[0]))
print(type(LOS_ts))

plt.figure(1, figsize=(15, 6))
for i in range(len(LOS_ts)):
	plt.plot(date, LOS_ts[i], label='InSAR time-series simulation')
plt.vlines(date[int(sim_num * move_rate)], -5, 5, color="red", linestyle='dashed')
plt.vlines(date[int(sim_num * move_rate)+4], -5, 5, color="red", linestyle='dashed')
plt.ylim(-5, 5)
plt.xlabel('Date')
plt.ylabel('deformetion')
plt.title('InSAR time-series simulation')
plt.legend
plt.grid(True)
plt.savefig('test_slc_'+str(sim_num)+'.png', format='png', dpi=200)



'''
###Elbow method###
inertia = []
for n_clusters in range(1, 12):
	km = TimeSeriesKMeans(n_clusters=n_clusters, metric='dtw', random_state=0)
	km.fit(LOS_ts)
	inertia.append(km.inertia_)

plt.figure(2, figsize=(15, 6))
plt.plot(range(1, 12), inertia, marker='o')
plt.xlabel('num_clusters')
plt.ylabel('SSE')
plt.title('Elbow method')
plt.savefig('Elbow.png', format='png', dpi=200)
'''

###time-series k-means using DTW###
n = 3	#from Elbow method

km_dtw = TimeSeriesKMeans(n_clusters=n, metric='dtw', random_state=0)
labels_dtw = km_dtw.fit_predict(LOS_ts)
print("====label====")
print(labels_dtw)
print(len(labels_dtw))
csv_path_label = r"TSKM_clustering_labels.csv"
labels_output = pd.DataFrame(labels_dtw)
labels_output.to_csv(csv_path_label, mode='w', index=False, header=False)

fig, axes = plt.subplots(n, figsize=(8, 16))
plt.subplots_adjust(hspace=0.5)
for i in range(n):
	ax = axes[i]
	
	for x in LOS_ts[labels_dtw == i]:
		ax.plot(x.ravel(), 'k-', alpha=0.2)
		ax.set_ylim(-5, 5)
		ax.axvline(x=int(sim_num * move_rate))
		ax.axvline(x=int(sim_num * move_rate+4))
	ax.plot(km_dtw.cluster_centers_[i].ravel(), 'r-')
	
	datenum = np.count_nonzero(labels_dtw == i)
	ax.text(0.5, -4.0, f'Cluster{(i)} : n = {datenum}')
	if i == 0:
		ax.set_title('time-series clustering')
plt.savefig('time-series_k-means_clustering_ts.png', format='png', dpi=200)


###label 1d to 2d(190*150)###
label_tskm = pd.read_csv('./TSKM_clustering_labels.csv', header=None)
label_tskm = np.array(label_tskm)
label_tskm_2d = label_tskm.reshape(numY, numX)
print(len(label_tskm_2d))
print(len(label_tskm_2d[0]))
