import os
import sys
import re
import string
import xlwt
import xlrd

logpath=[]
fd_list = []
last_line_list = []

def index_of_str2(s1, s2):
	n1=len(s1)
	n2=len(s2)
	times = 0;
	for i in range(n1-n2+1):
		if s1[i:i+n2] == s2:
			if 1 == times:
				return i
			else :
				times = 1;
	else:
		return -1

def index_of_str(s1, s2):
	n1=len(s1)
	n2=len(s2)
	for i in range(n1-n2+1):
		if s1[i:i+n2] == s2:
			return i
	else:
		return -1


def line_get_soc(line):
	begin = index_of_str2(line,'(')
	end = index_of_str2(line,')')
	value = line[begin + 1:end];
	return int(value)

def line_get_time(line):
	begin_time = index_of_str(line,'[')
	end_time = index_of_str(line,'.')
	value_time = line[begin_time + 1:end_time]
	return int(value_time)

def linelist_compara(line1,line2):
	if line1[2] > line2[2] :
		return True;
	else :
		return False;

def linelist_get_soc(linelist):
	return int(linelist[2]);

def linelist_value_equ(line1,line2):
	if line1[2] == line2[2] :
		return True;
	else :
		return False;

def clean_repetitive_line_after_sort(chooseline):
	i = 0;
	j = 0;
	while(i < len(chooseline)) :
		pass

## ----------------------- open file-----------------------------------

all_log = os.listdir("./")

for filename in all_log :
	if "kernel" in filename:
		logpath.append(filename);

for path_temp in logpath :
	if False == os.path.exists(path_temp):
		print("Invalid directory entered");
		exit();
	else :
		fd_list.append(open(path_temp,'r'))
	
##------------------------------------------------------------------
last_read = -1;
excel_line = 2;

excel_file = xlwt.Workbook();
sheet = excel_file.add_sheet("sheet1",cell_overwrite_ok=True);
sheet_line = 1;

chooseline = []

sheet.write(0,0,"Log");
sheet.write(0,1,"T");
sheet.write(0,2,"UI");

##----------------------------read line--------------------------------
''' mode 1 
for fd_handle in fd_list :
	all_line = fd_handle.readlines()
	for line in  all_line:
		if "UI_SOC=(" in line :
			sheet.write(sheet_line,0,line[0:-1]);
			sheet_line = sheet_line + 1;
			pass
		pass

''' #mode 2
for fd_handle in fd_list :
	all_line = fd_handle.readlines()
	for line in  all_line:
		if "UI_SOC=(" in line :
			value = line_get_soc(line)
			if value != last_read:
				# line
				last_read = value;
				#sheet.write(sheet_line,0,line[0:-1]);
				# time 
				time = line_get_time(line)
				#sheet.write(sheet_line,1,time);	
				#value
				#sheet.write(sheet_line,2,int(value));
				#empty line
				empty_line = [line[0:-1],time,value]
				chooseline.append(empty_line)
				# add 
				#sheet_line = sheet_line + 1;	
			pass
		pass
	last_line_list.append(all_line[-1])


max_line_time = 0;
max_line = ''

for last_line_temp in last_line_list :
	value = line_get_time(last_line_temp)
	if int(value) > int(max_line_time):
		max_line_time = value;
		max_line = last_line_temp
		pass
	pass

'''
sheet.write(sheet_line,0,max_line);
sheet.write(sheet_line,1,int(max_line_time));
sheet.write(sheet_line,2,int(0));
'''

chooseline.append([max_line,max_line_time,0])

#--------------------------------------clear and sort-----------------------

#chooseline = clean_repetitive_line()

writeline = sorted(chooseline, key = linelist_get_soc, reverse=True);
pictureline = sorted(chooseline, key = linelist_get_soc, reverse=True);

#---------------------------------------write file------------------------------

for line in writeline :
	print(line[0],line[1],line[2])
	sheet.write(sheet_line,0,line[0]);
	sheet.write(sheet_line,1,line[1]);
	sheet.write(sheet_line,2,line[2]);
	sheet_line = sheet_line + 1;

excel_file.save('result.xls')



