#!/usr/bin/python

import serial
import time

relay = serial.Serial('/dev/ttyUSB0')

relay.setDTR(True)
time.sleep(0.2)
relay.setDTR(False)
