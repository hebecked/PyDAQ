#!/usr/bin/python

import instruments as ik

inst = ik.generic_scpi.SCPIMultimeter.open_gpibusb('/dev/ttyUSB0', 1)
