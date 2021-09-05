#!/bin/bash

for i in 8000 16000 24000 32000 40000 48000 56000 64000 72000 80000 88000 96000 104000 112000 120000 128000 136000 144000;
do
sed -i "32s/.*/#   define TMAX 30/" stencils/fdtd-2d/fdtd-2d.h
sed -i "33s/.*/#   define NX $i/" stencils/fdtd-2d/fdtd-2d.h
sed -i "34s/.*/#   define NY $i/" stencils/fdtd-2d/fdtd-2d.h
gcc -O3 -I utiities -I stencils/fdtd-2d utilities/polybench.c stencils/fdtd-2d/fdtd-2d.c -DPOLYBENCH_TIME -o fdtd-2d_time
#papi provides us floating point operation counting
gcc -O3 -I utiities -I stencils/fdtd-2d utilities/polybench.c stencils/fdtd-2d/fdtd-2d.c -DPOLYBENCH_PAPI -lpapi -o fdtd-2d_papi
#we execute PolyBench on one socket of our environment using the numactl tool to bind the computation to cpu and memory resources of socket 0
numactl --membind=0 --cpubind=0 ./fdtd-2d_time > fdtd-2d_$(echo $i)_time.txt
./fdtd-2d_papi > fdtd-2d_$(echo $i)_papi.txt 
done
