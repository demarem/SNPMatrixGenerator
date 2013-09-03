SNPMatrixGenerator
==================

Combine nexus columns with two or more nucleotides into a single nexus matrix.

For additional help:
	./run -h
To run:
	./run inputFile outputFile [either 'all' or 'sample']

all vs. sample options:
	all option includes every column with two or more nucleotides.
	sample chooses one 'random' column from all of the columns in each
	matrix.

Note:
	this library depends on python-nexus library, install with
	&> sudo pip install python-nexus
	
	If you don't have pip install, first call
	&> sudo easy_install pip
