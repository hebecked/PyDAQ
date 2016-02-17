#!/usr/bin/python2.7

import os, sys
from bin.parser_wrapper import parsers
#import GUI
from bin.DAQ.DAQ_frontend import DAQ_handler
import multiprocessing
import time
import bin.Data_IO as DIO
import json

"""
Definig and reading input parameters and config Files.
"""
parser=parsers("This Program is meant as a DAQ for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

parser.add_argument( "InstructionFile", "-i", str, group="config", default=None, help='Please supply a instruction file describing all measurement steps. "-ih" will give you a format description.')
parser.add_argument( "InstructionFileHelp", "-ih", bool, group=None, default=False, help='Gives out the format of the instruction file and exits.')
parser.add_argument( "OutputFile", "-o", str, group="config", default="results.txt", help='Supply a file name for the results of the measurements')
parser.add_argument( "GUI", "-g", bool, group="config", default=False, help='Set this flag to use a graphical user interface to configure and supervise the DAQ. Runs won\'t start right away')
#parser.add_argument( "SignalLockInPort", "-slp", str, group="LockIn", default=None, help='Sets the com port for the signal Lock-In.', required=True)
#parser.add_argument( "ReferenceLockInPort", "-rlp", str, group="LockIn", default=None, help='Sets the com port for the reference Lock-In.', required=True)
#parser.add_argument( "XYZ_ScannerPort", "-sp", str, group="XYZ_Scanner", default=None, help='Sets the com port for the XYZ Scanner.', required=True)
#parser.add_argument( "MonochromatorPort", "-mp", str, group="Monochromator", default=None, help='Sets the com port for the Monochromator.', required=True)
#parser.add_argument( "RotationalPlatformPort", "-rp", str, group="RotationalPlatform", default=None, help='Sets the port for the RotationalPlatform.', required=True)
parser.add_argument( "ReadPorts", "-rp", bool, group="Ports", default=False, help='Refreshes the device ports.')
parser.add_argument( "XYZ_ScannerSafetyZone", "-ssz", list, group="XYZ_Scanner", default=[0,100], help='Please supply a safety range along the x-axis for your experiment in units of percent.', multiargs=True, multiargsn=2, required=True)

#TODo add flags for showing plots in command line mode

arguments=parser.done(store_if_file_supplied=True)

if arguments["InstructionFileHelp"]['val']:
	print "TODO: help"
	exit()

if arguments["GUI"]['val']:
#	gui=GUI(parser)
	pass
	#exit()
path2outfile = os.path.split(os.path.abspath(sys.modules['__main__'].__file__))[0]
outfile = os.path.join(path2outfile, arguments["OutputFile"]["val"] + time.strftime("_%d.%m.%y_%H.%M.result"))

#simple for the beginning, do error handling LATER

ports=DIO.serialports().get_ports(refresh=arguments['ReadPorts']['val'])
#ports={'monochromator':arguments["MonochromatorPort"]['val'], "xyz-scanner":arguments['XYZ_ScannerPort']['val'], 'sLockIn':arguments["SignalLockInPort"]['val'], 'rLockIn':arguments["ReferenceLockInPort"]['val'], 'rotPlatform':arguments["RotationalPlatformPort"]['val']}
daq=DAQ_handler(arguments["InstructionFile"]['val'], ports, outfile)

while daq.update()=='Running':
	#print "test"
	time.sleep(1)


'''
TODO:

safety zone (1 dimension for now)
add option to show plots on comandline
check (pos) bug on xyz
check "done" returne bug on XYZ
wait for positioning on xyz
make it possible for all commandline tools to use the same config file
'''