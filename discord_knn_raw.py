# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import sys


width = int(sys.argv[1])
nk = int(sys.argv[2])
sim_num = int(sys.argv[3])
move_rate = float(sys.argv[4])
num_train = int(sys.argv[5])
num_test = int(sys.argv[6])
plt_x = num_test - width
start_sse = int(sys.argv[7])
end_sse = int(sys.argv[8])
mv = int(sys.argv[9])


mount = "minusH"
    
def main():
    data = pd.read_csv("LOS_timeseries_"+mount+".csv", header=None)
    slip = pd.read_csv("LOSdisp_timeseries_"+mount+".csv", header=None)
    print(data)
    print(len(data))
    data = np.array(data)
    slip = np.array(slip)
    slip_amp = max(abs(slip))
    print(len(data))
    train_data = data[0:num_train]
    test_data = data[num_train:num_train+num_test]
    print(len(train_data))
    print(len(test_data))

    #train_data = moving_average(train_data, mv)

    #test_data = moving_average(test_data, mv)

    #width = 3
    #nk = 1

    train = embed(train_data, width)
    test = embed(test_data, width)
    print(len(train))
    print(len(train[0]))
    print(len(test))
    neigh = NearestNeighbors(n_neighbors=nk)
    neigh.fit(train)
    d = neigh.kneighbors(test)[0]
    d = np.mean(d, axis=1)
    mx = np.max(d)
    #d = d / mx


    # プロット
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
