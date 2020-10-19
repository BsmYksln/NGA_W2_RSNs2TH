import os
import time

def dir_size(Down_Dir):
	total_size = 0
	for path, dirs, files in os.walk(Down_Dir):
		for f in files:
			fp = os.path.join(path, f)
			total_size += os.path.getsize(fp)
	return total_size

def download_wait(Down_Dir):
	delta_size = 100
	flag = 0
	flag_lim = 5
	while delta_size > 0 and flag < flag_lim:
		print
		size_0 = dir_size(Down_Dir)
		time.sleep(6)
		size_1 = dir_size(Down_Dir)
		if size_1-size_0 > 0:
			delta_size = size_1-size_0
		else:
			flag += 1
			print(flag_lim-flag)
	print(f'Download has done to the directory:\n{Down_Dir}')
