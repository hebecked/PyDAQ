import serial
import os, sys
import numpy as np
import time

class lockin:

	def __init__(self,port, avrgn=10, autogain=False, timeconstant=-1):
		self.port=port#...
		self.avrgn=avrgn
		self.autogain=autogain
		self.baud=19200
		self.timeout=1
		self.bytesize=8
		self.sendtermchar='\n'
		if timeconstant==-1:
			self.get_timeconstant()
		else:
			self.set_timeconstant(timeconstant)
		
	def SerialCommand(self,command):
		#setup - if a Serial object can't be created, a SerialException will be raised.
		while True:
			try:
				self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout, bytesize=self.bytesize,parity='N',stopbits=1)
				#break out of while loop when connection is made
				break
			except serial.SerialException:
				print 'waiting for device ' + self.port + ' to be available'
				time.sleep(3)
		self.ser.flushInput()        
		self.ser.write(command + self.sendtermchar)
		#answer = self._read_LI()
		self.ser.close()
		return

	def SerialQuery(self,command):
		#setup - if a Serial object can't be created, a SerialException will be raised.
		while True:
			try:
				self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout, bytesize=self.bytesize,parity='N',stopbits=1)
				#break out of while loop when connection is made
				break
			except serial.SerialException:
				print 'waiting for device ' + self.port + ' to be available'
				time.sleep(3)
		self.ser.flushInput()        
		self.ser.write(command + self.sendtermchar)
		answer = self._read_LI()
		self.ser.close()
		return answer

 	def _read_LI(self):
		list_=[]
		help=0
		while help!='\r':
			#print help
			help=self.ser.read()
			list_.append(help)
		return ''.join(list_[0:-1])

	def StandardData(self,N=10):
		#setup - if a Serial object can't be created, a SerialException will be raised.
		if self.autogain and not self.AutoGain():
			return -1,0,-1,0,-1,0
		while True:
			try:
				self.ser = serial.Serial(self.port, self.baud, timeout=self.timeout, bytesize=self.bytesize,parity='N',stopbits=1)
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



 	def AutoGain(self):
 		list_=[2e-15,5e-15,1e-14,2e-14,5e-14,1e-13,2e-13,5e-13,1e-12,2e-12,5e-12,1e-11,2e-11,5e-11,1e-10,2e-10,5e-10,1e-9,2e-9,5e-9,1e-8,2e-8,5e-8,1e-7,2e-7,5e-7,1e-6]
 		index_old=2
 		change=20
 		extra=0
 		while change!=0 and extra=1:
 			if change==0:#check at the end of the cycle if there are some slow changes going on
 				extra=1
 			else:
 				extra=0
 			temp=self.SerialQuery('OUTP?3')
 			#print temp
 			value=float(temp)
 			index=np.argmin(np.abs(value-np.asarray(list_)))
 			if value>list_[index]:
 				if index<26:
 					index=index+1
 				else:
 					return False
 			self.SerialCommand('SENS' + str(index))
 			change=index_old-index
 			index_old=index
 			time.sleep(2*self.timeconstant) #Factor 2 protects also for slow changes
 		return True

	def get_phase(self):
		return self.SerialQuery('OUTP?4')


	def set_gain(self,range):
		list_=[2e-15,5e-15,1e-14,2e-14,5e-14,1e-13,2e-13,5e-13,1e-12,2e-12,5e-12,1e-11,2e-11,5e-11,1e-10,2e-10,5e-10,1e-9,2e-9,5e-9,1e-8,2e-8,5e-8,1e-7,2e-7,5e-7,1e-6]
		self.ser.write()
		self.range=range


	def get_frequency(self):
		return self.SerialQuery('FREQ?')

	def get_amplitude(self):
		return self.SerialQuery('OUTP?3')

	def get_phase(self):
		return self.SerialQuery('OUTP?4')


	def get_timeconstant(self):
		index=int(self.SerialQuery('OFLT?'))
		list_=[1e-5,3e-5,1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1,1.,3.,10.,30.,100.,300.,1e+3,3e+3,1e+4,3e+4]
		self.timeconstant=list_[index]
		return list_[index]

	def set_timeconstant(self,timeconst):
		list_=[1e-5,3e-5,1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1,1.,3.,10.,30.,100.,300.,1e+3,3e+3,1e+4,3e+4]
		index=np.argmin(np.abs(np.asarray(list_)-timeconst))
		self.timeconstant=list_[index]
		self.SerialCommand('OFLT' + str(index))


	def autoset_timeconstant(self,periodes=100.):
		frequency=self.get_frequency()
		set_timeconstant=float(periodes)/float(frequency)
		list_=[1e-5,3e-5,1e-4,3e-4,1e-3,3e-3,1e-2,3e-2,1e-1,3e-1,1.,3.,10.,30.,100.,300.,1e+3,3e+3,1e+4,3e+4]
		index=np.argmin(np.abs(np.asarray(list_)-set_timeconstant))
		self.timeconstant=list_[index]
		self.SerialCommand('OFLT' + str(index))


# try auto timeconstant from frequency*100 calculation

