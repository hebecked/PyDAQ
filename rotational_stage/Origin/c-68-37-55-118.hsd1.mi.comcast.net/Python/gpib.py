#!/usr/bin/python

# this contains functions to controll an HP 3325A frequency synthesizer using a Galvant industries USB-GPIB controller
# it depends on classes porvided by Galvant

from instruments import Instrument as ik
from time import sleep
from random import randint

#inst = ik.open_gpibusb('/dev/ttyUSB0', 17)
#inst.sendcmd('FR9KHZ')




inst = ik.open_gpibusb('/dev/ttyUSB0', 17)



def onstate():
	#continue to add functions i.e. sweep, offset 
	inst.sendcmd('FU1AM1MVPH0DEFR1KH')

def set_frequency(freq, unit):
		
	if unit == 'HZ' or unit == 'KH' or unit == 'MH':
		inst.sendcmd('FR%s%s' % (str(freq), unit))
	else:
		print 'invalid unit or value'

def set_amplitude(value, unit):
	if unit == 'VO' or unit =='MV' or unit == 'VR' or unit == 'MR':
		inst.sendcmd('AM%s%s' % (str(value), unit))
	else:
		print 'invalid unit or value'

def set_phase(value):
	inst.sendcmd('PH%sDE' % (str(value)))

def cont_sweep(start, startunit, stop, stopunit, ti):
	if startunit == 'HZ' or startunit == 'KH' or startunit == 'MH':
		if stopunit == 'HZ' or stopunit == 'KH' or stopunit == 'MH':
			inst.sendcmd('ST%s%sSP%s%sTI%sSE' % (str(start), startunit, str(stop), stopunit, ti))
			inst.sendcmd('SC')

def single_sweep(start, startunit, stop, stopunit, ti):
	if startunit == 'HZ' or startunit == 'KH' or startunit == 'MH':
		if stopunit == 'HZ' or stopunit == 'KH' or stopunit == 'MH':
			inst.sendcmd('ST%s%sSP%s%sTI%sSE' % (str(start), startunit, str(stop), stopunit, ti))
			inst.sendcmd('SSSS')
		

def get_frequency():
	fr = ''
	
	fr = inst.query('IFR')
	
	if fr == '':
		fr = inst.read()
	
	return fr

def get_amplitude():
	am = ''
	
	am = inst.query('IAM')
	
	if am == '':
		am = inst.read()
	
	return am
	
def get_phase():
	ph = ''
	
	ph = inst.query('IPH')
	
	if ph == '':
		ph = inst.read()
	
	return ph


