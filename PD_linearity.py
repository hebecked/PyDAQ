import bin.picoampmeter as pam
import os, sys
from bin.rotational_stage.rotLib import rotStages
import time
import serial
import struct
import numpy as np
import bin.Data_IO as DIO
from bin.XYZ_Scanner.Scanner import Scanner



ports=DIO.serialports().get_ports(refresh=False)


use=[True,False,False]
init=[False,False,False]


ROT_devices=rotStages(port=ports['rotPlatform'], unit="deg", Channels=use, init=init) # later 'Auto'
sc=Scanner(port=ports["xyz-scanner"], do_refrun=False, smooth_move=False,debug=False, show=False)
PAM=pam.picoamp('/dev/ttyUSB3')

unit="mm"

x=0
y=159
z=334
	
f=open('PD_pos_meas.csv','w')

f.write('z-pos\ty-pos\tsig\tsigerr\tref\treferr\tdark\tdarkerr\tdarkref\tdarkreferr\n')

print time.gmtime()

for i in range(20):
	for j in range(20):
		string=str(i/2.) + '\t' + str(j/2.) + '\t' 
		sc.move_to(x,y+(j/2.),z-(i/2.), unit=unit ,go=True,smooth_move=False,show=False,sequenced=False,history_forward=False,clean_forward=True)
		sig=[]
		ref=[]
		ROT_devices.move( 0, -20, rel=False, wait=True)
		for k in range(10):
			ref.append(float(PAM.get_channel_1()))
			time.sleep(0.1)
			sig.append(float(PAM.get_channel_2()))
			time.sleep(0.1)
		string+=str(np.mean(sig)) + '\t' + str(np.std(sig)) + '\t' + str(np.mean(ref)) + '\t' + str(np.std(ref)) + '\t'
		sig=[]
		ref=[]
		ROT_devices.move( 0, 10, rel=False, wait=True)
		for k in range(10):
			ref.append(float(PAM.get_channel_1()))
			time.sleep(0.1)
			sig.append(float(PAM.get_channel_2()))
			time.sleep(0.1)
		string+=str(np.mean(sig)) + '\t' + str(np.std(sig)) + '\t' + str(np.mean(ref)) + '\t' + str(np.std(ref)) + '\n'
		f.write(string)

f.close()

print time.gmtime()
