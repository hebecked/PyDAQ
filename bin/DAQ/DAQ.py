import multiprocessing
from multiprocessing import Pipe, Process
from ..Data_IO import instructions
from ..monochromator import CornerStone260
from ..XYZ_Scanner import Scanner
from .. import lockIn
from ..rotational_stage import rotLib #rotStages
import time
import numpy as np

class DAQ(multiprocessing.Process):

    def __init__(self, instructions, devices, pipe):
        multiprocessing.Process.__init__(self)
        self.pipe=pipe
        self.instructions=instructions
        self.devices=devices
        self.do="running"


    def run(self):
        timestart=time.time()
        cn=1
        for inst in self.instructions.instructions:
            print "Step ", inst["#"]
            if self.pipe.poll():
                self.do=self.pipe.recv()
            if self.do == "pause":
                while self.do=="pause":
                        print "Relaxing :)"
                        self.do=self.pipe.recv()
            if self.do == "stop":
                print "Bye, bye."
                exit()
            if self.do == "continue":
                    self.do="running"
                    print "Arbeit, Arbeit."

            '''Go through all devices and instructions.'''
            results={'#':inst["#"]}
            if self.instructions.monochromator:
                if inst["wavelength"]>=0:
                    self.devices['monochromator'].GoWave(inst["wavelength"])
                if inst["grating"]>=0:
                    self.devices['monochromator'].Grat(inst["grating"])
                if inst["filter"]>=0:
                    self.devices['monochromator'].Filter(inst["filter"])
            if self.instructions.XYZ_Scanner:
                if inst['vx']>0:
                    self.devices['xyz-scanner'].change_1axisVelocity(inst['vx'],1)
                if inst['vy']>0:
                    self.devices['xyz-scanner'].change_1axisVelocity(inst['vy'],2)
                if inst['vz']>0:
                    self.devices['xyz-scanner'].change_1axisVelocity(inst['vz'],3)
                if inst["xyz_pos_type"]=='abs':
                    x,y,z=self.devices['xyz-scanner'].read_position()
                    if inst["xpos"]>=0:
                        x=inst["xpos"]
                    if inst["ypos"]>=0:
                        y=inst["ypos"]
                    if inst["zpos"]>=0:
                        z=inst["zpos"]
                    self.devices['xyz-scanner'].move_to(x,y,z, unit="scanner", go=True,smooth_move=None,show=False,sequenced=False,history_forward=False,clean_forward=True)
                elif inst["xyz_pos_type"]=='rel':
                    self.devices['xyz-scanner'].shift_to(inst["xpos"],inst["ypos"],inst["zpos"], unit="scanner", go=True,smooth_move=None,show=False,sequenced=False,history_forward=False,clean_forward=True)
                elif inst["xyz_pos_type"]=='idl':
                    pass
                else:
                    raise ValueError('The positioning type %s is not known.', inst["xyz_pos_type"])
            for i in range(3):
                axis=["alpha","beta","gamma"]
                if inst["rot_pos_type"]=='abs':
                    if self.instructions.rotPlatform[i]:
                        self.devices['rotPlatform'].move(i, inst[axis[i]], rel=False, wait=True)
                elif inst["rot_pos_type"]=='rel':
                    if self.instructions.rotPlatform[i]:
                        self.devices['rotPlatform'].move(i, inst[axis[i]], rel=True, wait=True)
                elif inst["rot_pos_type"]=='idl':
                    pass
                else:
                    raise ValueError('The positioning type %s is not known.', inst["rot_pos_type"])
            if self.instructions.monochromator:
                results.update({"Wavelength":self.devices["monochromator"].GetWave()})
            else:
                results.update({"Wavelength":-1})
            if inst["delay"]>0:
                time.sleep(inst["delay"])
            amplr=[]
            ampls=[]
            phaser=[]
            phases=[]
            freqr=[]
            freqs=[]
            if self.instructions.sLockIn and inst["readLockins"]:
                self.devices['sLockIn'].AutoGain()
            if self.instructions.rLockIn and inst["readLockinr"]:
                self.devices['rLockIn'].AutoGain()
            for i in range(inst['avrgn']):
                if self.instructions.sLockIn and inst["readLockins"]:
                    sampl,sphase,sfreq = self.devices['sLockIn'].StandardData(N=1)
                    ampls.append(sampl)
                    phases.append(sphase)
                    freqs.append(sfreq)

                if self.instructions.rLockIn and inst["readLockinr"]:
                    rampl,rphase,rfreq = self.devices['rLockIn'].StandardData(N=1)
                    amplr.append(rampl)
                    phaser.append(rphase)
                    freqr.append(rfreq)

            if self.instructions.sLockIn and inst["readLockins"]:
                results.update({'sLockIn':np.mean(ampls)})
                results.update({'sLockInErr':np.std(ampls)})
                results.update({'sLockInFreq':np.mean(freqs)})
                results.update({'sLockInFreqErr':np.std(freqs)})
                results.update({'sLockInPhase':np.mean(phases)})
                results.update({'sLockInPhaseErr':np.std(phases)})

            if self.instructions.rLockIn and inst["readLockinr"]:
                results.update({'rLockIn':np.mean(amplr)})
                results.update({'rLockInErr':np.std(amplr)})
                results.update({'rLockInFreq':np.mean(freqr)})
                results.update({'rLockInFreqErr':np.std(freqr)})
                results.update({'rLockInPhase':np.mean(phaser)})
                results.update({'rLockInPhaseErr':np.std(phaser)})
            results.update({'Misc':None})

            self.pipe.send(results)
            time_left=float(time.time()-timestart)*float(len(self.instructions.instructions)-cn)/float(cn)
            print "%02d:%02d:%02d" % (time_left/3600, (time_left/60)%60,time_left%60) , " left"
            cn+=1
        self.pipe.send('DONE')
        return	



    def __del__(self):
        pass
        #close all devices





