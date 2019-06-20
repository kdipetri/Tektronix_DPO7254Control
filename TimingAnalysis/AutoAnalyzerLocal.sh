#!/bin/bash
export X509_USER_PROXY=$PWD/x509_proxy
voms-proxy-init --voms cms --noregen
echo $(voms-proxy-info)
for i in {0..32}
do
  $(./commandPrint.py $i 32) 2>&1 > log/log_$i.log &
done
