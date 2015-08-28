#! /usr/bin/python

from serial import Serial
from time import sleep


##### Defining Power State Functions #####

motor = Serial('/dev/ttyUSB0')

motor.setDTR(False)

def power_on():
	motor.setDTR(True)

def power_off():
	motor.setDTR(False)



##### Power Status Logic #####

# Create inital vacuum
power_on()
sleep(37)
power_off()

i = 0

while i < 0:
	sleep(300)
	power_on()
	sleep(32)
	power_off()
	
	i +=1
