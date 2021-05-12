from NGA_W2_RSNs2TH import *

RSNs_txt = open("vertical_RSNs.txt", "r")
# RSNs_txt = open("horizontal_RSNs.txt", "r")

RSNs_lines = RSNs_txt.readlines()
if len(RSNs_lines) > 1:
    RSNs = [int(RSN) for RSN in RSNs_lines]
else:
    RSNs = [int(RSN) for RSN in RSNs_lines[0].split(',')]

usr = 'roledi1998@labebx.com'
pwd = '123456789'

NGA = NGA_W2_RSNs2TH(usr, pwd)
NGA.RSNs_2_TH(RSNs)
