import multiprocessing
from multiprocessing import Pipe, Process
from ..Data_IO import instructions, files
import DAQ
from ..monochromator import CornerStone260
from ..XYZ_Scanner import Scanner
from .. import lockIn
from ..rotational_stage import rotLib #rotStages

class DAQ_handler(object):
	"""docstring for DAQ_handler"""
	def __init__(self, instructionfile, ports, resultfile, run=True):
		pipeend1, pipeend2 = multiprocessing.Pipe()
		self.pipe = pipeend1
		self.instructions=instructions(instructionfile)
		self.datastorage=[]
		self.resultfile=files(resultfile)
		self.resultfile.init_file("#Nr Wavelength Ref RefErr Sig SigErr RefFreq RefFreqErr RefPhase RefPhaseErr SigFreq SigFreqErr SigPhase SigPhaseErr Misc")
		 #init devices if aplicable allow access to device in main programm if possible
		self.devices={}
		if self.instructions.monochromator:
			self.devices['monochromator']=CornerStone260(port = ports['monochromator'])
			self.devices['monochromator'].Units_NM()
		if self.instructions.XYZ_Scanner:
			self.devices['xyz-scanner']=Scanner.Scanner(port=ports["xyz-scanner"],do_refrun=True,smooth_move=False,debug=False)

		if self.instructions.sLockIn:
			self.devices['sLockIn']=lockIn(port=ports['sLockIn'], autogain=True, timeconstant=0.3)

		if self.instructions.rLockIn:
			self.devices['rLockIn']=lockIn(port=ports['rLockIn'], autogain=True, timeconstant=0.3)

		if self.instructions.rotPlatform[0] or self.instructions.rotPlatform[1] or self.instructions.rotPlatform[2]:
			self.devices['rotPlatform']=rotLib.rotStages(port=ports['rotPlatform'], unit="deg", Channels=self.instructions.rotPlatform, init=["Auto","Auto","Auto"]) #switch to init true

		self.DAQ = DAQ(self.instructions, self.devices, pipeend2)
		if run:
			self.run()
		

	def run(self):
		self.DAQ.start()


	def convert_dict_to_line(self,dict_, separator='\t'):#add if "key" in dict.keys() for each
		keys=['#','Wavelength','rLockIn','rLockInErr','sLockIn','sLockInErr','rLockInFreq','rLockInFreqErr','rLockInPhase','rLockInPhaseErr','sLockInFreq','sLockInFreqErr','sLockInPhase','sLockInPhaseErr','Misc']
		line=''
		for key in keys:
			if key in dict_.keys():
				line+=str(dict_[key]) + separator
			else:
				line+=str("-1") + separator
		return line

	def update():
		if self.pipe.poll():
			with self.resultfile as resfile:
				while self.pipe.poll():
					result=self.pipe.get()
					if result == 'DONE':
						return 'DONE'
					else:
						resfile.append_line(convert_dict_to_line(result))
						self.datastorage.append(result)
						return 'Running'

	def send_signal(signal):
		if signal=="stop" or signal=="pause" or signal=="continue":
			self.pipe.send(signal)
		elif  signal=="kill":
			self.pipe.send("stop")
			self.DAQ.terminate()
		else:
			print "An error occured you have send a non valid signal.\nExiting!!!"
			exit()

	def close(self, urgent=True):
		if urgent:
			self.DAQ.send("kill")
			self.devices['xyz-scanner'].close(quick=True)
			#lockin not needed
			#monochromator not needed
			#Rotplatform not needed
		else:
			self.__del__()

	def __del__(self):
		self.DAQ.send("stop")
		self.devices['xyz-scanner'].close()
		del self.devices['monochromator']
		del self.devices['xyz-scanner']
		del self.devices['sLockIn']
		del self.devices['rLockIn']
		del self.devices['rotPlatform']
		del self.DAQ