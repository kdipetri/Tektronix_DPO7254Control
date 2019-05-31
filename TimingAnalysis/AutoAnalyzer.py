#!/cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-centos7-gcc62-opt/bin/python3
import csv
import sys
import subprocess
# import os


input_configFile = "Run_config.txt"

NewTracker = 0
if len(sys.argv)>2:
    NewTracker = int(sys.argv[2])

with open("April2019_geomCuts.csv") as csv_file:
    print("Opening file")
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row_i,content in enumerate(csv_reader):
        if (row_i == int(sys.argv[1])):
            configNumber = content[0]
            board = content[2]
            DUTchannel = content[3]
            sensor = content[4]
            xmin = content[5]
            xmax = content[6]
            ymin = content[7]
            ymax = content[8]
            DUT_threshold = 0 - float(content[9])*1e-3
            DUT_saturation = float(content[10])*1e-3
            MCPthreshold = 0 - float(content[11])*1e-3
            MCPsaturation = float(content[12])*1e-3
            CFD = content[15]
            filter = content[16]
            filter = "0"

            DUTName = f'{sensor}_{board}'
            # outputDir = sys.argv[3]
            # outputDir = f' /afs/cern.ch/user/t/toisidor/workspace/Tektronix_DPO7254Control/TimingAnalysis/AutoAnalysis/Results/config{configNumber}/'
            # try:
            #     os.stat(outputDir[:-1])
            # except:
            #     os.mkdir(outputDir[:-1])
            outputDir = "/eos/user/n/nminafra/www/FNAL_output/FNAL_2019/"

            s = f'./analyzeDataVsMCP -i {input_configFile} -f {DUTchannel} -k {configNumber} -t {DUT_threshold} -s {DUT_saturation} -c {CFD} --MCPthreshold {MCPthreshold} --lowpass {filter} -n {DUTName} -y {NewTracker} --xmin {xmin} --xmax {xmax} --ymin {ymin} --ymax {ymax} --MCPsaturation {MCPsaturation} --outputdir {outputDir}'
            print(s)
            subprocess.run(s,shell=True)
