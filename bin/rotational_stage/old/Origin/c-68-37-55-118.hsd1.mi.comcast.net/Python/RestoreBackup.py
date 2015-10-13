#!/usr/bin/env python

#******************************************************
#* Script to restore backups made with Backup.py      *
#* February 15, 2013                                  *
#* Andrew Ozimek                                      *
#******************************************************

import subprocess

loc_t = raw_input('Location of backup Tar:  ')
loc_e = raw_input('Extract to: ')

subprocess.call('sudo tar -xzvf ' + loc_t + ' -C' + loc_e, shell = True)

print 'Backup extracted to ', loc_e
