#!/usr/bin/python2.7

import os, sys
from bin.parser_wrapper import parsers
from bin.lockIn import lockin
import os, sys
import numpy as np
import time



parser=parsers("This Program is meant as a DAQ for a hardware setup in the Astroparticle group of the Humbolt University of Berlin\nIt is written and maintained by Dustin Hebecker, Mickael Rigault and Daniel Kuesters. (2015)\nFeel free to modify and reuse for non commercial purposes as long as credit is given to the original authors.\n")

parser.add_argument( "PortReference", "-pr", str, group="LockIn", default=None, help='Used to define the Port for the reference LockIn')
parser.add_argument( "PortSignal", "-ps", str, group="LockIn", default=None, help='Used to define the Port for the signal LockIn')
parser.add_argument( "Autogain", "-ag", bool, group="LockIn", default=True, help='Defines if autogain will be used.')
parser.add_argument( "AverageValues", "-an", int, group="LockIn", default=10, help='Defines amount of measurements to average over.')
parser.add_argument( "ReadSignalLockIn", "-rsl", bool, group="LockIn", default=False, help='Will print the current value of the signal Lock-In to the comandline.')
parser.add_argument( "ReadReferenceLockIn", "-rrl", bool, group="LockIn", default=False, help='Will print the current value of the reference Lock-In to the comandline.')

arguments=parser.done(store_if_file_supplied=True)


if arguments["ReadSignalLockIn"]['val'] and not arguments["ReadReferenceLockIn"]['val']:
	signal=lockin( port, avrgn=10, autogain=arguments['Autogain']['val'], timeconstant=0.3)
	sdata=[signal.StandardData(N=arguments['AverageValues']['val'])] # returns return np.mean(ampl),np.std(ampl),np.mean(phase),np.std(phase),np.mean(freq),np.std(freq)
	print 'Amp_mean Amp_err Phase_mean Phase_err Freq_mean Freq_err'
	print sdata

if arguments["ReadReferenceLockIn"]['val'] and not arguments["ReadSignalLockIn"]['val']:
	reference=lockin( port, avrgn=10, autogain=arguments['Autogain']['val'], timeconstant=0.3)
	rdata=[reference.StandardData(N=arguments['AverageValues']['val'])] # returns return np.mean(ampl),np.std(ampl),np.mean(phase),np.std(phase),np.mean(freq),np.std(freq)
	print 'Amp_mean Amp_err Phase_mean Phase_err Freq_mean Freq_err'
	print rdata

if arguments["ReadReferenceLockIn"]['val'] and arguments["ReadSignalLockIn"]['val']:
	for i in range(arguments['AverageValues']['val']):
		sampl,sphase,sfreq = self.devices['sLockIn'].StandardData(N=1)
		ampls.append(sampl)
		phases.append(sphase)
		freqs.append(sfreq)

		rampl,rphase,rfreq = self.devices['rLockIn'].StandardData(N=1)
		amplr.append(rampl)
		phaser.append(rphase)
		freqr.append(rfreq)

	results={}

	results.update({'sLockIn':np.mean(ampls)})
	results.update({'sLockInErr':np.std(ampls)})
	results.update({'sLockInFreq':np.mean(phases)})
	results.update({'sLockInFreqErr':np.std(phases)})
	results.update({'sLockInPhase':np.mean(freqs)})
	results.update({'sLockInPhaseErr':np.std(freqs)})

	results.update({'rLockIn':np.mean(amplr)})
	results.update({'rLockInErr':np.std(amplr)})
	results.update({'rLockInFreq':np.mean(phaser)})
	results.update({'rLockInFreqErr':np.std(phaser)})
	results.update({'rLockInPhase':np.mean(freqr)})
	results.update({'rLockInPhaseErr':np.std(freqr)})

	return results

