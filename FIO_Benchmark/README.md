## FIO - Flexible I/O tester
The FIO tester is a versatile storage benchmark tool that is used both for benchmarking and stress/hardware verification.
In this work we use the FIO tester to evaluate the performances of Intel Optane™ DCPMM, using various file systems. \
We compare the resulting performances of Intel Optane™ DCPMM with the performances of SATA-SSD. \
Note that the FIO tester does not exhebit sceintific computing patterns, but rather is used as a simple benchmarking tool to evaluate simple I/O patterns.
- Read more about the FIO tester [here](https://fio.readthedocs.io/en/latest/fio_doc.html).
- Get FIO for your machine (e.g. using yum for RPM-based distributions):
```
yum install fio
```
- Seq-Read Benchmark:
```
fio --name=seq-reader --rw=read --size=512MB --bs=8KB --runtime=30 --ioengine=sync --thread --filename=RELEVANT_MOUNTED_POINT --direct=1 --numjobs=8
```
- Rand-Read Benchmark:
```
fio --name=rand-reader --rw=randread --size=512MB --bs=8KB --runtime=30 --ioengine=sync --thread --filename=RELEVANT_MOUNTED_POINT --direct=1 --numjobs=8
```
- Seq-Write Benchmark:
```
fio --name=seq-writer --rw=write --size=512MB --bs=8KB --runtime=30 --ioengine=sync --thread --filename=RELEVANT_MOUNTED_POINT --direct=1 fsync=1 --numjobs=8
```
- Rand-Write Benchmark:
```
fio --name=rand-writer --rw=randwrite --size=512MB --bs=8KB --runtime=30 --ioengine=sync --thread --filename=RELEVANT_MOUNTED_POINT --direct=1 fsync=1 --numjobs=8
```
tune the 'numjobs' parameter to test the performances of your device in changing number of threads, conducting I/Os in parallel. 

refer to [here](https://github.com/Scientific-Computing-Lab-NRCN/StoringStorage/blob/main/NVRAM_Persistent_Memory_FSs/README.md#L34) to see how to mount different PMFSs on the DCPMM device.

The reuslts of FIO on our experimental system are given in *fio_benchmark_results.xlsx*.
