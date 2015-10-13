#!/usr/bin/python

import psutil
from time import sleep

memory = psutil.virtual_memory()

memory_file = open('/home/andrew/Desktop/memory.log', 'a')
cpu_file = open('/home/andrew/Desktop/cpu.log', 'a')

while True:
	# 1048576 bytes in one megabyte
	memory_used = memory.used / 1048576
	temp = check_output('acpi -t', shell=True)[15:19]
	
	
	cpu_file.write(str(psutil.cpu_percent(interval=1)) + '\n')
	memory_file.write(str(memory_used) + '\n')
	temperature_file.write(temp + '\n')
	
	sleep(0.1)

memory_file.close()
cpu_file.close()
