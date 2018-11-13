
import os
import sys
import re
import string

def get_fmt_in_line(path_handle,fmt):
	if type (path_handle) == str :
		handle = open(path_handle,'r')
	else :
		handle = path_handle
	lines = handle.readlines()
	handle.seek(0)
	for line in lines:
		if fmt in line:
			if type (path_handle) == str :
				handle.close()
			line = line[:-1]
			return line
	if type (path_handle) == str :
		handle.close()
	return 0

def get_match_define(path_handle, allstr, check_independdet = 1, check_only = 1,check_notes = 1):

	if type (path_handle) == str :
		handle = open(path_handle,'r')
	else :
		handle = path_handle

	lines = handle.readlines()
	handle.seek(0)
	result = []
	local = []
	on_notes = 0;
	notesend_local = -1
	local_out1 = -1
	local_out2 = -1

	for line in lines:
		del local[:]
		#in notes
		if 1 == on_notes :
			notesend_local = line.strip().find("*/")
			if notesend_local < 0:
				continue 
			else:
				if notesend_local+2 == len(line.strip()) : # it is line end
					on_notes = 0;
					continue
				else:
					on_notes = 0;

		for string in allstr:
			local.append(line.find(string))
		sumlocal = sum(local) + len(local) - 1

		if sumlocal >=0 :
			if 1 == check_notes : 
				local_out1 = line.find("//")
				local_out2 = line.find("/*")
				# due notes
				if local_out2 >=0 :
					if line.find("*/") < local_out2 :
						on_notes = 1;

			i = 0;
			while i < len(local) :
				# the local must exist
				if local[i] > 0 and \
					( not ((local_out1 >=0 and local_out1 < local[i]) or \
					(local_out2 >=0 and local_out2 < local[i]) or \
					(notesend_local >=0 and local[i] < notesend_local)
					)) :

					# make sure it is a independent string
					if (not check_independdet) or ( \
						(line[local[i] - 1].isspace() or local[i] - 1 == 0 ) and \
						line[local[i] + len(allstr[i])].isspace()) :

						# Avoid duplicate preservation
						if (not check_only) or (not (line in result)):
							result.append(line[:-1])
				i = i+1

	if type (path_handle) == str :
		handle.close()
	return result

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
platform = get_fmt_in_line(defconfig_handle,"CONFIG_BUILD_ARM_APPENDED_DTB_IMAGE_NAMES")
if platform != 0:
	platform = platform.strip()
	platform = platform[platform.index('=') + 1:]
	platform = platform.strip("\"")
else :
	print("No platform info !!")

k_platform = get_fmt_in_line(defconfig_handle,"CONFIG_BUILD_ARM_DTB_OVERLAY_IMAGE_NAMES")
if k_platform != 0:
	k_platform = k_platform.strip()
	k_platform = k_platform[k_platform.index('=') + 1:]
	k_platform = k_platform.strip("\"")
else :
	print("No k_platform info !!")

# check charging current************************************************************

mt_charging_path = "kernel-3.18/drivers/misc/mediatek/include/mt-plat/" + platform + \
					"/include/mach/mt_charging.h"

find_str = ["AC_CHARGER_CURRENT","USB_CHARGER_CURRENT","NON_STD_AC_CHARGER_CURRENT",\
			"RECHARGING_VOLTAGE","MAX_CHARGE_TEMPERATURE",\
			"MAX_CHARGE_TEMPERATURE_MINUS_X_DEGREE","MIN_CHARGE_TEMPERATURE",\
			"MIN_CHARGE_TEMPERATURE_PLUS_X_DEGREE",\
			"V_CHARGER_MAX","V_CHARGER_MIN"]

mt_charging_result = get_match_define(mt_charging_path,find_str)

for r in mt_charging_result:
	print(r)
#flash*********************************************************************************

flash_path = "vendor/mediatek/proprietary/bootable/bootloader/preloader/custom/" + \
			k_platform + "/inc/custom_MemoryDevice.h"

flash_result =  get_match_define(flash_path,['CS_PART_NUMBER'],0,0)

for r in flash_result:
	print(r)
#vibrator*********************************************************************************

vibrator_path = "kernel-3.18/arch/arm/boot/dts/" + k_platform + ".dts"

vibrator_result = get_fmt_in_line(vibrator_path,"vib_vol")

print(vibrator_result)
#zsd*************************************************************************************

subcamera_path = get_fmt_in_line(Pjconfig_handle,"CUSTOM_KERNEL_SUB_IMGSENSOR =")

subcamera_path = subcamera_path[subcamera_path.find("=") + 1 :].strip()

subcamera_path = "vendor/mediatek/proprietary/custom/" + platform + \
		"/hal/sendepfeature/" + subcamera_path + "/config.ftbl." + subcamera_path + ".h"

subcamera_handle = open(subcamera_path,'r')

subcamera_lines = subcamera_handle.readlines()

i = 0
while i < len(subcamera_lines) and not ("KEY_ZSD_MODE" in subcamera_lines[i]) :
	i = i + 1;

if i == len(subcamera_lines) : 
	print("No zsd setting")

subcamera_result = []
while i < len(subcamera_lines):
	if "ITEM_AS_DEFAULT_" in subcamera_lines[i]:
		subcamera_result.append(subcamera_lines[i][:-1])
		break
	subcamera_result.append(subcamera_lines[i][:-1])
	i = i + 1

subcamera_handle.close() 

for r in subcamera_result:
	print(r)
#lcd**************************************************************************************

lcm_list = get_fmt_in_line(sagereal + "/mk/" + project_name +"/" + k_platform + ".mk",\
			"CUSTOM_LK_LCM =")

lcm_list = (lcm_list[lcm_list.find("\"") + 1: \
			lcm_list.find("\"",lcm_list.find("\"") + 1)]).strip().split()

lcm_path_list=[]
for templist in lcm_list:
	lcm_path_list.append("kernel-3.18/drivers/misc/mediatek/lcm/" + templist +\
			"/" + templist + ".c");

lcm_result_list = []
temp_result = []
for temppath in lcm_path_list :
	del temp_result[:]
	temp_result = get_match_define(temppath,["params->dsi.lcm_esd_check_table"],0)
	lcm_result_list.append(temp_result)

for r in lcm_result_list:
	for r1 in r:
		print(r1)

#vgp************************************************************************************

vgp_config_result = get_match_define(defconfig_handle,["CONFIG_MTK_RF_VGP"],0,0)

pmic_path = "kernel-3.18/drivers/misc/mediatek/power/" + platform + "/pmic.c"

pmic_handle = open(pmic_path,'r')
pmic_lines = pmic_handle.readlines()

i = 0
pmic_result = []
while i < len(pmic_lines) :
	if "CONFIG_MTK_RF_VGP" in pmic_lines[i] :
		while i < len(pmic_lines) :
			pmic_result.append(pmic_lines[i][:-1])
			if "#endif" in pmic_lines[i] :
				break
			i = i + 1
	i = i + 1

pmic_handle.close()

for r in pmic_result:
	print(r)

#ntc*************************************************************************************

ntc_path = "kernel-3.18/drivers/misc/mediatek/include/mt-plat/" + platform + \
			"/include/mach/mt_battery_meter_table.h"

BAT_NTC_10_times = 0;
BAT_NTC_47_times = 0;

ntc_handle = open(ntc_path,'r')
ntc_lines = ntc_handle.readlines()

i = 0
ntc_result = []
while i < len(ntc_lines) :
	if "BAT_NTC_10" in ntc_lines[i] :
		if 0 == BAT_NTC_10_times :
			ntc_result.append(ntc_lines[i][:-1])
			i = i + 1
			BAT_NTC_10_times = BAT_NTC_10_times + 1;
		elif 1 == BAT_NTC_10_times :
			while i < len(ntc_lines):
				ntc_result.append(ntc_lines[i][:-1])
				if "#endif" in ntc_lines[i] :
					break
				i +=1
			BAT_NTC_10_times = BAT_NTC_10_times + 1;
	#*****
	if "BAT_NTC_47" in ntc_lines[i] :
		if 0 == BAT_NTC_47_times :
			ntc_result.append(ntc_lines[i][:-1])
			i = i + 1
			BAT_NTC_47_times = BAT_NTC_47_times + 1;
		elif 1 == BAT_NTC_47_times :
			while i < len(ntc_lines):
				ntc_result.append(ntc_lines[i][:-1])
				if "#endif" in ntc_lines[i] :
					break
				i +=1
			BAT_NTC_47_times = BAT_NTC_47_times + 1;
	i +=1

for r in ntc_result:
	print(r)