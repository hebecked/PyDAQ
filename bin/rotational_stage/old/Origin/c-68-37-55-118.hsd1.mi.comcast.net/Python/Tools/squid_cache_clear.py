#!/usr/bin/python

# This script is written to clear Squid3 proxy server cache at timed intervals.
#
# The script is written to stop running instance of squid3, delete cache, then 
# start squid3 afterwards; at a specified interval.

from subprocess import call
import time


# Option Constants
# Time to remove cache [hour, minute], 24-hour time format
EXECUTION_TIME = [23, 21]
CACHE_DIRECTORY = '/home/andrew/Desktop/cache'




def get_current_time():
	'''Gets current UTC time and returns the current hour and minute as integers (24-hour format)'''
	
	current_utc = time.ctime(time.time())
	current_time = current_utc[11:19]
	current_hour = int(current_time[0:2])
	current_minute = int(current_time[3:5])
	
	return [current_hour, current_minute]


error_status = False


while not error_status:
	
	exit_status = 0
	
	if get_current_time() == EXECUTION_TIME:
		exit_status = call('service squid3 stop', shell=True)
		
		if exit_status > 0:
			error_status = True
		
		exit_status = call('rm -R %s/*' % (CACHE_DIRECTORY), shell=True)
		
		if exit_status > 0:
			error_status = True
		
		exit_status = call('service squid3 start', shell=True)
		
		if exit_status > 0:
			error_status = True
		
		time.sleep(60)
		
		
	
	time.sleep(0.16)























