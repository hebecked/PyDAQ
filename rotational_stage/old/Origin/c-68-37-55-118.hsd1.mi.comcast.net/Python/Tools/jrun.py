#!/usr/bin/python3

# Author: Andrew Ozimek

# This script is used to compile then run Java class files, using the java and javac programs.
# This script takes an absolute or relatiove directory path to a Jave source file as its first argument;
# and subsequent arguments are passed to the java class being run.

from os.path import isfile
from subprocess import call
from subprocess import check_output
from sys import argv # argv returns a list variable of command-line arguments: argv == ['/current/working/directory', 'argument', 'argument1', ...]

try:
	# Check to make sure the command-line argument is a path to a file that exists
	if len(argv) >= 2:
		# If the absolute directory path is not given, add it to the file name
		if not ('/' in argv[1]):
			# Returns the current directory, which is not the directory this script is run from;
			# it is the current directory of the bash shell this script is run from 
			cd = str(check_output('readlink -f .', shell=True))
			
			# Adds the directory path to an argument without one
			argv[1] = cd[2:len(cd) - 3] + '/' + argv[1]
		
		# Make sure the file given actually exists
		if isfile(argv[1]):
			file_argument = argv[1]
			
			# Check to make sure the file has the '.java' extension
			if file_argument[len(file_argument) - 5:] == '.java':
		
				# Compile the java file using javac
				exit_status = call('javac \"%s\"' % (file_argument), shell=True)
			
				# Finding the index of the character just before the last '/' in the file path (used to isolate 'filename.java')
				if exit_status == 0:
					slash = ''
					i = len(file_argument) - 1
					while slash != '/':
						slash = file_argument[i]
						i -= 1
			
					# Build command string: cd into the java file's directory, and use java to run the .class file
					command_str = 'cd \"%s\" && java %s' % (file_argument[:i + 1], file_argument[i + 2:len(file_argument) - 5])
					
					# Add command line arguments to be passed to java class
					for i in range(2, len(argv)):
						command_str += ' ' + argv[i]
					
					# Run command string
					call(command_str, shell=True)
					
				else:
					# Throws an error and stops the script when javac encounters an error
					print('\nError: javac returned non-zero exit status.')
			else:
				# Throws an error and stops the script when the file argument doesn't have a .java extension
				print('Error: File is not a java file, \'.java\' file extension is missing.')
		else:
			# Throws an error and stops the script when the file argument does not exist
			print('Error: File does not exist')
	else:
		# Throws an error and stops the script when there is not exactly 2 arguments (current working directory and file to run)
		print('Error: Incorrect number of arguments. Usage:  jrun [path to java file] [arguments for java class (optional)]')
except KeyboardInterrupt: # Recover nicely from a keyboardInterrupt (CTRL+C) instead of stack trace
	# Tell user the program is exiting
	print('\n\nExiting program -- KeyboardIterrupt')
