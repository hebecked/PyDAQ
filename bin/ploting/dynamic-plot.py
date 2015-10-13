#!/usr/bin/python2.7



import matplotlib.pyplot as plt
import numpy as np

class live_plots:
	"""A small class for continuusly updating plots"""


	def __init__(self,x_min,x_max,x_label="Time",y_label="Temperature [C]",y2_label="Humidity [%]",color1='r',color2='b',two_plots=False):#variable x and or y autoscale (maybe a default and then additional function?)
		self.color1=color1
		self.color2=color2
		self.x_max=x_max
		self.x=np.array([])
		self.y=np.array([])
		self.y2=np.array([])
		self.twoplots=two_plots
		plt.ion()
		self.figure , self.ax1 = plt.subplots()
		self.lines1, = self.ax1.plot([],[],color1)
		self.ax1.set_xlabel(x_label)
		self.ax1.set_ylabel(y_label)
		self.ax1.set_autoscaley_on(True)
		self.ax1.set_xlim(x_min,x_max)
		self.ax1.grid()
		if(two_plots):
			self.ax1.set_ylabel(y_label, color=color1)
			self.ax1.tick_params(axis='y',colors=color1)
			self.ax2 = self.ax1.twinx()
			self.lines2, = self.ax2.plot([],[],color2)
			self.ax2.set_ylabel(y2_label, color=color2)
			self.ax2.tick_params(axis='y',colors=color2)
			self.ax2.set_xlim(x_min,x_max)


	def update(self,x,y1,y2,append=True):
		if append:
			self.x=np.append(self.x,x)
			self.y=np.append(self.y,y1)
			if(twoplots):
				self.y2=np.append(self.y2,y2)
		else:
			self.x=x
			self.y=y
		self.lines1.set_xdata(self.x)
		self.lines1.set_ydata(self.y)
		self.ax1.relim()
		self.ax1.autoscale_view()
		if(self.twoplots):		
			self.lines2.set_xdata(self.x)
			self.lines2.set_ydata(self.y2)
			self.ax2.relim()
			self.ax2.autoscale_view()
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()



	def update_time(self,x,y1,y2):
		self.x+=x
		self.x=np.append(self.x,0)
		self.y=np.append(self.y,y1)
		if(self.twoplots):
			self.y2=np.append(self.y2,y2)
		self.lines1.set_xdata(self.x)
		self.lines1.set_ydata(self.y)
		self.ax1.relim()
		self.ax1.autoscale_view()
		if(self.twoplots):		
			self.lines2.set_xdata(self.x)
			self.lines2.set_ydata(self.y2)
			self.ax2.relim()
			self.ax2.autoscale_view()
		self.figure.canvas.draw()
		self.figure.canvas.flush_events()



	def clean_arrays(self):
		rem=0
		for i in range(len(self.x)):
			if(self.x[i-rem]>self.x_max):
				self.x=np.delete(self.x,i-rem)
				self.y=np.delete(self.y,i-rem)
				if self.twoplots:
					self.y2=np.delete(self.y2,i-rem)
				rem+=1



	#write function for changes of parameters like lable axis etc.

	#how to include in QT windows