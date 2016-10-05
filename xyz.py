#!/usr/bin/python2.7

import os, sys
from bin.parser_wrapper import parsers
import serial
import time
import numpy as np
from bin.XYZ_Scanner.Scanner import Scanner
import bin.Data_IO as DIO

"""
Definig and reading input parameters and config Files.
"""


parser=parsers("This is a XYZ Scanner control sub-/main-program for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

parser.add_argument( "GUI", "-gui", bool,group="config",default=False,help='"set" this flag to use a graphical user interface to configure and supervise the DAQ.')
#parser.add_argument( "Port", "-p", str,group="basics",default=None,help='"set"s the com port for the XYZ scanner.',required=True)
parser.add_argument( "Inited", "-i", bool,group="basics",default=False,help='Makes the programm assume the scanner is already initialized. Therefore it does not go back to (0,0,0). This makes it impossible to use some of the safety features.')
parser.add_argument( "XYZ_ScannerUnit", "-su", str,group="XYZ_Scanner",default="mm",help='Defines the unit in which positions are supplied. (Only for manual use, not valid for instruction files.)')
parser.add_argument( "XPos", "-xp", float,group="XYZ_Scanner",help='Moves in absolute positions on the x-axis. Supply a unit of measure with -su, the default is "mm".')
parser.add_argument( "YPos", "-yp", float,group="XYZ_Scanner",default=None,help='Moves in absolute positions on the y-axis. Supply a unit of measure with -su, the default is "mm".')
parser.add_argument( "ZPos", "-zp", float,group="XYZ_Scanner",default=None,help='Moves in absolute positions on the z-axis. Supply a unit of measure with -su, the default is "mm".')
parser.add_argument( "XPosR", "-xpr", float,group="XYZ_Scanner",default=None,help='Moves in relative positions on the x-axis. Supply a unit of measure with -su, the default is "mm". Only usefull with -i. Runs after absolute positioning. (Not funktional due to firmwarebug)')
parser.add_argument( "YPosR", "-ypr", float,group="XYZ_Scanner",default=None,help='Moves in relative positions on the y-axis. Supply a unit of measure with -su, the default is "mm". Only usefull with -i. Runs after absolute positioning. (Not funktional due to firmwarebug)')
parser.add_argument( "ZPosR", "-zpr", float,group="XYZ_Scanner",default=None,help='Moves in relative positions on the z-axis. Supply a unit of measure with -su, the default is "mm". Only usefull with -i. Runs after absolute positioning. (Not funktional due to firmwarebug)')
parser.add_argument( "ReadPorts", "-rp", bool, group="Ports", default=False, help='Refreshes the device ports.')

arguments=parser.done(store_if_file_supplied=True)

if arguments["GUI"]["val"]:
    print "TODO goto GUI"
    exit()

ports=DIO.serialports().get_ports(refresh=arguments['ReadPorts']['val'])

sc=Scanner(port=ports["xyz-scanner"], do_refrun=not arguments["Inited"]["val"],smooth_move=False,debug=False, show=False)


if arguments["XYZ_ScannerUnit"]['status']=="set":
	unit=arguments["XYZ_ScannerUnit"]["val"]
else:  
	unit="mm"

if arguments["XPos"]['status']=="set" or arguments["YPos"]['status']=="set" or arguments["ZPos"]['status']=="set":
	# x,y,z=sc.read_position()
	if arguments["XPos"]['status']=="set":
		x=arguments["XPos"]["val"]
	if arguments["YPos"]['status']=="set":
		y=arguments["YPos"]["val"]
	if arguments["ZPos"]['status']=="set":
		z=arguments["ZPos"]["val"]
	sc.move_to(x,y,z, unit=unit ,go=True,smooth_move=False,show=False,sequenced=False,history_forward=False,clean_forward=True)

if arguments["XPosR"]['status']=="set" or arguments["YPosR"]['status']=="set" or arguments["ZPosR"]['status']=="set":
	if arguments["XPosR"]['status']=="set":
		x=arguments["XPosR"]["val"]
	else:
		x=0
	if arguments["YPosR"]['status']=="set":
		y=arguments["YPosR"]["val"]
	else:
		y=0
	if arguments["ZPosR"]['status']=="set":
		z=arguments["ZPosR"]["val"]
	else:
		z=0
	sc.shift_to(x,y,z, unit=unit ,go=True,smooth_move=False,show=False,sequenced=False,history_forward=False,clean_forward=True)