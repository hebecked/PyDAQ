#!/usr/bin/python2.7

import os, sys
from bin.parser_wrapper import parsers
from bin.monochromator import CornerStone260
import serial
import time
import bin.Data_IO as DIO

"""
Definig and reading input parameters and config Files.
"""

parser=parsers("This is a Monochromator control sub-/main-program for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

parser.add_argument( "GUI", "-gui", bool, group="config", default=False, help='Set this flag to use a graphical user interface to configure and supervise the DAQ.')
#parser.add_argument( "Port", "-p", str, group="basics", default=None, help='Sets the com port for the Monochromator.', required=True)
parser.add_argument( "Wavelength", "-wvl", float, group="Settings", default=None, help='Allows to set a wavelength manually in units of nm')
parser.add_argument( "OutPort", "-op", int, group="Settings", default=None, help='Allows to set the out port manually. (1-2)')
parser.add_argument( "Filter", "-f", int, group="Settings", default=None, help='Allows to set a Filter manually. (1-6)')
parser.add_argument( "Grating", "-g", int, group="Settings", default=None, help='Allows to set a Grating manually. (1-2{/3})')
parser.add_argument( "ShutterOpen", "-sO", bool, group="Settings", default=False, help='Will open the shutter')
parser.add_argument( "ShutterClose", "-sC", bool, group="Settings", default=False, help='Will close the shutter')
parser.add_argument( "Info", "-i", bool, group="Return", default=False, help='Gives a output on the current monochromator settings and type.') #possibly ad more Return options to obtain informations individually
parser.add_argument( "ReadPorts", "-rp", bool, group="Ports", default=False, help='Refreshes the device ports.')

arguments=parser.done(store_if_file_supplied=True)

ports=DIO.serialports().get_ports(refresh=arguments['ReadPorts']['val'])

cs = CornerStone260(port = ports['monochromator'])

if arguments["GUI"]['val']:
	print "TODO: Call GUI"

if arguments["ShutterClose"]['val']:
	cs.ShutterClose()

if arguments["OutPort"]['status']=='set': #1-6
	cs.OutPort(arguments["OutPort"]['val'])

if arguments["Filter"]['status']=='set': #1-6
	cs.Filter(arguments["Filter"]['val'])
	#print "Filter set to " + cs.GetFilter() + " with Label " cs.GetFilterLabel(arguments["Filter"]['val'])

if arguments["Grating"]['status']=='set':
	cs.Grat(arguments["Grating"]['val'])
	#print "Grating set to " + cs.GetGrat() + " with Label " cs.GratLabel(arguments["Grating"]['val'])

if arguments["Wavelength"]['status']=='set':
	cs.Units_NM()
	cs.GoWave(arguments["Wavelength"]['val'])
	print "Wavelength set to: " + cs.GetWave() + "nm"

if arguments["Info"]['val']:
	print cs.GetInfo()
	print "Unit: ", cs.GetUnits()
	print "Wavelength: ", cs.GetWave()
	print "Step: ", cs.GetStep()
	print "Grating (1-2{/3}): ", cs.GetGrat()
	print "Grating Label: ", cs.GetLines(int(cs.GetGrat().split(",")[0]))
	print "Grating factor: ", cs.GetFactor(int(cs.GetGrat().split(",")[0]))
	print "Grating Offset: ", cs.GetOffset(int(cs.GetGrat().split(",")[0]))
	print "Shutter State (0=open, C=closed): ", cs.GetShutter()
	print "Filter (1-6): ", cs.GetFilter()
	print "Filter Label: ", cs.GetFilterLabel(int(cs.GetFilter()))
	print "Out Port (1-2): ", cs.GetOutPort()
	print "Serial Port: ", cs.GetSerialPort()

if arguments["ShutterOpen"]['val']:
	cs.ShutterOpen()