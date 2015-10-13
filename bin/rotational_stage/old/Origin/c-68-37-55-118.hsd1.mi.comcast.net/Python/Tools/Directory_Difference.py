#!/usr/bin/Python3

# ***************************************************************
# * Script to compare the contents of one directory to another. *
# * Compatable with both Linux and Windows                      *
# * Written: March 25, 2015                                     *
# ***************************************************************

import os


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




dir_1 = input('Enter the absolute path for the first directory: ')
dir_2 = input('Enter the absolute path for the second directory: ')

#dir_1 = '/home/andrew/Desktop/Python_Copy'
#dir_2 = '/home/andrew/Documents/Python'

# Output files
match_file = open(os.getcwd() + '/matches.txt', 'w')
not_matched_file = open(os.getcwd() + '/not_matched.txt', 'w')


if os.path.exists(dir_1) and os.path.exists(dir_2):
	dir_1_abs = list_all_files(dir_1)[1]
	dir_2_abs = list_all_files(dir_2)[1]
	dir_1_files = []
	dir_2_files = []
	
	match_str = ''
	not_matched_str = ''
	
	# Remove the dir_1 and dir_2 paths from dir_1_files and dir_2_files
	for f in dir_1_abs:
		dir_1_files.append(f[len(dir_1):])
	
	for f in dir_2_abs:
		dir_2_files.append(f[len(dir_2):])
				
	# Sorting into matched and not_matched
	matched = []
	not_matched = []
	
	if len(dir_1_files) > len(dir_2_files):
		for i in range(len(dir_1_files)):
			if dir_1_files[i] in dir_2_files:
				matched.append(dir_1_abs[i])
				matched.append(dir_2_abs[dir_2_files.index(dir_1_files[dir_1_files.index(dir_1_files[i])])])
			else:
				not_matched.append(dir_1_abs[i])
		for i in range(len(dir_2_files)):
			if dir_2_files[i] not in dir_1_files:
				not_matched.append(dir_2_abs[i])
	else:
		for i in range(len(dir_2_files)):
			if dir_2_files[i] in dir_1_files:
				matched.append(dir_2_abs[i])
				matched.append(dir_1_abs[dir_1_files.index(dir_2_files[dir_2_files.index(dir_2_files[i])])])
			else:
				not_matched.append(dir_2_abs[i])
		for i in range(len(dir_1_files)):
			if dir_1_files[i] not in dir_2_files:
				not_matched.append(dir_1_abs[i])
	
	
	# create strings out of matched and not_matched
	i = 0
	while i < len(matched):
		match_str += matched[i] + '\n' + matched[i + 1] + '\n\n'
		i += 2
		
	for i in range(len(not_matched)):
		not_matched_str += not_matched[i] + '\n'
	
	
	# Writing to files
	match_file.write(match_str)
	not_matched_file.write(not_matched_str)
	
	match_file.close()
	not_matched_file.close()
	
else:
	print('Error: Directory %s or directory %s does not exist.' % (dir_1, dir_2))













