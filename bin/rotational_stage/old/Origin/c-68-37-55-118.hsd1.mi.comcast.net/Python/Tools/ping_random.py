#!/usr/bin/python

import subprocess
import random

def findIP():
	found_ip = False
	
	while not found_ip:
		r1 = str(random.randint(1, 250))
		r2 = str(random.randint(1, 250))
		r3 = str(random.randint(1, 250))
		r4 = str(random.randint(1, 250))
		ip = r1 + '.' + r2 + '.' + r3 + '.' + r4
    
		print "Pinging %s" % ip
		ret = subprocess.call("ping -c 1 %s" % ip,
			shell=True,
			stdout=open('/dev/null', 'w'),
			stderr=subprocess.STDOUT)
		if ret == 0:
			print "%s: is alive" % ip
			found_ip = True
		else:
			print "%s: did not respond\n" % ip
		
	return ip

done = False

while not done:	
	ip = findIP()
	
	c = raw_input('\nConnect to %s? [y/n]: ' % ip)
	
	if c == 'y':
		done = True
		print '\nconnecting to ' + ip + ' via ssh\n'
		ret = subprocess.call("ssh " + ip, shell=True)
		
		if ret == 0:
			c = raw_input('Look for another ip address? [y/n]: ')
	
			if c == 'y':
				done = False
			elif c == 'n':
				done = True
				print '\nProgram exiting...'
			else:
				done = True
				print 'Invalid Input'
		else:
			print '\nError connecting to ', ip, ' ssh exit code: ', ret
			
			print '\nconnecting to ' + ip + ' via telnet\n'
			ret = subprocess.call("telnet " + ip, shell=True)
		
			if ret == 0:
				c = raw_input('Look for another ip address? [y/n]: ')
	
				if c == 'y':
					done = False
				elif c == 'n':
					done = True
					print '\nProgram exiting...'
				else:
					done = True
				print 'Invalid Input'
			else:
				print '\nError connecting to ', ip, ' telnet exit code: ', ret
				
				c = raw_input('Look for another ip address? [y/n]: ')
	
				if c == 'y':
					done = False
				elif c == 'n':
					done = True
					print '\nProgram exiting...'
				else:
					done = True
					print 'Invalid Input'
			
	elif c == 'n':
		c = raw_input('Look for another ip address? [y/n]: ')
	
		if c == 'y':
			done = False
		elif c == 'n':
			done = True
			print '\nProgram exiting...'
		else:
			done = True
			print 'Invalid Input'
	else:
		done = True
		print 'Invalid Input'
