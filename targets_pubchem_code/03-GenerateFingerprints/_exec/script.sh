#!/bin/bash

### HEADER
# This script is for multiplying and adjusting a template jupyter notebook so that a cluster of .py programms can run consecutively without human intervention.
# the resulting .py programms execute a Morgan Fingerprint generation algorithm for the compounds found in the overlap of the CP-Dataset of Bray et al and varioud Pubchem Assays (AID).
# The Input data for this notebook is stored in 02-CorrectingAssays and is part of the master thesis of Luis Vollmers
# the output is stored in the _output directory of this subproject 03-GenerateFingerprints and is the ml_ready data set for input into the virtual machinery of the sub project 04-PredictFingerprints


### DECLARE GLOBAL VARIABLES
# set global variables for the output
SRC_IPYNB="fp_1030.ipynb"
SRC_PYTHON="fp_1030.py"
TMP_FILE="fp_AID.py"


### DEFINE FUNCTIONS
# first function to call; uses random forest notebooks to generate predictions
# for details see fp_1030.ipynb
generate_fingerprints () 
{
	# use the nbconvert to generate .py from notebook
	jupyter nbconvert --to script ${SRC_IPYNB}

	# rename the notebook and change the iterable (1030) to placeholder (AID)
	sed "s/1030/AID/g" $SRC_PYTHON > $TMP_FILE

	# for loop iterates over all input files in the 2nd step Dir. which are used in the .py files
	for aid in $(ls ../../02-CorrectingAssays/_output/*)
	do 
		# generate the sole AID from the input-filenames and declare name for executable file of "aid"-iteration
		aid=${aid%.*}
		aid=${aid##*_}
		EXEC_FILE="fp_${aid}.py"

		# change the placeholder to the concurrent AID and implement it into the filename
		sed "s/AID/$aid/g" $TMP_FILE > $EXEC_FILE
		# make file executable
		chmod 777 $EXEC_FILE
		
		# make the random forest prediction using cell-painting data to 
		printf "Running for $aid..."
		./$EXEC_FILE
		echo "done"

		mv $EXEC_FILE ../_trash/
	done

	# move temporary files to the trash
	mv $TMP_FILE ../_trash/
}


### CALL FUNCTIONS
generate_fingerprints
