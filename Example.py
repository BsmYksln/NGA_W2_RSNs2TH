import os
import numpy as np
from local_configs.user_configurations import *
from NGA_W2_RSN_2_TH import *

"""
Herein an example of use of NGA_W2_RSN_2_TH library 

"""

cwd = os.getcwd()
DOWNLOAD_DIR = os.getcwd()
local_dirs = os.listdir(f'{cwd}\\local_configs')

# Select User
# Check if there is a saved user data
if "User_Config.conf" not in local_dirs:
	# There is no!
	print('There is not any existing user!\nPlease provide user credentials\nInsert (1) to proceed with new credential data\nInsert (0) to exit')
	Way1 = input('Selection: ')
	if Way1 == '1' :
		# I want to continue with my credentials
		USERNAME, PASSWORD = add_new_user()
	elif Way1 == '0':
		print('Goodbye !!')
		sys.exit()
	"""
		To Do: Creating new peer account from the present code
	#elif Way1 = '2' (Which is create new account)

	"""
else:
	# If there is a conf file
	# Are you new or you knew?
	Way3 = input("A 'User_Config.conf' file has been found would you like to proceed (1) or you are new (2): ")
	if Way3 == '1':
		# Read the user names and ask for user name
		USER_NAMES,PASSWORDS,ALL_CREDENTIALS = read_user_conf()
		# find the user or let him give new credentials
		USERNAME = ''
		PASSWORD = ''
		while USERNAME == '' or PASSWORD == '':
			USERNAME, PASSWORD= find_the_user(USER_NAMES,PASSWORDS)
	elif Way3 == '2':
		USERNAME, PASSWORD = add_new_user()
	else:
		print('Undefined Selection !!!')
		sys.exit()
"""
	Herein, a range of RSNs have been generated according to input but it is easily can be changed according to ground motion selection algorithms

"""

START_RSN = int(input('Insert First RSN: '))
FINISH_RSN = int(input('Insert Last RSN: '))
RSN_NP = np.arange(START_RSN,FINISH_RSN)
RSN_LIST = list(RSN_NP)
RSNs = f'{str(RSN_LIST[0])}'
for i in range(1,len(RSN_LIST)):
	RSNs += f',{str(RSN_LIST[i])}'

RSN_2_TH(RSNs,DOWNLOAD_DIR,USERNAME,PASSWORD)

