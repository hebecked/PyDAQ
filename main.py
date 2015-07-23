#!/usr/bin/python2.7

import os, sys
from parser_wrapper import parsers
import GUI
import DAQ

"""
Definig and reading input parameters and config Files.
"""
parser=parsers("This Program is meant as a DAQ for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

parser.add_argument( "InstructionFile", "-i", str, group="config", default=None, help='Please supply a instruction file describing all measurement steps. "-ih" will give you a format description.')
parser.add_argument( "InstructionFileHelp", "-ih", bool, group=None, default=False, help='Gives out the format of the instruction file and exits.')
parser.add_argument( "OutputFile", "-o", str, group="config", default="results.txt", help='Supply a file name for the results of the measurements')
parser.add_argument( "GUI", "-g", bool, group="config", default=True, help='Set this flag to use a graphical user interface to configure and supervise the DAQ. Runs won\'t start right away')
parser.add_argument( "SignalLockInPort", "-slp", str, group="LockIn", default=None, help='Sets the com port for the signal Lock-In.', required=True)
parser.add_argument( "ReferenceMLockInPort", "-rlp", str, group="LockIn", default=None, help='Sets the com port for the reference Lock-In.', required=True)
parser.add_argument( "XYZ_ScannerPort", "-sp", str, group="XYZ_Scanner", default=None, help='Sets the com port for the XYZ Scanner.', required=True)
parser.add_argument( "MonochromatorPort", "-mp", str, group="Monochromator", default=None, help='Sets the com port for the Monochromator.', required=True)
parser.add_argument( "RotationalPlatformPort", "-rp", str, group="RotationalPlatform", default=None, help='Sets the port for the RotationalPlatform.', required=True)
parser.add_argument( "XYZ_ScannerSafetyZone", "-ssz", list, group="XYZ_Scanner", default=[0,100], help='Please supply a safety range along the x-axis for your experiment in units of percent.', multiargs=True, multiargsn=2, required=True)
###print "The following commands are only used for manual control of the devices. If aa instruction is supplied as well the will be run before the files instructions."
parser.add_argument( "XYZ_ScannerUnit", "-su", str, group="XYZ_Scanner", default="mm", help='Defines the unit in which positions are supplied. (Only for manual use, not valid for instruction files.)')
parser.add_argument( "XPos", "-xp", float, group="XYZ_Scanner", default=None, help='Moves in absolute positions on the x-axis. Supply a unit of measure with -su, the default is "mm". Will be run before -i.')
parser.add_argument( "YPos", "-yp", float, group="XYZ_Scanner", default=None, help='Moves in absolute positions on the y-axis. Supply a unit of measure with -su, the default is "mm". Will be run before -i.')
parser.add_argument( "ZPos", "-zp", float, group="XYZ_Scanner", default=None, help='Moves in absolute positions on the z-axis. Supply a unit of measure with -su, the default is "mm". Will be run before -i.')
parser.add_argument( "XPosR", "-xpr", float, group="XYZ_Scanner", default=None, help='Moves in relative positions on the x-axis. Supply a unit of measure with -su, the default is "mm". Will be run before -i.')
parser.add_argument( "YPosR", "-ypr", float, group="XYZ_Scanner", default=None, help='Moves in relative positions on the y-axis. Supply a unit of measure with -su, the default is "mm". Will be run before -i.')
parser.add_argument( "ZPosR", "-zpr", float, group="XYZ_Scanner", default=None, help='Moves in relative positions on the z-axis. Supply a unit of measure with -su, the default is "mm". Will be run before -i.')
parser.add_argument( "angle1", "-a1", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 1 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
parser.add_argument( "angle2", "-a2", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 2 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
parser.add_argument( "angle3", "-a3", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 3 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
parser.add_argument( "angle1r", "-a1r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 1 relative to the current position in units of degree. Will be run before -i.')
parser.add_argument( "angle2r", "-a2r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 2 relative to the current position in units of degree. Will be run before -i.')
parser.add_argument( "angle3r", "-a3r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 3 relative to the current position in units of degree. Will be run before -i.')
parser.add_argument( "Wavelength", "-wvl", float, group="Monochromator", default=None, help='Allows to set a wavelength manually in units of nm')
parser.add_argument( "ReadSignalLockIn", "-rsl", bool, group="LockIn", default=False, help='Will print the current value of the signal Lock-In to the comandline.')
parser.add_argument( "ReadReferenceLockIn", "-rrl", bool, group="LockIn", default=False, help='Will print the current value of the reference Lock-In to the comandline.')
#TODo add flags for showing plots in command line mode


arguments=parser.done()

if arguments["InstructionFileHelp"]['val']:
	print "TODO: help"
	exit()

if arguments["SCONFIG"]['status']=='set':
	parser.storeConfig()

if arguments["GUI"]['val']:
	gui=GUI(parser)


'''
Variables:
store config

config file
measurement file
output files
Gui?
manual positioning of (xyz rot1, rot2, wvl)
manual read lockin
safety zone (1 dimension for now)

'''