# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import csv
from sklearn.neighbors import NearestNeighbors
import sys

numX = int(sys.argv[1])
numY = int(sys.argv[2])
width = int(sys.argv[3])
nk = int(sys.argv[4])
sim_num = int(sys.argv[5])
moverate = float(sys.argv[6])
num_train = int(sys.argv[7])
num_test = int(sys.argv[8])
plt_x = num_test - width
start_sse = int(sys.argv[9])
end_sse = int(sys.argv[10])
mv = int(sys.argv[11])

figdir = './anom_map_MA_noise/'
    
def main():
    noise_df = pd.read_csv("noise_all_timeseries.csv", header=None)
    noise_ls = np.array(noise_df)
    print(noise_ls)
    print(len(noise_ls))
    for i in range(len(noise_ls)):
        noise = noise_ls[i]
        slip_amp = abs(0)
        train_noise = noise[0:num_train]
        test_noise = noise[num_train:num_train+num_test]
        train_noise = moving_average(train_noise, mv)
        test_noise = moving_average(test_noise, mv)
        train = embed(train_noise, width)
        test = embed(test_noise, width)

        neigh = NearestNeighbors(n_neighbors=nk)
        neigh.fit(train)
        d = neigh.kneighbors(test)[0]
        d = np.mean(d, axis=1)
        mx = np.max(d)
        #d = d / mx
        #print(d)
        #print(type(d))
        if i == 0:
            anom_ls = d
        else:
            anom_ls = np.vstack((anom_ls, d))
        
    anom_array = np.array(anom_ls) 
    anom_df = pd.DataFrame(anom_array)
    anom_list = anom_array.tolist()
    anom_df.to_csv("anom-noise_1d_timeseries_MA.csv", header=None, index=False)
    print(anom_array)
    print(anom_array.shape[0])
    print(anom_array.shape[1])
    anom_2dtime = np.reshape(anom_array.T, (len(anom_array[0]), numY, numX))
    
    
    
    # プロット
         # make coordinate and values
    x = np.arange(numX)
    y = np.arange(numY)
    X, Y = np.meshgrid(x, y)
    for i in range(len(anom_ls[0])):
        plt.figure(200+i)
        cs = plt.pcolormesh(X, Y, anom_2dtime[i], cmap='turbo')
        plt.colorbar(cs)
        plt.clim(0, 5)
        plt.title('noise-anomaly_'+str(i+1)+'movin-average')
        plt.savefig(figdir+'anomaly'+str(i+1)+'_MA_noise.png', format='png', dpi=200)


def moving_average(a, n) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n


def embed(lst, dim):
    emb = np.empty((0,dim), float)
    for i in range(lst.size - dim + 1):
        tmp = np.array(lst[i:i+dim])[::-1].reshape((1,-1))
        emb = np.append( emb, tmp, axis=0)
    return emb
    

if __name__ == '__main__':
    main()
