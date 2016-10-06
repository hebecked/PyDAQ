import serial
import os, sys
import numpy as np
import time

class picoamp:

	def __init__(self,port, avrgn=10, autogain=False, slep_milli=500):
		self.port=port#...
		self.avrgn=avrgn
		self.autogain=autogain
		self.baud=9600
		self.timeout=1
		self.bytesize=8
		self.sendtermchar='\n'
		self.slep_milli=slep_milli
		self.parity=serial.PARITY_NONE
		self.stopbits=1
		while True:
			try:
				self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout, bytesize=self.bytesize, parity=self.party, stopbits=self.stopbits)
				#break out of while loop when connection is made
				break
			except serial.SerialException:
				print 'waiting for device ' + self.port + ' to be available'
				time.sleep(3)
		
	def SerialCommand(self,command):
		self.ser.flushInput()        
		self.ser.write(command + self.sendtermchar)
		return

	def SerialQuery(self,command):
		self.ser.flushInput()        
		self.ser.write(command + self.sendtermchar)
		answer = self._read_LI()
		return answer

	def _read_LI(self):
		list_=[]
		help=0
		while help!='\r':
			#print help
			help=self.ser.read()
			list_.append(help)
		return ''.join(list_[0:-1])



	'''	def StandardData(self,N=10):
		#setup - if a Serial object can't be created, a SerialException will be raised.
		while True:
			try:
				self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout, bytesize=self.bytesize, parity=self.party, stopbits=self.stopbits)
				#break out of while loop when connection is made
				break
			except serial.SerialException:
				print 'waiting for device ' + self.port + ' to be available'
				time.sleep(3)
		self.ser.flushInput()  
		if N>1:
			ampl=[]
			phase=[]
			freq=[]
			for i in range(0,N):
				time.sleep(self.timeconstant)
				self.ser.flushInput()
				self.ser.write('OUTP?3' + self.sendtermchar)
				help=float(self._read_LI())
				ampl.append(help)
				time.sleep(0.01)
				self.ser.flushInput()
				self.ser.write('OUTP?4' + self.sendtermchar)
				phase.append(float(self._read_LI()))
				time.sleep(0.01)
				self.ser.flushInput()
				self.ser.write('FREQ?' + self.sendtermchar)
				freq.append(float(self._read_LI()))
			self.ser.close()
			return np.mean(ampl),np.std(ampl),np.mean(phase),np.std(phase),np.mean(freq),np.std(freq)
		else:
			time.sleep(self.timeconstant)
			self.ser.flushInput()
			self.ser.write('OUTP?3' + self.sendtermchar)
			ampl=float(self._read_LI())
			time.sleep(0.01)
			self.ser.flushInput()
			self.ser.write('OUTP?4' + self.sendtermchar)
			phase=float(self._read_LI())
			time.sleep(0.01)
			self.ser.flushInput()
			self.ser.write('FREQ?' + self.sendtermchar)
			freq=float(self._read_LI())
		self.ser.close()
		return ampl,phase,freq 
		'''

	def get_channel_1(self):
		return self.SerialQuery(':FORM:ELEM CURR1; :MEAS?')

	def get_channel_2(self):
		return self.SerialQuery(':FORM:ELEM CURR2; :MEAS?')

	def __del__(self):
		self.ser.close()


# try auto timeconstant from frequency*100 calculation

