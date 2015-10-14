#!/usr/bin/python

import os
from sys import exit


directory = set()
compare_dir = set()

main_dir = raw_input('Enter the directory path to compare to: ')
comp_dir = raw_input('Enter directory path to compare: ')

if os.path.isdir(main_dir) and os.path.isdir(comp_dir):
	#add directory files to set
	for dirname, dirnames, filenames in os.walk(main_dir):
		for filename in filenames:
			directory.add(os.path.join(dirname, filename))
	
	#add comparison directory files to set
	for dirname, dirnames, filenames in os.walk(comp_dir):
		for filename in filenames:
			compare_dir.add(os.path.join(dirname, filename))
			
elif not os.path.isdir(main_dir) and not os.path.isdir(comp_dir):
	print 'Error: Directories %s and %s do not exist.' % (main_dir, comp_dir)
	exit()
elif not os.path.isdir(main_dir):
	print 'Error: Directory %s does not exist.' % (main_dir)
	exit()
elif not os.path.isdir(comp_dir):
	print 'Error: Directory %s does not exist.' % (comp_dir)
	exit()


for f in compare_dir:
	if not f in directory:
		print 'File/directory %s does not exist in comparison directory' % (f)
