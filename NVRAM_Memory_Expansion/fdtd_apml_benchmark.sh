#!/bin/bash

for i in 500 700 900 1100 1300 1500 1700 1900 2100 2300 2500;
do

sed -i "32s/.*/#   define CZ $i/" stencils/fdtd-apml/fdtd-apml.h
sed -i "33s/.*/#   define CYM $i/" stencils/fdtd-apml/fdtd-apml.h
sed -i "34s/.*/#   define CXM $i/" stencils/fdtd-apml/fdtd-apml.h
gcc -O3 -I utiities -I stencils/fdtd-apml utilities/polybench.c stencils/fdtd-apml/fdtd-apml.c -DPOLYBENCH_TIME -o fdtd-apml_time
#papi provides us floating point operation counting
gcc -O3 -I utiities -I stencils/jacobi-apml utilities/polybench.c stencils/jacobi-apml/jacobi-apml.c -DPOLYBENCH_PAPI -lpapi -o jacobi-apml_papi
#we execute PolyBench on one socket of our environment using the numactl tool to bind the computation to cpu and memory resources of socket 0
numactl --membind=0 --cpubind=0 ./fdtd-apml_time > fdtd_apml_$(echo $i)_time.txt

./fdtd-apml_papi > fdtd_apml_$(echo $i)_papi.txt

done
