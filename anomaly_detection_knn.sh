#!/bin/bash

sim_num=$1
now=$2
slc=50
start_date='2018-1-1'
end_date='2019-11-18'
move_rate=0.5

slip_amp=$3
atm_amp=5




HOME=/home/sakurai/hdd2/sim_anom-detect/sim/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_SLC${slc}_rate${move_rate}/
Path=/home/sakurai/hdd2/sim_anom-detect/script/

X_ts_minus_H=60
Y_ts_minus_H=115
X_ts_minus_M=60
Y_ts_minus_M=100
X_ts_minus_L=60
Y_ts_minus_L=90
X_ts_plus_H=95
Y_ts_plus_H=115
X_ts_plus_M=95
Y_ts_plus_M=100
X_ts_plus_L=95
Y_ts_plus_L=90
X_ts_0=20
Y_ts_0=20




##noise-sim_par##
numX=190
numY=150

##anomaly_detection_par##
num_train=$4
num_test=$5
width=$6     #windowsize_knn
nk=$7        #num of nearest neighbor point
start_sse=26
end_sse=30
MV=$8         #moving_average_size
ts="minusH"  #which time-series


cd ${HOME}${now}/
mkdir -p ./knn_train${num_train}_test${num_test}_w${width}_nk${nk}_ma${MV}/
mkdir -p ./knn_train${num_train}_test${num_test}_w${width}_nk${nk}_ma${MV}/noise_csv/
mkdir -p ./knn_train${num_train}_test${num_test}_w${width}_nk${nk}_ma${MV}/anom_map_raw/
mkdir -p ./knn_train${num_train}_test${num_test}_w${width}_nk${nk}_ma${MV}/anom_map_MA/
cd ./knn_train${num_train}_test${num_test}_w${width}_nk${nk}_ma${MV}/

cp ${HOME}${now}/*.csv .


echo
echo ############################################
echo # anomaly_detection_1pixel(moving-average)
echo ############################################
echo
python3 ${Path}discord_knn_MV.py ${width} ${nk} ${slc} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV} ${ts}

echo
echo ############################################
echo # anomaly_detection_1pixel(raw)
echo ############################################
echo
python3 ${Path}discord_knn_raw.py ${width} ${nk} ${slc} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV} ${ts}

echo
echo ############################################
echo # anomaly_detection_map(moving-average)
echo ############################################
echo
python3 ${Path}knn_anom_map.py ${numX} ${numY} ${width} ${nk} ${slc} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV}

echo
echo ############################################
echo # anomaly_detection_map(raw)
echo ############################################
echo
python3 ${Path}knn_anom_map_notMvAv.py ${numX} ${numY} ${width} ${nk} ${slc} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse}

echo
echo ############################################
echo # noise-anomaly_detection_map(moving-average)
echo ############################################
echo
mkdir -p ./anom_map_MA_noise
python3 ${Path}knn_anom_map_noise.py ${numX} ${numY} ${width} ${nk} ${slc} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV}

echo
echo ############################################
echo # noise-anomaly_detection_map(raw)
echo ############################################
echo
mkdir -p ./anom_map_raw_noise
python3 ${Path}knn_anom_map_notMvAv_noise.py ${numX} ${numY} ${width} ${nk} ${slc} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse}

echo
echo ############################################
echo # anom_map_filt
echo ############################################
echo
mkdir -p ./anom_map_filt
mkdir -p ./anom_map_MA_filt
python3 ${Path}plot_distribution.py ${now} ${numX} ${numY} ${end_sse} ${num_train} ${num_test} ${width}


cp -r ./noise_csv ${HOME}all/noise_csv_${now}/
cp ./LOS0.csv ${HOME}all/
cp ./LOS2m.csv ${HOME}all/
cp ./LOS2w.csv ${HOME}all/
cp ./anom_1d_timeseries_MA.csv ${HOME}all/anom/anom_1d_timeseries_MA_${now}.csv
cp ./anom_1d_timeseries_raw.csv ${HOME}all/anom/anom_1d_timeseries_raw_${now}.csv
cp ./anom-noise_1d_timeseries_raw.csv ${HOME}all/anom/anom-noise_1d_timeseries_raw_${now}.csv
cp ./anom-noise_1d_timeseries_MA.csv ${HOME}all/anom/anom-noise_1d_timeseries_MA_${now}.csv




cd ${HOME}
