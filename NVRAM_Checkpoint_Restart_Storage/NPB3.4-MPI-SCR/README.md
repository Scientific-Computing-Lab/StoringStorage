# BT Checkpoint Restart (SCR)

In this directory you can find a variation of the BT benchmark taken from NAS Parallel Benchmarks (NPB v3.4.2), modified to perform internall checkpoint directly from the benchmark.
The internal Checkpoint/Restart is done using the Scalable Checkpoint / Restart (SCR). The Scalable Checkpoint / Restart (SCR) library enables MPI applications to utilize distributed storage on Linux clusters to attain high file I/O bandwidth for checkpointing, restarting, and writing large datasets.

## Prerequisites

The following modules were used to compile the benchmark:

* scr/v2.0.0
* gnu/9.1.0
* openmpi/4.0.4

## How to compile?

The benchmark uses a similar directory tree as the original NPB v3.4.2's directory tree. To compile NPB's BT benchmark, one needs to check the configuration file 'make.def' in the config directory and modify the config if necessary. If one doesn't exists, copy 'make.def.template'.
Specifically, for compiling and linking the benchmark with SCR, one must verify if the following flags require specification:

```config
  - FSCR_INC - SCR installation include directory.
  - FSCR_LIB - SCR lib directory.
```

Then run the following command:

```bash
  make <benchmark-name> CLASS=<class> [SUBTYPE=<type>] [VERSION=VEC]
```

   where `<benchmark-name>`  is "bt" and `<class>` is "S", "W", "A", "B", "C", "D", "E", or "F".

For additional information about the compilation process, please see [NAS NPB v3.4.2 compilation guide](https://www.nas.nasa.gov/software/npb.html).

> **_NOTE:_** : SCR Implementation does not support any *BT-IO* variation. Upon recovery, the benchmark behavior is undefined.

## Execution

The executable is named `<benchmark-name>.<class>.x` and is placed in the bin sub-directory (or in the specified BINDIR directory). The method for running the MPI program depends on your local system. As an example of running the BT benchmark Class C, the command might be:

```bash
  mpirun -np 16 bin/bt.C.x
```

## Configuring SCR

SCR supports customization and configuration which can lead to a significant performance improvement or to additional functionality which is disabled by default.

To configure SCR with NPB's BT benchmark, one needs to add or modify the configuration file '.scrconf' in the prefix directory and modify the config if necessary (note the leading dot). SCR looks for a the config file named in the prefix directory. Alternatively, one may specify the name and location of the user configuration file by setting the `SCR_CONF_FILE` environment variable at run time, e.g.,:

```bash
export SCR_CONF_FILE=config/scr.conf
```

To change the benchmark's checkpoint persist directory, besides setting the target directory in the configuration file, one must also set the environment variable `SCR_CHECKPOINT_DIR`:

```bash
export SCR_CHECKPOINT_DIR=/path/to/directory
```

To ease configuration, an SCR config template is located under 'config/scr.conf.template'. For additional info about SCR configuration, check [SCR documentation](https://scr.readthedocs.io/en/latest/users/config.html).  

### Execution Utility

To ease the benchmark execution, one can use the python utility script located under the `utils` directory. The utility enables to run the benchmark with/without crash and with/without recover.

To run the script execute the following command:

```bash
python3 utils/benchmark.py \
   --nvram-mount-directory /tmp/pmem_emul/bt \
   --benchmark-class <benchmark class> \ 
   --procs <number of processes> \  
   --crash \
   --crash-iteration <crash iteration number in multiples of 20> \
   --recover
```

The utility supports the following options:

```bash
$ python3 utils/benchmark.py --help
usage: benchmark.py [-h] -n NVRAM_MOUNT_DIRECTORY
                    [--scr_cache_dir SCR_CACHE_DIR] -c BENCHMARK_CLASS
                    [-p PROCS] [--crash] [--no-crash] [-i CRASH_ITERATION]
                    [--recover] [--no-recover]

optional arguments:
  -h, --help            show this help message and exit
  -n NVRAM_MOUNT_DIRECTORY, --nvram_mount_directory NVRAM_MOUNT_DIRECTORY
                        The mount directory of nvram.
  --scr_cache_dir SCR_CACHE_DIR
                        The cache directory of SCR.
  -c BENCHMARK_CLASS, --benchmark_class BENCHMARK_CLASS
                        The benchmark class
  -p PROCS, --procs PROCS
                        The number of processes to run the benchmark with.
  --crash               If set, the benchmark would perform a crash at the
                        specified iteration.
  --no-crash            If set, the benchmark would not perform a crash.
  -i CRASH_ITERATION, --crash-iteration CRASH_ITERATION
                        The iteration to crash/restart the benchmark.
  --recover             If true, the benchmark would perform a recovery after
                        a crash.
  --no-recover          If true, the benchmark would not perform a recovery
                        after a crash.
```

> **_NOTE:_**  After the utility execution the checkpoints are deleted from the persistent memory.
