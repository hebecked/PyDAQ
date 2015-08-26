import pylibftdi as ftdi
import serial
ser= serial.Serial("/dev/ttyS0",115200)
ser.write("\x23\x02\x00\x00\x21\x01")
device.Device(ID?)

