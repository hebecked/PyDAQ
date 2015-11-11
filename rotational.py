#!/usr/bin/python2.7

import os, sys
from bin.parser_wrapper import parsers
from bin.rotational_stage.rotLib import rotStages
import time
import serial
import struct
import numpy as np
import bin.Data_IO as DIO

"""
Definig and reading input parameters and config Files.
"""


parser=parsers("This Program is meant as a DAQ for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")
##move to sub processes:
parser.add_argument( "angle1", "-a1", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 1 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
parser.add_argument( "angle2", "-a2", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 2 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
parser.add_argument( "angle3", "-a3", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 3 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
parser.add_argument( "angle1r", "-a1r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 1 relative to the current position in units of degree. Will be run before -i.')
parser.add_argument( "angle2r", "-a2r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 2 relative to the current position in units of degree. Will be run before -i.')
parser.add_argument( "angle3r", "-a3r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 3 relative to the current position in units of degree. Will be run before -i.')
parser.add_argument( "init", "-i", bool, group="RotationalPlatform", default=True, help='Use if device is already initialized to avoid homing.')
#parser.add_argument( "port", "-p", str, group="RotationalPlatform", default=None, help='Defines the Port to connect to the device.')
parser.add_argument( "ReadPorts", "-rp", bool, group="Ports", default=False, help='Refreshes the device ports.')

arguments=parser.done(store_if_file_supplied=True)

ports=DIO.serialports().get_ports(refresh=arguments['ReadPorts']['val'])


use=[False,False,False]
init=[]
for i in range(len(use)):
	if arguments['angle'+str(i+1)]['val']!=None or arguments['angle'+str(i+1)+'r']['val']!=None:
		use[i]=True
	if use[i]==True and arguments['init']['val']:
		init.append(True)
	else:
		init.append(False)

devices=rotStages(port=ports['rotPlatform'], unit="deg", Channels=use, init=init) # later 'Auto'

for i in range(len(use)):
	if arguments['angle'+str(i+1)]['val']!=None:
		devices.move( i, arguments['angle'+str(i+1)]['val'], rel=False, wait=True)

for i in range(len(use)):
	if arguments['angle'+str(i+1)+'r']['val']!=None:
		devices.move( i, arguments['angle'+str(i+1)+'r']['val'], rel=True, wait=True)