
import os
import sys
import re
import string

def get_match_lines(handle,fmt):
	lines = handle.readlines()
	handle.seek(0)
	for line in lines:
		if fmt in line:
			return line
	return 0

#************************************************************************
if 4 != len( sys.argv ):
	print("Number of parameter")
	exit(0)

repertory_path = sys.argv[1]
project_name = sys.argv[2]
file_save_path = sys.argv[3]

project_path = repertory_path + '/' + 'sagereal' + '/' + 'mk' + '/' + project_name
# to become Absolute path
os.path.abspath(repertory_path)
os.path.abspath(file_save_path)

alps = repertory_path + '/' + 'alps'
sagereal = repertory_path + '/' + 'sagereal'

# check 
if False == os.path.exists(repertory_path) \
	or False == os.path.exists(project_path) \
	or False == os.path.exists(file_save_path) :
	print("Invalid directory entered");
	exit()

#change dir and clone
os.chdir(alps) 
#print("./mk " + project_name + " clone")
#os.system("echo \"y\" | " + "./mk " + project_name + " clone")

# lao!! get all infomation

# get key info************************************************************************

files = os.listdir(project_path)

for filename in files:
	if "full" in filename :
		full_file = project_path + '/' + filename
	elif "debug_defconfig" in filename :
		debug_deconfig_file = project_path + '/' + filename
	elif "defconfig"in filename :
		defconfig_file = project_path + '/' + filename
	elif "preloader" in filename or "pl" in filename:
		pr_mk = project_path + '/' + filename
	elif "ProjectConfig" in filename:
		Pjconfig_name = project_path + '/' + filename	
#print(files) open file
savefile_handle = open(file_save_path + "checklist_file" , 'w')
defconfig_handle = open(defconfig_file,'r')
Pjconfig_handle = open(Pjconfig_name,'r')
#get platform************************************************************************
'''
lines = defconfig_handle.readlines()

for line in lines:
	if "CONFIG_BUILD_ARM_APPENDED_DTB_IMAGE_NAMES" in line :
		platform = line[line.index('=') + 2 : -2]
	elif "CONFIG_BUILD_ARM_DTB_OVERLAY_IMAGE_NAMES" in line :
 		k_platform = line[line.index('=') + 2 : -2]
'''
platform = get_match_lines(defconfig_handle,"CONFIG_BUILD_ARM_APPENDED_DTB_IMAGE_NAMES")
if platform != 0:
	platform = platform[platform.index('=') + 2:-2]
else :
	print("No platform info !!")

k_platform = get_match_lines(defconfig_handle,"CONFIG_BUILD_ARM_DTB_OVERLAY_IMAGE_NAMES")
if k_platform != 0:
	k_platform = k_platform[k_platform.index('=') + 2:-2]
else :
	print("No k_platform info !!")

# check charging current************************************************************

mt_charging_path = "kernel-3.18/drivers/misc/mediatek/include/mt-plat/" + platform + \
					"/include/mach/mt_charging.h"

mt_charging_handle = open(mt_charging_path,'r')

lines = mt_charging_handle.readlines()
mt_charging_handle.seek(0)


'''
for line in line"AC_CHARGER_CURRENT")
	local2 = line.find("USB_CHARGER_CURRENT")
	local3 = line.find("NON_STD_AC_CHARGER_CURRENT")
	local = local1 + local2 + local3 + 2
	if local >=0 :
		local_out1 = line.find("//")
		local_out2 = line.find("/*")
		if not ((local_out1 >=0 and local_out1 < local) or \
			( local_out2 >=0 and local_out2 < local)) :
			if local1 >= 0 and line[local1 - 1].isspace() and \
				line[local1 + len("AC_CHARGER_CURRENT")].isspace() :
				AC_CHARGER = line
			elif local2 >= 0 and line[local2 - 1].isspace() and \
				line[local2 + len("USB_CHARGER_CURRENT")].isspace() :
				USB_CHARGER = line
			elif local3 >= 0 and line[local3 - 1].isspace() and \
				line[local3 + len("NON_STD_AC_CHARGER_CURRENT")].isspace() :
				NON_STD_AC_CHARGER = line
		
print(AC_CHARGER)
print(USB_CHARGER)
print(NON_STD_AC_CHARGER)
'''

local = []
find_str = ["AC_CHARGER_CURRENT","USB_CHARGER_CURRENT","NON_STD_AC_CHARGER_CURRENT"]
result = []

for line in lines:
	del local[:]
	for string in find_str:
		local.append(line.find(string))
	sumlocal = sum(local) + len(local) - 1
	if sumlocal >=0 :
		local_out1 = line.find("//")
		local_out2 = line.find("/*")
		if not ((local_out1 >=0 and local_out1 < sumlocal) or \
			( local_out2 >=0 and local_out2 < sumlocal)) :
			for i in local:
				if i > 0 and line[i - 1].isspace() and \
					line[i + len(find_str[local.index(i)])].isspace() :
					result.append(line)

for r in result:
	print(r)

#os.system("subl " + mt_charging_path)

