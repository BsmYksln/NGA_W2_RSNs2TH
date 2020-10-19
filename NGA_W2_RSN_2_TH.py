from selenium import webdriver
import sys
import os
import time
import random
from local_configs.utilities import download_wait

def go_to_sign_in_page(Download_Dir):
	ChromeOptions = webdriver.ChromeOptions()
	prefs = {"download.default_directory" : Download_Dir}
	ChromeOptions.add_experimental_option("prefs",prefs)
	ChromeOptions.headless = True
	path_of_driver = [i for i in sys.path if 'lib\\site-packages' in i][0] + '\\chromedriver.exe'
	if not os.path.exists(path_of_driver):
		print('Downloading the chromedriver!!')
		from local_configs import install_chromedriver
		install_chromedriver.seek_and_download()
	driver = webdriver.Chrome(executable_path = path_of_driver ,options=ChromeOptions)
	url_sign_in = 'https://ngawest2.berkeley.edu/users/sign_in'
	driver.get(url_sign_in)
	return driver

def sign_in_with_given_creds(driver,USERNAME,PASSWORD):
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
	# Go To NGA-WEST2 database
	url_get_record = 'https://ngawest2.berkeley.edu/spectras/new?sourceDb_flag=1'	
	print("Listing the Records!....")
	driver.get(url_get_record)
	driver.find_element_by_xpath("//button[@type='button']").submit()
	driver.find_element_by_id('search_search_nga_number').send_keys(RSNs)
	driver.find_element_by_xpath("//button[@type='button' and @onclick='uncheck_plot_selected();reset_selectedResult();OnSubmit();']").submit()
	note = driver.find_element_by_id('notice').text	
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
	driver = go_to_sign_in_page(DOWNLOAD_DIR)
	driver,warn = sign_in_with_given_creds(driver,USERNAME,PASSWORD)
	if str(warn) == 'Invalid email or password.':
		print(warn)
		driver.quit()
		sys.exit()
	else:
		Download_Given(RSNs,DOWNLOAD_DIR,driver)
