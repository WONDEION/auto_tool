

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


fd = open( 'ST7701S-IVO6.0IPS(C060SWY7-0).txt','r')
wd = open('./result_st7701s_bc2','w+')
lines = fd.readlines()

for line in lines:
	if "SSD_SEND" in line:
		i = line.find(",")
		wd.write("{")
		j = 1;
		while j :
			ret_str = get_onedata(line[i + 1:]);
			i = i + 5
			wd.write(ret_str)
			if line[i] == ')':
				wd.write('}')
				wd.write('}')
				wd.write(',\n')
				break;
			else:
				wd.write(',')
			if j == 1:
				wd.write(str(line.count(',') - 1))
				wd.write(',')
				wd.write("{")
			j=j+1;
	pass
