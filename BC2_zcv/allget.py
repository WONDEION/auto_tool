
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

sheet = xlrd.open_workbook('./F46012PA-4900-4.4-ZCV_test.xls')

table = sheet.sheet_by_name("ZCV")

#writefile = open("./result",'w+')
writefile_r = open("./result_r",'w+')

list = ["50",'25','0','-10','10']
#last_od = 0;
for j in [0,7,14,21,28]:
	#writefile.write(list[int(j/7)]+"\n")
	writefile_r.write(list[int(j/7)]+"\n")
	last_od = -1;
	for i in range(2,106):
		#od_value = int(table.cell(i,5).value)
		#if last_od == od_value:
		#	print(od_value)
		#	continue;
		#print((table.cell(i,j+1).value))
		ocv_value = (table.cell(i,j+1).value)
		#mah_value = round((table.cell(i,j+4).value)*10)
		R_value = round((table.cell(i,j+6).value))
		D_value = round(table.cell(i,j+5).value)
		if last_od == D_value:
			print(D_value)
			continue;
		#writefile.write("{"+str(D_value)+","+str(ocv_value)+"}")
		writefile_r.write("{"+str(R_value)+","+str(ocv_value)+"}")
		if 100 != D_value:
			#writefile.write(",")
			writefile_r.write(",")
		#writefile.write("\n")
		writefile_r.write("\n")
		last_od = D_value
		pass
	#writefile.write("\n")
	writefile_r.write("\n")




#print("ocv_value : is [%d]." %(ocv_value))
