#include "shmem.h"
#include <stdio.h>
#define FILEPERMISSION 0644
#define IPC_SEG_SIZE 1
char *addr;

int open_shmem(void) {
	int id;
	if ((id = shmget(IPC_PRIVATE, IPC_SEG_SIZE, IPC_CREAT | FILEPERMISSION)) < 0){
		perror("shmget");
		exit(-1);
	}
	return id;
}
char *get_shmem(int id)
{
	if ((addr = (char *)shmat(id, 0, 0)) < 0) {
		perror("shmat");
		exit(EXIT_FAILURE);
	}
	return addr;
}

char read_shmem(int dummy)
{
	return addr[0];
}

void write_shmem(char c)
{
	addr[0] = c;
}

void close_shmem(int id)
{
	if (shmctl(id, IPC_RMID, 0) < 0) {
		perror("shmdt");
	}
}
