# python3 checklist A B C D
# A means repertory path
# B means project name
# C means checklist.xls path
# D means hardword.xls path 


import os
import sys
import re
import string
import xlwt
import xlrd

#**************************************************************************************
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

	if str == type(allstr) :
		allstr = [allstr]

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

def string_get_after_eq(str, remove_quotation = 0, cleanspace = 1) :
	restr = (str.strip())[str.index('=') + 1:]
	if 1 == remove_quotation :
		restr = restr.strip().strip("\"")
	if 1 == cleanspace :
		restr = restr.strip()
	return restr

#def list_match_fmt(list,fmt):
#	result = [for I in list if fmt in I]
#	return result

def display_file(path):
	print("\033[1m\033[31mfile local:\033[36m%s\033[0m"%(path))
	pass

def display_define_one(name, list, path) :
	print("\033[1m\033[31m%s\033[0m"%(name))
	display_file(path)
	print("\033[1m\033[33m---\033[0m")
	for l in list :
		print(l)
	print("\033[1m\033[33m----------------\033[0m\n")

def boundary():
	print("\033[1m\033[35m==========================================================\
=====================\033[0m")

#*****************************************************************************
if 3 >= len( sys.argv ):
	print("Number of parameter")
	exit(0)

repertory_path = sys.argv[1]
project_name = sys.argv[2]
save = 0
if 3 < len(sys.argv) :
	save = 1;
	file_save_path = sys.argv[3]

project_path = repertory_path + '/' + 'sagereal' + '/' + 'mk' + '/' + project_name
# to become Absolute path
os.path.abspath(repertory_path)
os.path.abspath(file_save_path)
# the model of checklist.xls is on same fold with checklist_code , The file_save_path only is a directory
# which is where want to save

alps = repertory_path + '/' + 'alps'
sagereal = repertory_path + '/' + 'sagereal'

# check 
if False == os.path.exists(repertory_path) \
	or False == os.path.exists(project_path) \
	or False == os.path.exists(file_save_path) :
	print("Invalid directory entered");
	exit()

#open model	checklist.xls
#checklist_fb = xlrd.open_workbook(filename="checkList.xls")
#change dir and clone
os.chdir(alps) 
#print("./mk " + project_name + " clone")
os.system("echo \"y\" | " + "./mk " + project_name + " clone")

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
	elif "ProjectConfig" in filename:
		Pjconfig_name = project_path + '/' + filename	
#print(files) open file

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
	platform = string_get_after_eq(platform,1)
else :
	print("No platform info !!")

k_platform = get_fmt_in_line(defconfig_handle,"CONFIG_BUILD_ARM_DTB_OVERLAY_IMAGE_NAMES")
if k_platform != 0:
	k_platform = string_get_after_eq(k_platform,1)
else :
	print("No k_platform info !!")

kernel_version = get_fmt_in_line(Pjconfig_handle,"LINUX_KERNEL_VERSION")
kernel_version = string_get_after_eq(kernel_version)

print("\033[1m\033[47;30m*******************checklist_code********************\033[0m")
print("platform :\033[1m\033[32m %s,%s \033[0m\n"%(platform,k_platform))

# develop info************************************************
'''
platform k_platform is mt6XXX and kXX...
path is based on alps

'''
# all driver ***********************************************************************
'''
ProjectConfig_find_str = ["CUSTOM_HAL_IMGSENSOR","CUSTOM_HAL_MAIN_IMGSENSOR",\
						  "CUSTOM_HAL_SUB_IMGSENSOR","CUSTOM_KERNEL_TOUCHPANEL"]

kernel_config_find_str = ["CONFIG_CUSTOM_KERNEL_IMGSENSOR","CONFIG_MTK_FLASHLIGHT",\
						  "CONFIG_CUSTOM_KERNEL_LCM","TOUCHSCREEN"]

all_config_list = get_match_define(Pjconfig_handle,ProjectConfig_find_str)
all_config_list.extend(get_match_define(defconfig_handle,kernel_config_find_str))

lcd_config_list = list_match_fmt(all_config_list,"LCM")

camera_config_list = ((list_match_fmt(all_config_list,"CAMERA")).extend(list_match_fmt(all_config_list,"imgsensor")))

touchscreen_config_list = list_match_fmt(all_config_list,"TOUCHSCREEN")

boundary()
 

boundary()
'''
# check charging current************************************************************

mt_charging_path = kernel_version + "/drivers/misc/mediatek/include/mt-plat/" + platform + \
					"/include/mach/mt_charging.h"

find_str = ["AC_CHARGER_CURRENT","USB_CHARGER_CURRENT","NON_STD_AC_CHARGER_CURRENT",\
			"RECHARGING_VOLTAGE","MAX_CHARGE_TEMPERATURE",\
			"MAX_CHARGE_TEMPERATURE_MINUS_X_DEGREE","MIN_CHARGE_TEMPERATURE",\
			"MIN_CHARGE_TEMPERATURE_PLUS_X_DEGREE",\
			"V_CHARGER_MAX","V_CHARGER_MIN"]

mt_charging_result = get_match_define(mt_charging_path,find_str)
# display

display_define_one("电池报警温度和过温回充:",mt_charging_result[:4],mt_charging_path)
display_define_one("电池复充电压:",mt_charging_result[4:5],mt_charging_path)
display_define_one("充电电流:",mt_charging_result[5:8],mt_charging_path)
display_define_one("高压充电报警:",mt_charging_result[8:11],mt_charging_path)
boundary()
#flash*********************************************************************************

flash_path = "vendor/mediatek/proprietary/bootable/bootloader/preloader/custom/" + \
			k_platform + "/inc/custom_MemoryDevice.h"

flash_result =  get_match_define(flash_path,['CS_PART_NUMBER'],0,0)

display_define_one("flash:",flash_result,flash_path)
#vibrator*********************************************************************************

vibrator_path = kernel_version + "/arch/arm/boot/dts/" + k_platform + ".dts"
vibrator_c_path = kernel_version + "/drivers/misc/mediatek/vibrator/" + platform + "/vibrator.c"

vibrator_seclect_info = []
vibrator_result = get_fmt_in_line(vibrator_path,"vib_vol")
vibrator_seclect_info.append(get_fmt_in_line(vibrator_c_path,"Output voltage select"))
vibrator_seclect_info.append(get_fmt_in_line(vibrator_c_path,"Voltage selection"))
vibrator_seclect_info.extend(get_match_define(vibrator_c_path,"3'b",0,0,0))

display_define_one("vibrator info :",vibrator_seclect_info,vibrator_path)
display_define_one("vibrator value:",[vibrator_result],vibrator_c_path)
boundary()
#zsd*************************************************************************************

subcamera_name = get_fmt_in_line(Pjconfig_handle,"CUSTOM_KERNEL_SUB_IMGSENSOR =")

subcamera_list = string_get_after_eq(subcamera_name).split()

subcamera_path_list = []
for temp_name in subcamera_list :
	temp_path = "vendor/mediatek/proprietary/custom/" + platform + \
		"/hal/sendepfeature/" + temp_name + "/config.ftbl." + temp_name + ".h"
	subcamera_path_list.append(temp_path)

for temp_path in subcamera_path_list :
	subcamera_handle = open(temp_path,'r')

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
	display_define_one("zsd :",subcamera_result,temp_path)
	boundary()
#lcd**************************************************************************************

lcm_list = get_fmt_in_line(sagereal + "/mk/" + project_name +"/" + k_platform + ".mk",\
			"CUSTOM_LK_LCM")

lcm_list = string_get_after_eq(lcm_list,1).split()

lcm_path_list=[]
for templist in lcm_list:
	lcm_path_list.append(kernel_version + "/drivers/misc/mediatek/lcm/" + templist +\
			"/" + templist + ".c");

lcm_result_list = []
templist = []
for temppath in lcm_path_list :
	templist = get_match_define(temppath,["params->dsi.lcm_esd_check_table"],0)
	lcm_result_list.append(templist)

i = 0
while i < len(lcm_list):
	display_define_one("LCD ESD寄存器检测个数 :",lcm_result_list[i],lcm_path_list[i])
	i = i + 1

#vgp************************************************************************************

defconfig_handle.seek(0)
temp_lines = defconfig_handle.readlines()
defconfig_handle.seek(0)

i = 0
vgp_config_result = []
while i < len(temp_lines) :
	if "CONFIG_MTK_RF_VGP" in temp_lines[i] :
		vgp_config_result.append(temp_lines[i])
	i = i + 1

pmic_path = kernel_version + "/drivers/misc/mediatek/power/" + platform + "/pmic.c"

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

display_define_one("射频3G电路供电VGP1或VGP2检查 :",pmic_result,pmic_path)
display_define_one("deconfig :",vgp_config_result,defconfig_file)
boundary()
#ntc*************************************************************************************

ntc_path = kernel_version + "/drivers/misc/mediatek/include/mt-plat/" + platform + \
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

display_define_one("电池NTC 电阻检查 :",ntc_result,pmic_path)
boundary()
#fm ************************************************************************************



#print to file***************************************************************************

#savefile_handle = open(file_save_path + "checklist_file" , 'w')
