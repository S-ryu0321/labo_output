import sys

num = int(sys.argv[1])

f = open('/home/sakurai/hdd2/sim_anom-detect/script/sim_num.txt', mode='w', encoding='utf-8', newline='\n')

for i in range(num):
	f.write(str(i+1)+'\n')

f.close()
