import serial



class rotControler:

	def __init__(self,port="/dev/ttyUSB0"):
		self.port=port
		self.baud=115200
		self.rtscts=True
		self.ser=serial.Serial("/dev/ttyUSB0",115200, rtscts=True)
		self.ser.flushInput()
		self.ser.flushOutput()
		self.ser.flush()
		self.ser.close()
		#ser.write("\x23\x02\x00\x00\x21\x01")



class rotPlatform(rotControler):

	def __init__(self,rotControler,platform, init=True):
		if platform==0
			self.num="\x21"
			self.bay="\x01"
		elif platform==1:
			self.num="\x22"
			self.bay="\x02"
		elif platform==2:
			self.num="\x23"
			self.bay="\x03"
		else:
			print "error"
			exit(0)
		if init:
			goHome(self)


	def goHome(self):
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		self.ser.write("\x43\x04\x01\x00" + self.num + "\x01")
		result=self.ser.read(size=6)
		self.ser.close()
		self.pos=0

	def checkIfError(self,result):
		if result=="\x80\x00\x00\x00\x01\x11":
			print "Error"
			exit()


	def isBayOccupied(self):
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		self.ser.write("\x60\x00" + self.bay + "\x00\x11\x01")
		result=self.ser.read(size=6)
		self.ser.close()
		if result == ('\x61\x00' + self.bay + '\x02\x01\x11'):
			return False
		elif result == ('\x61\x00' + self.bay + '\x01\x01\x11'):
			return True
		else:
			print "Error"
			exit()



	def stopMove(self):
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		self.ser.write("\x65\x04" + self.bay + "\x01\x11\x01")
		result=self.ser.read(size=6)
		self.ser.close()

	def relLeft():
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		#self.ser.write("\x43\x04\x01\x00" + self.num + "\x01")
		#result=self.ser.read(size=6)
		self.ser.close()
		#self.pos=0


	def relRight():
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		#self.ser.write("\x43\x04\x01\x00" + self.num + "\x01")
		#result=self.ser.read(size=6)
		self.ser.close()
		#self.pos=0

	def absLeft():
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		#self.ser.write("\x43\x04\x01\x00" + self.num + "\x01")
		#result=self.ser.read(size=6)
		self.ser.close()
		#self.pos=0


	def absRight():
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		#self.ser.write("\x43\x04\x01\x00" + self.num + "\x01")
		#result=self.ser.read(size=6)
		self.ser.close()
		#self.pos=0

	def getStatus():
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		self.ser.close()