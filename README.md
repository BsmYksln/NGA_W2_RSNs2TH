# NGA_W2_RSNs2TH
This module has been created as a web automation tool in order to download unscaled record time histories from NGA-West2 Database (https://ngawest2.berkeley.edu/) by Record Sequence Numbers (RSNs).

Files:
----------------------
	
	|===>	'NGA_W2_RSNs2TH.py' : It is the main script for downloading the ground motion records of indicated RSNs with given credentials.
	|
	|===>	'Example.py' : It is an example which uses all utilities to download given TH according to RSNs.
	|
	|===>	'horizontal_RSNs.txt' : It is an example text file contains RSNs stored as comma-seperated (row-like) values.
	|
	|===>	'vertical_RSNs.txt' : It is an example text file contains RSNs in column-like order.

Required Libraries:
--------------------
	requests
	selenium
	
P.S.: This code only tested on Windows OS. However, it should be compatible with Windows, Linux, and Mac OS.
