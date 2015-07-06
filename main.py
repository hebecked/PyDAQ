#!/usr/bin/python2.7

import os, sys
import argparse
import ConfigParser

parser = argparse.ArgumentParser(description='This is a multifunction DAQ Program.')
parser.add_argument('-c', '--config', dest='CONF', action='store', type=str, default=None, help='Specify a config (.cfg) file to load.')

#initialize parsers
args = parser.parse_args()
config = ConfigParser.ConfigParser()


if args.CONF==None:
	config.read('./configs/default.cfg')
else:
	config.read('./configs/'+args.CONF+'.cfg')


if args.SPECT==None:
	if not config.has_option('files', 'spectrumWLS'):
		print "error no spectrum defined"
else:
	config.set('files','spectrumWLS',args.SPECT)




'''read 2 configs
1 settings config
1 todo config'''