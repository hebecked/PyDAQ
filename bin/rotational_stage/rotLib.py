import serial
import struct
import numpy as np
import os, sys
from ..parser_wrapper import parsers
###Implement in apt style with cmds, packeger, send packed, recieve package, query, convert units
##other file move left right like started imports low level

#conversion for nice view:             print [hex(i) for i in struct.unpack("I",resp[10:14])]

class rotStages:

    def __init__(self,port="/dev/ttyUSB0", unit="deg", Channels=[False,False,False], init=["Auto","Auto","Auto"]):
        self.port=port
        self.unit=unit #can be %,rad,deg
        self.Controler=rotControler(port)
        if self.Controler.getNChannels()<sum(Channels):
            raise ValueError("Not enough channels provided/available.")
        self.chan=[None,None,None]
        self.pos=[None,None,None]
        for i in range(3):
            if Channels[i]:
                self.chan[i]=rotPlatform(self.Controler,i,init=init[i])
                self.pos[i]=self.convert2Units(self.chan[i].getPos())

    def setUnit(unit="deg"):
        self.unit=unit

    def convert2Units(self,dev_val):
        if self.unit=="rad":
            return dev_val*180/(75091*np.pi) #*5.4546
        elif self.unit=="%":
            return dev_val*3.6/75091 #*5.4546
        elif self.unit=="deg":
            return dev_val/75091 #*5.4546
        elif self.unit=="dev":
            return dev_val
        else:
            raise ValueError("Unknown unit.")

    def convert2Steps(self,units):
        if self.unit=="rad":
            return int(units*75091*np.pi/180) #/5.4546
        elif self.unit=="%":
            return int(units*75091/3.6) #/5.4546
        elif self.unit=="deg":
            return int(units*75091) #/5.4546
        elif self.unit=="dev":
            return int(units)
        else:
            raise ValueError("Unknown unit.")

    def goHome(self,chan):
        self.chan[chan].goHome()
        self.pos[chan]=self.convert2Units(self.chan[chan].getPos())

    def move(self, chan, pos, rel=False, wait=True):#tobe implemented!!!!!
        if not wait:
            print "Not supported yet, will continue with wait."
        self.chan[chan].move( rel=rel, pos=self.convert2Steps(pos))
        self.pos[chan]=self.convert2Units(self.chan[chan].getPos())

    def jog(self,chan,dir_):
        self.chan[chan].go_jogging(dir_=dir_)

    def stopMove(self, chan):
        self.chan[chan].stopMove()
        self.pos[chan]=self.convert2Units(self.chan[chan].getPos())

    def getPos(self,chan):
        self.pos[chan]=self.convert2Units(self.chan[chan].getPos())
        print self.pos[chan]


class rotControler:

    def __init__(self,port="/dev/ttyUSB0"):
        self.port=port
        self.baud=115200
        self.rtscts=True
        self.ser=serial.Serial(self.port ,self.baud, rtscts=self.rtscts)
        self.ser.flushInput()
        self.ser.flushOutput()
        self.ser.flush()
        self.ser.close()
        self._dest = "\x11"
        '''
        # Provide defaults
        self._serial_number = None
        self._model_number = None
        self._hw_type = None
        self._fw_version = None
        self._notes = ""
        self._hw_version = None
        self._mod_state = None
        self._n_channels = 0
        self._channel = ()
        '''
        #initialisation
        self.instruction(self.makePacket( commands.MGMSG_HW_NO_FLASH_PROGRAMMING,"\x00","\x00","\x21"))
        self.instruction(self.makePacket( commands.MGMSG_HW_NO_FLASH_PROGRAMMING,"\x00","\x00","\x22"))
        self.instruction(self.makePacket( commands.MGMSG_HW_NO_FLASH_PROGRAMMING,"\x00","\x00","\x23"))
        # Perform a HW_REQ_INFO to figure out the model number, serial number,
        req_packet =  self.makePacket(commands.HW_REQ_INFO,"\x00","\x00",self._dest)
        hw_info=self.queryInstruction(req_packet, commands.HW_GET_INFO, expectedB=90)    
        self._serial_number = str(hw_info["data"][0:4]).encode('hex')
        self._model_number = str(hw_info["data"][4:12]).replace('\x00', '').strip()
        self._hw_type = struct.unpack('<H', str(hw_info["data"][12:14]))[0] ## should be 44 or 45 as integer. 45=> 'Multi-channel controller motherboard',44=>'Brushless DC controller',else => 'Unknown type: {}'.format(hw_type_int)
        # Note that the fourth byte is padding, so we strip out the first three bytes and format them.
        self._fw_version = "{0[0]}.{0[1]}.{0[2]}".format(str(hw_info["data"][14:18]).encode('hex'))
        self._notes = str(hw_info["data"][18:66]).replace('\x00', '').strip()
        self._hw_version = struct.unpack('<H', str(hw_info["data"][78:80]))[0]
        self._mod_state = struct.unpack('<H', str(hw_info["data"][80:82]))[0]
        self._n_channels = struct.unpack('<H', str(hw_info["data"][82:84]))[0]
        # Create a tuple of channels of length _n_channel_type
        #if self._n_channels > 0:
        #    self._channel = list(self._channel_type(self, chan_idx) for chan_idx in xrange(self._n_channels) )



    def makePacket(self, message_id,param1=None,param2=None,dest=None,source="\x01",data=None):
        #Some sanity checks
        if param1 is not None or param2 is not None:
            has_data = False
        elif data is not None:
            has_data = True
        else:
            raise ValueError("Must specify either parameters or data.")
        if not has_data and (data is not None):
            raise ValueError("A packet can either have parameters or data, but not both.")
        if param1 is None and param2 is None and data is None:
            raise ValueError("You must specify either data or parameters.")
        if dest is None:
            raise ValueError("You must specify a instructions destination.")
        
        packet=struct.pack("H",message_id)
        if has_data:
            data_length=len(data)
            packet+=struct.pack("H",data_length)
            packet+=struct.pack("B",0x80 | struct.unpack("B",dest)[0])
        else:
            packet+=param1
            packet+=param2
            packet+=dest
        packet+=source
        if has_data:
            packet+=data
        return packet

    def readPacket(self, packet, expected, expectedB=6):
        #check for errors first
        if not packet:
            raise ValueError("Expected a packet, got an empty string instead.")
        if len(packet) < 6:
            raise ValueError("Packet must be at least 6 bytes long.")
        if len(packet) < expectedB:
            raise ValueError("The packet is smaller than expected.")
        header = packet[:6]
        if struct.unpack("B", header[4])[0] & 0x80:
            msg_id, length, dest, source = struct.unpack('<HHBB', header)
            dest ^= 0x80 # Turn off 0x80.
            param1 = None
            param2 = None
            data = packet[6 : 6 + length]
        else:
            msg_id, param1, param2, dest, source = struct.unpack('<HBBBB', header)
            data = None
        if msg_id != expected:
            raise ValueError("The return packet (" + str(msg_id) + ") does not match the expected (" + str(expected) + ").")
        return {"message_id":msg_id, "param1":param1, "param2":param2, "dest":dest, "source":source, "data":data}


    def instruction(self, packet):
        self.ser=serial.Serial(self.port, self.baud, rtscts=self.rtscts)
        self.ser.write(packet)
        self.ser.close()

    def queryInstruction(self, packet, expected=None, expectedB=6, decode=True):
        self.ser=serial.Serial(self.port, self.baud, rtscts=self.rtscts)
        self.ser.write(packet)
        recieved=self.ser.read(size=expectedB)
        self.ser.close()
        if decode:
            return self.readPacket(recieved, expected, expectedB)
        return recieve

    def recieve(self, expected, expectedB=6, block=True, decode=True):
        if block:
            self.ser=serial.Serial(self.port, self.baud, rtscts=self.rtscts, timeout=None)
        else:
            self.ser=serial.Serial(self.port, self.baud, rtscts=self.rtscts, timeout=0.01)
        recieved=self.ser.read(size=expectedB)
        self.ser.close()
        if decode:
            return self.readPacket(recieved, expected, expectedB)
        return recieve

    def getNChannels(self):
        return self._n_channels


class rotPlatform:

    def __init__(self,rotControler, platform, init="Auto"):
        self.rotControler=rotControler
        if platform==0:
            self.num="\x21"
            self.bay="\x01"
        elif platform==1:
            self.num="\x22"
            self.bay="\x02"
        elif platform==2:
            self.num="\x23"
            self.bay="\x03"
        else:
            raise ValueError("You must choose a platform channel between [0-2].")

        #if not self.bayOccupied():
        #   raise AttributeError("Bay " + str(platform) + "is empty.")

        if not init:
            if not self.getDevicePos():
                raise ValueError("Device is not initialized.")
        elif init=="Auto":
            if self.getDevicePos():
                return


        pkt=self.rotControler.makePacket(commands.HW_REQ_INFO, "\x00","\x00",self.num)
        info_pkt=self.rotControler.queryInstruction(pkt, commands.HW_GET_INFO, expectedB=90,)
        self.enable()
        self._sendInstructionPacket(commands.MOD_SET_DIGOUTPUTS,"\x00","\x00",self.num )
        self._sendInstructionPacket(commands.MOT_SET_TRIGGER,"\x01","\x10",self.num )
        self._sendInstructionPacket(commands.MOT_SET_VELPARAMS,dest=self.num, data="\x01\x00\x00\x00\x00\x00\xA1\x50\x00\x00\xD0\x34\x03\x04")
        self._sendInstructionPacket(commands.MOT_SET_JOGPARAMS,dest=self.num,data="\x01\x00\x01\x00\xAA\x92\x00\x00\xE7\x14\x00\x00\x20\x10\x00\x00\x9C\x0A\x67\x02\x02\x00")
        self._sendInstructionPacket(commands.MOT_SET_LIMSWITCHPARAMS,dest=self.num ,data="\x01\x00\x03\x00\x01\x00\xFE\x6F\x03\x00\x55\x25\x01\x00\x81\x00")
        self._sendInstructionPacket(commands.MOT_SET_POWERPARAMS,dest=self.num ,data="\x01\x00\x0F\x00\x1E\x00")
        self._sendInstructionPacket(commands.MOT_SET_GENMOVEPARAMS,dest=self.num ,data="\x01\x00\x55\x25\x01\x00")
        self._sendInstructionPacket(commands.MOT_SET_HOMEPARAMS,dest=self.num ,data="\x01\x00\x02\x00\x01\x00\x72\x06\x71\x01\x00\xB0\x00\x00")
        #removed rel and abs move param
        self._sendInstructionPacket(commands.MOT_SET_BOWINDEX,dest=self.num ,data="\x01\x00\x00\x00")
        self._sendInstructionPacket(commands.MOT_SET_PMDJOYSTICKPARAMS,dest=self.num ,data="\x01\x00\x9C\x0A\x67\x02\x38\x15\xCE\x04\x40\x20\x00\x00\x81\x40\x00\x00\x01\x00")
        self.goHome()

    def _sendInstructionPacket(self, message_id,param1=None,param2=None,dest=None,source="\x01",data=None):
        self.rotControler.instruction( self.rotControler.makePacket(message_id,param1,param2,dest,source,data) )

    def getDevicePos(self):
        self.pos=0
        pkt = self.rotControler.makePacket(commands.MOT_REQ_STATUSUPDATE, param1=self.bay, param2="\x00", dest=self.num)
        resp = self.rotControler.queryInstruction(pkt, commands.MOT_GET_STATUSUPDATE, expectedB=20)
        self.pos= struct.unpack('i', str(resp["data"][2:6]))[0]
        return True

    def enabled(self):
        pkt = self.rotControler.makePacket(commands.MOD_REQ_CHANENABLESTATE, param1=self.bay, param2="\x00", dest=self.rotControler._dest)
        resp = self.rotControler.queryInstruction(pkt, commands.MOD_GET_CHANENABLESTATE)
        return not bool(resp["param2"] - 1)

    def enable(self, enable=True):
        self._sendInstructionPacket(commands.MOD_SET_CHANENABLESTATE,param1=self.bay,param2="\x01" if enable else "\x02",dest=self.rotControler._dest)

    def bayOccupied(self):
        result=self.rotControler.queryInstruction( self.rotControler.makePacket(commands.RACK_REQ_BAYUSED,self.bay,"\x00",self.num), commands.RACK_GET_BAYUSED)#549)
        if result["param2"]=='\x02':
            return False
        elif result["param2"]=='\x01':
            return True
        else:
            raise ValueError("Unexpected return value (" + str(result["param2"]) + ").")

    def goHome(self, block=True):
        pkt = self.rotControler.makePacket(commands.MOT_MOVE_HOME, param1="\x01", param2="\x00", dest=self.num)
        resp = self.rotControler.instruction(pkt)
        moving=block
        while moving:
            resp = self.getStatus()["data"]
            res=struct.unpack("I",resp[10:14])
            if res[0]&int('0x00000400',16):
                moving = False
        self.getDevicePos()


    def move(self, rel=False, pos=0, block=True):
        pos=struct.pack('i',pos)
        if rel:
            pkt = self.rotControler.makePacket(commands.MOT_MOVE_RELATIVE, dest=self.num, data="\x01\x00" + pos)
        else:
            pkt = self.rotControler.makePacket(commands.MOT_MOVE_ABSOLUTE, dest=self.num, data="\x01\x00" + pos)
        self.rotControler.instruction(pkt)#, commands.MOT_MOVE_COMPLETED, expectedB=20)
        moving=block
        while moving:
            resp = self.getStatus()["data"]
            res=struct.unpack("I",resp[10:14])
            if not res[0]&int('0x00000020',16) and not res[0]&int('0x00000010',16):
                moving = False
        self.getDevicePos()


    def stopMove(self):
        pkt = self.rotControler.makePacket(commands.MOT_MOVE_STOP, param1="\x01", param2="\x01", dest=self.num)
        resp = self.rotControler.queryInstruction(pkt, commands.MOT_MOVE_STOPPED, expectedB=20)
        self.getDevicePos()

    def go_jogging(self, dir_=1):
        self._sendInstructionPacket(commands.MOT_MOVE_JOG,param1="\x01",param2="\x01" if dir_>0 else "\x02",dest=self.num)

    def getPos(self):
        return self.pos

    def setVelParams(self,min_vel='\x00\x00\x00\x00',accel='\xA1\x50\x00\x00',max_vel='\xD0\x34\x03\x04'):#struct.pack("I",vals)
        self._sendInstructionPacket(commands.MOT_SET_VELPARAMS,dest=self.num, data="\x01\x00" + min_vel + accel + max_vel)

    def getStatus(self):
        pkt = self.rotControler.makePacket(commands.MOT_REQ_STATUSUPDATE, param1=self.bay, param2="\x00", dest=self.num)
        resp = self.rotControler.queryInstruction(pkt, commands.MOT_GET_STATUSUPDATE, expectedB=20)
        return resp


from flufl.enum import IntEnum
class commands(IntEnum):
    # General System Commands
    MOD_IDENTIFY            = 0x0223
    MOD_SET_CHANENABLESTATE = 0x0210
    MOD_REQ_CHANENABLESTATE = 0x0211
    MOD_GET_CHANENABLESTATE = 0x0212
    HW_DISCONNECT           = 0x0002
    HW_RESPONSE             = 0x0080
    HW_RICHRESPONSE         = 0x0081
    HW_START_UPDATEMSGS     = 0x0011
    HW_STOP_UPDATEMSGS      = 0x0012
    HW_REQ_INFO             = 0x0005
    HW_GET_INFO             = 0x0006
    RACK_REQ_BAYUSED        = 0x0060
    RACK_GET_BAYUSED        = 0x0061
    HUB_REQ_BAYUSED         = 0x0065
    HUB_GET_BAYUSED         = 0x0066
    RACK_REQ_STATUSBITS     = 0x0226
    RACK_GET_STATUSBITS     = 0x0227
    RACK_SET_DIGOUTPUTS     = 0x0228
    RACK_REQ_DIGOUTPUTS     = 0x0229
    RACK_GET_DIGOUTPUTS     = 0x0230
    MOD_SET_DIGOUTPUTS      = 0x0213
    MOD_REQ_DIGOUTPUTS      = 0x0214
    MOD_GET_DIGOUTPUTS      = 0x0215

    # Motor Control Messages
    MGMSG_HW_NO_FLASH_PROGRAMMING = 0x0018
    MOT_SET_POSCOUNTER      = 0x0410
    MOT_REQ_POSCOUNTER      = 0x0411
    MOT_GET_POSCOUNTER      = 0x0412
    MOT_SET_ENCCOUNTER      = 0x0409
    MOT_REQ_ENCCOUNTER      = 0x040A
    MOT_GET_ENCCOUNTER      = 0x040B
    MOT_SET_VELPARAMS       = 0x0413
    MOT_REQ_VELPARAMS       = 0x0414
    MOT_GET_VELPARAMS       = 0x0415
    MOT_SET_JOGPARAMS       = 0x0416
    MOT_REQ_JOGPARAMS       = 0x0417
    MOT_GET_JOGPARAMS       = 0x0418
    MOT_REQ_ADCINPUTS       = 0x042B
    MOT_GET_ADCINPUTS       = 0x042C
    MOT_SET_POWERPARAMS     = 0x0426
    MOT_REQ_POWERPARAMS     = 0x0427
    MOT_GET_POWERPARAMS     = 0x0428
    MOT_SET_GENMOVEPARAMS   = 0x043A
    MOT_REQ_GENMOVEPARAMS   = 0x043B
    MOT_GET_GENMOVEPARAMS   = 0x043C
    MOT_SET_MOVERELPARAMS   = 0x0445
    MOT_REQ_MOVERELPARAMS   = 0x0446
    MOT_GET_MOVERELPARAMS   = 0x0447
    MOT_SET_MOVEABSPARAMS   = 0x0450
    MOT_REQ_MOVEABSPARAMS   = 0x0451
    MOT_GET_MOVEABSPARAMS   = 0x0452
    MOT_SET_HOMEPARAMS      = 0x0440
    MOT_REQ_HOMEPARAMS      = 0x0441
    MOT_GET_HOMEPARAMS      = 0x0442
    MOT_SET_LIMSWITCHPARAMS = 0x0423
    MOT_REQ_LIMSWITCHPARAMS = 0x0424
    MOT_GET_LIMSWITCHPARAMS = 0x0425
    MOT_MOVE_HOME           = 0x0443
    MOT_MOVE_HOMED          = 0x0444
    MOT_MOVE_RELATIVE       = 0x0448
    MOT_MOVE_COMPLETED      = 0x0464
    MOT_MOVE_ABSOLUTE       = 0x0453
    MOT_MOVE_JOG            = 0x046A
    MOT_MOVE_VELOCITY       = 0x0457
    MOT_MOVE_STOP           = 0x0465
    MOT_MOVE_STOPPED        = 0x0466
    MOT_SET_BOWINDEX        = 0x04F4
    MOT_REQ_BOWINDEX        = 0x04F5
    MOT_GET_BOWINDEX        = 0x04F6
    MOT_SET_DCPIDPARAMS     = 0x04A0
    MOT_REQ_DCPIDPARAMS     = 0x04A1
    MOT_GET_DCPIDPARAMS     = 0x04A2
    MOT_SET_AVMODES         = 0x04B3
    MOT_REQ_AVMODES         = 0x04B4
    MOT_GET_AVMODES         = 0x04B5
    MOT_SET_POTPARAMS = 0x04B0
    MOT_REQ_POTPARAMS = 0x04B1
    MOT_GET_POTPARAMS = 0x04B2
    MOT_SET_BUTTONPARAMS = 0x04B6
    MOT_REQ_BUTTONPARAMS = 0x04B7
    MOT_GET_BUTTONPARAMS = 0x04B8
    MOT_SET_EEPROMPARAMS = 0x04B9
    MOT_SET_PMDPOSITIONLOOPPARAMS = 0x04D7
    MOT_REQ_PMDPOSITIONLOOPPARAMS = 0x04D8
    MOT_GET_PMDPOSITIONLOOPPARAMS = 0x04D9
    MOT_SET_PMDMOTOROUTPUTPARAMS = 0x04DA
    MOT_REQ_PMDMOTOROUTPUTPARAMS = 0x04DB
    MOT_GET_PMDMOTOROUTPUTPARAMS = 0x04DC
    MOT_SET_PMDTRACKSETTLEPARAMS = 0x04E0
    MOT_REQ_PMDTRACKSETTLEPARAMS = 0x04E1
    MOT_GET_PMDTRACKSETTLEPARAMS = 0x04E2
    MOT_SET_PMDPROFILEMODEPARAMS = 0x04E3
    MOT_REQ_PMDPROFILEMODEPARAMS = 0x04E4
    MOT_GET_PMDPROFILEMODEPARAMS = 0x04E5
    MOT_SET_PMDJOYSTICKPARAMS = 0x04E6
    MOT_REQ_PMDJOYSTICKPARAMS = 0x04E7
    MOT_GET_PMDJOYSTICKPARAMS = 0x04E8
    MOT_SET_PMDCURRENTLOOPPARAMS = 0x04D4
    MOT_REQ_PMDCURRENTLOOPPARAMS = 0x04D5
    MOT_GET_PMDCURRENTLOOPPARAMS = 0x04D6
    MOT_SET_PMDSETTLEDCURRENTLOOPPARAMS = 0x04E9
    MOT_REQ_PMDSETTLEDCURRENTLOOPPARAMS = 0x04EA
    MOT_GET_PMDSETTLEDCURRENTLOOPPARAMS = 0x04EB
    MOT_SET_PMDSTAGEAXISPARAMS = 0x04F0
    MOT_REQ_PMDSTAGEAXISPARAMS = 0x04F1
    MOT_GET_PMDSTAGEAXISPARAMS = 0x04F2
    MOT_GET_STATUSUPDATE = 0x0481
    MOT_REQ_STATUSUPDATE = 0x0480
    MOT_GET_DCSTATUSUPDATE = 0x0491
    MOT_REQ_DCSTATUSUPDATE = 0x0490
    MOT_ACK_DCSTATUSUPDATE = 0x0492
    MOT_REQ_STATUSBITS = 0x0429
    MOT_GET_STATUSBITS = 0x042A
    MOT_SUSPEND_ENDOFMOVEMSGS = 0x046B
    MOT_RESUME_ENDOFMOVEMSGS = 0x046C
    MOT_SET_TRIGGER = 0x0500
    MOT_REQ_TRIGGER = 0x0501
    MOT_GET_TRIGGER = 0x0502

    # Solenoid Control Messages
    MOT_SET_SOL_OPERATINGMODE = 0x04C0
    MOT_REQ_SOL_OPERATINGMODE = 0x04C1
    MOT_GET_SOL_OPERATINGMODE = 0x04C2
    MOT_SET_SOL_CYCLEPARAMS = 0x04C3
    MOT_REQ_SOL_CYCLEPARAMS = 0x04C4
    MOT_GET_SOL_CYCLEPARAMS = 0x04C5
    MOT_SET_SOL_INTERLOCKMODE = 0x04C6
    MOT_REQ_SOL_INTERLOCKMODE = 0x04C7
    MOT_GET_SOL_INTERLOCKMODE = 0x04C8
    MOT_SET_SOL_STATE = 0x04CB
    MOT_REQ_SOL_STATE = 0x04CC
    MOT_GET_SOL_STATE = 0x04CD



if __name__=='__main__':

    parser=parsers("This Program is meant as a DAQ for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")
    ##move to sub processes:
    parser.add_argument( "angle1", "-a1", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 1 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
    parser.add_argument( "angle2", "-a2", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 2 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
    parser.add_argument( "angle3", "-a3", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 3 to the absolute position in degrees. For positive values it will go right and for negative values left. Will be run before -i.')
    parser.add_argument( "angle1r", "-a1r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 1 relative to the current position in units of degree. Will be run before -i.')
    parser.add_argument( "angle2r", "-a2r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 2 relative to the current position in units of degree. Will be run before -i.')
    parser.add_argument( "angle3r", "-a3r", float, group="RotationalPlatform", default=None, help='Moves the rotational platform 3 relative to the current position in units of degree. Will be run before -i.')

    arguments=parser.done()
