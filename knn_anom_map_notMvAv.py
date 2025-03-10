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

figdir = './anom_map_raw/'
    
def main():
    data_df = pd.read_csv("LOS_all_timeseries.csv", header=None)
    slip_df = pd.read_csv("LOS_slip_all_timeseries.csv", header=None)
    data_ls = np.array(data_df)
    slip_ls = np.array(slip_df)
    print(data_ls)
    print(len(data_ls))
    print(slip_ls)
    print(len(slip_ls))
    for i in range(len(data_ls)):
        data = data_ls[i]
        slip = slip_ls[i]
        slip_amp = max(abs(slip))
        #print(len(data))
        train_data = data[0:num_train]
        test_data = data[num_train:num_train+num_test]
        #print(len(train_data))
        #print(len(test_data))
        #train_data = moving_average(train_data, 4)
        #test_data = moving_average(test_data, 4)
        #width = 3
	#nk = 1
        train = embed(train_data, width)
        test = embed(test_data, width)
        #print(len(train))
        #print(len(train[0]))
        #print(len(test))
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
    anom_df.to_csv("anom_1d_timeseries_raw.csv", header=None, index=False)
    #print(anom_array)
    #print(anom_array.shape[0])
    #print(anom_array.shape[1])
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
        plt.title('anomaly_'+str(i+1))
        plt.savefig(figdir+'anomaly'+str(i+1)+'.png', format='png', dpi=200)
    '''
    test_for_plot = data[num_train+width-1:num_train+num_test]
    print(len(test_for_plot))
    print(test_for_plot)

    #fig = plt.figure(figsize=(15, 6))
    fig = plt.figure()

    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()

    #p1, = ax1.plot(d, '-m',linewidth = 1, linestyle="dotted" )
    p1, = ax1.plot(d, '-b',linewidth = 1 )

    ax1.set_ylim(0, 5.0)
    ax1.set_xlim(0, plt_x)
    ax1.axvline(x=start_sse-num_train-width)
    ax1.axvline(x=end_sse-num_train-width)
    p2, = ax2.plot(test_for_plot, '-k')

    ax2.set_ylim(-5.0, 5.0)
    ax2.set_xlim(0, plt_x)
    plt.text(0, 4, "max_anom = "+str(mx))
    plt.text(0, 3, "slip_amp = "+str(slip_amp))
    plt.savefig("knn_FL_plot_"+mount+".png", format='png', dpi=200 )
    #plt.show()
    '''


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
