import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys

atm_mean = float(sys.argv[1])
atm_sigma = float(sys.argv[2])

disp = pd.read_csv("./LOS2m.csv", header=None)
disp = np.array(disp)

def amp_max(array):
	return np.max(array)

def amp_min(array):
	return np.min(array)

def diff_var(sig1, sig2):
	var1 = sig1 ** 2
	var2 = sig2 ** 2
	return 2 * var1

std_diff = np.sqrt(diff_var(atm_sigma, atm_sigma))
print(std_diff)

###atmnoise_amp###
amp_atm = atm_mean + 1.96*atm_sigma  #95%

###diffatmnoise_amp###
amp_diffatm = 1.96*std_diff

###signal###
plus_maxamp = abs(amp_max(disp))
minus_minamp = abs(amp_min(disp))

###S/N_atm##
snr_atm1_plus = plus_maxamp / amp_atm
snr_atm1_minus = minus_minamp / amp_atm

###S/N_atmdiff##
snr_atmdiff_plus = plus_maxamp / amp_diffatm
snr_atmdiff_minus = minus_minamp / amp_diffatm

print(f"LOS+変位の最大振幅:{plus_maxamp}")
print(f"LOS-変位の最大振幅:{minus_minamp}")
print(f"大気遅延量の最大振幅(95%点):{amp_atm}")
print(f"大気遅延差分振幅(95%点):{amp_diffatm}")
print(f"LOS+変位の最大振幅と大気遅延量の最大振幅(95%点)の比:{snr_atm1_plus}")
print(f"LOS-変位の最大振幅と大気遅延量の最大振幅(95%点)の比:{snr_atm1_minus}")
print(f"LOS+変位の最大振幅と大気遅延差分振幅(95%点)の比:{snr_atmdiff_plus}")
print(f"LOS-変位の最大振幅と大気遅延差分振幅(95%点)の比:{snr_atmdiff_minus}")


f = open('./SNR.txt', mode='w', encoding='utf-8', newline='\n')

f.write("LOS+変位の最大振幅:"+str(plus_maxamp)+'\n')
f.write("LOS-変位の最大振幅:"+str(minus_minamp)+'\n')
f.write("大気遅延量の最大振幅(95%点):"+str(amp_atm)+'\n')
f.write("大気遅延差分振幅(95%点):"+str(amp_diffatm)+'\n')
f.write("LOS+変位の最大振幅と大気遅延量の最大振幅(95%点)の比:"+str(snr_atm1_plus)+'\n')
f.write("LOS-変位の最大振幅と大気遅延量の最大振幅(95%点)の比:"+str(snr_atm1_minus)+'\n')
f.write("LOS+変位の最大振幅と大気遅延差分振幅(95%点)の比:"+str(snr_atmdiff_plus)+'\n')
f.write("LOS-変位の最大振幅と大気遅延差分振幅(95%点)の比:"+str(snr_atmdiff_minus)+'\n')


f.close()

