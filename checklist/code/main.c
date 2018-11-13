

#include "file_operate.h"
#include "path_analyse.h"

char repertory_path[DIRECTORY_SIZE];
char project_name[FILE_NAME_SIZE];
char file_save_path[DIRECTORY_SIZE];

// 1 obj_path, 2 project name 3 file_save_path
int main(int argc, char const *argv[])
{
	/* code */
	if(4 != argc)
	{
		printf("error!!! : Number of parameter error !!!\n");
	}
	// save
	strcpy(repertory_path,argv[1]);
	strcpy(project_name,argv[2]);
	strcpy(file_save_path,argv[3]);
	// develop
	develop_dir(repertory_path);
	develop_dir(file_save_path);
	//

	// access

	//
	printf("repertory_path : [%s]\n", repertory_path);
	printf("project_name : [%s]\n", project_name);
	printf("file_save_path : [%s]\n", file_save_path);
	return 0;
}

int check_filename(char* repertory_path, char* project_name, char* file_save_path)
{
	char buf[DIRECTORY_SIZE];
	POINT_NULL_TEST(repertory_path);
	POINT_NULL_TEST(project_name);
	POINT_NULL_TEST(file_save_path);

	strcpy(buf,repertory_path);
	strcat(buf,"/");
	strcat(buf,"sagereal");
	strcat(buf,"/");
	strcat(buf,"mk");
	strcat(buf,"/");
	strcat(buf,project_name);

	if(0 == access(repertory_path) && 
		0 == access(buf) &&
		0 == access(file_save_path) )
	{
		return 0;
	}
	else
	{
		return -1;
	}
}