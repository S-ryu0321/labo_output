#!/bin/bash

slip_amp=$1
atm_mean=$2
atm_std=$3
atm_amp=$4

sim_num=$5
now=$6

num_train=$7
num_test=$8

HOME=/home/sakurai/hdd2/sim_anom-detect/anom-map/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/
Path=/home/sakurai/hdd2/sim_anom-detect/script/

##okada_par##
time=50
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

start_date='2018-1-1'
end_date='2019-11-18'

move_rate=0.5

##noise-sim_par##
numX=190
numY=150

##anomaly_detection_par##
width=3      #windowsize_knn
nk=5        #num of nearest neighbor point

start_sse=26
end_sse=30
MV=3         #moving_average_size
ts="minusH"  #which time-series


mkdir -p ${HOME}${now}/
cd ${HOME}${now}/
mkdir -p ./noise_csv/
mkdir -p ./anom_map_raw/
mkdir -p ./anom_map_MA/
cp -r ${Path}module/ .
cp -r ${Path}lib/ .

echo
echo ############################################
echo # mk_SSE_time-series_disp+noise
echo ############################################
echo
python3 ${Path}sim_SSE_ts.py ${time} ${slip_amp} ${atm_std} ${move_rate} ${X_ts_minus_H} ${Y_ts_minus_H} ${X_ts_minus_M} ${Y_ts_minus_M} ${X_ts_minus_L} ${Y_ts_minus_L} ${X_ts_plus_H} ${Y_ts_plus_H} ${X_ts_plus_M} ${Y_ts_plus_M} ${X_ts_plus_L} ${Y_ts_plus_L} ${X_ts_0} ${Y_ts_0} ${start_date} ${end_date}

echo
echo ############################################
echo # mk_SSE_time-series_disp
echo ############################################
echo
python3 ${Path}sse_ts_slip.py ${time} ${move_rate} ${X_ts_minus_H} ${Y_ts_minus_H} ${X_ts_minus_M} ${Y_ts_minus_M} ${X_ts_minus_L} ${Y_ts_minus_L} ${X_ts_plus_H} ${Y_ts_plus_H} ${X_ts_plus_M} ${Y_ts_plus_M} ${X_ts_plus_L} ${Y_ts_plus_L} ${X_ts_0} ${Y_ts_0} ${start_date} ${end_date}

echo
echo ############################################
echo # LOS2d to LOS1d
echo ############################################
echo
python3 ${Path}mk_LOSts_list_ver2.py ${time} ${numX} ${numY} ${move_rate} ${start_date} ${end_date}

echo
echo ############################################
echo # disp2d to disp1d
echo ############################################
echo
python3 ${Path}mk_LOSslip_list.py ${time} ${numX} ${numY} ${move_rate} ${start_date} ${end_date}

echo
echo ############################################
echo # noise2d to noise1d
echo ############################################
echo
python3 ${Path}mk_noisets_list.py ${time} ${numX} ${numY} ${move_rate} ${start_date} ${end_date}

echo
echo ############################################
echo # anomaly_detection_1pixel(moving-average)
echo ############################################
echo
python3 ${Path}discord_knn_MV.py ${width} ${nk} ${time} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV} ${ts}

echo
echo ############################################
echo # anomaly_detection_1pixel(raw)
echo ############################################
echo
python3 ${Path}discord_knn_raw.py ${width} ${nk} ${time} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV} ${ts}

echo
echo ############################################
echo # anomaly_detection_map(moving-average)
echo ############################################
echo
python3 ${Path}knn_anom_map.py ${numX} ${numY} ${width} ${nk} ${time} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV}

echo
echo ############################################
echo # anomaly_detection_map(raw)
echo ############################################
echo
python3 ${Path}knn_anom_map_notMvAv.py ${numX} ${numY} ${width} ${nk} ${time} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse}

echo
echo ############################################
echo # noise-anomaly_detection_map(moving-average)
echo ############################################
echo
mkdir -p ./anom_map_MA_noise
python3 ${Path}knn_anom_map_noise.py ${numX} ${numY} ${width} ${nk} ${time} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse} ${MV}

echo
echo ############################################
echo # noise-anomaly_detection_map(raw)
echo ############################################
echo
mkdir -p ./anom_map_raw_noise
python3 ${Path}knn_anom_map_notMvAv_noise.py ${numX} ${numY} ${width} ${nk} ${time} ${move_rate} ${num_train} ${num_test} ${start_sse} ${end_sse}

echo
echo ############################################
echo # anom_map_filt
echo ############################################
echo
mkdir -p ./anom_map_filt
mkdir -p ./anom_map_MA_filt
python3 ${Path}plot_distribution.py ${now} ${numX} ${numY} ${end_sse} ${num_train} ${num_test} ${width}



echo
echo ############################################
echo # SNR
echo ############################################
echo
python3 ${Path}plot_SNR.py ${atm_mean} ${atm_std}

cp -r ./noise_csv ${HOME}all/noise_csv_${now}/
cp ./LOS0.csv ${HOME}all/
cp ./LOS2m.csv ${HOME}all/
cp ./LOS2w.csv ${HOME}all/
cp ./anom_1d_timeseries_MA.csv ${HOME}all/anom/anom_1d_timeseries_MA_${now}.csv
cp ./anom_1d_timeseries_raw.csv ${HOME}all/anom/anom_1d_timeseries_raw_${now}.csv
cp ./anom-noise_1d_timeseries_raw.csv ${HOME}all/anom/anom-noise_1d_timeseries_raw_${now}.csv
cp ./anom-noise_1d_timeseries_MA.csv ${HOME}all/anom/anom-noise_1d_timeseries_MA_${now}.csv




cd ${HOME}
