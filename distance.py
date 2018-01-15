#!/usr/bin/env python

import time
import subprocess
from ctypes import *

class I2C:
    i2c_module = CDLL('./i2c.so')
    i2c_write_func_type = CFUNCTYPE(c_void_p, c_int *5)
    i2c_write_func = cast(i2c_module.i2c_write, i2c_write_func_type)
    i2c_read_func_type = CFUNCTYPE(c_void_p, c_char_p)
    i2c_read_func = cast(i2c_module.i2c_read, i2c_read_func_type)

    @classmethod
    def i2c_write(cls, angles):
        cls.i2c_write_func(angles)

    @classmethod
    def i2c_read(cls, stat):
        cls.i2c_read_func(stat);

#angle -> list (ex: [90,90,90,90,90])
def write_angles(angle):
    angle5 = c_int * 5
    angles = angle5(* angle)
    time.sleep(0.001)
    I2C.i2c_write(angles)

#bit1 = distance, bit2 = touch sensor status
def get_stat():
    stat = "aa"
    time.sleep(0.001)
    I2C.i2c_read(stat)
    return [int(stat[0].encode("hex"),16), int(stat[1].encode("hex"), 16)]

if __name__ == '__main__':
    angles = [90,90,90,90,90]
    list = get_stat()
    print list[0]
    print list[1]
    if (list[1] == 0):
        write_angles(angles)
    quit()
    #angle5 = c_int * 5
    #angle = [90, 90, 90, 90, 90]
    #angles = angle5(* angle)
    #stat = "aa"
    #I2C.i2c_read(stat)
    #print int(stat[0].encode("hex"), 16)
    #print int(stat[1].encode("hex"), 16)
    #if (int(stat[1].encode("hex")) == 0) :
    #    I2C.i2c_write(angles)
    #quit()
