#!/usr/bin/python

import urllib2

for i in range(101):
	response = urllib2.urlopen('http://www.google.com/')
	html = response.read()
	
	file = open('/home/andrew/Desktop/HTML/file_' + str(i) + '.html', 'w')
	file.write(html)
	file.close()


