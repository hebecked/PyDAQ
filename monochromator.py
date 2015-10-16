#!/usr/bin/python2.7

import os, sys
from bin.parser_wrapper import parsers
from bin.monochromator import CornerStone260
import serial
import time


"""
Definig and reading input parameters and config Files.
"""

parser=parsers("This is a Monochromator control sub-/main-program for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

parser.add_argument( "GUI", "-gui", bool, group="config", default=False, help='Set this flag to use a graphical user interface to configure and supervise the DAQ.')
parser.add_argument( "Port", "-p", str, group="basics", default=None, help='Sets the com port for the Monochromator.', required=True)
parser.add_argument( "Wavelength", "-wvl", float, group="Settings", default=None, help='Allows to set a wavelength manually in units of nm')
parser.add_argument( "Filter", "-f", int, group="Settings", default=None, help='Allows to set a Filter manually')
parser.add_argument( "Grating", "-g", int, group="Settings", default=None, help='Allows to set a Grating manually')
parser.add_argument( "ShutterOpen", "-so", bool, group="Settings", default=False, help='Will open the shutter')
parser.add_argument( "ShutterClose", "-sc", bool, group="Settings", default=False, help='Will close the shutter')
parser.add_argument( "Info", "-i", float, group="Return", default=None, help='Gives a output on the current monochromator settings') #possibly ad more Return options to obtain informations individually

arguments=parser.done(store_if_file_supplied=True)

cs = CornerStone260( port = arguments["Port"])

if arguments["SCONFIG"]['status']=='set':
	parser.storeConfig()

if arguments["GUI"]['val']:
	print "TODO: Call GUI"

if arguments["Wavelength"]['status']=='set':
	cs.Units_NM()
	cs.GoWave(arguments["Wavelength"]['val'])
	print "Wavelength set to: " + cs.GetWave() + "nm"

if arguments["Filter"]['status']=='set':
	cs.Filter(arguments["Filter"]['val'])
	#print "Filter set to " + cs.GetFilter() + " with Label " cs.GetFilterLabel(arguments["Filter"]['val'])

if arguments["Grating"]['status']=='set':
	cs.Grat(arguments["Grating"]['val'])
	#print "Grating set to " + cs.GetGrat() + " with Label " cs.GratLabel(arguments["Grating"]['val'])

if arguments["ShutterOpen"]['val']:
	cs.ShutterOpen()

if arguments["ShutterClose"]['val']:
	cs.ShutterClose()

if arguments["Info"]['val']:
	print cs.GetInfo()