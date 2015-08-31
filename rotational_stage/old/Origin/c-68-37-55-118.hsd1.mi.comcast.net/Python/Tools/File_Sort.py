#!/usr/bin/python

import os
from shutil import copyfile
from subprocess import call

# Script to copy files with a certian file extension to a specified directory


def list_all_files(path):
	'''Lists all files contained in a given directory, returns a list of those file paths and file names.
	Args: directory path (string)'''
	file_paths = []
	file_names = []

	for dirname, dirnames, filenames in os.walk(path):
		for filename in filenames:
			file_names.append(filename)
			file_paths.append(os.path.join(dirname, filename))
	
	return [file_names, file_paths]



search_dir = '/home/andrew/Documents'
file_extension = '.py'
copy_dir = '/home/andrew/Desktop/dir'

#search_dir = raw_input('Enter the directory to be searched: ')
#file_extension = raw_input('Enter a file extension: ')
#copy_dir = raw_input('Enter a new directory for the files to be transfered into: ')
files = list_all_files(search_dir)
file_paths = files[1]
file_names = files[0]

if not os.path.exists(search_dir):
	print '\n\nDirectory to be searched does not exist.'
	exit(1)
	
	
if copy_dir[:len(copy_dir)] == '/':
	copy_dir = copy_dir[:len(copy_dir - 1)]
	

if not os.path.exists(copy_dir):
	os.mkdir(copy_dir)




for i in range(0, len(file_names)):
	f = file_names[i]
	if f[len(file_names[i]) - len(file_extension):] == file_extension:
		try:
			copyfile(file_paths[i], (copy_dir + '/' +  file_names[i]))
		except IOError:
			print 'Copy directory unreadable.'
			exit(1)







