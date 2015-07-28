import multiprocessing
from multiprocessing import Pipe, Process
from Data_io import instructions
from monochromator import CornerStone260
import Scanner
import lockin

class DAQ(multiprocessing.Process):

    def __init__(self, instructions, devices, pipe):
        multiprocessing.Process.__init__(self)
        self.pipe=pipe
        self.instructions=instruction
        self.devices=devices


    def run(self):
        for inst in self.instructions.instructions:
            if self.pipe.poll():
                do=self.pipe.recv()
            if do == "pause":
                while do=="pause":
                        print "Relaxing :)"
                        do=self.pipe.recv()
            if do == "stop":
                print "Bye, bye."
                exit()
            if do == "continue":
                    print "Arbeit, Arbeit."

            '''Go through all devices and instructions.'''
            results={'#':inst["#"]}
            if instructions.monochromator:
                if inst["wavelength"]>=0:
                    devices['monochromator'].GoWave(inst["wavelength"])
                if inst["grating"]>=0:
                    devices['monochromator'].Grat(inst["grating"])
                if inst["filter"]>=0:
                    devices['monochromator'].Filter(inst["filter"])
            if instructions.XYZ_Scanner:
                #do I have to use a sleep after this?



            if instructions.monochromator:
                results.update({"Wavelength":self.monochromator.GetWave()})
            else:
                results.update({"Wavelength":-1})

needs to pipe:
        dict_['#']
        dict_['Wavelength']
        dict_['rLockIn']
        dict_['rLockInErr']
        dict_['sLockIn']
        dict_['sLockInErr']
        dict_['rLockInFreq']
        dict_['rLockInPhase']
        dict_['sLockInFreq']
        dict_['sLockInPhase']
        dict_['Misc']



            #make dict
            self.pipe.send(results)
        return	



    def __del__(self):
        #close all devices





