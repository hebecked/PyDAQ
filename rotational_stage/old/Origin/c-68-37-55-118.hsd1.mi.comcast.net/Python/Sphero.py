#!/usr/bin/python

import sphero
import dbus



bus = dbus.SystemBus()

manager = dbus.Interface(bus.get_object('org.bluez', '/'), 'org.bluez.Manager')

adapterPath = manager.DefaultAdapter()

adapter = dbus.Interface(bus.get_object('org.bluez', adapterPath), 'org.bluez.Adapter')

for devicePath in adapter.ListDevices():
    device = dbus.Interface(bus.get_object('org.bluez', devicePath),'org.bluez.Device')
    deviceProperties = device.GetProperties()
    print deviceProperties["Address"]


import bluetooth

target_name = "My Phone"
target_address = None

nearby_devices = bluetooth.discover_devices()

for bdaddr in nearby_devices:
    if target_name == bluetooth.lookup_name( bdaddr ):
        target_address = bdaddr
        break

if target_address is not None:
    print "found target bluetooth device with address ", target_address
else:
    print "could not find target bluetooth device nearby"
