import requests
import os
import sys
import zipfile

#############################################################################################################
#### This script meant to download the chromedriver.exe for web automation purposes with selenium python ####
#### PS.: This code has been tested only on Windows OS!!!												 ####
#### 	  It is going to download it to the "...\Lib\..."						Besim Yukselen			 ####
#############################################################################################################

def download_url(url, save_path, chunk_size=128):
	"""	

	Details
	-------	

	This function downloads file from given url.Herein, it is being used 	

	Parameters
	----------
	url          : str
	        e.g.: 'www.example.com/example_file.pdf'
	save_path    : str
	        Save directory.	

	"""
	r = requests.get(url, stream=True)
	with open(save_path, 'wb') as fd:
		for chunk in r.iter_content(chunk_size=chunk_size):
			fd.write(chunk)

def find_latest_ver():
	"""
	
	Details
	-------
	
	This function finds the latest version of the chrome driver from  
	'https://chromedriver.chromium.org/'.
	
	"""

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
	package = [i for i in paths if 'lib' in i][0]
	with zipfile.ZipFile(save_path, 'r') as zip_ref:
		zip_ref.extractall(package)	

def seek_and_download():
	"""
	
	Details
	-------
            
	This function finds the latest version of the chrome driver from  
	'https://chromedriver.chromium.org/' and downloads the compatible
	version to the OS and extract it to the path.

	"""
	paths = sys.path
	package = [i for i in paths if 'lib' in i][0]
	if 'win' in sys.platform:
		current_platform = 'win32'
		aim_driver = 'chromedriver.exe'
	elif 'linux' in sys.platform:
		current_platform = 'linux64'
		aim_driver = 'chromedriver'
	else:		
		current_platform = 'mac64'
		aim_driver = 'chromedriver'
	if aim_driver not in os.listdir(package):
		latest_ver = find_latest_ver()
		save_path = os.path.join(os.getcwd().'chromedriver.zip')
		url = f"https://chromedriver.storage.googleapis.com/{latest_ver}/chromedriver_{current_platform}.zip"
		download_url(url, save_path, chunk_size=128)
		add_driver_to_the_PATH(save_path)
		print ('chromedriver downloaded successfully!!')
		os.remove(save_path)
	else:
		print("chromedriver allready exists!!")
seek_and_download()