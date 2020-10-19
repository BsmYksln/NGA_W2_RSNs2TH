import requests
import os
import sys
import zipfile

#############################################################################################################
#### This script meant to download the chromedriver.exe for web automation purposes with selenium python ####
#### PS.: For now only working in windows!!!															 ####
#### 	  It is going to download it to the "\Lib\site-packages"				Besim Yukselen			 ####
#############################################################################################################

def download_url(url, save_path, chunk_size=128):
	r = requests.get(url, stream=True)
	with open(save_path, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=chunk_size):
			fd.write(chunk)

def find_latest_ver():
	r = requests.get('https://chromedriver.chromium.org/')
	a = r.text
	start = a.find('Latest stable release:')
	text = a.replace(a[0:start],'')
	start = text.find('path=')

	text = text.replace(text[0:start+5],'')
	end = text.find("/")
	latest_ver = text.replace(text[end::],'')
	return latest_ver

def add_driver_to_the_PATH(save_path):
	paths = sys.path
	site_package = [i for i in paths if 'lib\\site-packages' in i][0]
	with zipfile.ZipFile(save_path, 'r') as zip_ref:
		zip_ref.extractall(site_package)	

def seek_and_download():
	paths = sys.path
	site_package = [i for i in paths if 'lib\\site-packages' in i][0]
	if 'chromedriver.exe' not in os.listdir(site_package):
		latest_ver = find_latest_ver()
		save_path = f'{os.getcwd()}\\chromedriver.zip'
		url = f"https://chromedriver.storage.googleapis.com/{latest_ver}/chromedriver_win32.zip"
		download_url(url, save_path, chunk_size=128)
		add_driver_to_the_PATH(save_path)
		print ('chromedriver.exe downloaded successfully!!')
	else:
		print("chromedriver.exe allready exists!!")
seek_and_download()