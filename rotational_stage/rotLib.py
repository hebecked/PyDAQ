import serial
import struct
###Implement in apt style with cmds, packeger, send packed, recieve package, query, convert units
##other file move left right like started imports low level


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
            packet+=struckt.pack("H",data_length)
            packet+=struckt.pack("B",0x80 | struckt.unpack("B",dest)[0])
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
            raise ValueError("The return packet does not match the expected.")
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


class rotPlatform():

    def __init__(self,rotControler, platform, init=True):
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
        if not init:
            self.getPos()
            return


        if not self.bayOccupied():
           raise AttributeError("Bay " + str(platform) + "is empty.")
        pkt=self.rotControler.makePacket(commands.HW_REQ_INFO, "\x00","\x00",self.num)
        info_pkt=self.rotControler.queryInstruction(pkt, commands.HW_GET_INFO, expectedB=90,)
        self.enable()
        self._sendInstructionPacket(commands.MOD_SET_DIGOUTPUTS,"\x00","\x00",self.num )
        self._sendInstructionPacket(commands.MOT_SET_TRIGGER,"\x01","\x10",self.num )
        self._sendInstructionPacket(commands.MOD_SET_VELPARAMS,dest=self.num, data="\x01\x00\x00\x00\x00\x00\xA1\x50\x00\x00\xD0\x34\x03\x00")
        self._sendInstructionPacket(commands.MOD_SET_JOGPARAMS,dest=self.num,data="\x01\x00\x02\x00\xAA\x92\x00\x00\xE7\x14\x00\x00\x20\x10\x00\x00\x9C\x0A\x67\x02\x02\x00")
        self._sendInstructionPacket(commands.MOD_SET_LIMSWITCHPARAMS,dest=self.num ,data="\x01\x00\x03\x00\x01\x00\xFE\x6F\x03\x00\x55\x25\x01\x00\x81\x00")
        self._sendInstructionPacket(commands.MOD_SET_POWERPARAMS,dest=self.num ,data="\x01\x00\x0F\x00\x1E\x00")
        self._sendInstructionPacket(commands.MOD_SET_GENMOVEPARAMS,dest=self.num ,data="\x01\x00\x55\x25\x01\x00")
        self._sendInstructionPacket(commands.MOT_SET_HOMEPARAMS,dest=self.num ,data="\x01\x00\x02\x00\x01\x00\x72\x06\x71\x01\x00\xB0\x00\x00")
        #removed rel and abs move param
        self._sendInstructionPacket(commands.MOD_SET_BOWINDEX,dest=self.num ,data="\x01\x00\x00\x00")
        self._sendInstructionPacket(commands.MOD_SET_PMDJOYSTICKPARAMS,dest=self.num ,data="\x01\x00\x9C\x0A\x67\x02\x38\x15\xCE\x04\x40\x20\x00\x00\x81\x40\x00\x00\x01\x00")
        self.goHome()

    def _sendInstructionPacket(self, message_id,param1=None,param2=None,dest=None,source="\x01",data=None):
        self.rotControler.instruction( self.rotControler.makePacket(message_id,param1,param2,dest,source,data) )

    def getPos(self):
        print "do"#self.pos=x

    def enabled(self):
        pkt = self.rotControler.makePacket(commands.MOD_REQ_CHANENABLESTATE, param1=self.bay, param2="\x00", dest=self.rotControler._dest)
        resp = self.rotControler.queryInstruction(pkt, commands.MOD_GET_CHANENABLESTATE)
        return not bool(resp["param2"] - 1)

    def enable(self, enable=True):
        pkt = self._sendInstructionPacket(commands.MOD_SET_CHANENABLESTATE,param1=self.bay,param2="\x01" if enable else "\x02",dest=self.rotControler._dest)

    def bayOccupied(self):
        result=self.rotControler.queryInstruction( self.rotControler.makePacket(commands.RACK_REQ_BAYUSED,self.bay,"\x00",self.num), commands.RACK_GET_BAYUSED)
        if result["param2"]=='\x02':
            return False
        elif result["param2"]=='\x01':
            return True
        else:
            raise ValueError("Unexpected return value.")

    def goHome(self):#rework
        pkt = self.rotControler.makePacket(commands.MOT_MOVE_HOME, param1="\x01", param2="\x00", dest=self.num)
        resp = self.rotControler.queryInstruction(pkt, commands.MOT_MOVE_HOMED) 
        self.pos=0


    def stopMove(self):
        #pkt = self.rotControler.makePacket(commands.MOD_REQ_CHANENABLESTATE, param1=self.bay, param2="\x00", dest=self.rotControler._dest)
        #resp = self.rotControler.queryInstruction(pkt, commands.MOD_GET_CHANENABLESTATE)

        self.ser=serial.Serial(self.port,self.baud,rtscts=self.rtscts)
        self.ser.write("\x65\x04" + self.bay + "\x01\x11\x01")
        result=self.ser.read(size=6)
        self.ser.close()

    def move(self):


    def getPos(self):

    #change vel accel 

#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#########################################################################################
#
#class ThorLabsAPT(_abstract.ThorLabsInstrument):
#    '''
#    Generic ThorLabs APT hardware device controller. Communicates using the 
#    ThorLabs APT communications protocol, whose documentation is found in the
#    thorlabs source folder.
#    '''
#    
#    class APTChannel(object):
#        '''
#        Represents a channel within the hardware device. One device can have 
#        many channels, each labeled by an index.
#        '''
#        def __init__(self, apt, idx_chan):
#            self._apt = apt
#            # APT is 1-based, but we want the Python representation to be
#            # 0-based.
#            self._idx_chan = idx_chan + 1
#            
#        @property
#        def enabled(self):
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOD_REQ_CHANENABLESTATE,
#                                          param1=self._idx_chan,
#                                          param2=0x00,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=None)
#            resp = self._apt.querypacket(pkt, expect=_cmds.ThorLabsCommands.MOD_GET_CHANENABLESTATE)
#            return not bool(resp._param2 - 1)
#        @enabled.setter
#        def enabled(self, newval):
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOD_SET_CHANENABLESTATE,
#                                          param1=self._idx_chan,
#                                          param2=0x01 if newval else 0x02,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=None)
#            self._apt.sendpacket(pkt)
#    
#    _channel_type = APTChannel
#    
#    def __init__(self, filelike):
#        super(ThorLabsAPT, self).__init__(filelike)
#        self._dest = 0x50 # Generic USB device; make this configurable later.
#        
#        # Provide defaults in case an exception occurs below.
#        self._serial_number = None
#        self._model_number = None
#        self._hw_type = None
#        self._fw_version = None
#        self._notes = ""
#        self._hw_version = None
#        self._mod_state = None
#        self._n_channels = 0
#        self._channel = ()
#        
#        # Perform a HW_REQ_INFO to figure out the model number, serial number,
#        # etc.
#        try:
#            req_packet = _packets.ThorLabsPacket(
#                message_id=_cmds.ThorLabsCommands.HW_REQ_INFO,
#                param1=0x00,
#                param2=0x00,
#                dest=self._dest,
#                source=0x01,
#                data=None
#                )
#            hw_info = self.querypacket(req_packet, expect=_cmds.ThorLabsCommands.HW_GET_INFO)
#            
#            self._serial_number = str(hw_info._data[0:4]).encode('hex')
#            self._model_number  = str(hw_info._data[4:12]).replace('\x00', '').strip()
#            
#            hw_type_int = struct.unpack('<H', str(hw_info._data[12:14]))[0]
#            if hw_type_int == 45:
#                self._hw_type = 'Multi-channel controller motherboard'
#            elif hw_type_int == 44:
#                self._hw_type = 'Brushless DC controller'
#            else:
#                self._hw_type = 'Unknown type: {}'.format(hw_type_int)
#            
#            # Note that the fourth byte is padding, so we strip out the first
#            # three bytes and format them.
#            self._fw_version    = "{0[0]}.{0[1]}.{0[2]}".format(
#                str(hw_info._data[14:18]).encode('hex')
#            )
#            self._notes         = str(hw_info._data[18:66]).replace('\x00', '').strip()
#            
#            self._hw_version    = struct.unpack('<H', str(hw_info._data[78:80]))[0]
#            self._mod_state     = struct.unpack('<H', str(hw_info._data[80:82]))[0]
#            self._n_channels    = struct.unpack('<H', str(hw_info._data[82:84]))[0]
#        except Exception as e:
#            logger.error("Exception occured while fetching hardware info: {}".format(e))
#
#        # Create a tuple of channels of length _n_channel_type
#        if self._n_channels > 0:
#            self._channel = list(self._channel_type(self, chan_idx) for chan_idx in xrange(self._n_channels) )
#    
#    @property
#    def serial_number(self):
#        return self._serial_number
#    
#    @property
#    def model_number(self):
#        return self._model_number
#        
#    @property
#    def name(self):
#        return "ThorLabs APT Instrument model {model}, serial {serial} (HW version {hw_ver}, FW version {fw_ver})".format(
#            hw_ver=self._hw_version, serial=self.serial_number, 
#            fw_ver=self._fw_version, model=self.model_number
#        )
#                
#    @property
#    def channel(self):
#        return self._channel
#        
#    @property
#    def n_channels(self):
#        return self._n_channels
#        
#    @n_channels.setter
#    def n_channels(self, nch):
#        # Change the number of channels so as not to modify those instances already existing:
#        # If we add more channels, append them to the list,
#        # If we remove channels, remove them from the end of the list.
#        if nch > self._n_channels:
#            self._channel = self._channel + \
#                list( self._channel_type(self, chan_idx) for chan_idx in xrange(self._n_channels, nch) )
#        elif nch < self._n_channels:
#            self._channel = self._channel[:nch]
#        self._n_channels = nch
#    
#    def identify(self):
#        '''
#        Causes a light on the APT instrument to blink, so that it can be
#        identified.
#        '''
#        pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOD_IDENTIFY,
#                                      param1=0x00,
#                                      param2=0x00,
#                                      dest=self._dest,
#                                      source=0x01,
#                                      data=None)
#        self.sendpacket(pkt)
#
#class APTMotorController(ThorLabsAPT):
#
#    class MotorChannel(ThorLabsAPT.APTChannel):
#    
#        ## INSTANCE VARIABLES ##
#        
#        #: Sets the scale between the encoder counts and physical units
#        #: for the position, velocity and acceleration parameters of this
#        #: channel. By default, set to dimensionless, indicating that the proper
#        #: scale is not known.
#        #:
#        #: In keeping with the APT protocol documentation, the scale factor
#        #: is multiplied by the physical quantity to get the encoder count,
#        #: such that scale factors should have units similar to microsteps/mm,
#        #: in the example of a linear motor.
#        #:
#        #: Encoder counts are represented by the quantities package unit
#        #: "ct", which is considered dimensionally equivalent to dimensionless.
#        #: Finally, note that the "/s" and "/s**2" are not included in scale
#        #: factors, so as to produce quantities of dimension "ct/s" and "ct/s**2"
#        #: from dimensionful input.
#        #: 
#        #: For more details, see the APT protocol documentation.
#        scale_factors = (pq.Quantity(1, 'dimensionless'), ) * 3
#        
#        __SCALE_FACTORS_BY_MODEL = {
#            re.compile('TST001|BSC00.|BSC10.|MST601'): {
#                # Note that for these drivers, the scale factors are identical
#                # for position, velcoity and acceleration. This is not true for
#                # all drivers!
#                'DRV001': (pq.Quantity(51200, 'ct/mm'),) * 3,
#                'DRV013': (pq.Quantity(25600, 'ct/mm'),) * 3,
#                'DRV014': (pq.Quantity(25600, 'ct/mm'),) * 3,
#                'DRV113': (pq.Quantity(20480, 'ct/mm'),) * 3,
#                'DRV114': (pq.Quantity(20480, 'ct/mm'),) * 3,
#                'FW103':  (pq.Quantity(25600/360, 'ct/deg'),) * 3,
#                'NR360':  (pq.Quantity(25600/5.4546, 'ct/deg'),) * 3
#            },
#            # TODO: add other tables here.
#        }
#        
#        __STATUS_BIT_MASK = {
#            'CW_HARD_LIM':          0x00000001,
#            'CCW_HARD_LIM':         0x00000002,
#            'CW_SOFT_LIM':          0x00000004,
#            'CCW_SOFT_LIM':         0x00000008,
#            'CW_MOVE_IN_MOTION':    0x00000010,
#            'CCW_MOVE_IN_MOTION':   0x00000020,
#            'CW_JOG_IN_MOTION':     0x00000040,
#            'CCW_JOG_IN_MOTION':    0x00000080,
#            'MOTOR_CONNECTED':      0x00000100,
#            'HOMING_IN_MOTION':     0x00000200,
#            'HOMING_COMPLETE':      0x00000400,
#            'INTERLOCK_STATE':      0x00001000
#        }
#    
#        ## UNIT CONVERSION METHODS ##
#        
#        def set_scale(self, motor_model):
#            """
#            Sets the scale factors for this motor channel, based on the model
#            of the attached motor and the specifications of the driver of which
#            this is a channel.
#            
#            :param str motor_model: Name of the model of the attached motor,
#                as indicated in the APT protocol documentation (page 14, v9).
#            """
#            for driver_re, motor_dict in self.__SCALE_FACTORS_BY_MODEL.iteritems():
#                if driver_re.match(self._apt.model_number) is not None:
#                    if motor_model in motor_dict:
#                        self.scale_factors = motor_dict[motor_model]
#                        return
#                    else:
#                        break
#            # If we've made it down here, emit a warning that we didn't find the
#            # model.
#            logger.warning(
#                "Scale factors for controller {} and motor {} are unknown".format(
#                    self._apt.model_number, motor_model
#                )
#            )
#    
#        ## MOTOR COMMANDS ##
#        
#        @property
#        def status_bits(self):
#            # NOTE: the difference between MOT_REQ_STATUSUPDATE and MOT_REQ_DCSTATUSUPDATE confuses me
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOT_REQ_STATUSUPDATE,
#                                          param1=self._idx_chan,
#                                          param2=0x00,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=None)
#            # The documentation claims there are 14 data bytes, but it seems there are sometimes
#            # some extra random ones...
#            resp_data = self._apt.querypacket(pkt)._data[:14]
#            ch_ident, position, enc_count, status_bits = struct.unpack('<HLLL', resp_data)
#            
#            status_dict = dict(
#                (key, (status_bits & bit_mask > 0))
#                for key, bit_mask in self.__STATUS_BIT_MASK.iteritems()
#            )
#            
#            return status_dict
#        
#        @property
#        def position(self):
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOT_REQ_POSCOUNTER,
#                                          param1=self._idx_chan,
#                                          param2=0x00,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=None)
#            response = self._apt.querypacket(pkt, expect=_cmds.ThorLabsCommands.MOT_GET_POSCOUNTER)
#            chan, pos = struct.unpack('<Hl', response._data)
#            return pq.Quantity(pos, 'counts') / self.scale_factors[0]
#            
#        @property
#        def position_encoder(self):
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOT_REQ_ENCCOUNTER,
#                                          param1=self._idx_chan,
#                                          param2=0x00,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=None)
#            response = self._apt.querypacket(pkt, expect=_cmds.ThorLabsCommands.MOT_GET_ENCCOUNTER)
#            chan, pos = struct.unpack('<Hl', response._data)
#            return pq.Quantity(pos, 'counts')
#        
#        def go_home(self):
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOT_MOVE_HOME,
#                                          param1=self._idx_chan,
#                                          param2=0x00,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=None)
#            self._apt.sendpacket(pkt)
#            
#        def move(self, pos, absolute=True):
#            # Handle units as follows:
#            # 1. Treat raw numbers as encoder counts.
#            # 2. If units are provided (as a Quantity), check if they're encoder
#            #    counts. If they aren't, apply scale factor.
#            if not isinstance(pos, pq.Quantity):
#                pos_ec = int(pos)
#            else:
#                if pos.units == pq.counts:
#                    pos_ec = int(pos.magnitude)
#                else:
#                    scaled_pos = (pos * self.scale_factors[0])
#                    # Force a unit error.
#                    try:
#                        pos_ec = int(scaled_pos.rescale(pq.counts).magnitude)
#                    except:
#                        raise ValueError("Provided units are not compatible with current motor scale factor.")
#            
#            # Now that we have our position as an integer number of encoder
#            # counts, we're good to move.
#            pkt = _packets.ThorLabsPacket(message_id=_cmds.ThorLabsCommands.MOT_MOVE_ABSOLUTE if absolute else _cmds.ThorLabsCommands.MOT_MOVE_RELATIVE,
#                                          param1=None,
#                                          param2=None,
#                                          dest=self._apt._dest,
#                                          source=0x01,
#                                          data=struct.pack('<Hl', self._idx_chan, pos_ec))
#                                          
#            response = self._apt.querypacket(pkt, expect=_cmds.ThorLabsCommands.MOT_MOVE_COMPLETED)
#            
#    _channel_type = MotorChannel
#
##########################################################################################
##########################################################################################
##########################################################################################
##########################################################################################




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
