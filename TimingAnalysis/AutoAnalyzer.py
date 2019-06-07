#!/cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-centos7-gcc62-opt/bin/python3
import csv
import sys
import subprocess
# import os


# To send jobs:
# $>source /cvmfs/sft.cern.ch/lcg/views/LCG_94python3/x86_64-centos7-gcc62-opt/setup.sh
# $> voms-proxy-init --valid 12:00 -voms cms --out x509_proxy
# $> condor_submit condor_submit.jdl



input_configFile = "Run_config.txt"

NewTracker = 0
if len(sys.argv)>2:
    print(f'Arguments: {sys.argv[1]}        {sys.argv[2]}')
    period = int(sys.argv[2])/2
    id = int(sys.argv[1])
    if id >= period:
        id -= period
        NewTracker = 1
    print(f'Using: id {id} with NewTracker {NewTracker}')

with open("April2019_geomCuts.csv") as csv_file:
    print("Opening file")
    csv_reader = csv.reader(csv_file, delimiter=',')
    row_counter = 0;
    for content in csv_reader:
        try:
            float(content[12])
            row_counter += 1
        except:
            continue
        if (row_counter-1 == int(sys.argv[1])):
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
            # filter = content[16]
            filter = "0"

            DUTName = f'{sensor}_{board}'
            outputDir = "/eos/user/n/nminafra/www/FNAL_output/FNAL_2019/"

            s = f'./analyzeDataVsMCP --outputdir {outputDir} -i {input_configFile} -f {DUTchannel} -k {configNumber} -t {DUT_threshold} -s {DUT_saturation} -c {CFD} --MCPthreshold {MCPthreshold} --lowpass {filter} -n {DUTName} -y {NewTracker} --xmin {xmin} --xmax {xmax} --ymin {ymin} --ymax {ymax} --MCPsaturation {MCPsaturation}'
            print(s)
            subprocess.call('export X509_USER_PROXY=$PWD/x509_proxy',shell=True)
            subprocess.call('voms-proxy-init --voms cms --noregen',shell=True)
            subprocess.call('voms-proxy-info',shell=True)
            subprocess.call(s,shell=True)
            print("Done!")
            # with open(f'{outputDir}test_{int(sys.argv[1])}_{int(sys.argv[2])}.log','w') as f:
            #     f.write("This is a test!")
