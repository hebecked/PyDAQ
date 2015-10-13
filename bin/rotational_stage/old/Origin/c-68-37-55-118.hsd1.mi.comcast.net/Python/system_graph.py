#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from subprocess import check_output
from time import sleep


def data_gen():
	time_incr = 0.5
	
	time = 0
	while True:
		
		temp_str = check_output('acpi -t', shell=True)
		temp = float(temp_str[15:19])
		
		time += time_incr
		sleep time_incr
