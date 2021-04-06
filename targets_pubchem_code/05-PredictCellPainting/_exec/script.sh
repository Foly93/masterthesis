#!/bin/bash

### HEADER
# This script is for multiplying and adjusting a template jupyter notebook so that a cluster of .py programms can run consecutively without human intervention.
# the resulting .py programms execute a Randon Forest prediction for a dataset generated from Cell painting data and Pubchem Assay data.
# The Input data for this notebook is stored in 02-CorrectingAssays and is part of the master thesis of Luis Vollmers
# the output is stored in the _output directory of this subproject 05-PredictCellPainting and is a single summarization of the statistival prediction metrics like AUC, Sensitivity and so forth


### DECLARE GLOBAL VARIABLES

# since I am using a german computer the default decimal is "," which is changed here
export LC_ALL=C

# set global variables for the output
OUT_FILE="summary_results.txt"
OUT_DIR="../_output"


### DEFINE FUNCTIONS

# first function to call; uses random forest notebooks to generate predictions
# for details see rf_cp_1030.ipynb
generate_predictions () 
{
	# use the nbconvert to generate .py from notebook
	jupyter nbconvert --to script rf_cp_1030.ipynb

	# rename the notebook and change the iterable (1030) to placeholder (AID)
	sed "s/1030/AID/g" rf_cp_1030.py > rf_cp_AID.py
	# remove the plt.show() which is disturbing the automatic process
	sed -i '/show/d' rf_cp_AID.py

	# for loop iterates over all input files in the 2nd step Dir. which are used in the .py files
	for aid in $(ls ../../02-CorrectingAssays/_output/*)
	do 
		# generate the sole AID from the input-filenames
		aid=${aid%.*}
		aid=${aid##*_}

		# change the placeholder to the concurrent AID and implement it into the filename
		sed "s/AID/$aid/g" rf_cp_AID.py > rf_cp_${aid}.py
		# make file executable
		chmod 777 rf_cp_${aid}.py
		
		# make the random forest prediction using cell-painting data to 
		printf "Running for $aid..."
		./rf_cp_${aid}.py
		echo "done"
	done

	# move temporary files to the trash
	mv rf_cp_AID.py ../_trash/
}

# second funtion summarizes the results
# different metrics are saved to the summary file that give information about the prediction quality
summarize_results () 
{
	# print the date to the newly made output file
	date > ${OUT_DIR}/${OUT_FILE}
	# print the header line to the output file
	printf "%-6s\t%6s\t%6s\t%6s\t%6s\t%6s\n" "AID" "AUC-Sc" "BalAcc" "MatCff" "Sensit" "Specif" >> ${OUT_DIR}/${OUT_FILE}
	
	# iterate over all inputs like in the prior function
	for aid in $(ls ../../02-CorrectingAssays/_output/*)
	do
		# see prior function
		aid=${aid%.*}
	        aid=${aid##*_}
		# declare input file name corresponding to the analysis file from the rf prediction
		INP_FILE="rf_cp_${aid}_analysis.txt"
	
		# grep the metrics from the individiual analysis files
		# see rf_cp_${aid}_analysis.txt for understanding the grep-pattern in detail
		AUC=$(grep 'AUC' ${OUT_DIR}/${INP_FILE} | awk '{print $2}')
		BA=$(grep 'Bal' ${OUT_DIR}/${INP_FILE} | awk '{print $3}')
		MCC=$(grep 'Mat' ${OUT_DIR}/${INP_FILE} | awk '{print $3}')
		SENS=$(grep 'Sensi' ${OUT_DIR}/${INP_FILE} | awk '{print $2}')
		SPEC=$(grep 'Speci' ${OUT_DIR}/${INP_FILE} | awk '{print $2}')
	
		# print the metrics sorted by AID to the output file 
		printf "%-6d\t%.4f\t%.4f\t%.4f\t%.4f\t%.4f\n" "$aid" "$AUC" "$BA" "$MCC" "$SENS" "$SPEC" >> ${OUT_DIR}/${OUT_FILE}
	done
	sed -i 's/ //g' ${OUT_DIR}/${OUT_FILE}
}


### CALL FUNCTIONS
generate_predictions
summarize_results
