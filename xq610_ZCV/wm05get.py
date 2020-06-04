
import os
import sys
import re
import string
import xlwt
import xlrd

def get_value(table,x,y):
	string = table.cell(x,y)
	string = str(string) 
	value = table.cell(x,y).value
	value = value*10;
	print(value)
	i = len(string) - 2
	if(string[i] == '.'):
		value = (int(string[i+1])) + value
	return (int(value))

sheet = xlrd.open_workbook('./副本C1000放电曲线.xlsx')

table = sheet.sheet_by_name("Sheet2")

writefile = open("./wm05_result",'w+')

i = 0;
writefile.write("0.33+0.66:\n")
while i < 100:
	writefile.write("{")
	writefile.write(str(i))
	writefile.write(",")
	value = round((table.cell(i,4).value)*1000,1)
	writefile.write(str(value))
	writefile.write("},\n")
	i = i+2;

i = 0;
writefile.write("\n0.66+0.33:\n")
while i < 100:
	writefile.write("{")
	writefile.write(str(i))
	writefile.write(",")
	value = round((table.cell(i,5).value)*1000,1)
	writefile.write(str(value))
	writefile.write("},\n")
	i = i+2;



#print("ocv_value : is [%d]." %(ocv_value))