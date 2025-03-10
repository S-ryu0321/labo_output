#!/bin/bash

slip_amp=$1
atm_mean=$2
atm_std=$3
atm_amp=$4

sim_num=$5
now=$6
slc=$7
start_date=$8
end_date=$9

move_rate=0.5



HOME=/home/sakurai/hdd2/sim_anom-detect/sim/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_SLC${slc}_rate${move_rate}/
Path=/home/sakurai/hdd2/sim_anom-detect/script/

SLC=50
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
python3 ${Path}sim_SSE_ts.py ${SLC} ${slip_amp} ${atm_std} ${move_rate} ${X_ts_minus_H} ${Y_ts_minus_H} ${X_ts_minus_M} ${Y_ts_minus_M} ${X_ts_minus_L} ${Y_ts_minus_L} ${X_ts_plus_H} ${Y_ts_plus_H} ${X_ts_plus_M} ${Y_ts_plus_M} ${X_ts_plus_L} ${Y_ts_plus_L} ${X_ts_0} ${Y_ts_0} ${start_date} ${end_date}

echo
echo ############################################
echo # mk_SSE_time-series_disp
echo ############################################
echo
python3 ${Path}sse_ts_slip.py ${SLC} ${move_rate} ${X_ts_minus_H} ${Y_ts_minus_H} ${X_ts_minus_M} ${Y_ts_minus_M} ${X_ts_minus_L} ${Y_ts_minus_L} ${X_ts_plus_H} ${Y_ts_plus_H} ${X_ts_plus_M} ${Y_ts_plus_M} ${X_ts_plus_L} ${Y_ts_plus_L} ${X_ts_0} ${Y_ts_0} ${start_date} ${end_date}

echo
echo ############################################
echo # LOS2d to LOS1d
echo ############################################
echo
python3 ${Path}mk_LOSts_list_ver2.py ${SLC} ${numX} ${numY} ${move_rate} ${start_date} ${end_date}

echo
echo ############################################
echo # disp2d to disp1d
echo ############################################
echo
python3 ${Path}mk_LOSslip_list.py ${SLC} ${numX} ${numY} ${move_rate} ${start_date} ${end_date}

echo
echo ############################################
echo # noise2d to noise1d
echo ############################################
echo
python3 ${Path}mk_noisets_list.py ${SLC} ${numX} ${numY} ${move_rate} ${start_date} ${end_date}


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





cd ${HOME}
