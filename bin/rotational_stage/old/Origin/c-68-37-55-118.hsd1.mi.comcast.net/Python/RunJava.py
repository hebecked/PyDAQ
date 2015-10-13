#!/usr/bin/env python

#     .' o)=-      *******************************************
#    /.-.'         * Script to compile and run java programs *
#   //  |\         * February 07, 2013                       *
#   ||  |'         * Andrew Ozimek                           *
# _,:(_/_          *******************************************

import subprocess

files = []
exit = False

path = raw_input('Path to java files --> ')

while exit == False:
    choice = input('\n1) Add java file to compile\n2) Compile selected files\n3) Run main class\n4) Exit\nEnter a choice to continue --> ')

    if choice == 1:
        f = raw_input('File name --> ')
        files.append(f)
    elif choice == 2:
        i = 0
        while i < len(files):
            subprocess.call('javac ' + path + files[i] , shell = True)
            i = i + 1
    elif choice == 3:
        main_class = raw_input('Main class file name --> ')

        subprocess.call('cd ' + path, shell = True)
        subprocess.call('java ' + main_class, shell = True)
    elif choice == 4:
        exit = True
    else:
        print 'Invalid Option'
