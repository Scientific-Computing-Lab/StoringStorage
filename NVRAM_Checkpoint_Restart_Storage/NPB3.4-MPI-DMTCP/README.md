# BT Checkpoint Restart (DMTCP)

In this directory you can find a variation of the BT benchmark taken from NAS Parallel Benchmarks (NPB v3.4.2), modified to trigger external checkpoint directly from the benchmark.
The external checkpoint restart is done using the Distributed MultiThreaded Checkpointing library (DMTCP) which transparently checkpoints a single-host or distributed computation in user-space -- with no modifications to user code or to the O/S.

## Prerequisites

The following modules were used to compile the benchmark:

* dmtcp/v2.6
* gnu/9.1.0
* mpich/3.2.1

## How to compile?

The benchmark uses a similar directory tree as the original NPB v3.4.2's directory tree. To compile NPB's BT benchmark, one needs to check the configuration file 'make.def' in the config directory and modify the config if necessary. If one doesn't exists, copy 'make.def.template'.
Specifically, for compiling and linking the benchmark with DMTCP, one must verify if the following flags require specification:

```config
  - DMTCP_INC - DMTCP installation include directory.
  - DMCTP_LIB - DMTCP lib directory.
```

Then run the following command:

```bash
       make <benchmark-name> CLASS=<class> [SUBTYPE=<type>] [VERSION=VEC]
```

   where `<benchmark-name>`  is "bt" and `<class>` is "S", "W", "A", "B", "C", "D", "E", or "F".

For additional information about the compilation process, please see NPB v3.4.2 compilation guide.

## Execution

DMTCP uses an external coordinator program in order to synchronize and control the checkpoint restart process. Therefore, for running the benchmark we'll have to run two commands in parallel:

1. Run DMTCP coordinator program.
1. Run the NPB Benchmark.

### DMTCP Coordinator Execution

To run DMTCP coordinator, we'll have to specify the following:

* The port in which the coordinator will listen to requests.
* The directory to store the checkpoints.
* The temp directory to store the DMTCP temporary files.

This can be achieved by the following command:

```bash
dmtcp_coordinator \
    --exit-on-last \
    --coord-port <port> \
    --ckptdir <path/to/checkpoint/directory> \
    --tmpdir <path/to/tmp/directory>
```

### DMTCP NPB Benchmark Execution

Once DMTCP coordinator is running, we can execute the benchmark by specify the following:

* DMTCP's coordinator listening port.
* The directory to store the checkpoints.
* The temp directory to store the DMTCP temporary files.
* Number of process to run the NPB benchmark with.
* The path to the compiled benchmark.

For convenience, please see the DMTCP execution below.

```bash
dmtcp_launch \
   --allow-file-overwrite \
   --no-gzip \
   --join-coordinator \
   --coord-port <port> \
   --tmpdir <path/to/checkpoint/directory> \
   --ckptdir <path/to/tmp/directory> mpirun -np <num-of-processes> <path/to/benchmark/executable>
```

### Stopping DMTCP Execution

To stop or kill the DMTCP run the following command:

```bash
dmtcp_command -kill --port <coordinator-port>
```

### Execution Utility

To ease the benchmark execution, one can use the python utility script located under the `utils` directory. The utility enables to run the benchmark with/without crash and with/without recover.

To run the script execute the following command:

```bash
python3 utils/benchmark.py \
   --nvram-mount-directory /tmp/pmem_emul/bt \
   --benchmark-class <benchmark class> \ 
   --coord_port 12345 \
   --procs <number of processes> \  
   --crash \
   --crash-iteration <crash iteration number in multiples of 20> \
   --recover
```

The utility supports the following options:

```bash
$ python3 utils/benchmark.py --help
usage: benchmark.py [-h] -n NVRAM_MOUNT_DIRECTORY -c BENCHMARK_CLASS
                    [-p PROCS] [-o COORD_PORT] [--crash] [--no-crash]
                    [-i CRASH_ITERATION] [--recover] [--no-recover]

optional arguments:
  -h, --help            show this help message and exit
  -n NVRAM_MOUNT_DIRECTORY, --nvram-mount-directory NVRAM_MOUNT_DIRECTORY
                        The mount directory of nvram.
  -c BENCHMARK_CLASS, --benchmark-class BENCHMARK_CLASS
                        The benchmark class.
  -p PROCS, --procs PROCS
                        The number of processes to run the benchmark with.
  -o COORD_PORT, --coord_port COORD_PORT
                        The checkpoint interval to run the benchmark with.
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
