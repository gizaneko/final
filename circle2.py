# -*- coding: utf-8 -*-
import numpy as np
import cv2.cv as cv
import cv2
import os
import signal
import sys

def handler(signal, frame):
		os.system("python motor2.py STOP 0")
		cam.release()
		cv2.destroyAllWindows()
		sys.exit(0)


cam = cv2.VideoCapture(1)


signal.signal(signal.SIGINT, handler)

while(cam.isOpened()):

		ret, frame = cam.read()

		frame = frame[:,::-1]

		size = (640, 480)
		frame = cv2.resize(frame, size)

		gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

		gray = cv2.GaussianBlur(gray, (33,33), 1)


		colimg = frame.copy() #cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)


        #circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 60, param1=10, param2=85, minRadius=10, maxRadius=80)
		circles = cv2.HoughCircles(gray, cv.CV_HOUGH_GRADIENT, 1, 60, param1=10, param2=100, minRadius=10, maxRadius=100)

        #if circles != None:
		if circles is not None:
			circles = np.uint16(np.around(circles))
			for i in circles[0,:]:
				cv2.circle(colimg,(i[0],i[1]),i[2],(255,255,0),2)

				cv2.circle(colimg,(i[0],i[1]),2,(0,0,255),3)
               
				if i[0] > 320:
					os.system("python motor2.py LEFT " + str(i[0] - 320))
					print 'right'
				if i[0] < 320:
					os.system("python motor2.py RIGHT " + str(320 - i[0]))					
					print 'left'    
                    
		#cv2.imshow('preview', colimg)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			os.system("python motor2.py STOP 0")
			break

cam.release()
cv2.destroyAllWindows()



