#!/usr/bin/python

import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=10)



print ser.read(100)

ser.close()
