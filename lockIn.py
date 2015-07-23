import serial
import os, sys
import numpy as np

class lockin:

	def __init__(self,port, avrgn=10):
		self.port=port
		self.ser = serial.Serial(port,baud,timeout=timeout)#...
		time.sleep(0.2) #give system time to setup stuff
		self.ser.read(100) #remove any trash from the buffer
		if(self.ser.isOpen()):
			return None
		else:
			print "Error opening serial connection!"
			return None


	def get_signal(dyn_range=True,avrgn=None):
		#measure self.avrgn times and return value + error
		if dyn_range:
			dyn_range()
		if avrgn==None:
			avrgn=self.avrgn
		results=[]
		for i in range(avrgn):
			results.append(self.measure())
		val=np.mean(results)
		error=np.std(results)
		return val, error


	def get_phase():
		#measure self.avgn times and return value + error
		if dyn_range:
			dyn_range()
		if avrgn==None:
			avrgn=self.avrgn
		results=[]
		for i in range(avrgn):
			results.append(self.measure('phase'))
		val=np.mean(results)
		error=np.std(results)
		return val, error


	def _measure(value='signal'):
		'''
		Takes a single value (signal, phase, ...)
		'''
		return 1


	def get_range():
		return self.range


	def set_range(range):
		self.ser.write()
		self.range=range


	def dyn_range():
		"""
		dynamically changes the ADC detection range according to the current signal.
		"""
		while(overload()):
			set_range(self.range/2)
		while(get_signal(avrgn=2, dyn_range=False)[0]<range/2):
			set_range(self.range*2)
		set_range(range)


	def overload():
		'''returns True if overload otherwise False'''
		return False


	def close(self):
		"""
		Removes class element and closes serial connection
		""" 
		self.__del__()


	def __del__(self):
		self.ser.close()