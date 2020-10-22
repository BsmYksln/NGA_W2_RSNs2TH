import base64
import pickle as pkl
import os

def read_user_conf():
	cwd = os.getcwd()
	if 'local_configs' not in cwd:
		os.chdir(os.path.join(cwd,'local_configs'))
	with open('User_Config.conf', 'rb') as handle:
		USER_CONFIG_ENCODED = pkl.load(handle)
	USER_NAMES = [base64.b64decode(i[0]).decode('utf-8') for i in USER_CONFIG_ENCODED]
	PASSWORDS = [base64.b64decode(i[1]).decode('utf-8') for i in USER_CONFIG_ENCODED]
	ALL_CREDENTIALS = [(base64.b64decode(i[0]).decode('utf-8'),base64.b64decode(i[1]).decode('utf-8')) for i in USER_CONFIG_ENCODED]
	os.chdir(cwd)
	return USER_NAMES,PASSWORDS,ALL_CREDENTIALS


def add_new_user():
	cwd = os.getcwd()
	if 'local_configs' not in cwd:
		os.chdir(os.path.join(cwd,'local_configs'))
	NEW_USERNAME = input('username (email) : ')
	PASSWORD = input('Password : ')
	SAVE_CONFIG = input('Would you like to your credentials to be saved? (1/0): ')
	# I want to save the credentials for next time
	if SAVE_CONFIG == '1':
		NEW_USERNAME_ENCODED = base64.b64encode(NEW_USERNAME.encode("utf-8"))
		PASSWORD_ENCODED = base64.b64encode(PASSWORD.encode("utf-8"))
		if not os.path.exists('User_Config.conf'):
			CREDENTIALS = [(NEW_USERNAME_ENCODED,PASSWORD_ENCODED)]
			with open('User_Config.conf', 'wb') as f:
				pkl.dump(CREDENTIALS, f)
			f.close()
		else:
			_,_,ALL_CREDENTIALS = read_user_conf()
			ALL_CREDENTIALS_ENCODED = [(base64.b64encode(ALL_CREDENTIALS[i][0].encode("utf-8")),base64.b64encode(ALL_CREDENTIALS[i][1].encode("utf-8"))) for i in range(len(ALL_CREDENTIALS))]
			ALL_CREDENTIALS_ENCODED.append((NEW_USERNAME_ENCODED,PASSWORD_ENCODED))
			with open('User_Config.conf', 'wb') as f:
				pkl.dump(ALL_CREDENTIALS_ENCODED, f)
	os.chdir(cwd)
	return NEW_USERNAME, PASSWORD

def find_the_user(USER_NAMES,PASSWORDS):
	GIVEN_NAME = input('Please Insert Your Email: ' )
	try:
		# Find the credentials
		idx = [n for n, x in enumerate(USER_NAMES) if GIVEN_NAME == x][0]
		USERNAME = USER_NAMES[idx]
		PASSWORD = PASSWORDS[idx]
		print(PASSWORD)
	except:
		# if there is no
		print('!!! THERE IS NO EXISTING CREDENTIAL FOR GIVEN USERNAME !!!\n')
		print('!!! PLEASE PROVIDE NEW CREDENTIALS (1) OR TRY NEW USERNAME (0) !!!\n')
		Way2 = input('Selection: ')
		if Way2 == '1':
			# OK I'll give you new credentials
			USERNAME, PASSWORD = add_new_user()
		elif Way2 == '0':
			USERNAME = ''
			PASSWORD = ''
	return USERNAME, PASSWORD
