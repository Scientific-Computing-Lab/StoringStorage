## Persistent Memory File Systems (PMFSs)
Local persistent file systems include ext4, xfs (for Linux-based systems), 
and NTFS (for Windows-based systems). They support a special mode called Direct Access (DAX) that enables memory mapping directly from the NVM to the application memory space. This bypasses the kernel, page cache, I/O subsystem, avoids interrupts and context switching, and allows the application to perform byte-addressable load/store memory operations.

Several other file systems have been developed with performance and other guarantees (e.g. consistency, atomicity, fault tolerance) in mind. 
These include [NOVA](https://www.usenix.org/system/files/conference/fast16/fast16-papers-xu.pdf) and [SplitFS](https://www.cs.utexas.edu/~vijay/papers/sosp19-splitfs.pdf), both providing POSIX compliant interfaces that support legacy scientific applications. NOVA and SplitFS offer novel approaches for designing a file system. 
NOVA is designed to maximize performance on hybrid memory (combining DRAM and NVM) systems while providing strong consistency guarantees. It is log-structured, and as such, it exploits the fast random access that NVMs provide, by storing the logs in the NVM and the indexes in the DRAM to allow fast search operations.
To improve concurrency, each inode has its own log. Finally, avoiding logging of file data yields a shorter log, accelerates the recovery process, and simplifies garbage collection. SplitFS presents a split of responsibilities between a user-space library file system and an existing kernel PMFS. 
The user-space library file system handles data operations via POSIX calls interception, memory-mapping the underlying files, and serving the read and overwrites using processors loads and stores. The PM file system (ext4-dax) handles metadata operations. 

**The SPlitFS file system software is available [here](https://github.com/utsaslab/SplitFS). Instructions how to install and mount SplitFS over NVM devices are included.**

In this section of the work we evaluate some PMFSs (ext4, SplitFS, Nova) using the BTIO benchmark, focusing on the MPI-IO method. We compare these results with conducting I/O operations to SATA-SSD device (throuth the xfs file system).

The reuslts of BTIO on our experimental system are given in *btio_pmfs_results.xlsx*.

## Running
- get the BTIO benchmark:
```
git clone git@github.com:wkliao/BTIO.git
cd  BTIO
```
- edit ```./Makefile``` and change the following 3 variables:
```
MPIF90        -- MPI Fortran compiler
FCFLAGS       -- compile flag
PNETCDF_DIR   -- path of PnetCDF library (1.4.0 and higher is required)
```
- run command ```make``` to build the executable, named *btio*, in the current folder.
- move the attached script file ```run_btio_benchmark.sh``` from this repo to the current dir (```BTIO```).
- edit ```RELEVANT_MOUNTED_POINT``` in ```run_btio_benchmark.sh``` to the relevant mounted directory path where you want to perform I/Os.
- run the attached script ```./run_btio_benchmark.sh```.

## Mount PMFSs to DCPMM Namespace
First, create an App Direct namespace, with the ```ndctl``` tool:
```
ndctl create-namespace --force --reconfig=namespace0.0 --mode=fsdax --map=mem
```
### ext4-dax
```
mkfs -t xfs /dev/pmem0
mount -o dax /dev/pmem0 RELEVANT_MOUNTED_POINT
```
### Nova
If Nova already exists in your given kernel, it is easy to use it in the following way:
```
insmod /usr/lib/modules/4.13.0/kernel/fs/nova/nova.ko
mount -t NOVA -o init /dev/pmem0 RELEVANT_MOUNTED_POINT
```

### SplitFS
Please refer [here](https://github.com/utsaslab/SplitFS) for detailed instructions how to install, mount and use SplitFS.
