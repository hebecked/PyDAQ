import multiprocessing
from multiprocessing import Pipe, Process
from Data_io import instructions


class DAQ(multiprocessing.Process):

    def __init__(self, instructions, ports, pipe):
        multiprocessing.Process.__init__(self)
        self.pipe=pipe
        #init devices if aplicable
        if instructions.monochromator:
            #init monochromator ...
        if instructions.XYZ_Scanner:
            #init scanner ...

        self.sLockIn=False
        self.rLockIn=False
        self.rotPlatform=False

    def run(self):
        for inst in instructions.instructions:
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
            # goo through all devices and instructions
            inst.

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


