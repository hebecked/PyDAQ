#!/usr/bin/python

import serial
import time

relay = serial.Serial('/dev/ttyUSB0')


relay.setDTR(False)
dot = 0.05
dash = 0.07

c = [dot, dash, dash, dot, dash, dot, dot, dot, dash, dot, dot, dot, dash, dash, 0.0, dash, dash, dash, dash, dash, dot, dot, dot, dot, dash, dash, dot, dash, dot, dash]

for i in c:
	relay.setDTR(True)
	time.sleep(i)
	relay.setDTR(False)
	time.sleep(0.05)

