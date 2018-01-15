# -*- coding: utf-8 -*-

import socket
import string

import wiringpi as wp
import time
import struct
import signal

import subprocess
import sys

import jtalk
from ctypes import *

host = 'localhost'
port = 10500


L6470_SPI_SPEED         = 1000000
STEPPING_TICK           = 200


BUSY_PIN_0      = 21
BUSY_PIN_1      = 20
io = wp.GPIO(wp.GPIO.WPI_MODE_GPIO)
io.pinMode(BUSY_PIN_0,io.INPUT)
io.pinMode(BUSY_PIN_1,io.INPUT)

class ShmemError(Exception):
	pass

class Shmem:
	shmem_module = CDLL('./shmem.so')
	get_shmem_func_type = CFUNCTYPE(c_char_p, c_int);
	get_shmem_func = cast(shmem_module.get_shmem, get_shmem_func_type);
	read_shmem_func_type = CFUNCTYPE(c_char, c_int);
	read_shmem_func = cast(shmem_module.read_shmem, read_shmem_func_type);
	write_shmem_func_type = CFUNCTYPE(c_void_p, c_char);
	write_shmem_func = cast(shmem_module.write_shmem, write_shmem_func_type);

	@classmethod
	def get_shmem(cls, id):
		if id == None or not isinstance(id, int):
			raise SpamError('invalid argument')
		cls.addr = cls.get_shmem_func(id)
		return cls.addr
	@classmethod
	def read_shmem(cls):
	    return cls.read_shmem_func(0);
	@classmethod
	def write_shmem(cls, c):
		cls.write_shmem_func(c)

def exit_handler(signal, frame):
		print("\nExit")
		L6470_softstop(0)
		L6470_softstop(1)
		L6470_softhiz(0)
		L6470_softhiz(1)
		quit()

signal.signal(signal.SIGINT, exit_handler)

def L6470_write(channel, data):
		data = struct.pack("B", data)
		return wp.wiringPiSPIDataRW(channel, data)

def L6470_init(channel):

		L6470_write(channel, 0x07)
		L6470_write(channel, 0x00)
		L6470_write(channel, 0x25)

		L6470_write(channel, 0x09)

		L6470_write(channel, 0xFF)

		L6470_write(channel, 0x0A)

		L6470_write(channel, 0xFF)


		L6470_write(channel, 0x0B)

		L6470_write(channel, 0xFF)


		L6470_write(channel, 0x0C)

		L6470_write(channel, 0x40)


		L6470_write(channel, 0x13)

		L6470_write(channel, 0x0F)


		L6470_write(channel, 0x14)

		L6470_write(channel, 0x7F)

		L6470_write(channel, 0x0e)
		L6470_write(channel, 0x00)

		L6470_write(channel, 0x10)
		L6470_write(channel, 0x29)



def L6470_run(channel, speed):
		if (speed < 0):
				dir = 0x50
				spd = -1 * speed
		else:
				dir = 0x51
				spd = speed

		spd_h   = (0x0F0000 & spd) >> 16
		spd_m   = (0x00FF00 & spd) >> 8
		spd_l   = (0x0000FF & spd)

		L6470_write(channel, dir)

		L6470_write(channel, spd_h)
		L6470_write(channel, spd_m)
		L6470_write(channel, spd_l)


def L6470_move(channel, n_step):
		if (n_step < 0):
			dir = 0x40
			stp = -1 * n_step
		else:
			dir = 0x41
			stp = n_step


		stp_h   = (0x3F0000 & stp) >> 16
		stp_m   = (0x00FF00 & stp) >> 8
		stp_l   = (0x0000FF & stp)


		L6470_write(channel, dir)

		L6470_write(channel, stp_h)
		L6470_write(channel, stp_m)
		L6470_write(channel, stp_l)


def L6470_softstop(channel):
		print("***** SoftStop. *****")
		dir = 0xB0

		L6470_write(channel, dir)


def L6470_softhiz(channel):
		print("***** Softhiz. *****")
		dir = 0xA8

		L6470_write(channel, dir)


def L6470_getstatus(channel):
		print("***** Getstatus. *****")
		dir = 0xD0

		L6470_write(channel, dir)
		time.sleep(0.2)

if __name__=="__main__":
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host,port))
		params = sys.argv
		length = len(params)
		if (length < 2) :
			print 'Invalid argumen'
			quit()
		id = int(params[1])
		ret = Shmem.get_shmem(id)

		data = ""
		speed = 0
		v = 1

		print("***** start spi program *****")

		wp.wiringPiSPISetup (0, L6470_SPI_SPEED)
		wp.wiringPiSPISetup (1, L6470_SPI_SPEED)


		L6470_init(0)
		L6470_init(1)

		speed = 20000

		proc = 0

		while True:
			args = sys.argv
			if (length < 2) :
				print 'Invalid argument'
				quit()

			while (string.find(data, "\n.") == -1):
				data = data + sock.recv(1024)
			strTemp = ""
			for line in data.split('\n'):
				index = line.find('WORD="')
				if index != -1:
					line = line[index+6:line.find('"',index+6)]
					strTemp = strTemp + line
			if strTemp != "":
				print("Result:" + strTemp)

			c = unicode(strTemp,'utf-8')

			if(c == unicode("<s>青を追え</s>",'utf-8')):
				#subprocess.Popen(['python','jtalk.py','青を追います'])
				#jtalk.jsay('青を追います')
				aplay = ['aplay','-q','rapras_ao.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				speed = 20000
				v = 1
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				Shmem.write_shmem('C')

			if(c == unicode("<s>丸を追え</s>",'utf-8')):
				#jtalk.jsay('丸を追います')
				aplay = ['aplay','-q','rapras_maru.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				speed = 20000
				v = 1
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				proc = subprocess.Popen(['python','circle2.py'])
				Shmem.write_shmem('R')

			if(c == unicode("<s>話を聞け</s>",'utf-8')):
				aplay = ['aplay','-q','rapras_kike.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				Shmem.write_shmem('S')

			if c == unicode("<s>止まれ</s>",'utf-8') or c == unicode("STOP",'utf-8'):
				aplay = ['aplay','-q','rapras_susume.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				print(unicode("止まります。",'utf-8'))				
				if proc != 0 :
					proc.terminate()
					proc = 0
				L6470_softstop(0)
				L6470_softstop(1)
				L6470_softhiz(0)
				L6470_softhiz(1)
				Shmem.write_shmem('S')
				#break
			if c == unicode("<s>ブルータスお前もか</s>",'utf-8'):
				print(unicode("Juliusは死にました",'utf-8'))
				#subprocess.Popen(['python','jtalk.py','ジュリアスは死にました'])
				jtalk.jsay('ジュリアスは死にました')
				L6470_softstop(0)
				L6470_softstop(1)
				L6470_softhiz(0)
				L6470_softhiz(1)
				break
				  
			ch = Shmem.read_shmem()

			if ch != 'S' :
				data = ""
				continue
			
			if ( c == unicode("<s>おはよう</s>",'utf-8')) :
                                #sorry, I removed face.py due to camera error...
				#proc = subprocess.Popen(['python','face.py'])
				aplay = ['aplay','-q','rapras_aisatu.wav']
				wr = subprocess.Popen(aplay)
                                #Rapras bows !!
                                for i in range (0,10):
                                    distance.write_angles([105,100,160,90,90])
                                    time.sleep(0.1)
                                for i in range (0,10):
                                    distance.write_angles([105,120,140,90,90])
                                    time.sleep(0.1)
				#time.sleep(1)
				wr.terminate()	
				

			if ( c == unicode("<s>前へ進め</s>",'utf-8') or c == unicode("<s>前に進め</s>",'utf-8') ):
				aplay = ['aplay','-q','rapras_susume.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				speed = 20000
				v = 1
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				print(speed)
			if ( c == unicode("<s>後ろへ下がれ</s>",'utf-8') or c == unicode("<s>後ろに下がれ</s>",'utf-8') ):
				aplay = ['aplay','-q','rapras_susume.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				L6470_run(0, 0)
				L6470_run(1, 0)
				v = -1
				speed = 20000
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				print(speed)
			if  c == unicode("<s>右に曲がれ</s>",'utf-8'):
				aplay = ['aplay','-q','rapras_magare.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed/2)
				#L6470_move(0, 500)
				#L6470_move(1, 500)
			if  c == unicode("<s>左に曲がれ</s>",'utf-8'):
				aplay = ['aplay','-q','rapras_magare.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				L6470_run(0, v*speed/2)
				L6470_run(1, (-1)*v*speed)
				#L6470_move(0, -500)
				#L6470_move(1, -500)
			if  c == unicode("<s>スピード速く</s>",'utf-8'):
				aplay = ['aplay','-q','rapras_kasoku.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				if speed == 35000:
					print(unicode("最大速度です",'utf-8'))
				else :
					speed = speed+5000
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				print(speed)
			if  c == unicode("<s>スピード遅く</s>",'utf-8'):
				aplay = ['aplay','-q','rapras_kasoku.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				if speed < 10000:
					print(unicode("一時停止",'utf-8'))
					speed = 0
				else :
					speed = speed-5000
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				print(speed)
			if  c == unicode("<s>スピード普通</s>",'utf-8'):
				aplay = ['aplay','-q','rapras_kasoku.wav']
				wr = subprocess.Popen(aplay)
				time.sleep(2)	
				wr.terminate()
				speed = 20000
				L6470_run(0, v*speed)
				L6470_run(1, (-1)*v*speed)
				print(speed)
			data = ""

		quit()
