#! /usr/bin/env python
# -*- coding: utf-8 -*-

#####################################
#                                   #
# Dev: Mickael Rigault              #
# (mrigault@physik.hu0-berlin.de)   #
#
# = IO Control of the 3d Scanner  = #
#
#####################################

import serial
import time
import numpy as N 
# -- Internal functions
import scanner_toolbox as tb
import ScannerPlot     as splot
# -- SCANNER Number
baudrate = 115200
bytesize = 7
stopbits = 1
scan_lag = 0.1 # in s
parity   = serial.PARITY_EVEN
# -- Controler Number


# ========================== #
#  3d Scanner Basic Class    #
# ========================== #
class Scanner( object ):
    """
    """
    # ----------------- #
    # - Security cuts - #
    # ----------------- #
    _x_range = [0,99000]
    _y_range = [0,49000]
    _z_range = [0,42900]
    
    _min_deceleration   = 10000
    
    
    # -------------- #
    # default Values #
    # -------------- #
    # 300 and vcorrectif: such that the up and down scan is as fast as the others
    _default_acceleration = [10,10,300] 
    _vcorrectif           = [1,1,1.01]
    _default_velocity     = 100
    _default_deceleration = 10000
    _sequencing           = [1,2,3] # Defines the axis sorting
    _moving_sequence      = [3,2,1] # Defines the axis sorting
    # ----------------- #
    # - Test Purposes - #
    # ----------------- #
    _known_prefixes =  N.asarray(["Acc","Dec","Vel",
                                  "Ref","Rel","Abs"])
    _known_read_prefixes = N.asarray(["POS"])
    # ----------------- #
    # - Read Stuff    - #
    # ----------------- #
    _end_message = "\x00"
    
    # =========================== #
    # =  GENERAL INPUT OUTPUT   = # 
    # =========================== #
    def __init__(self,port="/dev/tty.usbserial-FTYK04LVD",
                 do_refrun=False,smooth_move=True,
                 debug=True,show=True):
        """
        do_refrun:   [bool] starts by moving the scanner to the [0,0,0] position
        smooth_move: [bool] changes the axis velocities to have a smooth move.
        
        
        """
        self._port   = port
        self._smooth_move = smooth_move
        self._debug  = debug
        self._define_basic_number_()
        
        self._connect_serial_()
        self.load_default_setup()
        # -- This must be done once by scanner switching on/off 
        if do_refrun:
            self.do_refrun()
        else:
            self.current_coords = N.asarray(self.read_position())
            
        self._coord_history = []
        self._coord_forward = []
        # -- Lunch the Visial
        if show:
            self.load_plot()
            self.scannerplot.draw()
            
    def _connect_serial_(self):
        """
        This function connection the Serial port of the scanner
        and register the serial class in self.ser
        """
        self.ser = serial.Serial(self._port, parity=parity,
                                 baudrate=baudrate, bytesize=bytesize,
                                 stopbits=stopbits,
                                 timeout=None,xonxoff=0, rtscts=0)

    def _define_basic_number_(self):
        """
        This function defines the basic number about the scanner
        like the sizes
        """
        self._xsize = N.max(self._x_range) - N.min(self._x_range)
        self._ysize = N.max(self._y_range) - N.min(self._y_range)
        self._zsize = N.max(self._z_range) - N.min(self._z_range)
        self._sizes = N.asarray([self._xsize,self._ysize,self._zsize])
        self._mean_size = N.mean(self._sizes)

        
    def close(self,quick=False):
        """
        quick [bool]: if requested, this will directly close the Scanner.
            -> if false, the scanner first goes back to (0,0,0) 
        """
        if quick is False:
            self.move_to(0,0,0)
            
        self.ser.close()
        
    def __str__(self):
        """
        This function will print basic data from the scanner
        """
        print "SCANNER 3D -- Mickael Rigault main Scanner Class"

    # ======================== #
    # -  USAGE METHODS       - #
    # ======================== #
    def do_refrun(self, sequenced=True):
        """
        This function enables to go to [0,0,0] and initialize the (0,0,0)
        """
        for i in self._moving_sequence:
            self._write_("Ref",axis-1,None)
            if sequenced:
                self._go_(wait_for_it=True)
                
        self.current_coords = N.asarray([0,0,0])



        
    def load_default_setup(self):
        """
        """
        self.change_velocities(   self._default_velocity    )
        self.change_decelerations(self._default_deceleration)
        self.change_accelerations(self._default_acceleration)
        

    # ======================== #
    # -  METHODS TO MOVE     - #
    # ======================== #
    # - Absolute Move
    def move_to(self,x,y,z, unit="cm",
                go=True,smooth_move=None,
                show=True,sequenced=True,
                history_forward=False,clean_forward=True):
        """
        The will move the scanner to x,y,z ; *Absolute Coordinate*
        (see shift_to for Relative Coordinate)
        
        x,y,z: integer in `unit` (smaller = 10*micrometer)
             (scanner unit = 10 microns)
        
        unit: unit of the given x,y,z parameter (see scanner_toolbox.value_in_micron)
              (could be e.g., m,cm, mm ...)
              -> Spectial units: *percent* means in fraction of the size of the scanner
                                 *scanner* means 10 mim (unit of the scanner)
              = This input goes to _get_requested_coordinate_ =

        smooth_move: [bool/None] if None the default registered value will be used.
                     -> if bool this will overwrite self._smooth_move

        sequenced: [bool] = will set smooth_move to False =
              The Scanner will move 1 dimension after the other.
        """
        if sequenced:
            smooth_move = False
            
        # -- What is going to happen
        self._requested_coords = self._get_requested_coordinate_(x,y,z,unit=unit,
                                                                 shift=False)
        self._requested_shift = self._requested_coords - self.current_coords
        if (self._requested_shift == N.asarray([0,0,0])).all():
            print "WARNING: You requested the coordinate you currently have. Nothing happens"
            return
        
        # -- Can we ? 
        self._test_final_coords_(*self._requested_coords)
        self._test_path_(*self._requested_coords)

        # -- How do we go there:
        if smooth_move is not None:
            self._smooth_move = smooth_move
            
        if self._smooth_move:
            self._load_smooth_velocities_(*self._requested_shift)
            
        # -- Ok? So sent the command
        for i in self._moving_sequence:
            axis = i-1
            self._write_("Abs",axis,self._requested_coords[axis])
            if sequenced:
                self._go_(wait_for_it=True)

        # -- And let's go!
        if go:
            if sequenced is False:
                self._go_()
            # -- Scave what you just did
            if "current_coords" in dir(self):
                if history_forward:
                    self._coord_forward.append(self.current_coords)
                else:
                    self._coord_history.append(self.current_coords)
                    if clean_forward:
                        self._coord_forward = []
                        
            self.current_coords = N.asarray(self._requested_coords)
            # -- Show what you have
            if show:
                if "scannerplot" not in dir(self):
                    self.load_plot()
                else:
                    self.scannerplot.draw()
                
    # - Relative shift
    def shift_to(self,x,y,z, unit="cm",**kwargs):
        """
        The will move the scanner to x,y,z in comparison to what was their before;
        *Relative Coordinate*
        (see move_to for Absolute Coordinate)
        = The requested shifted coord is than sent to self.move_to =
        
        x,y,z: integer in `unit` (smaller = 10*micrometer)
             (scanner unit = 10 microns)

        unit: unit of the given x,y,z parameter (see scanner_toolbox.value_in_micron)
              (could be e.g., m,cm, mm ...)
              -> Spectial units: *percent* means in fraction of the size of the scanner
                                 *scanner* means 10 mim (unit of the scanner)
              = This input goes to _get_requested_coordinate_ =
              
        **kwargs: goes to self.move_to
        """
        self._requested_coords = self._get_requested_coordinate_(x,y,z,unit=unit,
                                                                 shift=True)
        
        self.move_to(*self._requested_coords,
                     unit="scanner",**kwargs)

        
    def _get_requested_coordinate_(self,x,y,z, unit="cm",
                                   shift=False):
        """
        Information -- This function will translate the given input in requested absolute coordinate.
        
        --------
        x,y,z: integer in `unit` (smaller = 10*micrometer)
               (scanner unit = 10 microns)
        
        unit: unit of the given x,y,z parameter (see scanner_toolbox.value_in_micron)
              (could be e.g., m,cm, mm ...)
              -> Spectial units: *percent* means in fraction of the size of the scanner
                                 *scanner* means 10 mim (unit of the scanner)
             
        shift: [bool] if the requested is in comparison to the current coords

        --------
        return x,y,z in scanner unit 
        """
        # -- What's your unit ?
        
        if unit == "scanner":
            requested_coords = x,y,z
        elif unit == "percent":
            x = tb.relativepercent_to_value(x,self._x_range)
            y = tb.relativepercent_to_value(y,self._y_range)
            z = tb.relativepercent_to_value(z,self._z_range)
            requested_coords = [x,y,z]
        else:  
            requested_coords = N.asarray([tb.value_in_micron(a,unit)/10.
                                          for a in [x,y,z]],dtype="int").T
        if self._debug:
            print "Requested coords, ", requested_coords
            
        # -- Shift or Absolute ?    
        if shift:
            if self._debug:
                print " -> shift request"
            return N.asarray(requested_coords) + N.asarray(self.current_coords)
        
        return N.asarray(requested_coords)


    # -------- 1 axis shifts -------- #
    def go_back(self):
        """
        """
        if "_coord_history" not in dir(self) or \
          len(self._coord_history) < 1:
            raise ValueError("You can not go back (no or too small _coord_history)")
        
        toberemove = self._coord_history.pop(-1)
        self.move_to(*toberemove,unit="scanner",
                     clean_forward=False,
                     history_forward=True)
        
        
    def go_forward(self):
        """
        """
        if "_coord_forward" not in dir(self) or \
          len(self._coord_forward) < 1:
            raise ValueError("You can not go forward (no or too small _coord_forward)")

        toberemove = self._coord_forward.pop(-1)
        self.move_to(*toberemove,unit="scanner",
                     clean_forward=False,
                     history_forward=False)
        
        
    # -------- 1 axis shifts -------- #
    def shift_side(self,x,unit,vx=None):
        """
        This move along the long axis only
        """
        if "current_coords" not in dir(self):
            raise ValueError("There is no known current_coords ; can't move up")

        if vx is not None:
            self.change_1axisVelocity(vx,1)
            
        self.shift_to(x,0,0,unit=unit,
                      smooth_move=False)

    def shift_upanddown(self,z,unit,vz=None):
        """
        This move along the up and down axis only
        """
        if "current_coords" not in dir(self):
            raise ValueError("There is no known current_coords ; can't move up")

        if vz is not None:
            self.change_1axisVelocity(vz,3)
            
        self.shift_to(0,0,z,unit=unit,
                      smooth_move=False)
        
    # ======================== #
    # -  METHODS TO CHANGE   - #
    # ======================== #
    def change_1axisVelocity(self,velocity,axis):
        """
        axis: {1,2,3}
        """
        if axis not in [1,2,3]:
            raise ValueError("The given axis must be 1,2 or 3 (%s given) "%axis)
        new_v    = self.velocities
        new_v[axis-1] = velocity
        self.change_velocities(new_v)
            
    def change_velocities(self,velocity_ies):
        """
        """
        self._initiate_velocities_(velocity_ies)
        self._mean_velocity = N.mean(self.velocities)
        
    def change_decelerations(self,deceleration_s):
        """
        """
        self._initiate_decelerations_(deceleration_s)
        self._mean_deceleration = N.mean(self.decelerations)
        
    def change_accelerations(self,acceleration_s):
        """
        """
        self._initiate_accelerations_(acceleration_s)
        self._mean_acceleration = N.mean(self.accelerations)


    # ======================== #
    # - Visual Basics        - #
    # ======================== #
    def load_plot(self,axin=None):
        """
        """
        self.scannerplot = splot.VisualScanner(self)
        
    # ======================== #
    # - Read Tools           - #
    # ======================== #
    def read_position(self):
        """
        """
        
        x = self._read_message_("POSA1/")
        y = self._read_message_("POSA2/")
        z = self._read_message_("POSA3/")
        return int(x), int(y), int(z)

    
    @tb.timeout(5)
    def _read_message_(self,input_message,
                       max_step=100):
        """
        SHOULD NOT BE USED DIRECTLY
        """
        # -- Input Test -- #
        if ("A1" in input_message or \
            "A2" in input_message or \
            "A3" in input_message) is False:
            raise ValueError("Unknown input message %s"%input_message)
        
        if input_message.split("A")[0] not in self._known_read_prefixes:
            raise ValueError("Unknown input message %s"%input_message)
        
        if input_message[-1] != "/":
            raise ValueError("Incomplete input message (no '/') %s"%input_message)
            
        # -- Send the Request -- #
        self.ser.flushInput()
        self.ser.write(input_message)
        
        message,add = "",""
        i = 0
        while add!=self._end_message:
            add = self.ser.read()
            message += add
            i +=1
            
        return message.split(self._end_message)[0]
    
    # ======================== #
    # -  Low level functions - #
    # ======================== #
    # --- Distances Tools        
    
    # --- Velocities 
    def _initiate_velocities_(self,velocity_ies):
        """
        -- velocity_ies is either a float or an list or 3 floats
            = This will crash if something else is given =
        """
        # -------------- #
        # - Test input - #
        v = tb.Make_Me_Iterable(velocity_ies)
        if len(v) != 1 and len(v) != 3:
            raise ValueError("velocity_ies must either be a float (or [float]) or a array of 3 floats - %d values given"%(len(v)))
        # -> Ok we are good
        
        self.velocities = v
        # -- Share a unique velocity
        if len(self.velocities) == 1:
            self.velocities = list(self.velocities)*3

        if self._debug or self._verbose:
            print "new velocities requested, ",self.velocities
            
        for i,v in enumerate(self.velocities):
            self._write_("Vel",i,v)
            
    def _load_smooth_velocities_(self,delta_x,delta_y,delta_z):
        """
        delta_x,delta_y,delta_z: must be in *scanner* unit
        """
        mean_delta = N.mean([delta_x,delta_y,delta_z])
        self._initiate_velocities_([ N.abs(d/mean_delta) * self._mean_velocity * self._vcorrectif[i]#/self._mean_size
                                    for i,d in enumerate([delta_x,delta_y,delta_z])])
        
    # --- Deceleration
    def _initiate_decelerations_(self,deceleration_s):
        """
        -- deceleration_s is either a float or an list or 3 floats
            = This will crash if something else is given =
        """
        # -------------- #
        # - Test input - #
        d = tb.Make_Me_Iterable(deceleration_s)
        if len(d) != 1 and len(d) != 3:
            raise ValueError("deceleration_s must either be a float (or [float]) or a array of 3 floats - %d values given"%(len(d)))
        
        if (N.asarray(d) < self._min_deceleration).any():
            raise ValueError("decelerations have to be greater than %d"%self._min_deceleration)
        # -> Ok we are good

        self.decelerations = d
        # -- Share a unique velocity
        if len(self.decelerations) == 1:
            self.decelerations = list(self.decelerations)*3
        
        for i,d in enumerate(self.decelerations):
            self._write_("Dec",i,d)
            

    # --- Accelerations
    def _initiate_accelerations_(self,acceleration_s):
        """
        -- acceleration_s is either a float or an list or 3 floats
            = This will crash if something else is given =
        """
        # -------------- #
        # - Test input - #
        d = tb.Make_Me_Iterable(acceleration_s)
        if len(d) != 1 and len(d) != 3:
            raise ValueError("acceleration_s must either be a float (or [float]) or a array of 3 floats - %d values given"%(len(d)))
        
        #if (N.asarray(d) < self._min_deceleration).any():
        #    raise ValueError("decelerations have to be greater than %d"%self._min_deceleration)
        # -> Ok we are good

        self.accelerations = d
        # -- Share a unique velocity
        if len(self.accelerations) == 1:
            self.accelerations = list(self.accelerations)*3
        
        for i,a in enumerate(self.accelerations):
            self._write_("Acc",i,a)
            
        
    # ======================= #
    # - The Tests FUNCTION  - #
    # ======================= #
    def _test_final_coords_(self,x,y,z):
        """
        x,y,z given in micrometer (unit of the scanner)
        """
        if x < self._x_range[0] or x > self._x_range[1]:
            raise ValueError("x (%d) is out of its range"%x)
        if y < self._y_range[0] or y > self._y_range[1]:
            raise ValueError("y (%d) is out of its range"%y)
        if z < self._z_range[0] or z > self._z_range[1]:
            raise ValueError("z (%d) is out of its range"%z)

    def _test_path_(self,x,y,z):
        """
        This will test that all what is in between will be ok.
        == For Now empty Function == 
        """
        return
    
    # ======================= #
    # - The WRITE FUNCTION  - #
    # ======================= #
    def _go_(self, wait_for_it=False):
        """
        """
        self.ser.write("Go/")
        if wait_for_it:
            print " I'll Wait for 4 secondes -> ToBeImproved"
            time.sleep(4) # ToBe Chance
            
        
    def _write_(self,prefix,axis,value,sequenced=False):
        """
        prefix: Must be in the _known_prefixes list (e.g., Acc)
        
        axis:   0,1 or 2 will then use self._sequencing[axis]

        value: a positive integer with 6 or less digits
               -> Could be None for Reference run (prefix=Ref)

        (a `scan_lag` pause will be made afterward)
        """
        # -- Test the Prefix
        if prefix not in self._known_prefixes:
            raise ValueError("%s is not a known prefix"%prefix)

        # -- Test the axis number
        axis_ = N.int(self._sequencing[axis])
        if axis_ not in N.asarray([1,2,3]):
            raise ValueError("axis must be 1, 2, or 3. %d given"%axis)

        # -- Test the input value (could be None)
        if value is None:
            if prefix is not "Ref":
                raise ValueError("Only Reference run (Ref as prefix) can have None as value")
            self.ser.write("%sA%d/"%(prefix,axis_))
            print "sleep 1"
            time.sleep(scan_lag)
            return
        try:
            value_ = "%06d"%value
        except:
            raise ValueError("%s could not be parsed in 06d"%value)
        if len(value_) > 6 or (value < 0 and prefix =="Abs"):
            raise ValueError("value must be an integer with 6 digit max (0< <999999) %d given"%value)

        # - What should be written
        tobewritten = "%sA%d%s/"%(prefix,axis_,value_)
        if self._debug or self._verbose:
            print "%s to be sent"%tobewritten
            
        # - let's do it.
        self.ser.write(tobewritten)
        print "%s done"%tobewritten
        # - forced pause.
        time.sleep(scan_lag)
        print "sleep 2"
        print "sleep over"
        
# ========================== #
#  3d Scanner Basic Class    #
# ========================== #
class ScannerSimulator( Scanner ):
    """
    Does everything like scanner, but do not send the information.
    """
    def _connect_serial_(self):
        """
        """
        self.ser = SerialFake()
        
    
    
class SerialFake(object):
    """
    """
    def __init__(self):
        """
        """
        print "FAKE SERIAL CLASS"

    def write(self,*arg,**kwargs):
        """
        """
        return
    
    def close(self):
        """
        """
        return



if __name__ == '__main__':

    parser=parsers("This is a Monochromator control sub-/main-program for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

    parser.add_argument( "GUI", "-gui", bool,
                         group="config",
                         default=False,
                         help='Set this flag to use a graphical user interface to configure and supervise the DAQ.')
    parser.add_argument( "Port", "-p", str,
                         group="basics",
                         default=None,
                         help='Sets the com port for the XYZ scanner.',
                         required=True)
    
    parser.add_argument( "Inited", "-i", bool,
                         group="basics",
                         default=False,
                         help='Makes the programm assume the scanner is already initialized. Therefore it does not go back to (0,0,0). This makes it impossible to use some of the safety features.')
    
    parser.add_argument( "XYZ_ScannerUnit", "-su", str,
                         group="XYZ_Scanner",
                         default="mm",
                         help='Defines the unit in which positions are supplied. (Only for manual use, not valid for instruction files.)')
    
    parser.add_argument( "XPos", "-xp", float,
                         group="XYZ_Scanner",
                         default=None,
                         help='Moves in absolute positions on the x-axis. Supply a unit of measure with -su, the default is "mm".')
    
    parser.add_argument( "YPos", "-yp", float,
                         group="XYZ_Scanner",
                         default=None,
                         help='Moves in absolute positions on the y-axis. Supply a unit of measure with -su, the default is "mm".')
    
    parser.add_argument( "ZPos", "-zp", float,
                         group="XYZ_Scanner",
                         default=None,
                         help='Moves in absolute positions on the z-axis. Supply a unit of measure with -su, the default is "mm".')
    parser.add_argument( "XPosR", "-xpr", float,
                         group="XYZ_Scanner",
                         default=None,
                         help='Moves in relative positions on the x-axis. Supply a unit of measure with -su, the default is "mm". Only usefull with -i. Runs after absolute positioning.')
    parser.add_argument( "YPosR", "-ypr", float,
                         group="XYZ_Scanner",
                         default=None,
                         help='Moves in relative positions on the y-axis. Supply a unit of measure with -su, the default is "mm". Only usefull with -i. Runs after absolute positioning.')
    parser.add_argument( "ZPosR", "-zpr", float,
                         group="XYZ_Scanner",
                         default=None,
                         help='Moves in relative positions on the z-axis. Supply a unit of measure with -su, the default is "mm". Only usefull with -i. Runs after absolute positioning.')

    arguments=parser.done()

    if arguments["GUI"]["val"]:
        print "TODO goto GUI"
        exit()

    sc=Scanner(self,port=arguments["Port"]["val"], do_refrun=False,smooth_move=False,debug=False)

    if not arguments["Inited"]["val"]:
        sc.do_step_wise_refrun()

    if arguments["XYZ_ScannerUnit"]["set"]:
        unit=arguments["XYZ_ScannerUnit"]["val"]
    else:  
        unit="mm"

    if arguments["XPos"]["set"] or arguments["YPos"]["set"] or arguments["ZPos"]["set"]:
        if arguments["XPos"]["set"]:
            x=arguments["XPos"]["val"]
        else:
            x=-1
        if arguments["YPos"]["set"]:
            y=arguments["YPos"]["val"]
        else:
            y=-1
        if arguments["ZPos"]["set"]:
            z=arguments["ZPos"]["val"]
        else:
            z=-1
        sc._real_move_to(x,y,z, unit=unit)

    if arguments["XPosR"]["set"] or arguments["YPosR"]["set"] or arguments["ZPosR"]["set"]:
        if arguments["XPosR"]["set"]:
            x=arguments["XPosR"]["val"]
        else:
            x=0
        if arguments["YPosR"]["set"]:
            y=arguments["YPos"]["val"]
        else:
            y=0
        if arguments["ZPosR"]["set"]:
            z=arguments["ZPoR"]["val"]
        else:
            z=0
        sc._real_shift_to(x,y,z, unit=unit)
