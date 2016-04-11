import multiprocessing
from multiprocessing import Pipe, Process
from ..Data_IO import instructions, files
import DAQ
from ..monochromator import CornerStone260
from ..XYZ_Scanner import Scanner
from .. import lockIn
from ..rotational_stage import rotLib #rotStages
from ..dynamicPlot.dynamic_plot import live_plots

class DAQ_handler(object):
	"""docstring for DAQ_handler"""
	def __init__(self, instructionfile, ports, resultfile, run=True):
		pipeend1, pipeend2 = multiprocessing.Pipe()
		self.pipe = pipeend1
		self.instructions=instructions(instructionfile)
		self.datastorage=[]
		self.resultfile=files(resultfile)
		self.resultfile.init_file("#Nr Wavelength Ref RefErr Sig SigErr RefFreq RefFreqErr RefPhase RefPhaseErr SigFreq SigFreqErr SigPhase SigPhaseErr Misc\n",  override=False)
		self.ploting=False
		 #init devices if aplicable allow access to device in main programm if possible
		self.devices={}
		if self.instructions.monochromator:
			self.devices['monochromator']=CornerStone260(port = ports['monochromator'])
			self.devices['monochromator'].Units_NM()
		if self.instructions.XYZ_Scanner:
			self.devices['xyz-scanner']=Scanner.Scanner(port=ports["xyz-scanner"],do_refrun=True,smooth_move=False,debug=False,show=False)

		if self.instructions.sLockIn:
			self.devices['sLockIn']=lockIn.lockin(port=ports['sLockIn'], autogain=True, timeconstant=0.3)

		if self.instructions.rLockIn:
			self.devices['rLockIn']=lockIn.lockin(port=ports['rLockIn'], autogain=True, timeconstant=0.3)

		if self.instructions.rotPlatform[0] or self.instructions.rotPlatform[1] or self.instructions.rotPlatform[2]:
			self.devices['rotPlatform']=rotLib.rotStages(port=ports['rotPlatform'], unit="deg", Channels=self.instructions.rotPlatform, init=self.instructions.rotPlatform) #switch to init true

		self.DAQ = DAQ.DAQ(self.instructions, self.devices, pipeend2)
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

	def update(self):
		if self.pipe.poll():
			with self.resultfile as resfile:
				while self.pipe.poll():
					result=self.pipe.recv()
					if result == 'DONE':
						return 'DONE'
					else:
						resfile.append_line(self.convert_dict_to_line(result))
						self.datastorage.append(result)
						return 'Running'
		#include is running test here
		return 'Running'

	def plot(self):
		if not self.ploting:
			self.plotframe = live_plots(0,1,x_label="Step",y_label="Signal/Reference [A.U.]",y2_label=" ",color1='r',color2='b',two_plots=False)
			self.ploting = True
		if len(self.datastorage) < 1:
			return
		number = self.datastorage[-1]['#']
		if "sLockIn" in self.datastorage[-1] and "rLockIn" in self.datastorage[-1]:
			value = self.datastorage[-1]["sLockIn"]/self.datastorage[-1]["rLockIn"]
		else:
			value = -1
		self.plotframe.update(number,value, "placeholder")
		self.plotframe.autoscale()



	def send_signal(self,signal):
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
			self.pipe.send("kill")
			self.devices['xyz-scanner'].close(quick=True)
			#lockin not needed
			#monochromator not needed
			#Rotplatform not needed
		else:
			self.__del__()

	def __del__(self):
		self.pipe.send("stop")
		if self.instructions.XYZ_Scanner:
			self.devices['xyz-scanner'].close()
			del self.devices['xyz-scanner']
		if self.instructions.monochromator:
			del self.devices['monochromator']
		if self.instructions.rLockIn:
			del self.devices['sLockIn']
		if self.instructions.sLockIn:
			del self.devices['rLockIn']
		if self.instructions.rotPlatform[0] or self.instructions.rotPlatform[1] or self.instructions.rotPlatform[2]:	
			del self.devices['rotPlatform']
		del self.DAQ
