#include <stdio.h>
#include <fcntl.h>
#include <stdlib.h>
#include <linux/i2c-dev.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/ioctl.h>
#define SLAVE_ADDR 0x55

void i2c_write (int *angles);
void i2c_read(char *stat);

int main(void)
{
    int buf[5];
    char stat[2];
    int angle;
    int i;

    while(1){
	i2c_read(stat);
	printf("distance = %d\n", stat[0]);
	printf("touched = %s\n", stat[1]? "true" : "false");

	printf("angle0:");
	if (scanf("%d", &angle)==EOF)break;
	buf[0] = (char)angle;
	printf("angle1:");
	if (scanf("%d", &angle)==EOF)break;
	buf[1] = (char)angle;
	printf("angle2:");
	if (scanf("%d", &angle)==EOF)break;
	buf[2] = (char)angle;
	printf("angle3:");
	if (scanf("%d", &angle)==EOF)break;
	buf[3] = (char)angle;
	printf("angle4:");
	if (scanf("%d", &angle)==EOF)break;
	buf[4] = (char)angle;
	for(i=0; i<6; i++) {
	    i2c_write(buf);
	    usleep(110000);
	}
    }
}

void i2c_write (int *angles) {
    int fd1;
    char buf[ 10 ];
    int i;

    //sprintf( filename, "/dev/i2c-1" );
    fd1 = open("/dev/i2c-1", O_RDWR );
    if ( fd1 < 0 ) {
	printf( "Error on open\n" );
	exit( 1 );
    }
    if ( ioctl( fd1, I2C_SLAVE,SLAVE_ADDR ) < 0 ) {
	printf( "Error on slave address 0xE0\n" );
	exit( 1 );
    }

    for (i=0; i<5; i++) {
	    buf[i] = angles[i];
        printf("c: %d\n", buf[i]);
    }
    buf[5] = 0; //reseved bit6
    write(fd1, buf, 6);
    // 閉じる！！
    close( fd1 );
}

void i2c_read(char *stat)
{
    int fd1;
    char buf[10];
    int i;

    //sprintf( filename, "/dev/i2c-1" );
    fd1 = open("/dev/i2c-1", O_RDWR );
    if ( fd1 < 0 ) {
	printf( "Error on open\n" );
	    exit( 1 );
    }
    if (ioctl( fd1, I2C_SLAVE,SLAVE_ADDR ) < 0 ) {
	    printf( "Error on slave address 0xE0\n" );
	    exit( 1 );
    }
    
    read(fd1, buf, 2);
    stat[0] = buf[0];
    stat[1] = buf[1];

    close( fd1 );
}
