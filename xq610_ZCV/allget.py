
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

sheet = xlrd.open_workbook('./F46009MA-3140-4.4-ZCV.xls')

table = sheet.sheet_by_name("ZCV")

writefile = open("./result",'w+')
list = ["50",'25','0','-10','10']
#last_od = 0;
for j in [0,7,14,21,28]:
	writefile.write(list[int(j/7)]+"\n")
	last_od = -1;
	for i in range(2,108):
		#od_value = int(table.cell(i,5).value)
		#if last_od == od_value:
		#	print(od_value)
		#	continue;
		D_value = round(table.cell(i,j+5).value)
		ocv_value = round((table.cell(i,j+1).value)*10)
		mah_value = round((table.cell(i,j+4).value)*(10))
		R_value = round((table.cell(i,j+6).value)*10)
		ocv_value = ocv_value - (400)
		if last_od == D_value:
			print(D_value)
			continue;
		if 100 > D_value:
			writefile.write("\t"+str(mah_value)+"\t"+str(ocv_value)+"\t"+str(R_value)+'\n')
		last_od = D_value
		pass
	writefile.write("\n")




#print("ocv_value : is [%d]." %(ocv_value))