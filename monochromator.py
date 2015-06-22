
import serial
import time

class CornerStone260:
    """This class controlls the Cornerstone 260 monochromator"""
    def __init__(self, port='COM4'):
        self.serialport = port  #windows: 'COMx', Linux: '/dev/<your_device_file>'
        self.baud = 9600
        self.sendtermchar = "\r\n"
        self.rectermchar = "\r\n"
        self.timeout = 10

    def SerialCommand(self,command):
        #setup - if a Serial object can't be created, a SerialException will be raised.
        while True:
            try:
                ser = serial.Serial(self.serialport, self.baud, timeout=self.timeout)
                #break out of while loop when connection is made
                break
            except serial.SerialException:
                print 'waiting for device ' + self.serialport + ' to be available'
                time.sleep(3)
        ser.flushInput()        
        ser.write(command + self.sendtermchar)
        answer = ser.readline()
        ser.close()
        return answer.upper()[:-2] == command.upper()
        
    def SerialQuery(self,command):
        #setup - if a Serial object can't be created, a SerialException will be raised.
        while True:
            try:
                ser = serial.Serial(self.serialport, self.baud)
                #break out of while loop when connection is made
                break
            except serial.SerialException:
                print 'waiting for device ' + self.serialport + ' to be available'
                time.sleep(3)
        ser.flushInput()        
        ser.write(command + self.sendtermchar)
        answer1 = ser.readline()
        answer2 = ser.readline()
        ser.close()
        return answer2[:-2]
        
    def Units_NM(self):
        """Specifies the operational units: nanometer"""
        return self.SerialCommand('UNITS NM')
        
    def Units_UM(self):
        """Specifies the operational units: micrometer"""
        return self.SerialCommand('UNITS UM')
    def Units_WN(self):
        """Specifies the operational units: wavenumbers (1/cm)"""
        return self.SerialCommand('UNITS WN')
    def GetUnits(self):
        """Returns the operational units: NM, UM, WN"""
        return self.SerialQuery('UNITS?')[0:2]
 
    def GoWave(self, position):
        """Moves the wavelength drive to the specified position (see units!)"""
        return self.SerialCommand('GOWAVE %f' % (position))
    def GetWave(self):
        """Returns the wavelength drive position (see units!)"""
        return self.SerialQuery('WAVE?') 
 
    def Calibrate(self, cal):
        """Define the current position as the wavelength specified in the numeric parameter"""
        return self.SerialCommand('CALIBRATE %f' % (cal))

    def Abort(self):
        """Stops any wavelength motion immediately"""
        return self.SerialCommand('ABORT')   

    def Step(self, n):
        """Moves the wavelength drive by the integer number of n"""
        return self.SerialCommand('STEP %d' % (n))
    def GetStep(self):
        """Returns the wavelength drive position in steps"""
        return self.SerialQuery('STEP?') 
        
    def Grat(self,n):
        """Selects the grating Nr. 'n' """
        return self.SerialCommand('GRAT %d' % (n))
    def GetGrat(self):
        """Returns the grating parameters"""
        return self.SerialQuery('GRAT?') 
        
    def GratLabel(self,n,label=' '):
        """Defines the label of the grating Nr. 'n' """
        return self.SerialCommand('GRAT%dLABEL %s' % (n, label[:8]))
    def GetLabel(self,n):
        """Returns the label of the grating"""
        return self.SerialQuery('GRAT%dLABEL?' % (n)) 

    def GratZero(self,n,zero):
        """Defines the zero of the grating Nr. 'n' """
        return self.SerialCommand('GRAT%dZERO %f' % (n, zero))
    def GetZero(self,n):
        """Returns the zero of the grating"""
        return self.SerialQuery('GRAT%dZERO?' % (n)) 	
        
    def GratLines(self,n,lines):
        """Defines the lines of the grating Nr. 'n' """
        return self.SerialCommand('GRAT%dLINES %d' % (n, lines))
    def GetLines(self,n):
        """Returns the label of the grating"""
        return self.SerialQuery('GRAT%dLINES?' % (n)) 

    def GratFactor(self,n,factor):
        """Sets the calibration factor of the grating Nr. 'n' """
        return self.SerialCommand('GRAT%dFACTOR %f' % (n, factor))
    def GetFactor(self,n):
        """Returns the calibration factor of the grating"""
        return self.SerialQuery('GRAT%dFACTOR?' % (n)) 

    def GratOffset(self,n,offset):
        """Sets the calibration offset of the grating Nr. 'n' """
        return self.SerialCommand('GRAT%dOFFSET %f' % (n, offset))
    def GetOffset(self,n):
        """Returns the calibration offset of the grating"""
        return self.SerialQuery('GRAT%dOFFSET?' % (n))     

    def ShutterOpen(self):
        """Opens the shutter"""
        return self.SerialCommand('SHUTTER O')
    def ShutterClose(self):
        """Closess the shutter"""
        return self.SerialCommand('SHUTTER C')  
    def GetShutter(self):
        """Returns the shutter state"""
        return self.SerialQuery('SHUTTER?')        

    def Filter(self,n):
        """Moves the filter wheel to the position specified in 'n' """
        return self.SerialCommand('FILTER %d' % (n))
    def GetFilter(self):
        """Returns the current filter position"""
        return self.SerialQuery('FILTER?')    

    def OutPort(self,n):
        """Selects the output port"""
        return self.SerialCommand('OUTPORT %d' % (n))
    def GetOutPort(self):
        """Returns the current out port"""
        return self.SerialQuery('OUTPORT?')             
    
    def FilterLabel(self,n,label):
        """Defines the label of the filter Nr. 'n' """
        return self.SerialCommand('FILTER%dLABEL %s' % (n, label[:8]))
    def GetFilterLabel(self,n):
        """Returns the label of the filter"""
        return self.SerialQuery('FILTER%dLABEL?' % (n))     

    def GetInfo(self):
        """Returns the system info"""
        return self.SerialQuery('INFO?')   
    def GetStatus(self):
        """Returns the status byte"""
        return self.SerialQuery('STB?')  
    def GetError(self):
        """Returns the error code"""
        return self.SerialQuery('ERROR?')         
    
    def GetSerialPort(self):
        return self.serialport
    def SetSerialPort(self, port):
        self.serialport = port

 
if __name__ == '__main__':
    cs = CornerStone260( port = 'COM4')
    print cs.GetInfo()
    