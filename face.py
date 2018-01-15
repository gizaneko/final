#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import time
import os
import jtalk
import distance
import smbus

#definiton of pin_num, address
HEAD_VERT = 2
NECK_HDRZ = 0
NECK_VERT = 1
ADDR = 0x55

# bus
bus = smbus.SMBus(1)


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')

capture = cv2.VideoCapture(0) # カメラセット
# 画像サイズの指定
ret = capture.set(3, 480)
ret = capture.set(4, 320)


i = 0
while True:
    start = time.clock() # 開始時刻
    ret, image = capture.read() # 画像を取得する作業
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    face = faceCascade.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=2, minSize=(30, 30))

    if len(face) > 0:
        for rect in face:
            cv2.rectangle(image, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0, 0,255), thickness=2)
            print(rect[0] + rect[2] / 2)
            d = distance.get_stat()
            print("distance:"+str(d[0]))
            print("status:"+str(d[1]))
            if d[0] > 120 :
                os.system("python motor2.py STOP 0")
                jtalk.jsay('おはようございます')
                quit()
            else :
				if (rect[0] + rect[2] / 2) > 120:
					os.system("python motor2.py RIGHT " + str (2 * (rect[0] + rect[2]/2 - 120)) )
				if (rect[0] + rect[2] / 2) < 120:
					os.system("python motor2.py LEFT " + str (2 * (120 - rect[0] - rect[2]/2)) )

    get_image_time = int((time.clock()-start)*1000) # 処理時間計測
    # 1フレーム取得するのにかかった時間を表示
    cv2.putText( image, str(get_image_time)+"ms", (10,10), 1, 1, (0,255,0))

    cv2.imshow("Camera Test",image)
    # キーが押されたら保存・終了
    if cv2.waitKey(10) == 32: # 32:[Space]
        cv2.imwrite(str(i)+".jpg",image)
        i+=1
        print("Save Image..."+str(i)+".jpg")
    elif cv2.waitKey(10) == 27: # 27:Esc
        capture.release()
        cv2.destroyAllWindows()
        break
