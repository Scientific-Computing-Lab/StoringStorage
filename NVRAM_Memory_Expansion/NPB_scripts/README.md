## Compiling NPB and Running the Attached Scripts
- enter the source directory of NBP suite you have download, and enter the MPI verison of the suite.
- move ```suite.def``` file attached in this repo to the ```config``` directory of the suite (```config/suite.def```).
- run ```make suite``` to compile the specified benchmarks in the ```suite.def``` file.
- then you are able to run the attached scripts.

**NOTE**: \
In order to run with Memory Mode of DCPMM, you need to configure the server before booting, using the ```ipmctl``` tool ([see here](https://docs.pmem.io/ipmctl-user-guide/provisioning/create-memory-allocation-goal)). 

