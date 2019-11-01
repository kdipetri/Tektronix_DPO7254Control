#!/usr/bin/env python
import os, glob, sys

import argparse
p = argparse.ArgumentParser()
p.add_argument('-r','--run',default='')
args = p.parse_args()

scope_dir='/Users/karridipetrillo/Documents/Fermilab/MTD/SiDetTesting'
done_runs = glob.glob(scope_dir+'/ROOT/*.root')
new_runs = glob.glob(scope_dir+'/RAW/*'+str(args.run)+'/')

for ifile in new_runs:
    root_file = scope_dir+'/ROOT/'+ifile.split("/")[-1]+".root"
    if not os.path.exists(root_file):
        print 'Processing', ifile
        cmd = 'python conversion.py '+ ifile
        os.system(cmd)
