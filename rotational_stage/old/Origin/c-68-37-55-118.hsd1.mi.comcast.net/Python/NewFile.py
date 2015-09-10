#!/usr/bin/env python 

#     .' o)=-      *******************************
#    /.-.'         * Script to create a new file *
#   //  |\         * January 23, 2013            *
#   ||  |'         * Andrew Ozimek               *
# _,:(_/_          *******************************

import getpass

type = raw_input('What type of file? Python, Java, or other.  [p/j/o]: ')

if type == 'p':
    ext = '.py'
elif type == 'j':
    ext = '.java'
elif type == 'o':
    ext = raw_input('File extension: ')
else:
    print 'Invalid Option'

default = raw_input('Use default directory? /home/' + getpass.getuser() + '/Desktop/ [y/n]: ')

if default == 'y':
    path = '/home/' + getpass.getuser() + '/Desktop/'
elif default == 'n':
    path = raw_input('Path to the file: ')
else:
    print 'Invalid Option'

filenm = raw_input('File name: ')

pathtofile = path + filenm + ext

error = True

try:
    file = open(pathtofile, 'w')
    file.write('')
    file.close()
except IOError:
    print 'Error creating file.'
    error = True

if error == False:
    print 'File created: ', pathtofile
