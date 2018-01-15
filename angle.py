import RPi.GPIO as GPIO
import time
import sys
import signal

PIN = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
servo = GPIO.PWM(PIN, 50)

def exit_handler(signal, frame):
	print("\nExit")
	servo.stop()
	GPIO.cleanup()
	quit()

signal.signal(signal.SIGINT, exit_handler)

if __name__ == '__main__':
	servo.start(0.0)
	while True:
		input = sys.stdin.readline()
		angle = int(input)
		if (angle > 180 and angle < 0):
			continue
		else:
			dc = 2.5 + 9.5*angle/180
			print('duty cycle : %d' %(dc))
		servo.ChangeDutyCycle(dc)
			


