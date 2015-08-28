import serial



class rotStages:

	def __init__(self,port="/dev/ttyUSB0", unit="deg", Channels=[False,False,False]):
		self.port=port
		self.unit=unit #can be %,rad,deg
		if available open desired channels and make availible as variable




class rotStage:

	def goHome(self):
	'''\x43\x04\x01\x00" + self.num + "\x01"'''
		self.pos=0

	#def checkIfError(self,result):
	#	if result=="\x80\x00\x00\x00\x01\x11":
	#		print "Error"
	#		exit()


	#def isBayOccupied(self):
	#	self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
	#	self.ser.write("\x60\x00" + self.bay + "\x00\x11\x01")
	#	result=self.ser.read(size=6)
	#	self.ser.close()
	#	if result == ('\x61\x00' + self.bay + '\x02\x01\x11'):
	#		return False
	#	elif result == ('\x61\x00' + self.bay + '\x01\x01\x11'):
	#		return True
	#	else:
	#		print "Error"
	#		exit()



	def stopMove(self):
		self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
		self.ser.write("\x65\x04" + self.bay + "\x01\x11\x01")
		result=self.ser.read(size=6)
		self.ser.close()

	def move(self, pos(dir?), rel=False, wait=True"aka block?"):#alternative

	def moveRelLeft(self):

		#self.pos=0


	def moveRelRight(self):

		#self.pos=0

	def moveAbsLeft(self):

		#self.pos=0


	def moveAbsRight(self):
		#self.pos=0

	def getStatus(self):


	def getPos(self):
	#self.pos=0