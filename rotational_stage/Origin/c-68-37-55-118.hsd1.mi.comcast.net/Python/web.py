#!/usr/bin/env python

import urllib

filehandle = urllib.urlopen('http://www.techyupdates.blogspot.com')

for lines in filehandle.readlines():
   print lines

filehandle.close()
