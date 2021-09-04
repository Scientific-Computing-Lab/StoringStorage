#!/bin/bash

for i in 8000 16000 24000 32000 40000 48000 56000 64000 72000 80000 88000 96000 104000 112000 120000;
do
sed -i "30s/.*/#   define TSTEPS 30/" stencils/adi/adi.h
sed -i "31s/.*/#   define N $i/" stencils/adi/adi.h
gcc -O3 -I utiities -I stencils/adi utilities/polybench.c stencils/adi/adi.c -DPOLYBENCH_TIME -o adi_time
#papi provides us floating point operation counting
gcc -O3 -I utiities -I stencils/adi utilities/polybench.c stencils/adi/adi.c -DPOLYBENCH_PAPI -lpapi -o adi_papi
#we execute PolyBench on one socket of our environment using the numactl tool to bind the computation to cpu and memory resources of socket 0
numactl --membind=0 --cpubind=0 ./adi_time > adi_$(echo $i)_time.txt 
./adi_papi > adi_$(echo $i)_papi.txt 
done
