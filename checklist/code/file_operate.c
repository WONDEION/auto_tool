
#include "file_operate.h"

int file_goto_line(int file_fd,int line_num)
{
	int i = 1;
	char ch = 0;
	FILE_FD_CHECK(file_fd);
	FILELINENUM_CHECK(line_num);
	// set lseek
	lseek(file_fd,0,SEEK_SET);
	// find 
	for(i = 1;i < line_num; i++)
	{
		while((ch = file_read_next_char(file_fd)) && ('\0' != ch) && ('\n' != ch))
		{
			;
		}
		if('\0' == ch)
		{
			return -1;
		}
		if('\r' != file_read_next_char(file_fd))
		{
			lseek(file_fd,-1,SEEK_CUR);
		}
	}
	return 0;
}

int file_get_line(int file_fd, int line_num,char* string)
{
	FILE_FD_CHECK(file_fd);
	FILELINENUM_CHECK(line_num);
	POINT_NULL_TEST(string);
	CHAECK_FUN_SUCCESS(file_goto_line(file_fd,line_num));
	CHAECK_FUN_SUCCESS(file_read_line(file_fd,string));
	return 0;
}
// form now to line tail, skip '\n'
int file_read_line(int file_fd, char* string)
{
	int i = 0;
	char c = 0;
	FILE_FD_CHECK(file_fd);
	POINT_NULL_TEST(string);
	
	while('\n' != (c = file_read_next_char(file_fd)) && ('\0' != c))
	{
		string[i] = c;
		i++;
	}
	string[i] = '\0';
	return 0;
}


char file_read_next_char(int file_fd)
{
	return file_read_char_direction(file_fd,'r');
}

char file_read_last_char(int file_fd)
{
	return file_read_char_direction(file_fd,'l');
}

static char file_read_char_direction(int file_fd, char dir)
{
	char buf[2];
	int rtread = 0;
	FILE_FD_CHECK(file_fd);
	if(dir == 'l')
	{
		CHAECK_FUN_SUCCESS(lseek(file_fd,SEEK_CUR,-1));
	}
	rtread = read(file_fd,buf,1);
	if(-1 == rtread)
	{
		return -1;
	}
	if(0 == rtread)
	{
		return 0;
	}
	return buf[0];
}