import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
import seaborn as sns

#now = int(sys.argv[1])
#numX = int(sys.argv[2])
#numY = int(sys.argv[3])
#end_sse = int(sys.argv[4])
#num_train = int(sys.argv[5])
#num_test = int(sys.argv[6])
#width = int(sys.argv[7])

now = 1
numX = 190
numY = 150
end_sse = 30
num_train = 20
num_test = 30
width = 3

anom_1d_dir = './'
anomdir = './anom_map_filt/'
anomMAdir =  './anom_map_MA_filt/'
#noise_dir = 'noise_csv_'+str(now)



anom = pd.read_csv(anom_1d_dir+'anom_1d_timeseries_raw.csv', header=None)
print(anom)
anom_MA = pd.read_csv(anom_1d_dir+'anom_1d_timeseries_MA.csv', header=None)
anom_noise = pd.read_csv(anom_1d_dir+'anom-noise_1d_timeseries_raw.csv', header=None)
anom_MA_noise = pd.read_csv(anom_1d_dir+'anom-noise_1d_timeseries_MA.csv', header=None)
anom = np.array(anom)
anom_MA = np.array(anom_MA)
anom_noise = np.array(anom_noise)
anom_MA_noise = np.array(anom_MA_noise)
print(anom)
print(len(anom))
print(len(anom[0]))

def th(ar):
	thr = np.mean(ar) + 1.96*np.std(ar)
	return thr

anom_95 = th(anom)
anom_noise_95 = th(anom_noise)
anom_MA_95 = th(anom_MA)
anom_MA_noise_95 = th(anom_MA_noise)

anom_filt = np.ma.masked_where(anom < anom_noise_95, anom)
anom_MA_filt = np.ma.masked_where(anom_MA < anom_MA_noise_95, anom_MA)


anom_filt_2dtime = np.reshape(anom_filt.T, (len(anom_filt[0]), numY, numX))
anom_MA_filt_2dtime = np.reshape(anom_MA_filt.T, (len(anom_MA_filt[0]), numY, numX))

# プロット
    # make coordinate and values
x = np.arange(numX)
y = np.arange(numY)
X, Y = np.meshgrid(x, y)
for i in range(len(anom[0])):
    plt.figure(200+i)
    cs = plt.pcolormesh(X, Y, anom_filt_2dtime[i], cmap='turbo')
    plt.colorbar(cs)
    plt.clim(0, 5)
    plt.title('anomaly_'+str(i+1)+' mask' )
    plt.savefig(anomdir+'anomaly'+str(i+1)+'_filt.png', format='png', dpi=200)

x = np.arange(numX)
y = np.arange(numY)
X, Y = np.meshgrid(x, y)
for i in range(len(anom_MA[0])):
    plt.figure(300+i)
    cs = plt.pcolormesh(X, Y, anom_MA_filt_2dtime[i], cmap='turbo')
    plt.colorbar(cs)
    plt.clim(0, 5)
    plt.title('anomaly_'+str(i+1)+'moving-average mask')
    plt.savefig(anomMAdir+'anomaly'+str(i+1)+'_MA_filt.png', format='png', dpi=200)

#anom_std = np.std(anom)
#anom_mean = np.mean(anom)
#anom_95 = anom_mean + 1.96*anom_std
#anom_MA_std = np.std(anom_MA)
#anom_MA_mean = np.mean(anom_MA)
#anom_noise_std = np.std(anom_noise)
#anom_noise_mean = np.mean(anom_noise)
#anom_MA_noise_std = np.std(anom_MA_noise)
#anom_MA_noise_mean = np.mean(anom_MA_noise)
#print(anom_std)
#print(anom_mean)
#print(anom_noise_std)
#print(anom_noise_mean)

anom_all = anom.reshape(numX*numY*len(anom[0]))
anom_noise_all = anom_noise.reshape(numX*numY*len(anom_noise[0]))
anom_MA_all = anom_MA.reshape(numX*numY*len(anom_MA[0]))
anom_MA_noise_all = anom_MA_noise.reshape(numX*numY*len(anom_MA_noise[0]))

sns.displot(anom_all)
plt.savefig('anom_dist.png')
sns.displot(anom_noise_all)
plt.savefig('anom_noise_dist.png')
sns.displot(anom_MA_all)
plt.savefig('anom_MA_dist.png')
sns.displot(anom_MA_noise_all)
plt.savefig('anom_MA_noise_dist.png')
#end_sse-num_train-width

