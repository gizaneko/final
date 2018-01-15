#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdlib.h>
#include <fcntl.h> 
#include <stdio.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <sys/time.h>
#include "opencv2/highgui/highgui.hpp" 
#include "opencv2/imgproc/imgproc.hpp"
#define IMAGE_WIDTH 640
#define CENTER IMAGE_WIDTH/2 
using namespace cv;
using namespace std;
char *addr;
#define MINIMUM_OBJECT_AREA 10000
#define SYNC_FILE "tmp"
#define FILEPERM 0644
char *get_shmem(int id);
char read_shmem(int dummy);

void handler(int signo)
{
    char *argv[] = {"python", "motor2.py", "STOP", NULL};
    int stat;
    if (fork() ==0) {
		execvp(argv[0], argv);
    } else {
		wait(&stat);
    	if (stat < 0) {
	    	cerr << "error: stop" << endl;
	    	exit(1);
		}
    }
    exit(0);
}

void timer_handler(int signo)
{
}

int main(int argc, char **argv)
{
	//2nd argument == shared memory id
	int id;
	id = atoi(argv[1]);
	addr = get_shmem(id);
	struct itimerval value = {0, 300*1000, 0, 300*1000};
    //signal
    signal(SIGINT, handler);
    signal(SIGALRM, timer_handler);
    setitimer(ITIMER_REAL, &value, NULL);

    //Initiate web camera
    VideoCapture cap(0);
    if (!cap.isOpened()) {
        cout << "Cannot open the web cam" << endl;
        return -1;
    }

    //namedWindow("Control", CV_WINDOW_AUTOSIZE);

    int iLowH = 100;
    int iHighH = 140;
    int iLowS = 75;
    int iHighS = 255;
    int iLowV = 75;
    int iHighV = 255;

    /*Mat imgTmp;
    cap.read(imgTmp);
    Mat imgLines = Mat::zeros(imgTmp.size(), CV_8UC3);*/
	int dpre = 0;
	int d = 0;

    while(true) {
		pause();
		if (read_shmem(0) != 'C') {
			//if colordetect Control is not allowed... continue
			continue;
		}

		Mat imgOriginal;
		if (!cap.read(imgOriginal)) {
	    	cout << "Cannot read a frame from video stream" << endl;
	    	break;
		}


		//Create two color image
		Mat imgHSV;
		cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV);
		Mat imgThresholded;
		inRange(imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded);
		erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5,5)));
		dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5,5)));
		dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5,5)));
		erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5,5)));

		//calculate moment for red object
		Moments oMoments = moments(imgThresholded);

		double dM01 = oMoments.m01;
		double dM10 = oMoments.m10;
		double dArea = oMoments.m00;

		if (read_shmem(0) != 'C') {
			//if colordetect Control is not allowed... continue
			continue;
		}

		if (dArea > MINIMUM_OBJECT_AREA) {
		    int posX = dM10 / dArea;
		    int posY = dM01 / dArea;

		    char diff[10];
			char diff0[10];
		    d = posX - CENTER;
			sprintf(diff, "%d", d >= 0 ? d : -d);
			sprintf(diff0, "%d", (d - dpre) >= 0 ? d - dpre : dpre -d);
			if (posX <= CENTER) {
			    char *argv[] = {"python","motor2.py", "LEFT" ,diff ,diff0, NULL};
			    int stat;
	
			    if (fork() == 0) {
					execvp(argv[0], argv);
			    } else {
					wait(&stat);
					if (stat < 0) {
				   		cerr << "error: wait" << endl;
				    	exit(1);
					}
			    }
			} else {
			    char *argv[] = {"python","motor2.py","RIGHT", diff, diff0, NULL};
			    int stat;
	
			    if (fork() == 0) {
					execvp(argv[0], argv);
			    } else {
					wait(&stat);
					if (stat < 0) {
				    	cerr << "error: wait" << endl;
				    	exit(1);
					}
			    }
		    }
		}
		dpre = d;
	
		//Show created images
		/*imshow("Thresholded Image", imgThresholded);
		imgOriginal = imgOriginal + imgLines;
		imshow("Original", imgOriginal);*/
   	}
   	return 0;
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

