#!/bin/bash

# ${home} should be set at InSAR data directory
#home=/home/sakurai/hdd2/18-2900/interf/
#cd ${home}

Home=/home/sakurai/hdd2/sim_anom-detect/anom-map/
Path=/home/sakurai/hdd2/sim_anom-detect/script/

sim_num=20

slip_amp=0.07
atm_mean=3
atm_std=1
atm_amp=5

num_train=20
num_test=30

mkdir -p ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/
cd ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/
mkdir -p ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/all/
mkdir -p ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/all/anom/

###make sim_num.txt###
python3 ${Path}mk_sim-num.py ${sim_num}



cat ${Path}sim_num.txt | while read line
do
	#echo ${line}
	num=`echo ${line}`
	echo
	echo "######################################"
	echo "               ${num}                 "
	echo "######################################"
	echo
	
	mkdir -p ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/
	bash ${Path}mk_timeseries-map_anom-map.sh ${slip_amp} ${atm_mean} ${atm_std} ${atm_amp} ${sim_num} ${num} ${num_train} ${num_test}
	
	#cd ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/${num}/
	#python3 ${Path}1pixel
	
done

cd ${Path}

mkdir -p ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/all/
cd ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/all/
#mkdir -p ${Home}/slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_train${num_train}/all/



