SHELL=/bin/sh
CLASS=U
SUBTYPE=
VERSION=
SFILE=config/suite.def

default: header
	@ sys/print_instructions

BT: bt
bt: header
	cd BT; $(MAKE) CLASS=$(CLASS) SUBTYPE=$(SUBTYPE) VERSION=$(VERSION)


# Awk script courtesy cmg@cray.com, modified by Haoqiang Jin
suite:
	@ awk -f sys/suite.awk SMAKE=$(MAKE) $(SFILE) | $(SHELL)


# It would be nice to make clean in each subdirectory (the targets
# are defined) but on a really clean system this will won't work
# because those makefiles need config/make.def
clean:
	- rm -f core *~ */core */*~
	- rm -f */*.o */*.so */*.mod */*.obj */*.exe */npbparams.h
	- rm -f MPI_dummy/test MPI_dummy/libmpi.a
	- rm -f sys/setparams sys/makesuite sys/setparams.h
	- rm -f btio.*.out*

veryclean: clean
	- rm -f config/make.def config/suite.def 
	- rm -f bin/bt.*

header:
	@ sys/print_header

