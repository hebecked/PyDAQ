import os, sys
import argparse
import ConfigParser




class parsers:

	def __init__(self, description):
		parser = argparse.ArgumentParser(description=description)
		self.elements = {}


	def add_argument(self,name, type, group, flag, default=None, help=''):# if conditions for type
		self.parser.add_argument(flag, '--' + name, dest=name, action='store', type=type, default=default, help=help)
		self.elements[name]=type

	def done(self):
		self.args = parser.parse_args()
		self.config = ConfigParser.ConfigParser()


	def isSet(self,name):
		if self.elements[name]==None and not config.has_option(type, name)::


	def storeConfig(self,filename):



if args.CONF==None:
	config.read('./configs/default.cfg')
else:
	config.read('./configs/'+args.CONF+'.cfg')


if args.SPECT==None:
	if not config.has_option('files', 'spectrumWLS'):
		print "error no spectrum defined"
else:
	config.set('files','spectrumWLS',args.SPECT)
