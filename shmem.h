#ifndef _SHMEM_H_INCLUDED
#define _SHMEM_H_INCLUDED

#include <stdlib.h>
#include <sys/ipc.h>
#include <sys/shm.h>

char *get_shmem(int id);
int open_shmem(void);
char read_shmem(int dummy);
void write_shmem(char c);
void close_shmem(int id);
#endif
