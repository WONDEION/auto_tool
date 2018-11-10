
#include "path_analyse"

int develop_dir(char* dir)
{
	char buf[DIRECTORY_SIZE];
	char nowdir[DIRECTORY_SIZE]

	if(NULL == dir)
	{
		return -1;
	}


	// get nowdir 
	// get homedir

	// develop
	//printf("dir : \"%s\"\n", dir);
	if('.' == dir[0] && '.' != dir[1] )  //.~~
	{
		if('/' == dir[1])  // ./
		{
			strcpy(buf,nowdir);
			strcat(buf,dir + 1); // include '/'
			strcpy(dir,buf);
		}
		else if('\0' == dir[1])  // .
		{
			strcpy(dir,nowdir);
		}
		else  // .string
		{
			if(!islegaldirectory(dir + 1))
			{
				return -1;
			}
			strcpy(buf,nowdir);
			if(strcmp(nowdir,"/"))
			{
				strcat(buf,"/");
			}
			strcat(buf,dir);
			strcpy(dir,buf);
		}
		return 0;
	}
	else if('.' == dir[0] && '.' == dir[1] )  // ..~~
	{
		if('/' == dir[2])  // ../
		{
			strcpy(buf,nowdir);
			delete_lastlv_dir_string(buf);
			strcat(buf,dir +2);  // include '/'
			strcpy(dir,buf);
		}
		else if('\0' == dir[2])  // ../
		{
			strcpy(buf,nowdir);
			delete_lastlv_dir_string(buf);
			strcpy(dir,buf);
		}
		else   // ..string
		{
			strcpy(buf,nowdir);
			if(strcmp(nowdir,"/"))
			{
				strcat(buf,"/");
			}
			strcat(buf,dir);
			strcpy(dir,buf);
		}
		return 0;
	}
	else if('/' == dir[0])
	{
		return 0;
	}
	else if ('~' == dir[0])
	{
		/* code */
	}
	else
	{
		strcpy(buf,nowdir);
		if(strcmp(nowdir,"/"))
		{
			strcat(buf,"/");
		}
		strcat(buf,dir);
		strcpy(dir,buf);
		return 0;
	}
	return 0;
}

int Path_analyse_get_userinfo()
{
	//getcwd
}

int Path_Analyse_get_nowdir()
{
	//getpwuid(uid);
} 