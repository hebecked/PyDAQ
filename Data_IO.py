#class dataIO:

class files(object):
	import os, sys

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
		self.openfile=open(filename)
		return self

	def append_line(line):
		if self.openfile is None:
			with open(self.filename,'a') as tempfile:
				tempfile.write(line + '\n')
		else:
			self.openfile.write(line + '\n')


	def __exit__(self, exception_type, exception_value, traceback):
		self.openfile.close()
		del self.openfile





class serialports:
	import PyQt5.QtSerialPort
	element = PyQt5.QtSerialPort.QSerialPortInfo()
	ports=a.availablePorts()
	realloc=[]
	for port in ports:
		realloc.append(port.systemLocation())


class instructions(object):

	def __init__(self, instrctionfile):
		super.__init__(self)
		self.instructions=[]
		version=1
		self.monochromator=False
		self.sLockIn=False
		self.rLockIn=False
		self.XYZ_Scanner=False
		self.rotPlatform=False
		with open(instrctionfile,'r') as FILE:
			for line in FILE:
				if line[0]=='#':
					temp=[[False,str.replace(inst,"v=","")][inst.find("v=")==0] for inst in line.split()]
					for i in temp:
						version=i if i else version
				elif version==1:
					'''
					1)measurement/step# 
					2)wavelength 
					3)grating 
					4)filter 
					5)readLockinr 
					6)readLockins
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
					if inst[9] != "idl":
						self.XYZ_Scanner=True
					if inst[16] != "idl":
						self.rotPlatform=True
					TODO_dict={}
					task=["#","wavelength","grating","filter","readLockinr","readLockins","xpos","ypos","zpos","xyz_pos_type","vx","vy","vz","alpha","beta","gamma","rot_pos_type","delay"]:
					for i in range(len(task)):
						if i==4 or i==5:
							TODO_dict.update({task[i]:bool(inst[i])})
						elif i==9 or i==16:
							TODO_dict.update({task[i]:str(inst[i])})
						else:
							TODO_dict.update({task[i]:int(inst[i])})
					self.instructions.append(TODO_dict)
				else:
					print "Error instruction file has no (known) version.\nExiting!!!"
					exit()

