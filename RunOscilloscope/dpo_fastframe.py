"""
VISA Control: FastFrame Acquisition
Tektronix TDS7704B Control
FNAL November 2018
CMS MTD ETL Test beam
"""

import numpy as np
import matplotlib.pyplot as plt
import sys
import optparse
import argparse
import signal
import os
import shutil
import datetime
import time              
from shutil import copy

stop_asap = False

import visa


def get_waveform_info():
    """Gather waveform transfer information from scope."""
    dpo.write('acquire:stopafter sequence')
    dpo.write('acquire:state on')
    dpo.query('*OPC?')
    binaryFormat = dpo.query('wfmoutpre:bn_fmt?').rstrip()
    print('Binary format: ', binaryFormat)
    numBytes = dpo.query('wfmoutpre:byt_nr?').rstrip()
    print('Number of Bytes: ', numBytes)
    byteOrder = dpo.query('wfmoutpre:byt_or?').rstrip()
    print('Byte order: ', byteOrder)
    encoding = dpo.query('data:encdg?').rstrip()
    print('Encoding: ', encoding)
    if 'RIB' in encoding or 'FAS' in encoding:
        dType = 'b'
        bigEndian = True
    elif encoding.startswith('RPB'):
        dType = 'B'
        bigEndian = True
    elif encoding.startswith('SRI'):
        dType = 'b'
        bigEndian = False
    elif encoding.startswith('SRP'):
        dType = 'B'
        bigEndian = False
    elif encoding.startswith('FP'):
        dType = 'f'
        bigEndian = True
    elif encoding.startswith('SFP'):
        dType = 'f'
        bigEndian = False
    elif encoding.startswith('ASCI'):
        raise visa.InvalidBinaryFormat('ASCII Formatting.')
    else:
        raise visa.InvalidBinaryFormat
    return dType, bigEndian

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        shutil.copytree(item, d, symlinks, ignore)
def copynew(source,destination):
    for files in source:
        shutil.copy(files,destination)

"""#################SEARCH/CONNECT#################"""
# establish communication with dpo
visa.log_to_screen
rm = visa.ResourceManager("@py")
dpo = rm.open_resource('TCPIP0::192.168.133.1::INSTR')
#dpo = rm.open_resource('TCPIP::192.168.133.1::INSTR')
dpo.timeout = 3000000
dpo.encoding = 'latin_1'
dpo.read_termination = '\n'
dpo.write_termination = '\n'
dpo.write('SYSTEM:REMOTE')
print(dpo)
print(dpo.query('*IDN?'))
# dpo.write('*rst')


parser = argparse.ArgumentParser(description='Run info.')
parser.add_argument('--numEvents',metavar='Events', type=str,default = 10, help='numEvents (default 10)',required=False)
parser.add_argument('--trigCh',metavar='trigCh', type=str, default=1,help='trigger Channel (default Ch1 (-0.01V))',required=False)
parser.add_argument('--trig',metavar='trig', type=float, default= -0.01, help='trigger value in V (default Ch1 (-0.01V))',required=False)
parser.add_argument('--horizontalWindow',metavar='horizontalWindow', type=str,default = 50, help='horizontal Window (default 50)',required=False)

args = parser.parse_args()


"""#################CONFIGURE INSTRUMENT#################"""
# variables for individual settings
#hScale = 10e-9  # horizontal scale in seconds, !!!!DO NOT CHANGE!!!! 
#numFrames = int(args.numFrames) # number of frames for each file
hScale = float(args.horizontalWindow)*1e-9 # horizontal scale in seconds
numEvents = int(args.numEvents) # number of events for each file
#samplingrate = float(args.sampleRate)*1e+9
#numPoints = samplingrate*hScale

#vertical scale
vScale_ch1 = 0.50 # in Volts for division
vScale_ch2 = 0.05 # in Volts for division
vScale_ch3 = 0.01 # in Volts for division
vScale_ch4 = 0.01 # in Volts for division

#vertical position
vPos_ch1 = 0  # in Divisions
vPos_ch2 = 0  # in Divisions
vPos_ch3 = 0  # in Divisions
vPos_ch4 = 0  # in Divisions

#trigger
#trigCh = (args.trigCh) # string with trigger channel number [CH1..CH4]
trigCh = str(args.trigCh)
if trigCh != "AUX": trigCh = 'ch'+trigCh
trigLevel = float(args.trig)

date = datetime.datetime.now()


#if numEvents < numFrames:
#    raise Exception("total number of frames < number of frames for each file")    
#    
#if numFrames > 2000:
#    ("WARNING: numFrames > 2000 --> the DUT might need more than one spill to fill a waveform file.\n")    


"""#################CONFIGURE RUN NUMBER#################"""
# increment the last runNumber by 1
with open('runNumber.txt') as file:
    runNumber = int(file.read())
print('######## Starting RUN {} ########\n'.format(runNumber))
print('---------------------\n')
print(date)
print('---------------------\n')


with open('runNumber.txt','w') as file:
    file.write(str(runNumber+1))


"""#################SET THE OUTPUT FOLDER#################"""
# Sets the ouptut folder on the scope
# The scope save runs locally at KarriWaveforms
# This directory is shared with my laptop at ScopeMount 
path = "C:/KarriWaveforms/scope_run{}".format(runNumber)
#path = "C:/KarriWaveforms/run_scope{}".format(runNumber)
dpo.write('filesystem:mkdir "{}"'.format(path))
log_path = "Logbook.txt"


#Write in the log file
logf = open(log_path,"a+")


logf.write("\n\n#### SCOPE LOGBOOK -- RUN NUMBER {} ####\n\n".format(runNumber))
logf.write("Date:\t{}\n".format(date))
logf.write("---------------------------------------------------------\n")
logf.write("Total number of  acquired: {} \n".format(numEvents))
logf.write("---------------------------------------------------------\n\n")



"""#################SCOPE HORIZONTAL SETUP#################"""
# dpo setup
dpo.write('acquire:state off')
dpo.write('horizontal:mode:scale {}'.format(hScale))
dpo.write('horizontal:fastframe:state on')
dpo.write('horizontal:fastframe:count {}'.format(numEvents))

print("# SCOPE HORIZONTAL SETUP #")
print('Horizontal scale set to {} for division\n'.format(hScale))

logf.write("HORIZONTAL SETUP\n")
logf.write('- Horizontal scale set to {} s for division\n\n'.format(hScale))


"""#################SCOPE CHANNELS BANDWIDTH#################"""
#'full' set the bandwidth to 2.5GHz(HW) IMPORTANT: the vertical scale has to be at least 10mV/division to use this feature!
dpo.write('ch1:bandwidth full')
dpo.write('ch2:bandwidth full')
dpo.write('ch3:bandwidth full')
dpo.write('ch4:bandwidth full')

"""#################SCOPE VERTICAL SETUP#################"""
#vScale expressed in Volts
dpo.write('ch1:scale {}'.format(vScale_ch1))
dpo.write('ch2:scale {}'.format(vScale_ch2))
dpo.write('ch3:scale {}'.format(vScale_ch3))
dpo.write('ch3:scale {}'.format(vScale_ch4))

dpo.write('ch1:position {}'.format(vPos_ch1))
dpo.write('ch2:position {}'.format(vPos_ch2))
dpo.write('ch3:position {}'.format(vPos_ch3))
dpo.write('ch4:position {}'.format(vPos_ch4))

print("# SCOPE VERTICAL SETUP #")
print('CH1: verical scale set to {} V for division'.format(vScale_ch1))
print('CH2: verical scale set to {} V for division'.format(vScale_ch2))
print('CH3: verical scale set to {} V for division'.format(vScale_ch3))
print('CH4: verical scale set to {} V for division'.format(vScale_ch4))

logf.write("VERTICAL SETUP\n")
logf.write('- CH1: verical scale set to {} V for division\n'.format(vScale_ch1))
logf.write('- CH2: verical scale set to {} V for division\n'.format(vScale_ch2))
logf.write('- CH3: verical scale set to {} V for division\n'.format(vScale_ch3))
logf.write('- CH4: verical scale set to {} V for division\n\n'.format(vScale_ch4))


"""#################TRIGGER SETUP#################"""
dpo.write('TRIGGER:A:TYPE EDGE;:TRIGGER:A:LEVEL %f;:TRIGGER:A:EDGE:SOURCE %s'%(trigLevel,trigCh))
dpo.write('TRIGGER:A:EDGE:SLOPE:%s FALL;:TRIGGER:A:MODE NORMAL'%(trigCh))
# dpo.write(':TRIGGER:A:EDGE:SOURCE LINE') #TO trigger on the line (60Hz)

trigprint='%.3f'%(trigLevel)

print("# TRIGGER SETUP #")
print('Trigger scale set to %s V\n'%(trigprint))

logf.write("TRIGGER SETUP\n")
logf.write('- Trigger Channel set to %s\n'%(trigCh))
logf.write('- Trigger scale set to %s V\n\n\n\n'%(trigprint))



"""#################TERMINATIONS SETUP#################"""
dpo.write(':CH1:TER 50;:CH2:TER 50;:CH3:TER 50;:CH4:TER 50');

print("# TERMINATIONS SETUP #")
print('All The Terminations set to 50 ohm.\n')

print('Horizontal, vertical, and trigger settings configured.\n')


"""#################DATA TRANSFERRING#################"""
# configure data transfer settings
dpo.write('header off')
dpo.write('horizontal:fastframe:sumframe none')
dpo.write('data:encdg fastest')
# dpo.write('data:source ch1')
#recordLength = 2000 
recordLength = int(dpo.query('horizontal:recordlength?').strip())
dpo.write('data:stop {}'.format(recordLength))
dpo.write('wfmoutpre:byt_n 1')
dpo.write('data:framestart 1')
dpo.write('data:framestop {}'.format(numEvents))
print('Data transfer settings configured.\n')





"""#################ACQUIRE DATA#################"""
i = 0
filename='{}/fastframe'.format(path)

#while (i<numEvents) and stop_asap==False:
#    i+=1

print('Acquiring waveform {}'.format(i))
dpo.write('acquire:stopafter sequence')
print('aquiring')
dpo.write('acquire:state on')
print('state on')

# dpo.query_ascii_values("trace:data?")
# dpo.query('*opc?')
print(dpo.query('*opc?'))
print('Waveform {} acquired'.format(i))

dpo.write('save:waveform:fileformat INTERNAL')
dpo.write('save:waveform ch1, "%s_%d_CH1.wfm"'%(filename,i))
dpo.write('save:waveform ch2, "%s_%d_CH2.wfm"'%(filename,i))
dpo.write('save:waveform ch3, "%s_%d_CH3.wfm"'%(filename,i))
dpo.write('save:waveform ch4, "%s_%d_CH4.wfm"'%(filename,i))
print(dpo.query('*opc?'))
print('Waveform {} saved.\n'.format(i))
#if (int(dpo.query(':ADER?')) == 1): 
#    print( "Acquisition complete")
#    break
#else:
#    print( "Still waiting") 

print('Waiting to be sure.\n')
time.sleep(0.1)

        
dpo.close()
    
# Check if saved on my computer      
# Be sure to mount the directory beforehand
# sudo mount_smbfs //192.168.133.1/KarriWaveforms ScopeMount/ 
# and enter laptop password
path_karri_laptop = "/Users/karridipetrillo/Documents/Fermilab/MTD/SiDetTesting/ScopeMount/scope_run{}".format(runNumber) #

# check  
i=0
while len(os.listdir(path_karri_laptop)) < 4: 
    i+=1
    print("waiting for files... loop {}\n".format(i))
    time.sleep(1)

#path_lxplus = ("/lxplus/Scope_standalone/RAW/run_scope%d"%(runNumber)) # lxplus folder mounted on otsdaq
#print('Start copying the file on lxplus....')   
#shutil.copytree(path_ftbf,path_lxplus)  
#print('Waveforms copied.\n')

print('Ending Run {}.\n'.format(runNumber))

print("\n\n\n ********  DID YOU UPDATE THE LOGBOOK AND SPREADSHEET?? ******** \n\n")
print("LogBook: https://docs.google.com/document/d/1PVd6DxdxLFYFbk_dmaxY3c2C5qMCfLAmNJD_r8xbN_4/edit#")
print('\n')
print("\nSpreadsheet: https://docs.google.com/spreadsheets/d/1w8Xzyr6kfaaHiJRtUg55FBBeXtrGfKv6OfC9XdTYLko/edit?ts=5be4d629#gid=0")
print('\n')

# Retrieve vertical and horizontal scaling information
# yOffset = float(dpo.query('wfmoutpre:yoff?'))
# yMult = float(dpo.query('wfmoutpre:ymult?'))
# yZero = float(dpo.query('wfmoutpre:yzero?'))
#
# numPoints = int(dpo.query('wfmoutpre:nr_pt?'))
# xIncr = float(dpo.query('wfmoutpre:xincr?'))
# xZero = float(dpo.query('wfmoutpre:xzero?'))
#
# dType, bigEndian = get_waveform_info()
# data = dpo.query_binary_values(
#     'curve?', datatype=dType, is_big_endian=bigEndian, container=np.array)
#


