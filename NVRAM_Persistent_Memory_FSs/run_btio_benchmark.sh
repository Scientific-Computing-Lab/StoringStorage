#!/bin/bash

#MPI collective 0

for i in 32 64 128 256 512 1024;
do
	rm -rf RELEVANT_MOUNTED_POINT/btio.mpi
	sync; echo 1 > /proc/sys/vm/drop_caches
	sed -i "1s/.*/w                 # IO mode:    w for write, r for read/" inputbt.data
        sed -i "2s/.*/0                 # IO method:  0 for MPI collective IO, 1 for MPI_independent IO, 2 for PnetCDF blocking IO, 3 for PnetCDF nonblocking IO/" inputbt.data
	sed -i "3s/.*/1                  # number of time steps/" inputbt.data
	sed -i "4s/.*/$i $i $i           # grid_points(1), grid_points(2), grid_points(3)/" inputbt.data
	mpiexec -n 4 ./btio inputbt.data >> result_$i-write_mpi_collective.txt 
        echo "done write " $i

	sync; echo 1 > /proc/sys/vm/drop_caches
	sed -i "1s/.*/r                 # IO mode:    w for write, r for read/" inputbt.data
	mpiexec -n 4 ./btio inputbt.data >> result_$i-read_mpi_collective.txt 
	echo "done read " $i
done

#MPI independent 1

for i in 32 64 128 256 512 1024;
do
	rm -rf RELEVANT_MOUNTED_POINT/btio.mpi
	sync; echo 1 > /proc/sys/vm/drop_caches
	sed -i "1s/.*/w                 # IO mode:    w for write, r for read/" inputbt.data
        sed -i "2s/.*/1                 # IO method:  0 for MPI collective IO, 1 for MPI_independent IO, 2 for PnetCDF blocking IO, 3 for PnetCDF nonblocking IO/" inputbt.data
	sed -i "3s/.*/1                  # number of time steps/" inputbt.data
	sed -i "4s/.*/$i $i $i           # grid_points(1), grid_points(2), grid_points(3)/" inputbt.data
	mpiexec -n 4 ./btio inputbt.data >> result_$i-write_mpi_independent.txt 
        echo "done write " $i

	sync; echo 1 > /proc/sys/vm/drop_caches
	sed -i "1s/.*/r                 # IO mode:    w for write, r for read/" inputbt.data
	mpiexec -n 4 ./btio inputbt.data >> result_$i-read_mpi_independent.txt 
	echo "done read " $i
done
