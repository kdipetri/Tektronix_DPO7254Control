#!/bin/bash
for filename in `ls log/*.log | sort -V`; do
  echo $filename
  cat $filename | grep SELECTED
  cat $filename | grep Filling
  cat $filename | grep SCAN
  printf "\n\n\n"
done
