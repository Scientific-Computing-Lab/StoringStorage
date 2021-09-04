#!/bin/bash

for i in 8000 16000 24000 32000 40000 48000 56000 64000 72000 80000 88000 96000 104000 112000 120000 128000 136000 144000 152000 160000;
do
sed -i "30s/.*/#   define NX $i/" linear-algebra/kernels/atax/atax.h
sed -i "31s/.*/#   define NY $i/" linear-algebra/kernels/atax/atax.h
gcc -O3 -I utiities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_TIME -o atax_time
#papi provides us floating point operation counting
gcc -O3 -I utiities -I linear-algebra/kernels/atax utilities/polybench.c linear-algebra/kernels/atax/atax.c -DPOLYBENCH_PAPI -lpapi -o atax_papi
#we execute PolyBench on one socket of our environment using the numactl tool to bind the computation to cpu and memory resources of socket 0
numactl --membind=0 --cpubind=0 ./atax_time > atax_$(echo $i)_time.txt
./atax_papi > atax_$(echo $i)_papi.txt

done
