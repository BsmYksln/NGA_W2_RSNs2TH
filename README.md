# NGA-West2-RSNs-2-TH
This library has been created as a web automation tool in order to download unscaled record time histories from NGA-West2 Database (https://ngawest2.berkeley.edu/) by their Record Sequence Numbers (RSNs).

Directories and Files:
----------------------
	
	|===>	'\\local_configs'
	|		|
	|		|===>	'User_Config.conf' : This file contains the peer account information.
	|		|			   [In first run it might not be exists.If so, please continue with, function 'add_new_user' from user_configurations.py]
	|		|			   !!!! Note that conf file stores the data as basic encoding system please do not obey on this security. !!!!
	|		|
	|		|===>	'install_chromedriver.py' : Install and add the "chromedriver.exe" to the "...\Lib\site-packages" path.
	|		|
	|		|===>	'utilities.py' : '.py' script contains a function which controls the download.
	|		|
	|		|===>	'user_configurations.py' :	'.py' script contains functions to read or add existing user and find the credentials of existing user.
	|											
	|
	|===>	'NGA_W2_RSN_2_TH.py' : It is the main script for downloading the RSNs with given credentials
	|
	|===>	'Example.py' : It is an example which uses all utilities to download given TH according to RSNs
