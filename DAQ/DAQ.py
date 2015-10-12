import multiprocessing
from multiprocessing import Pipe, Process
from Data_io import instructions
from monochromator import CornerStone260
import Scanner
import lockin
from rotational_stage import rotLib #rotStages

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
                if inst['vx']>0:
                    devices['xyz-scanner'].change_1axisVelocity(inst['vx'],1):
                if inst['vy']>0:
                    devices['xyz-scanner'].change_1axisVelocity(inst['vy'],2):
                if inst['vz']>0:
                    devices['xyz-scanner'].change_1axisVelocity(inst['vz'],3):
                if inst["xyz_pos_type"]=='abs':
                    x,y,z=devices['xyz-scanner'].read_position(self)
                    if inst["xpos"]>=0:
                        x=inst["xpos"]
                    if inst["ypos"]>=0:
                        y=inst["ypos"]
                    if inst["zpos"]>=0:
                        z=inst["zpos"]
                    devices['xyz-scanner'].move_to(x,y,z, unit="scanner", go=True,smooth_move=None,show=False,sequenced=False,history_forward=False,clean_forward=True):
                elif inst["xyz_pos_type"]=='rel':
                    devices['xyz-scanner'].shift_to(inst["xpos"],inst["ypos"],inst["zpos"], unit="scanner", go=True,smooth_move=None,show=False,sequenced=False,history_forward=False,clean_forward=True):
                elif inst["xyz_pos_type"]=='idl':
                    pass
                else:
                    raise ValueError('The positioning type %s is not known.', inst["xyz_pos_type"])
            for i in range(3):
                axis=["alpha","beta","gamma"]
                if inst["rot_pos_type"]=='abs':
                    if instructions.rotPlatform[i]:
                        devices['rotPlatform'].move(i, inst[axis[i]], rel=False, wait=True)
                elif inst["rot_pos_type"]=='rel':
                    if instructions.rotPlatform[i]:
                        devices['rotPlatform'].move(i, inst[axis[i]], rel=True, wait=True)
                elif inst["rot_pos_type"]=='idl':
                    pass
                else:
                    raise ValueError('The positioning type %s is not known.', inst["rot_pos_type"])
            if instructions.monochromator:
                results.update({"Wavelength":self.monochromator.GetWave()})
            else:
                results.update({"Wavelength":-1})
            if inst["delay"]>0:
                time.sleep(imst["delay"])

            if self.instructions.sLockIn:
                self.devices['sLockIn']

            if self.instructions.rLockIn:



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





