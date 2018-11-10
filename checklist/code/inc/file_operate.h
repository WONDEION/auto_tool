
#ifndef FILE_OPRERATE_H
#define FILE_OPRERATE_H

#include <sys/stat.h>
#include <sys/types.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <malloc.h>
#include <fcntl.h>

#define CHAECK_FUN_SUCCESS(fun) if((fun) < 0){return -1;}

#define CHAECK_FUN_SUCCESS_PRINT(fun,pr) if((fun) < 0){(pr); return -1;}
#define GET_AND_CHAECK_FUN_SUCCESS_PRINT(g,fun,pr) if(( (g) = (fun) ) < 0){(pr); return -1;}

#define FILE_FD_CHECK(fd) CHAECK_FUN_SUCCESS(fd)
#define FILELINENUM_CHECK(ln) CHAECK_FUN_SUCCESS(ln)
#define POINT_NULL_TEST(p) if(NULL == (p)){return -1;}
#define FUN_EQUAL_ERROR(a,b) if((a) == (b)){return -1;}
#define FUN_UNEQUAL_ERROR(a,b) if((a) != (b)){return -1;}

// function extren----------------------------------------



int file_goto_line(int file_fd,int line_num);
int file_get_line(int file_fd, int line_num, char* string);
int file_read_line(int file_fd, char* string);
char file_read_next_char(int file_fd);
char file_read_last_char(int file_fd);

static char file_read_char_direction(int file_fd, char dir);

#endif