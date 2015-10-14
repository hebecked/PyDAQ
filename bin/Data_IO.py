#class dataIO:
import os, sys

class files(object):

	def __init__(self,filename):
		baspath=os.path.dirname(os.path.abspath(__file__))
		self.filename=os.path.join(baspath,filename)
		self.isfile=os.path.isfile(self.filename)

	def init_file(self, header, override=False):
		if self.isfile and not override:
			print "Error the file " + self.filename + "exists already\nExiting!!!"
			exit()
		with open(self.filename,'w') as FILE:
			FILE.write(header)

	def __enter__(self):
		self.openfile=open(self.filename,"a")
		return self

	def append_line(self, line):
		if self.openfile is None:
			with open(self.filename,"a") as tempfile:
				tempfile.write(line + '\n')
		else:
			self.openfile.write(line + '\n')


	def __exit__(self, exception_type, exception_value, traceback):
		self.openfile.close()
		del self.openfile





class serialports:
#	import PyQt5.QtSerialPort
#
#	def __init__(self):
#		ports=PyQt5.QtSerialPort.QSerialPortInfo().availablePorts()
#		realloc=[]
#		for port in ports:
#			realloc.append(port.systemLocation())
#		self.ports=realloc
	import sys
	import glob
	import serial


	def __init__(self):
		"""Lists serial ports
		:raises EnvironmentError:
			On unsupported or unknown platforms
		:returns:
			A list of available serial ports
		"""
		if self.sys.platform.startswith('win'):
		    ports = ['COM' + str(i + 1) for i in range(256)]
		elif self.sys.platform.startswith('linux') or self.sys.platform.startswith('cygwin'):
		    # this is to exclude your current terminal "/dev/tty"
		    ports = self.glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
		    ports = self.glob.glob('/dev/tty.*')
		else:
		    raise EnvironmentError('Unsupported platform')
		result = []
		for port in ports:
		    try:
		        s = self.serial.Serial(port)
		        s.close()
		        result.append(port)
		    except (OSError, self.serial.SerialException):
		        pass
		self.ports=result



class instructions(object):

	def __init__(self, instrctionfile):
		#super.__init__(self)
		self.instructions=[]
		version=1
		self.monochromator=False
		self.sLockIn=False
		self.rLockIn=False
		self.XYZ_Scanner=False
		self.rotPlatform=[False,False,False]
		with open(instrctionfile,'r') as FILE:
			for line in FILE:
				if line[0]=='#':
					temp=[[False,str.replace(inst,"v=","")][inst.find("v=")==0] for inst in line.split()]
					for i in temp:
						version=i if i else version
				elif version=="1":
					'''
					0)measurement/step# 
					1)wavelength 
					2)grating 
					3)filter 
					4)readLockinr 
					5)readLockins
					6)avrgn
					7)xpos 
					8)ypos 
					9)zpos 
					10)pos(abs/rel/idl)
					11)vx
					12)vy
					13)vz
					14)alpha #sign gives direction for abs and rel
					15)beta
					16)gamma
					17)pos(abs/rel/idl)
					18)sleep/delay
					'''
					inst = line.split()
					if inst[1] != "-1" or inst[2] != "-1" or inst[3] != "-1":
						self.monochromator=True
					if bool(inst[4]):
						self.rLockIn=True
					if bool(inst[5]):
						self.sLockIn=True
					if inst[10] != "idl":
						self.XYZ_Scanner=True
					if float(inst[14]) != 0:#This needs to change in future file versions
						self.rotPlatform[0]=True
					if float(inst[15]) != 0:
						self.rotPlatform[1]=True
					if float(inst[16]) != 0:
						self.rotPlatform[2]=True
					TODO_dict={}
					task=["#","wavelength","grating","filter","readLockinr","readLockins","avrgn","xpos","ypos","zpos","xyz_pos_type","vx","vy","vz","alpha","beta","gamma","rot_pos_type","delay"]
					for i in range(len(task)):
						if i==5 or i==6:
							TODO_dict.update({task[i]:bool(inst[i])})
						elif i==10 or i==17:
							TODO_dict.update({task[i]:str(inst[i])})
						else:
							TODO_dict.update({task[i]:int(inst[i])})
					self.instructions.append(TODO_dict)
				elif version==2:
					print 'Not implemented yet'
					'''This part will be based on changes per iteration only (json?)'''
				else:
					raise IOError("Instruction file has no (known) version.\nExiting!!!")

