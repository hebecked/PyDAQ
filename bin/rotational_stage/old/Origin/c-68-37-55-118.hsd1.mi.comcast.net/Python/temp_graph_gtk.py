#!/usr/bin/python

import matplotlib.pyplot as plt
from gi.repository import Gtk
from subprocess import check_output
from time import sleep
from matplotlib.backends.backend_gtk import FigureCanvasGTK as FigureCanvas



def get_system_temp():
		temp_str = check_output('acpi -t -f', shell=True)
		temp = float(temp_str[15:19])
		
		return temp



#plt.ion()
#class DynamicUpdate():
	##Suppose we know the x range
	#min_y = 0
	#max_y = 200

	#def on_launch(self):
		##Set up plot
		#self.figure, self.ax = plt.subplots()
		#self.lines, = self.ax.plot([],[], lw=2)
		##Autoscale on x-axis, and limits on y-axis
		#self.ax.set_ylim(self.min_y, self.max_y)
		#self.ax.set_autoscalex_on(True)
		##Other stuff
		#self.ax.grid()
		#plt.ylabel('Temperature (F)')
		#plt.xlabel('Time (S)')
		

	#def on_running(self, xdata, ydata):
		##Update data (with the new _and_ the old points)
		#self.lines.set_xdata(xdata)
		#self.lines.set_ydata(ydata)
		##Need both of these in order to rescale
		#self.ax.relim()
		#self.ax.autoscale_view()
		##We need to draw *and* flush
		#self.figure.canvas.draw()
		#self.figure.canvas.flush_events()

	##Calls class to update data for each iteration of the loop
	#def __call__(self):
		#self.on_launch()
		
		#xdata = []
		#ydata = []
		
		#time = 0
		#while True:
			#time_incr = 0.3
			
			#xdata.append(time)
			#ydata.append(get_system_temp())
			
			#time += time_incr
			#self.on_running(xdata, ydata)
			#sleep(time_incr)
		
		
		#return xdata, ydata

#d = DynamicUpdate()
#d()

#canvas = FigureCanvas(d)

class TempIndicator(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title='System Temperature Graph')
        
        self.set_default_size(400, 300)
        




win = TempIndicator()
win.connect('delete-event', Gtk.main_quit)
#win.add(canvas)
win.show_all()
Gtk.main()
