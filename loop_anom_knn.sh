#!/bin/bash

# ${home} should be set at InSAR data directory
#home=/home/sakurai/hdd2/18-2900/interf/
#cd ${home}

Home=/home/sakurai/hdd2/sim_anom-detect/sim/
Path=/home/sakurai/hdd2/sim_anom-detect/script/


###sim_par###
sim_num=100
atm_mean=3
atm_std=1
atm_amp=5
slc=50
start_date='2018-1-1'
end_date='2019-11-18'
move_rate=0.5


###ML_par###
num_train=20
num_test=30
width=5
nk=1
MA=3





###make sim_num.txt###
python3 ${Path}mk_sim-num.py ${sim_num}

###loop###
cat ${Path}slip_amp_ls.txt | while read hoge
do
	slip_amp=`echo ${hoge}`
	echo
	echo "######################################"
	echo "               ${slip_amp}            "
	echo "######################################"
	echo
	cd ${Home}slip${slip_amp}-atmamp${atm_amp}_sim${sim_num}_SLC${slc}_rate${move_rate}/
	cat ${Path}sim_num.txt | while read line
	do
		#echo ${line}
		num=`echo ${line}`
		echo
		echo "######################################"
		echo "               ${num}                 "
		echo "######################################"
		echo
		
		bash ${Path}anomaly_detection_knn.sh ${sim_num} ${num} ${slip_amp} ${num_train} ${num_test} ${width} ${nk} ${MA}
	done
	cd ${Home}
done

cd ${Path}


