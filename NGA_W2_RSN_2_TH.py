from selenium import webdriver
import sys
import os
import time
import random
from local_configs.utilities import *

def go_to_sign_in_page(Download_Dir):
	"""
	
	Details
	-------
            
	This function starts the webdriver in headless mode and 
	opens the sign in page to 'https://ngawest2.berkeley.edu/'

	Parameters
	----------
	Download_Dir     : str
	        Directory for the output time histories to be downloaded

	"""
	ChromeOptions = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : Download_Dir}
	ChromeOptions.add_experimental_option("prefs",prefs)
	ChromeOptions.headless = True
	if 'win' in sys.platform:
		aim_driver = 'chromedriver.exe'
	elif 'linux' in sys.platform:
		aim_driver = 'chromedriver'
	else:       
		aim_driver = 'chromedriver'
	path_of_driver = os.path.join([i for i in sys.path if 'lib' in i][0] , aim_driver)
	if not os.path.exists(path_of_driver):
		print('Downloading the chromedriver!!')
		from local_configs import install_chromedriver
		install_chromedriver.seek_and_download()
	driver = webdriver.Chrome(executable_path = path_of_driver ,options=ChromeOptions)
	url_sign_in = 'https://ngawest2.berkeley.edu/users/sign_in'
	driver.get(url_sign_in)
	return driver

def sign_in_with_given_creds(driver,USERNAME,PASSWORD):
	"""
	
	Details
	-------
	
	This function signs in to 'https://ngawest2.berkeley.edu/' with
	given account credentials

	Parameters
	----------
	driver     : selenium webdriver object
	        Please use the driver have been generated as output of 
	        'go_to_sign_in_page' function
	USERNAME   : str
	        Account username (e-mail)
	                    e.g.: 'username@mail.com'
	PASSWORD   : str
	        Account password
	                    e.g.: 'password!12345' 
	"""
	print("Signing in with given account!...")
	driver.find_element_by_id('user_email').send_keys(USERNAME)
	driver.find_element_by_id('user_password').send_keys(PASSWORD)
	driver.find_element_by_id('user_submit').click()
	try:
		alert = driver.find_element_by_css_selector('p.alert')
		warn = alert.text
		print(warn)
	except:
		warn = ''
		pass
	return driver, warn

def Download_Given(RSNs,Download_Dir,driver):
	"""
	
	Details
	-------
	
	This function dowloads the time histories which have been indicated with their RSNs
	from 'https://ngawest2.berkeley.edu/'.

	Parameters
	----------
	RSNs     : str
	        A string variable contains RSNs to be downloaded which uses ',' as delimeter
	        between RNSs
	                    e.g.: '1,5,91,35,468'
	Download_Dir     : str
	        Directory for the output timehistories to be downloaded
	driver     : selenium webdriver object
	        Please use the driver have been generated as output of 
	        sign_in_with_given_creds' function

	"""
	url_get_record = 'https://ngawest2.berkeley.edu/spectras/new?sourceDb_flag=1'	
	print("Listing the Records!....")
	driver.get(url_get_record)
	driver.find_element_by_xpath("//button[@type='button']").submit()
	driver.find_element_by_id('search_search_nga_number').send_keys(RSNs)
	driver.find_element_by_xpath("//button[@type='button' and @onclick='uncheck_plot_selected();reset_selectedResult();OnSubmit();']").submit()
	note = driver.find_element_by_id('notice').text
	try:
		note = driver.find_element_by_id('notice').text 
	except:
		note = 'NO'
	if 'NO' in note:
		driver.quit()
		pass
	else:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
		time.sleep(random.randint(2,5))
		driver.find_element_by_xpath("//button[@type='button' and @onclick='getSelectedResult(true)']").click()
		print("Downloading the Records!...")
		obj = driver.switch_to.alert
		msg=obj.text
		print ("Alert shows following message: "+ msg )
		time.sleep(random.randint(8,16))
		obj.accept()		

		obj = driver.switch_to.alert
		msg=obj.text
		print ("Alert shows following message: "+ msg )
		time.sleep(random.randint(2,5))
		obj.accept()
		print("Downloading the Records!...")	
		download_wait(Download_Dir)
		driver.quit()

def RSN_2_TH(RSNs,DOWNLOAD_DIR,USERNAME,PASSWORD):
	"""
	
	Details
	-------
	
	This function combines all procedures to dowload the time histories
	which have been indicated with their RSNs 
	from 'https://ngawest2.berkeley.edu/' with given credentials

	Parameters
	----------
	RSNs    		: str
	        A string variable contains RSNs to be downloaded which uses ',' as delimeter
	        between RNSs
	                e.g.: '1,5,91,35,468'
	DOWNLOAD_DIR    : str
	        Directory for the output timehistories to be downloaded
	USERNAME     	:  str
            Account username (e-mail)
                    e.g.: 'username@mail.com'
	PASSWORD        : str
            Account password
                    e.g.: 'password!12345'
	"""
	driver = go_to_sign_in_page(DOWNLOAD_DIR)
	driver,warn = sign_in_with_given_creds(driver,USERNAME,PASSWORD)
	if str(warn) == 'Invalid email or password.':
		print(warn)
		driver.quit()
		sys.exit()
	else:
		Download_Given(RSNs,DOWNLOAD_DIR,driver)
