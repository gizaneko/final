# -*- coding: utf-8 -*-

import string
import wiringpi as wp
import time
import struct 
import signal
import sys
import subprocess

L6470_SPI_SPEED         = 1000000
STEPPING_TICK           = 200


BUSY_PIN_0      = 21
BUSY_PIN_1      = 20
io = wp.GPIO(wp.GPIO.WPI_MODE_GPIO)
io.pinMode(BUSY_PIN_0,io.INPUT)
io.pinMode(BUSY_PIN_1,io.INPUT)

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


		data = ""
		speed = 20000
		v = 1
		args = sys.argv
		diff = 0
		kp = 30
		if (len(args) == 4) :
		    	c = unicode(args[1], 'utf-8')
			kp = 30
			kd = 1
			dt = 0.1
			diff = kp*int(args[2])
			diff0 = kd*int(args[3])/dt #previous diff
			diff += int(diff0)
			print(diff)
		elif (len(args) == 3) :
			c = unicode(args[1], 'utf-8')
			kp = 30
			diff = kp*int(args[2])
			print(diff)
		else :
			quit()

		wp.wiringPiSPISetup (0, L6470_SPI_SPEED)
		wp.wiringPiSPISetup (1, L6470_SPI_SPEED)


		#L6470_init(0)
		#L6470_init(1)

		if c == unicode("RIGHT",'utf-8'):
			print ('Right diff:')
			print (diff)
			L6470_run(0, v*speed + diff)
			L6470_run(1, (-1)*v*speed + diff)
		if c == unicode("LEFT",'utf-8'):
			print ('Left diff:')
			print (diff)
			L6470_run(0, v*speed - diff)
			L6470_run(1, (-1)*v*speed - diff)
		if c == unicode("STOP",'utf-8'):
			print ('STOP')
			L6470_softstop(0)
			L6470_softstop(1)
			L6470_softhiz(0)
			L6470_softhiz(1)
		data = ""

		quit()
