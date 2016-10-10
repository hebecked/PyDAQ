import bin.picoampmeter as pam
import os, sys
from bin.rotational_stage.rotLib import rotStages
import time
import serial
import struct
import numpy as np
import bin.Data_IO as DIO



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

f.write('z-pos\ty-pos\tsig\tsigerr\tref\treferr\tdark\tdarkerr\tdarkref\tdarkreferr')

for i in range(10):
	for j in range(10):
		string=str(i) + '\t' + str(j) + '\t' 
		sc.move_to(x,y+j,z-i, unit=unit ,go=True,smooth_move=False,show=False,sequenced=False,history_forward=False,clean_forward=True)
		sig=[]
		ref=[]
		ROT_devices.move( 0, 0, rel=False, wait=True)
		for k in range(10)
			ref.append(pam.get_channel_1())
			sig.append(pam.get_channel_2())
			time.sleep(0.1)
		string+=str(np.mean(sig)) + '\t' + str(np.std(sig)) + '\t' + str(np.mean(ref)) + '\t' + str(np.std(ref)) + '\t'
		sig=[]
		ref=[]
		ROT_devices.move( 0, -15, rel=False, wait=True)
		for k in range(10)
			ref.append(pam.get_channel_1())
			sig.append(pam.get_channel_2())
			time.sleep(0.1)
		string+=str(np.mean(sig)) + '\t' + str(np.std(sig)) + '\t' + str(np.mean(ref)) + '\t' + str(np.std(ref)) + '\t'
		f.write(string)

f.close()