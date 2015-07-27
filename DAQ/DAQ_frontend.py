import multiprocessing
from multiprocessing import Pipe, Process
from Data_IO import instructions, files
from DAQ import DAQ

class DAQ_handler(object):
	"""docstring for DAQ_handler"""
	def __init__(self, instructionfile, ports, resultfile):
		pipeend1, pipeend2 = multiprocessing.Pipe()
		self.pipe = pipeend1
		self.instructions=instructions(instructionfile)
		self.datastorage=[]
		self.resultfile=files(resultfile)
		self.resultfile.init_file("#Nr Wavelength Ref RefErr Sig SigErr RefFreq RefPhase SigFreq SigPhase Misc")
		self.DAQ = DAQ(self.instructions, ports, pipeend2)
		self.DAQ.start()


	def convert_dict_to_line(self,dict_, separator='\t'):
		line=''
		line+=str(dict_['#']) + '\t'
		line+=str(dict_['Wavelength']) + separator
		line+=str(dict_['rLockIn']) + separator
		line+=str(dict_['rLockInErr']) + separator
		line+=str(dict_['sLockIn']) + separator
		line+=str(dict_['sLockInErr']) + separator
		line+=str(dict_['rLockInFreq']) + separator
		line+=str(dict_['rLockInPhase']) + separator
		line+=str(dict_['sLockInFreq']) + separator
		line+=str(dict_['sLockInPhase']) + separator
		#line+=str(dict_['sLockIn']) + ' '
		line+=str(dict_['Misc'])
		return line

	def update():
		if self.pipe.poll():
			with self.resultfile as resfile:
				while self.pipe.poll():
					result=self.pipe.get()
					resfile.append_line(convert_dict_to_line(result))
					self.datastorage.append(result)

	def send_signal(signal):
		if signal=="stop" or signal=="pause" or signal=="continue":
			self.pipe.send(signal)
		elif  signal=="kill":
			self.pipe.send("stop")
			self.DAQ.terminate()
		else:
			print "An error occured you have send a non valid signal.\nExiting!!!"
			exit()

	def __del__(self):
		self.DAQ.send_signal("kill")
		del self.DAQ
