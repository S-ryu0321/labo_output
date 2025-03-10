### load python mpdules ###
print('### load python mpdules ###')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ctypes import *
import os
import sys
from pyproj import Proj
# original module
sys.path.append('./module/')
import rotate_fault
import udisp2enu
import cal_Mw
import cal_LOS
import cal_UTM_zone

#####par#####
sim_num =50

numX = 190
numY = 150

start_date = '2018-1-1'
end_date = '2019-11-18'
#########sim_dip_0###############







### constant parameters ###
nu = 6.0 * 1e10   # Lame's second constant [Pa] (basically 5*1e10 ~ 7*1e10)
# value of nu is derived from 
# "http://www.kyoshin.bosai.go.jp/kyoshin/gk/publication/1/I-5.1.4.html"
# (2018/08/09)
c = 299792458.0   # speed of light [m/s]


### file IO parameters ###
libdir = './lib/'
figdir = './fig/'
os.system('mkdir -p '+figdir)

### parameter setting for fault modeling ###
dlon = 0.01   # [degree], grid interval in EW direction
dlat = 0.01   # [degree], grid interval in NS direction
lon = np.arange(139.5, 141.399, dlon)   # area extent in EW
lat = np.arange(34.5, 36.0, dlat)   # area extent in NS
cornerlon = 140.5   # corner lon for fault
cornerlat = 35.2   # corner lon for fault
zone = cal_UTM_zone.UTMzone(cornerlon, cornerlat)    # UTM zone
z = -0.1   # [m], not changed
depth = 15000.0   # [m], source depth at the corner coordinate
dip = 60   # [degree], dip angle
strike_angle = 90.0   # [degree], direction angle of fault plane
alpha = 2.0 / 3.0   # from original Okada fault model manual
L = 60000.0   # [m], fault length along strike direction
W = 40000.0   # [m], fault width along dip direction
slip = 0.0   # [m], slip amount
rake = 90.0   # [degree], slip direction, anti-clockwise from right
'''
disl1 = 0.0   # [m], strike slip component
disl2 = -1.0   # [m], dip slip component
# disl1 and 2 can be calculated by "slip" and "rake" parameters
'''
disl3 = 0.0   # [m], tensile opening component (0 for EQ fault)


### parameter setting for InSAR data ###
cfreq = 5.6 * 1e9   # radar frequency on Sentinel-1 [Hz]
wl = c / cfreq   # radar wavelength [m]
inc_angle = 40.0   # scene-average incident angle [deg]
heading = -10.0   # satellite heading angle (deg, clockwise from north)
sensor_direc = 90.0   # right: +90 deg,   left: -90 deg



### calc some parameters for DC3D ###
disl1 = slip * np.cos(rake * 2.0 * np.pi / 360.0)
disl2 = slip * np.sin(rake * 2.0 * np.pi / 360.0)
al1 = 0.0
al2 = L
aw1 = W * (-1.0)
aw2 = 0.0
lam = nu * (1.0 - 2.0 * alpha) / (alpha - 1.0)   # Lame's first constant [Pa]


### load fortran library ###
print('### load fortran library ###')
dc3d = np.ctypeslib.load_library(libdir+'DC3Dfortran.so', '.')
dc3d.okada1992.argtypes = [np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32), \
   np.ctypeslib.ndpointer(dtype=np.float32), np.ctypeslib.ndpointer(dtype=np.float32)]


### prepare xyz coordinate (lonlat => UTM) ###
print('### prepare xyz coordinate (lonlat => UTM) ###')
converter = Proj(proj='utm', zone=zone, ellps='WGS84')
LON, LAT = np.meshgrid(lon, lat)   # make 2D lon lat arrays
print('shape of LON, LAT:   ', np.shape(LON))
sl = np.shape(LON)
LON1 = LON.reshape([sl[0]*sl[1], 1])
LAT1 = LAT.reshape([sl[0]*sl[1], 1])
utmx1, utmy1 = converter(LON1, LAT1)   # make UTM coordinates
utmx = utmx1.reshape([sl[0], sl[1]])   # reshape 1D to 2D
utmy = utmy1.reshape([sl[0], sl[1]])   # reshape 1D to 2D
cornerX, cornerY = converter(cornerlon, cornerlat)   # UTM coordinate for fault corner location
print('fault_corner_location:   ', cornerX, cornerY)


### rotate coordinate ###
print('### rotate coordinate ###')
X0, Y0 = rotate_fault.rotate_fault(utmx-cornerX, utmy-cornerY, strike_angle)   # for DC3D calculation, lon, lat coordinates are rotated to fault-referenced coordinate
X1, Y1 = rotate_fault.rotate_fault_rev(utmx-cornerX, utmy-cornerY, strike_angle)   # same as above code, but for result projection


### array preparation ###
print('### array preparation ###')
ss = np.shape(LON)
ux = np.zeros(ss)
uy = np.zeros(ss)
uz = np.zeros(ss)
uxx = np.zeros(ss)
uyx = np.zeros(ss)
uzx = np.zeros(ss)
uxy = np.zeros(ss)
uyy = np.zeros(ss)
uzy = np.zeros(ss)
uxz = np.zeros(ss)
uyz = np.zeros(ss)
uzz = np.zeros(ss)
iret = np.zeros(ss)


### calculate displacement ###
print('### calculate displacement (DC3D) ###')
for i in range(ss[0]):
	for j in range(ss[1]):
		xx = np.array(X0[i, j], dtype=np.float32)
		yy = np.array(Y0[i, j], dtype=np.float32)
		zz = np.array(z, dtype=np.float32)
		ddepth = np.array(depth, dtype=np.float32)
		ddip = np.array(dip, dtype=np.float32)
		aalpha = np.array(alpha, dtype=np.float32)
		aal1 = np.array(al1, dtype=np.float32)
		aal2 = np.array(al2, dtype=np.float32)
		aaw1 = np.array(aw1, dtype=np.float32)
		aaw2 = np.array(aw2, dtype=np.float32)
		ddisl1 = np.array(disl1, dtype=np.float32)
		ddisl2 = np.array(disl2, dtype=np.float32)
		ddisl3 = np.array(disl3, dtype=np.float32)
		uux = np.array(0.0, dtype=np.float32)
		uuy = np.array(0.0, dtype=np.float32)
		uuz = np.array(0.0, dtype=np.float32)
		uuxx = np.array(0.0, dtype=np.float32)
		uuyx = np.array(0.0, dtype=np.float32)
		uuzx = np.array(0.0, dtype=np.float32)
		uuxy = np.array(0.0, dtype=np.float32)
		uuyy = np.array(0.0, dtype=np.float32)
		uuzy = np.array(0.0, dtype=np.float32)
		uuxz = np.array(0.0, dtype=np.float32)
		uuyz = np.array(0.0, dtype=np.float32)
		uuzz = np.array(0.0, dtype=np.float32)
		iiret = np.array(0.0, dtype=np.float32)
		dc3d.okada1992(aalpha, xx, yy, zz, ddepth, ddip, aal1, aal2, aaw1, aaw2, \
		   ddisl1, ddisl2, ddisl3, uux, uuy, uuz, uuxx, uuyx, uuzx, uuxy, uuyy, uuzy, uuxz, uuyz, uuzz, iiret)
		ux[i,j] = uux   # eastward displacement (m)
		uy[i,j] = uuy   # northward displacement (m)
		uz[i,j] = uuz   # upward displacement (m)

### [ux, uy, uz] ==> [disp_ew, disp_ns, disp_ud] ###
#rx, ry, rz = 
d_ew, d_ns, d_ud = udisp2enu.udisp2enu(ux, uy, uz, strike_angle)

### calc LOS displacement ###
print('### calc LOS displacement ###')
inc_map = np.ones(ss) * inc_angle
look_map = np.ones(ss) * (90.0 - heading)
LOS = cal_LOS.cal_LOS(d_ew, d_ns, d_ud, inc_map, look_map)   # (m)
unw = LOS / wl * 2.0 * np.pi   # (rad)
# phase re-wrap
phs = (unw + np.pi) % (2 * np.pi) - np.pi   # (rad)

###LOS(m)>>(cm)
LOS = LOS * 100



### calc Mw (moment magnitude) ###
print('### calc Mw ###')
M0, Mw = cal_Mw.cal_Mw(nu, slip, L, W)
print('')
print('seismic moment :   {:.5e} [N m]'.format(M0))
print('moment magnitude :   %f [N m]'   % Mw)
print('')



### make figure ###
print('### make figure ###')
# fault geometry
refx1, refy1 = rotate_fault.rotate_fault_rev_scalar(0, 0, strike_angle)
refx2, refy2 = rotate_fault.rotate_fault_rev_scalar(L, 0, strike_angle)
refx3, refy3 = rotate_fault.rotate_fault_rev_scalar(L, -W*np.cos(dip*2.0*np.pi/360.0), strike_angle)
refx4, refy4 = rotate_fault.rotate_fault_rev_scalar(0, -W*np.cos(dip*2.0*np.pi/360.0), strike_angle)
refx1 = refx1+cornerX
refx2 = refx2+cornerX
refx3 = refx3+cornerX
refx4 = refx4+cornerX
refy1 = refy1+cornerY
refy2 = refy2+cornerY
refy3 = refy3+cornerY
refy4 = refy4+cornerY
refx1l, refy1l = converter(refx1, refy1, inverse=True)
refx2l, refy2l = converter(refx2, refy2, inverse=True)
refx3l, refy3l = converter(refx3, refy3, inverse=True)
refx4l, refy4l = converter(refx4, refy4, inverse=True)



### tskm label 1d to 2d(numX*numY) ###
###label 1d to 2d(190*150)###
label_tskm = pd.read_csv('./TSKM_clustering_labels.csv', header=None)
label_tskm = np.array(label_tskm)
label_tskm_2d = label_tskm.reshape(numY, numX)
print(len(label_tskm_2d))
print(len(label_tskm_2d[0]))

### plot LOS displacement ###
plt.figure(1)
cs = plt.pcolormesh(utmx, utmy, label_tskm_2d, cmap='jet', zorder=0, alpha=1)
plt.plot([refx1, refx2], [refy1, refy2], 'k', linewidth=3, zorder=5)
plt.plot([refx2, refx3, refx4, refx1], [refy2, refy3, refy4, refy1], 'k', linewidth=1, zorder=5)
plt.plot()
plt.title('time-series k-means clustering map', fontsize=16)
plt.xlim([np.amin(utmx), np.amax(utmx)])
plt.ylim([np.amin(utmy), np.amax(utmy)])
plt.savefig('time-series_k-means_clustering_2d.png', format='png', dpi=200)


