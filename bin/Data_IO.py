#class dataIO:
import os, sys

class files(object):

	def __init__(self,filename):
		#baspath=os.path.dirname(os.path.abspath(__file__))
		baspath=os.getcwd()
		self.filename=os.path.join(baspath,filename)
		self.isfile=os.path.isfile(self.filename)
		self.openfile=None

	def init_file(self, header, override=False):
		if self.isfile and not override:
			raise ValueError("Error the file " + self.filename + "exists already\nExiting!!!")
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
		self.openfile=None





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
	import struct
	import json

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
		    #ports = self.glob.glob('/dev/tty[A-Za-z]*')
		    ports = self.glob.glob('/dev/ttyUSB*')
		elif sys.platform.startswith('darwin'):
		    ports = self.glob.glob('/dev/tty.*')
		else:
		    raise EnvironmentError('Unsupported platform')
		self.ports=ports
		self.sig=''
		self.ref=''
		self.mono=''
		self.rot=''
		self.xyz=''
		#alternatively python -m serial.tools.list_ports

	def find_monochromator(self):
		for port in self.ports:
			try:
				ser = self.serial.Serial(port, 9600, timeout=0.5)
				ser.flushInput()        
				ser.write("\r\n" + 'INFO?' + "\r\n")
				answer1 = ser.readline()
				answer2 = ser.readline()
				#print answer2
				ser.close()
				if answer2[:-2]=='INFO?':
					self.mono=port
					return port
			except Exception as e:
				print e
				#pass
		return ''

	def find_lockin(self, IDN=None):
		for port in self.ports:
			try:
				self.ser = self.serial.Serial(port, 19200, timeout=0.5, bytesize=8, parity='N', stopbits=1)
				self.ser.flushInput()
				self.ser.flushOutput()
				self.ser.flush()
				self.ser.write('\n' + "*IDN?" + '\n')
				answer = self._read_LI()
				self.ser.close()
				if answer==IDN or IDN==None:		
					return port
			except IOError:
				pass
		return ''


	def find_sig_lockin(self):
		self.sig=self.find_lockin(IDN="Stanford_Research_Systems,SR830,s/n53701,ver1.07 ")
		return self.sig

	def find_ref_lockin(self):
		self.ref=self.find_lockin(IDN="Stanford_Research_Systems,SR830,s/n53700,ver1.07 ")
		return self.ref

	def _read_LI(self):
		list_=[]
		help=0
		counter=0
		while help!='\r':
			help=self.ser.read()
			if help=='':
				raise IOError("Not the right port ... maybe next time ;)")
			list_.append(help)
		return ''.join(list_[0:-1])


	def find_rot_platform(self):
		for port in self.ports:
			try:
				self.ser=self.serial.Serial(port ,115200, rtscts=True, timeout=0.5)
				self.ser.flushInput()
				self.ser.flushOutput()
				self.ser.flush()
				packet=self.struct.pack("H",0x0005)
				packet+="\x00"
				packet+="\x00"
				packet+="\x11"
				packet+="\x01"
				self.ser.write(packet)
				#self.ser.write(packet)
				#self.ser.write(packet)
				#recieved=""
				#for i in range(90):
				#	recieved+=self.ser.read()
				recieved=self.ser.read(size=90)
				self.ser.close()
				#header = recieved[:6]
				#msg_id, length, dest, source = self.struct.unpack('<HHBB', header)
				#dest ^= 0x80 # Turn off 0x80.
				#data = recieved[6 : 6 + length]
				#serial_number = str(data[0:4]).encode('hex')
				if len(recieved)==90:
					self.rot=port
					return port
			except Exception as e:
				print e
				#pass
		return ''


	def find_xyz(self):
		for port in self.ports:
			if port==self.mono:
				continue
			elif port==self.sig:
				continue
			elif port==self.ref:
				continue
			elif port==self.rot:
				continue
			else:
				if self.xyz!='' and type(self.xyz)==str(): 
					self.xyz=[self.xyz]
					self.xyz.append(port)
				else:
					self.xyz=port
		return self.xyz

	def find_all_devices(self):
		print "looking for devices..."
		self.find_rot_platform()
		if self.rot!="":
			i=self.ports.index(self.rot)
			del self.ports[i]
		self.find_monochromator()
		self.find_sig_lockin()
		self.find_ref_lockin()
		self.find_xyz()
		print "Done"
		return {'monochromator':self.mono, "xyz-scanner":self.xyz, 'sLockIn':self.sig, 'rLockIn':self.ref, 'rotPlatform':self.rot}
		#return {'monochromator':self.mono, "sig_lockin":self.sig,  "ref_lockin":self.ref, "rot_platform":self.rot, "XYZ_Scanner":self.xyz}


	def get_ports(self,refresh=False, path='configs/ports.store'):
		if refresh:
			ports=self.find_all_devices()
			with open(path,'w') as file_:
				self.json.dump(ports,file_)
		else:
			with open(path,'r') as file_:
				ports=self.json.load(file_)
		return ports



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
					4)avrgn
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
					if inst[10] != "idl":
						self.XYZ_Scanner=True
					if str(inst[17]) != "idl":
						if float(inst[14]) != 0:#This needs to change in future file versions
							self.rotPlatform[0]=True
						if float(inst[15]) != 0:
							self.rotPlatform[1]=True
						if float(inst[16]) != 0:
							self.rotPlatform[2]=True
					TODO_dict={}
					task=["#","wavelength","grating","filter","avrgn","readLockinr","readLockins","xpos","ypos","zpos","xyz_pos_type","vx","vy","vz","alpha","beta","gamma","rot_pos_type","delay"]
					for i in range(len(task)):
						if i==5 or i==6:
							if inst[i]=="False":
								TODO_dict.update({task[i]:False})
							else:
								TODO_dict.update({task[i]:bool(inst[i])})
						elif i==10 or i==17:
							TODO_dict.update({task[i]:str(inst[i])})
						elif i==18:
							TODO_dict.update({task[i]:float(inst[i])})
						else:
							TODO_dict.update({task[i]:int(inst[i])})
					self.instructions.append(TODO_dict)
				elif version==2:
					print 'Not implemented yet'
					'''This part will be based on changes per iteration only (json?)'''
				else:
					raise IOError("Instruction file has no (known) version.\nExiting!!!")




class instruction_maker(object):

	def __init__(self,filename=None,version=1):
		if version==1:
			self.version=version
			self.tasks=["#","wavelength","grating","filter","avrgn","readLockinr","readLockins","xpos","ypos","zpos","xyz_pos_type","vx","vy","vz","alpha","beta","gamma","rot_pos_type","delay"]
		else:
			raise ValueError('The version ' + str(version) + ' is not supportd')
		if filename!=None:
			self.file=files(filename)
		else:
			raise ValueError('Please define a filename')#
		header='# v=' + str(self.version) + ' Instruction file created with instruction_maker (by Dustin hebecker).\n'
		for task in self.tasks:
			header+=task + ' '
		header=header[0:-2]+'\n'
		self.file.init_file(header, override=True)
		self.count=0

	def add_instruction(self,wavelength=-1,grating=-1,filter_=-1,avrgn=10,readLockinr=False,readLockins=False,xpos=0,ypos=0,zpos=0,xyz_pos_type='idl',vx=-1,vy=-1,vz=-1,alpha=0,beta=0,gamma=0,rot_pos_type='idl',delay=0):
		'''Add new instructions. Default values will do nothing.'''
		line=''
		if self.version==1:
			if type(wavelength)!=int:
				raise ValueError(str(wavelength) +' is not of type int.')
			if type(grating)!=int:
				raise ValueError(str(grating) +' is not of type int.')
			if type(filter_)!=int:
				raise ValueError(str(filter_) +' is not of type int.')			
			if type(avrgn)!=int:
				raise ValueError(str(avrgn) +' is not of type int.')
			if type(readLockinr)!=bool:
				raise ValueError(str(readLockinr) +' is not of type bool.')
			if type(readLockins)!=bool:
				raise ValueError(str(readLockins) +' is not of type bool.')
			if type(xpos)!=int:
				raise ValueError(str(xpos) +' is not of type int.')
			if type(ypos)!=int:
				raise ValueError(str(ypos) +' is not of type int.')
			if type(zpos)!=int:
				raise ValueError(str(zpos) +' is not of type int.')
			if xyz_pos_type!='idl' and xyz_pos_type!='abs' and xyz_pos_type!='rel': 
				raise ValueError(str(xyz_pos_type) +' is not a valid xyz_pos_type.')
			if type(vx)!=int:
				raise ValueError(str(vx) +' is not of type int.')
			if type(vy)!=int:
				raise ValueError(str(vy) +' is not of type int.')
			if type(vz)!=int:
				raise ValueError(str(vz) +' is not of type int.')
			if type(alpha)!=float and type(alpha)!=int:
				raise ValueError(str(alpha) +' is not of type float.')
			if type(beta)!=float and type(beta)!=int:
				raise ValueError(str(beta) +' is not of type float.')
			if type(gamma)!=float and type(gamma)!=int:
				raise ValueError(str(gamma) +' is not of type float.')
			if rot_pos_type!='idl' and rot_pos_type!='abs' and rot_pos_type!='rel': 
				raise ValueError(str(rot_pos_type) +' is not a valid rot_pos_type.')
			if type(delay)!=float and type(delay)!=int:
				raise ValueError(str(delay) +' is not of type float.')
			line+=str(self.count)+' ' #"#"
			line+=str(wavelength)+' ' #"wavelength"
			line+=str(grating)+' ' #"grating"
			line+=str(filter_)+' ' #"filter"
			line+=str(avrgn)+' ' #"avrgn"
			line+=str(readLockinr)+' ' #"readLockinr"
			line+=str(readLockins)+' ' #"readLockins"
			line+=str(xpos)+' ' #"xpos"
			line+=str(ypos)+' ' #"ypos"
			line+=str(zpos)+' ' #"zpos"
			line+=str(xyz_pos_type)+' ' #"xyz_pos_type"
			line+=str(vx)+' ' #"vx"
			line+=str(vy)+' ' #"vy"
			line+=str(vz)+' ' #"vz"
			line+=str(alpha)+' ' #"alpha"
			line+=str(beta)+' ' #"beta"
			line+=str(gamma)+' ' #"gamma"
			line+=str(rot_pos_type)+' ' #"rot_pos_type"
			line+=str(delay)+' ' #"delay"
		self.file.append_line(line)
		self.count+=1

