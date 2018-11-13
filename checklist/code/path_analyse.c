
#include "path_analyse.h"

int develop_dir(char* dir)
{
	char buf[DIRECTORY_SIZE];
	char nowdir[DIRECTORY_SIZE];
	char homedir[DIRECTORY_SIZE];

	if(NULL == dir)
	{
		return -1;
	}

	// get nowdir
	Path_Analyse_get_nowdir(nowdir);
	// get homedir
	Path_analyse_get_homedir(homedir);
	//printf("nowdir : [%s\n]",nowdir );
	//printf("homedir : [%s\n]",homedir );

	// develop
	//printf("dir : \"%s\"\n", dir);
	if('.' == dir[0] && '.' != dir[1] )  //.~~
	{
		if('/' == dir[1])  // ./
		{
			strcpy(buf,nowdir);
			if('\0' !=  dir[2])
			{
				strcat(buf,dir + 1); // include '/'
			}
			strcpy(dir,buf);
		}
		else if('\0' == dir[1])  // .
		{
			strcpy(dir,nowdir);
		}
		else  // .string
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
	else if('.' == dir[0] && '.' == dir[1] )  // ..~~
	{
		if('/' == dir[2])  // ../
		{
			strcpy(buf,nowdir);
			delete_lastlv_dir(buf);
			strcat(buf,dir +2);  // include '/'
			strcpy(dir,buf);
		}
		else if('\0' == dir[2])  // ../
		{
			strcpy(buf,nowdir);
			delete_lastlv_dir(buf);
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
		strcpy(buf,homedir);
		strcpy(buf + strlen(homedir),dir + 1);
		strcpy(dir,buf);
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
	}
	return 0;
}

int Path_analyse_get_homedir(char* dir)
{ 
	int uid = getuid();
	if(NULL == dir)
	{
		return -1;
	}		
	struct passwd *user_inf = NULL;
	user_inf = getpwuid(uid);
	strncpy(dir,user_inf->pw_dir,DIRECTORY_SIZE);
	return 0;
}	

int Path_Analyse_get_nowdir(char* dir)
{
	if(NULL == dir)
	{
		return -1;
	}
	//getcwd
	if(NULL == getcwd(dir,DIRECTORY_SIZE))
	{
		return -1;
	}
	return 0;
} 

int delete_lastlv_dir(char* directory) // delete Absolute path
{
	int i = 0;	
	if(NULL == directory || directory[0] != '/')
	{
		return -1;
	}
	// if '/' return 
	if(1 == strlen(directory) )
	{
		return 0;
	}
 	// find 
	i = strlen(directory);
	if(directory[i] == '/')
	{
		i--;
	}
	while(directory[i] != '/')
	{
		i--;
	}
	// clean
	if(i == 0)
	{
		directory[1] = '\0';
	}
	else
	{
		directory[i] = '\0';
	}	

	return 0;
}