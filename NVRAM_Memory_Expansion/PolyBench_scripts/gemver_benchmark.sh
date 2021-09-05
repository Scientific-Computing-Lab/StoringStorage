#!/bin/bash

for i in 8000 16000 24000 32000 40000 48000 56000 64000 72000 80000 88000 96000 104000 112000 120000 128000 136000 144000 152000 160000 168000 176000 184000 192000 200000 208000 216000 224000 232000 240000 248000;
do

sed -i "28s/.*/#   define N $i/" linear-algebra/kernels/gemver/gemver.h
gcc -O3 -I utiities -I linear-algebra/kernels/gemver utilities/polybench.c linear-algebra/kernels/gemver/gemver.c -DPOLYBENCH_TIME -o gemver_time
#papi provides us floating point operation counting
gcc -O3 -I utiities -I linear-algebra/kernels/gemver utilities/polybench.c linear-algebra/kernels/gemver/gemver.c -DPOLYBENCH_PAPI -lpapi -o gemver_papi
#we execute PolyBench on one socket of our environment using the numactl tool to bind the computation to cpu and memory resources of socket 0
numactl --membind=0 --cpubind=0 ./gemver_time > gemver_$(echo $i)_time.txt
./gemver_papi > gemver_$(echo $i)_papi.txt

done
