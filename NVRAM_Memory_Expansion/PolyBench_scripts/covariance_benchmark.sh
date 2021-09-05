#!/bin/bash

for i in 4000 8000 16000 24000 32000 40000 48000 56000 64000 72000 80000 88000 96000 104000 112000 120000 128000 136000;
do
sed -i "30s/.*/#   define N $i/" datamining/covariance/covariance.h
sed -i "31s/.*/#   define M $i/" datamining/covariance/covariance.h
gcc -O3 -I utiities -I datamining/covariance -lm utilities/polybench.c datamining/covariance/covariance.c -DPOLYBENCH_TIME -o covariance_time
#papi provides us floating point operation counting
gcc -O3 -I utiities -I datamining/covariance -lm utilities/polybench.c datamining/covariance/covariance.c -DPOLYBENCH_PAPI -lpapi -o covariance_papi
#we execute PolyBench on one socket of our environment using the numactl tool to bind the computation to cpu and memory resources of socket 0
numactl --membind=0 --cpubind=0 ./covariance_time > covariance_$(echo $i)_time.txt
./covariance_papi > covariance_$(echo $i)_papi.txt

done
