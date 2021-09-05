# BT Checkpoint Restart

In this directory you can find two variations of the NAS Parallel Benchmarks (NPB v3.4.2), modified to benchmark two methods of conducting Checkpoint Restart (C/R). The benchmarks can run on NVRAM, but also on top of other storage devices.

The benchmarks demonstate the differences between transperent C/R and explicit C/R.

## Explicit Checkpoint Restart

In explicit C/R, in order to successfully checkpoint and restart a program from a valid state, the program has to store (and restore from) the whole required computational state. Since it is done explicitly, it is the responsibility ofthe programmer to understand what information is necessaryand sufficient for correct recovery.

The implementation of the BT benchmark is done using the Scalable Checkpoint Restart (SCR) library, and is located under the `NPB3.4-MPI-SCR/` directory.

## Transparent Checkpoint Restart

In transparent C/R the state of the program is savedwithout any knowledge of the application or interventionfrom the programmer.
The implementation of the BT benchmark is done using the Distributed Multi-Threaded CheckPointing (DMTCP) library, and is located under the `NPB3.4-MPI-DMTCP/` directory.

**The results on our experimental system are given in *checkpoint_restart_results.xlsx*.**

