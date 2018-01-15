#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <fcntl.h>
#include "shmem.h"
#define CONTROL_SOUND "S"
#define FILEPERM 0644
#define SHMIDSIZE 8

int pid_module, pid_client, pid_cd;
char shmem_id[SHMIDSIZE];
int id;

void exit_func(int signum)
{
    printf("\nProgram End By SIGINT\n");
    close_shmem(id);
    exit(0);
}

int main(void)
{
    pthread_t julius_module, julius_client, colordetect;
    int pid_module, pid_client, pid_cd, pid_circle, pid_face;
    char *addr;
    int stat;

    signal(SIGINT, exit_func);
    id = open_shmem();
    printf("Shared memory ID = %d\n", id);
    sprintf(shmem_id, "%d", id);
    addr = get_shmem(id);
    addr[0] = 'S';

    if ((pid_module = fork()) == 0) {
    	char *argv_module[] = {"./my-run-gmm.sh", "-module", NULL};
		if (execvp(argv_module[0], argv_module) < 0) {
	    	fprintf(stderr, "fork error: module\n");
	    	exit(1);
		}
    } else if ((pid_cd = fork()) == 0) {
    	char *argv_cd[] = {"./a.out",shmem_id, NULL};
		if (execvp(argv_cd[0], argv_cd) < 0) {
			fprintf(stderr, "fork error: color detection\n");
			exit(1);
		}
    } else if ((pid_client = fork()) == 0) {
    	char *argv_client[] = {"python", "motor_track.py", shmem_id, NULL};
		sleep(2); //sleep two sec to wait start up of module
		if (execvp(argv_client[0], argv_client) < 0) {
	    	fprintf(stderr, "fork error: client\n");
	    	exit(1);
		}
		//execvp(argv_client[0], argv_client);*/
    /*} else if ((pid_circle = fork()) == 0) {
    	char *argv_client[] = {"python", "circle2.py", shmem_id, NULL};
		sleep(2); //sleep two sec to wait start up of module
		if (execvp(argv_client[0], argv_client) < 0) {
	    	fprintf(stderr, "fork error: client\n");
	    	exit(1);
		}
		//execvp(argv_client[0], argv_client);
    } else if ((pid_face = fork()) == 0) {
    	char *argv_client[] = {"python", "face.py", shmem_id, NULL};
		sleep(2); //sleep two sec to wait start up of module
		if (execvp(argv_client[0], argv_client) < 0) {
	    	fprintf(stderr, "fork error: client\n");
	    	exit(1);
		}
		//execvp(argv_client[0], argv_client);*/ 
    }  else {
		//client end -> other 3 processes kill
		wait(&stat);
		if (stat >= 0) {
	   		kill(pid_module, SIGINT);
	    		kill(pid_cd, SIGINT);
			kill(pid_circle, SIGINT);
            kill(pid_face, SIGINT);
		}
		wait(&stat);
		wait(&stat);
		wait(&stat);
		wait(&stat);
    }
    return EXIT_SUCCESS;
}


