

import os
import sys
import re
import string
import xlwt
import xlrd

def get_onedata(str_o):
	str_ret = ''
	for i in range(0,4):
		str_ret = str_ret + str_o[i]
		pass

	return str_ret;

def get_onedata_in_(strings):
	i_begin = strings.find("(")
	i_end = strings.find(")")
	str_ret = strings[i_begin + 1 : i_end]
	return str_ret

def is_daley(strings):
	if 0 != strings[0] and 'x' != strings[1]:
		print(strings)
		return True;
	return False;

def get_first(strings,enchar):
	i = strings.find(enchar)
	str_ret = strings[0:i]
	return str_ret
	pass

def find_last(string,str):
    last_position=-1
    while True:
        position=string.find(str,last_position+1)
        if position==-1:
            return last_position
        last_position=position


fd = open('ST7701S-IVO6.0IPS(C060SWY7-0).txt','r')
wd = open('./result_st7701s_bc2','w+')
wd_temp = open('./result_temp','w+')
lines = fd.readlines()

begin = 1;
send_number = 0;

for line in lines:
	data = get_onedata_in_(line)
	if "WriteComm" in line:
		if 0 == begin:
			wd_temp.write(str(send_number));
			wd_temp.write("\n");
		else :
			begin = 0;
			pass
		wd_temp.write(data+',')
		send_number = 0;
	if "WriteData" in line:
		send_number = send_number + 1
		wd_temp.write(data+',')
	if "Delayms" in line:
		if 0 == begin:
			wd_temp.write(str(send_number));
			wd_temp.write("\n");
		else :
			begin = 0;
			pass
		wd_temp.write(data+',')
		send_number = 0;
	pass

wd_temp.close()

wd_temp = open('./result_temp','r')
lines_temp = wd_temp.readlines()

for line_temp in lines_temp:
	str_data = get_first(line_temp,",")
	wd.write("{")
	if True == is_daley(line_temp) :
		wd.write("REGFLAG_DELAY, " + str_data + ", {}},\n")
	else :
		wd.write(str_data+',')
		i_begin = line_temp.find(",");
		i_end = find_last(line_temp,',')
		number = get_first(line_temp[i_end + 1 :],'\n')
		wd.write(number+',{')
		wd.write(line_temp[i_begin + 1: i_end])
		wd.write("}},")
		wd.write("\n")
		pass
	pass

wd.write("\n"+"{REGFLAG_END_OF_TABLE, 0x00, {}}"+"\n")