
#ifndef PATH_ANALYSE_H
#define PATH_ANALYSE_H value

#include <sys/types.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <sys/ioctl.h>
#include <pwd.h>
#include <sys/stat.h>
#include <malloc.h>

#define DIRECTORY_SIZE 8192
#define FILE_NAME_SIZE 255

int develop_dir(char* dir);
int Path_analyse_get_homedir(char* dir);
int Path_Analyse_get_nowdir(char* dir);
int delete_lastlv_dir(char* directory);

#endif