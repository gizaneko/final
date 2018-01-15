#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import cv2
import time
import os
import distance
#import smbus
import signal
import subprocess
import random

#angles to write
angles = [105,120, 140, 90, 90]
angles_dfl = [105,120, 140, 90, 90]
#monitor touched event 
two_past_stat = 0
past_stat = 0
current_stat = 0
#how many loop it takes to reach target angles
cycles = 10
count = 0 #if count gets change_count move moter
change_count = 40

#definiton of pin_num, address
HEAD_VERT = 2 #頭縦方向
NECK_HORZ = 0 #首横方向
NECK_VERT = 1 #首縦方向
FIN_RIGHT = 3
FIN_LEFT = 4
ADDR = 0x55

#send i2c angle data to stm32
def servo_control(signal, frame):
        stat = distance.get_stat()
        global past_stat, current_stat, two_past_stat, count
        distance.write_angles(angles)
        #update status
        two_past_stat = past_stat
        past_stat = current_stat
        current_stat = stat[1]
        count = (count+1)%change_count #count 0~19(for example)

#send i2c signal once in 100ms
signal.signal(signal.SIGALRM, servo_control)
signal.setitimer(signal.ITIMER_REAL, 0.1, 0.1)

#camera settings
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
capture = cv2.VideoCapture(0)
ret = capture.set(3, 480)
ret = capture.set(4, 320)

i = 0
while True:
    #reacts when touched
    if (current_stat == 1 and (past_stat == 0 or two_past_stat == 0)) :
        #reset time not to prevent reaction
        signal.setitimer(signal.ITIMER_REAL, 0, 0)
        aplay = ['aplay','-q','rapras_touch.wav']
        wr = subprocess.Popen(aplay)
        angles[HEAD_VERT] = angles[HEAD_VERT] - 30
        for i in range (0,10):
            distance.write_angles(angles)
            time.sleep(0.1)
        angles[HEAD_VERT] = angles[HEAD_VERT] + 30
        for i in range (0,10):
            distance.write_angles(angles)
            time.sleep(0.1)
        #time.sleep(2)
        wr.terminate()
        signal.setitimer(signal.ITIMER_REAL, 0.1, 0.1)

    #once in a few seconds fin moves
    if count == 0:
        angles[FIN_RIGHT] += 15
        angles[FIN_LEFT] += 15
        #change angle of neck randomly once in change_count*0.1seconds
        angles[NECK_VERT] += random.randint(-15, 15)
        angles[NECK_HORZ] += random.randint(-15, 15)
        angles[HEAD_VERT] += random.randint(-15, 15)
        #also change change_count with random number
        change_count = random.randint(2, 8)*10
    elif count == change_count/2:
        angles[FIN_LEFT] -= 15
        angles[FIN_RIGHT] -= 15

    #boudnary --> original angle +- 30
    #prevent not to go too far
    for i in range(len(angles)) :
        if anlges[i] > angles_dfl[i]+30:
            angles[i] = angles_dfl[i]+30
        elif anlges[i] < angles_dfl[i]-30:
            angles[i] = angles_dfl[i]-30

    #capture image
    ret, image = capture.read()
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=2, minSize=(30, 30))

    if len(face) > 0:
        for rect in face:
            cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=2)

            #if (rect[0] + rect[2] / 2) > 120:
                #os.system("python motor2.py RIGHT " + str (2 * (rect[0] + rect[2]/2 - 120)) )
            #if (rect[0] + rect[2] / 2) < 120:
                #os.system("python motor2.py LEFT " + str (2 * (120 - rect[0] - rect[2]/2)) )

