import os, sys
import argparse
import ConfigParser

class parsers:
	"""
	A small wrapper to merge argparse and ConfigParser.
	There are other possibly easier ways to do this.
	However this wrapper has a view advantages.
	You just include it and use it as you used argparse before with the additional comfort of 
	being able to store them in a config. While it is still possible to overwrite them with a command line flag.
	"""

	def __init__(self, description):
		"""Constructor initialising things and setting command line flags for config parsing"""
		self.parser = argparse.ArgumentParser(description=description + '\nComandline arguments are allways more dominant than a config file.')
		self.parser.add_argument('-c', '--config', dest="CONFIG", action='store', type=str, default=None, help='Specifies the suplementary config file.')
		self.parser.add_argument('-sc', '--store-config', dest="SCONFIG", action='store', type=str, default=None, help='Specifies a config file to store modifications.')
		self.elements = {}

	def add_argument(self, name, flag, datatype, group="Defaults", default=None, help='', required=False, multiargs=False):# if conditions for type
		"""
		Adds an argument to be used and its properties
		It is recommended to use capital LETTERS
		"""
		if not isinstance(datatype, type):
			print "You need to supply a datatype for datatype"
		if multiargs:
			self.parser.add_argument(flag, '--' + name, dest=name, action='store', type=datatype, default=default, help=help, nargs='+')
		elif datatype==bool:
			if default==True:
				self.parser.add_argument(flag, '--' + name, dest=name, action='store_false', type=bool, default=True, help=help)
			else:
				self.parser.add_argument(flag, '--' + name, dest=name, action='store_true', type=bool, default=True, help=help)
		else:
			self.parser.add_argument(flag, '--' + name, dest=name, action='store', type=datatype, default=default, help=help)
		self.elements[name]={'type': datatype, 'status': 'init', 'required': required, 'group': group, 'multiargs': multiargs}

	def done(self):
		"""
		After adding all the arguments you need this to do all the conversions.
		It will return a dict including all arguments set and their properties.
		It is not mandatory to use this dict. The functions isSet and get can be used instead. 
		"""
		self.args = self.parser.parse_args()
		self.config = ConfigParser.ConfigParser()
		if not self.args.CONFIG==None:
			self.config.read(self.args.CONFIG)
			config_args=_as_dict(self.config)
		else:
			config_args={}
		cmd_args=vars(self.args)
		for name in self.elements:
			if name in cmd_args.keys() and not cmd_args[name]==None:
				try:
					val=self.elements[name]['type'](cmd_args[name])
				except:
					print str(cmd_args[name])+ " is not " + str(self.elements[name]['type'])
					exit()
				self.elements[name].update({'val': val, 'status': "set"})
			else:
				if self.elements[name]['group'] in config_args.keys() and name in config_args[self.elements[name]['group']].keys() and not config_args[self.elements[name]['group']][name]==None:
					try:
						val=self.elements[name]['type'](config_args[self.elements[name]['group']][name])
					except:
						print str(config_args[self.elements[name]['group']][name])+ " is not " + str(self.elements[name]['type'])
						exit()
					self.elements[name].update({'val': val, 'status': "set"})
				else:
					if self.elements[name]['required']:
						print "Error the element " + self.elements[name] + " is required.\n Pleas supply by flag or config.\n[EXITING]"
						exit()
					else:
						self.elements[name].update({'val': None, 'status': "notset"})
		return self.elements

	def _as_dict(config):
		"""
		Converts a ConfigParser object into a dictionary.
		The resulting dictionary has sections as keys which point to a dict of the
		sections options as key => value pairs.
		"""
		the_dict = {}
		for section in config.sections():
			the_dict[section] = {}
			for key, val in config.items(section):
				the_dict[section][key] = val
		return the_dict


	def isSet(self,name):
		"""Returns True or False depending on whether a variable is set or not""" 
		if self.elements[name]['set']=="notset":
			return False
		return True



	def get(self,name, propperty='val'):
		"""
		Returns by default the value accociated with a variable name.
		however properties can be returned too.
		Propperties currently are: 'type','status','required','multiargs' and 'group'
		Use all to get a dict with all properties
		"""
		if propperty=="all":
			return self.elements[name]
		return self.elements[name][propperty]

	def set(self,name, val, datatype=None, group="Defaults", multiargs=False):
		"""
		This function allows to add additional arguments during runtime.
		This might be use full for iterative program execution (e.g. on a Farm).
		They are stored when the other values are stored, too.
		"""
		if datatype==None:
			datatype=type(val)
		self.elements[name]={'group': group,'multiargs': multiargs,'required': False,'status': 'set','type': datatype, 'val': val}


	def storeConfig(self,filename='__'):
		"""
		Stores the current set of configurations to file.
		Be aware that here also the command line flag is more dominant than any filename you supply as default!!!
		(this is a feature not a bug)
		"""
		new_dict = {}
		new_confparser=ConfigParser.ConfigParser()
		for name in self.elements:
			new_dict[self.elements[name]['group']]={}
		for name in self.elements:
			new_dict[self.elements[name]['group']].update({name:self.elements[name]['val']})
		for group in new_dict:
			new_confparser.add_section(group)
			for val in new_dict[group]:
				new_confparser.set(group,val,new_dict[group][val])
		if not self.args.SCONFIG==None:
			filename = self.args.SCONFIG
		else:
			if filename=='__':
				print "Please, specify a file name to store the config file."
		with open(filename, 'wb') as configfile:
			new_confparser.write(configfile)

